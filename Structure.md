High-Level Plan

    Project Structure

        FriendsBook/
            settings.py
            urls.py
            wsgi.py
            asgi.py
        app/
            migrations/
            __init__.py
            admin.py
            models.py
            views.py
            serializers.py
            urls.py
            backend.py
            constants.py
        Dockerfile
        docker-compose.yml
        requirements.txt
        manage.py
        README.md
        postman_collection.json
    
    APIs to Implement

        User Authentication:
            Signup
            Login
        User Management:
            Search Users
            Send Friend Request
            Accept/Reject Friend Request
            List Friends
            List Pending Friend Requests

        Authentication:
            Use JWT for token-based authentication.
            Protect endpoints with a custom permission class.
        
        Database Models(MySql):
            User
            FriendRequest

        Rate Limiting:

            Implement rate limiting to restrict the number of friend requests per user.