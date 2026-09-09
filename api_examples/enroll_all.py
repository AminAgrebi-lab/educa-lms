import requests


username = 'amin_student'    
password = 'StrongPass123!'    

base_url = 'http://127.0.0.1:8000/api/'
url = f'{base_url}courses/'

all_courses = []  

print("📡 Fetching all available courses (handling pagination)...\n")


while url is not None:
    print(f'Loading page: {url}')
    r = requests.get(url)
    response = r.json()
    
  
    url = response.get('next') 
    
  
    courses_in_page = response.get('results', [])
    all_courses.extend(courses_in_page)

print(f"\n Found a total of {len(all_courses)} courses.\n")
print("🎓 Attempting to enroll in all courses...\n")


for course in all_courses:
    course_id = course['id']
    course_title = course['title']
    

    r = requests.post(
        f'{base_url}courses/{course_id}/enroll/',
        auth=(username, password)
    )
    
    if r.status_code == 200:
        print(f'Successfully enrolled in: {course_title}')
    elif r.status_code == 401:
        print(f'AUTH FAILED for {course_title}. Check username/password.')
    else:
        print(f'Unexpected status {r.status_code} for {course_title}')

print("\n🏁 Script finished.")