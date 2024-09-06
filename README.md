# Online Learning Platform

This project is an online learning platform built using Django and Django REST Framework. The platform allows users to register, enroll in courses, access course modules, lessons, assignments, and track submissions. It also includes a dummy payment system for course transactions and a real-time chat feature powered by WebSockets using Django Channels and Redis.

## Features

- **User Authentication**: User registration, login, and token-based authentication with JWT.
- **Course Management**: Categories, courses, modules, lessons, assignments, and submissions.
- **Enrollment System**: Students can enroll in courses.
- **Transaction Management**: Users can manage and view their payment transactions.
- **Real-time Chat**: Real-time messaging between users using WebSockets with Redis as the message broker.

## Apps Overview

### Users App

This app handles user authentication, registration, and profile management.

#### Endpoints:
- `POST /register/`: Register a new user.
- `POST /login/`: Login and request verification code.
- `POST /get-token/`: Validate verification code and get JWT tokens.
- `GET /users/`: Get list of all users.
- `GET /users/<username>/`: Get user details by username.
- `GET/PUT /user-profile/<username>/`: Get or update user profile.

### Courses App

This app handles the core functionality of managing courses, modules, lessons, and assignments.

#### Endpoints:
- `GET/POST /categories/`: List or create course categories.
- `GET/PUT /categories/<pk>/`: Retrieve or update category details.
- `GET/POST /courses/`: List or create courses.
- `GET/PUT /courses/<pk>/`: Retrieve or update course details.
- `GET /my-courses/`: List courses that a user is enrolled in or instructs.
- `GET/POST /modules/`: List or create modules for a course.
- `GET/PUT /modules/<pk>/`: Retrieve or update module details.
- `GET/POST /lessions/`: List or create lessons for a module.
- `GET/PUT /lessions/<pk>/`: Retrieve or update lesson details.
- `GET/POST /assignments/`: List or create assignments for a module.
- `GET/PUT /assignments/<pk>/`: Retrieve or update assignment details.
- `GET/POST /submissions/`: List or create submissions for an assignment.
- `GET/PUT /submissions/<pk>/`: Retrieve or update submission details.
- `GET/POST /enrolls/`: List or enroll in a course.

### Payments App

This app handles user transactions for course payments.

#### Endpoints:
- `GET/POST /transaction/`: List or create payment transactions for a user.

### Chats App

This app provides real-time messaging functionality between users using WebSockets.

#### WebSocket Endpoint:
- `ws/chat/`: WebSocket connection for real-time chat.

1. Clone the repository:
  ```bash
   git clone https://github.com/Estaheri7/online-learning-platform.git
   cd online-learning-platform
  ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
    - **Database settings**
    - **Email settings**
    - **Redis settings**
    - **JWT settings**
    - **Django secret key**
4. Apply migration:
   ```bash
   python manage.py migrate
   ```
5. Start the development server:
   ```bash
    python manage.py runserver
   ```
6. Set up Redis for Websockets:
   - **Install and run Redis server**
   - **Update Django Channels settings to point to your Redis instance.**

## Technologies Used

- **Backend**: Django, Django REST Framework
- **Authentication**: JWT (Django SimpleJWT)
- **Real-time**: Django Channels, Redis
- **Database**: PostgreSQL (or any other Django-supported database)
- **Caching**: Redis (used for caching verification codes)
- **WebSockets**: Django Channels


## License

This project is licensed under the MIT License.

## Contribution

Contributions are welcome! To contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push the branch to your fork (`git push origin feature-name`).
5. Create a Pull Request.

Please make sure to update tests as appropriate and follow the project's coding standards.
