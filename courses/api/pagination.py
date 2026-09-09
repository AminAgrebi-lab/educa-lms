from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    # Default number of items per page when ?page_size= is not given
    page_size = 10
    # Clients may override the size via ?page_size=N
    page_size_query_param = 'page_size'   # ⚠️ Reading typo: ' page_size ' with spaces
    # Hard ceiling to prevent abusive requests like ?page_size=999999
    max_page_size = 50