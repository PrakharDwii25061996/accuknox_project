
## Steps to run project without Docker
1. Create virtual environment and activate it in Windows 11
```
python -m venv venv
venv/Scripts/Activate
```

2. Install required modules and run the project
```
cd ./accuknox_assignment
pip install -r requirements.txt
python manage.py runserver 0.0.0.0:8000
```

## Steps to Run the project via Docker
1. Build the image
```
docker build -t my-django-app .
```

2. Run the container
```
docker-compose up
```
3. To stop currently running container
```
Ctrl + C
```
4. To remove containers
```
docker-compose down
```

## API endpoints of this project from postman collection

## User app
1. User List api
```
https://winter-capsule-260343.postman.co/workspace/d6340aa9-9e63-494f-9c37-506e76d02289/request/15415457-d697d17c-4fcb-48c1-b632-78074f155cca?action=share&source=copy-link&creator=15415457&ctx=documentation
```

2. User Create API
```
https://winter-capsule-260343.postman.co/workspace/d6340aa9-9e63-494f-9c37-506e76d02289/request/15415457-f9639829-3de5-433d-8844-d39dcc693a56?action=share&source=copy-link&creator=15415457&ctx=documentation
```

3. User Login API
```
https://winter-capsule-260343.postman.co/workspace/d6340aa9-9e63-494f-9c37-506e76d02289/request/15415457-76f8f16c-af50-48c5-b83b-9fb8521ba6dc?action=share&source=copy-link&creator=15415457&ctx=documentation
```

4. User Search API
```
https://winter-capsule-260343.postman.co/workspace/d6340aa9-9e63-494f-9c37-506e76d02289/request/15415457-89a63aad-933c-42e1-83ea-8e1efc215033?action=share&source=copy-link&creator=15415457&ctx=documentation
```

5. Friend Request Create API
```
https://winter-capsule-260343.postman.co/workspace/d6340aa9-9e63-494f-9c37-506e76d02289/request/15415457-df780293-e7b3-46d6-be98-d2bc2ff4db41?action=share&source=copy-link&creator=15415457&ctx=documentation
```

6. Friend Request Pending API
```
https://winter-capsule-260343.postman.co/workspace/d6340aa9-9e63-494f-9c37-506e76d02289/request/15415457-4750ac44-c819-4b23-bf57-6b04cba516ec?action=share&source=copy-link&creator=15415457&ctx=documentation
```

7. Friend Request Accept Reject API
```
https://winter-capsule-260343.postman.co/workspace/d6340aa9-9e63-494f-9c37-506e76d02289/request/15415457-eb7217c0-426f-4273-b4fe-9efa42cea0b0?action=share&source=copy-link&creator=15415457&ctx=documentation
```

8. Friend Request Accept List API
```
https://winter-capsule-260343.postman.co/workspace/d6340aa9-9e63-494f-9c37-506e76d02289/request/15415457-eb7217c0-426f-4273-b4fe-9efa42cea0b0?action=share&source=copy-link&creator=15415457&ctx=documentation
```
