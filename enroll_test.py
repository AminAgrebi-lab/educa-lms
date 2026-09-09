import requests

# ⚠️ IMPORTANT: Replace these with REAL credentials of a student you created
username = 'Adam'   # e.g., 'amin_student'
password = 'azeaze123'   # e.g., 'StrongPassword123'

base_url = 'http://127.0.0.1:8000/api/'
url = f'{base_url}courses/'

print("📡 Fetching available courses (public, no auth needed)...")
r = requests.get(url)

if r.status_code != 200:
    print(f"❌ Failed to fetch courses. Status code: {r.status_code}")
    print(f"Response: {r.text}")
    exit(1)

response = r.json()
courses = response.get('results', [])

if not courses:
    print("⚠️ No courses found on the platform. Create some as an instructor first!")
    exit(0)

print(f"✅ Found {len(courses)} courses. Attempting to enroll as '{username}'...\n")

for course in courses:
    course_id = course['id']
    course_title = course['title']
    
    enroll_url = f'{base_url}courses/{course_id}/enroll/'
    r = requests.post(enroll_url, auth=(username, password))
    
    if r.status_code == 200:
        print(f"✅ Successfully enrolled in: {course_title}")
    elif r.status_code == 401:
        print(f"❌ AUTHENTICATION FAILED for '{course_title}'. Check your username/password in the script.")
        print(f"   Response: {r.text}")
    elif r.status_code == 403:
        print(f"🚫 PERMISSION DENIED for '{course_title}'. The user is authenticated but not allowed.")
    elif r.status_code == 404:
        print(f"🔍 Course ID {course_id} not found.")
    else:
        print(f"⚠️ Unexpected status {r.status_code} for '{course_title}': {r.text}")

print("\n🏁 Script finished.")