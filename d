# Image Upload API using Django REST Framework

This is a README file for an application built with Django REST Framework that allows users to upload images in PNG or JPG format. The API provides functionality to upload images, list user's images, and supports different account tiers with varying privileges.
Requirements

    Django
    Django REST Framework
    Pillow (for image processing)
    Docker (optional, for easy project setup with docker-compose)

Getting Started

To run the project locally, follow the instructions below.
Prerequisites

Make sure you have Python and pip installed on your system.
Installation

Clone the repository:

    git clone <repository_url>

Install the project dependencies:

    cd <project_directory>
    pip install -r requirements.txt


Create and apply the database migrations:

    python manage.py makemigrations
    python manage.py migrate

Running the Server

    python manage.py runserver

The API will be accessible at http://localhost:8000.
API Endpoints

    POST /upload/: Upload an image in PNG or JPG format. The authenticated user can upload an image by sending a multipart/form-data POST request with the image field containing the image file.

    GET /images/: List all images uploaded by the authenticated user. Returns a JSON array of image objects.

    GET /profile/: Retrieve the user's profile information, including the user's tier. Returns a JSON object containing the user profile information.

Customization
Account Tiers

The application supports three built-in account tiers: Basic, Premium, and Enterprise. Each tier has different privileges for image access. You can customize the tiers by creating or modifying tier objects in the Django admin panel.
Admin Panel

The Django admin panel allows administrators to manage user accounts, tiers, and other system configurations. To access the admin panel, navigate to http://localhost:8000/admin and log in with an administrator account.
Testing

To run the tests, execute the following command:

    python manage.py test

The test suite includes unit tests for models, serializers, and views.
Performance Considerations

The application is designed to handle a large number of images and frequent API access. It utilizes Django's efficient ORM for database operations and supports pagination to manage large image collections.
Docker Compose (optional)

If you prefer to run the project with Docker, make sure you have Docker and Docker Compose installed on your system.

    docker-compose build

    docker-compose up

The application will be accessible at http://localhost:8000.
