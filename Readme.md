graph-dependency
Graph-based Data Representation with FastAPI and Django and Vue.js

This project is an implementation of a graph data structure using FastAPI and Django. It demonstrates how to create a graph where nodes and edges are stored in a Django backend and fetched via FastAPI for visualization or other uses.

Technologies Used: FastAPI: A modern web framework for building APIs with Python 3.7+ based on standard Python type hints.

Django: A high-level Python web framework that encourages rapid development and clean, pragmatic design.

Django ORM: For interacting with the database and handling models such as Node and Edge.

ASGI (Asynchronous Server Gateway Interface): For handling asynchronous requests efficiently.

Project Features: Node and Edge Models: Django models represent nodes and edges of the graph.

FastAPI Endpoints: Expose endpoints for fetching node and edge data as JSON.

Database Interaction: Uses Django ORM to fetch data from the database asynchronously.

Setup Instructions:

Clone the repository: git clone https://github.com/your-username/repository-name.git

Install dependencies: It’s recommended to create a virtual environment for this project. pip install -r requirements.txt

Run the Django server: python manage.py runserver

Run FastAPI: Make sure to run FastAPI separately if it’s a part of the project: uvicorn api:app --reload

Access the API: After starting the servers, you can access the API at: Django Admin: http://localhost:8000/admin/

FastAPI: http://localhost:8001/api/graph

Database Configuration: The project uses a basic database configuration for storing nodes and edges. Make sure to run migrations: python manage.py migrate

Issues/Challenges: This project may encounter some challenges related to asynchronous database queries in Django. Make sure to use the proper configuration for handling async calls efficiently in Django and FastAPI.

Additional Notes: Ensure that your environment is properly set up for both Django and FastAPI to run concurrently.

Database models and interactions are based on Django’s ORM, and the graph data is fetched and served via FastAPI.

About
Graph-based Data Representation with FastAPI and Django and Vue.js


