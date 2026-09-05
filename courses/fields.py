# Import the exception raised when a QuerySet lookup finds no object
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class OrderField(models.PositiveIntegerField):
    """
    A custom field that automatically assigns an order value to objects.
    Inherits from PositiveIntegerField and adds auto-ordering behavior.
    """

    def __init__(self, for_fields=None, *args, **kwargs):
        # Store the fields used to scope the ordering
        # (e.g., order modules within the same course)
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        """
        Executed automatically right before saving the field to the database.
        """
        # If NO order value was provided, calculate it automatically
        if getattr(model_instance, self.attname) is None:
            try:
                # Start with a QuerySet of all objects of this model
                qs = self.model.objects.all()

                # If for_fields is set, filter by those fields first
                # (e.g., only modules that belong to the same course)
                if self.for_fields:
                    query = {
                        field: getattr(model_instance, field)
                        for field in self.for_fields
                    }
                    qs = qs.filter(**query)

                # Get the object with the highest current order
                last_item = qs.latest(self.attname)
                # New order = highest existing order + 1
                value = getattr(last_item, self.attname) + 1
            except ObjectDoesNotExist:
                # No existing objects found: this is the first one, so order = 0
                value = 0

            # Assign the calculated order to the model instance
            setattr(model_instance, self.attname, value)
            return value
        else:
            # An order value WAS provided: use it as-is
            return super().pre_save(model_instance, add)