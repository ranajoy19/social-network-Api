# Django Friend Request API

## Installation

1. Clone the repository:


git clone https://github.com/ranajoy19/social-network-Api.git
cd social-network-Api

2. Create Virtual Environmemnt:

commande = py -m venv venv

active = venv\Scripts\activate


3. Install the dependencies:
    pip install -r requirements.txt


4. run server 
    python manage.py runserver 


**** important note Data Base setting need to change to run the project locally( data base "HOST" need to change to localhost)

5. Build and run the Docker containers:
    docker-compose -f docker-compose.yaml up --build -d


6. Access the application at http://localhost:8000.


7. API Endpoints

    POST /api/signup/ - Signup
    POST /api/login/ - Login
    GET /api/search/?search=<email or username> - Search Users
    POST /api/friend-request/send/ - Send Friend Request
    POST /api/friend-request/accept/ - Accept Friend Request
    POST /api/friend-request/reject/ - Reject Friend Request
    GET /api/friends/ - List Friends
    GET /api/friend-requests/pending/ - List Pending Friend Requests

8. Postman Collection

    Import the FriendsBook.postman_collection.json file into Postman for easy testing of the API endpoints.