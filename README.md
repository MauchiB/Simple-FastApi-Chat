# FastAPI WebSocket API with Alembic, SQLAlchemy, and JWT Auth

This repository contains a RESTful API built using FastAPI, enhanced with WebSocket support, and backed by a sqlite database using SQLAlchemy and Alembic migrations. The API uses JWT (JSON Web Tokens) for authentication via cookies, requiring login before accessing protected resources.

## Features

*   **FastAPI:** Modern, high-performance web framework for building APIs with Python.
*   **Alembic:** Database migration tool.
*   **SQLAlchemy:** ORM for interacting with databases.
*   **PostgreSQL:** Database used for storage.
*   **WebSocket:** Real-time, bidirectional communication support.
*   **JWT Authentication:** Secure authentication using JWT stored in cookies.
*   **Authorization Required:** Access to protected resources requires prior login.

## Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your_username/your_repository.git
    cd your_repository
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/macOS
    # venv\Scripts\activate  # Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure the database:**
    *  Create a `.env` file in the root directory of the project.
    *  Add environment variables for the database connection (details below).
5.  **Run database migrations:**

    ```bash
    alembic revision --autogenerate -m 'create db'
    alembic upgrade head
    ```

6.  **Start the application:**

    ```bash
    uvicorn main:app --reload
    ```

    *   `main.py` is your file containing the FastAPI app instance
    *   `app` is the name of the FastAPI variable
    *   `--reload` enables auto-reloading on code changes

## Environment Configuration

Create a `.env` file in the root of the project and add the following variables:

## WebSocket Usage

WebSockets are available at `/ws`. To connect, the client (usually a frontend application) sends a GET request to the `/ws` endpoint with the header `Upgrade: websocket`.

**Connecting to a Chat:**

1.  **Chat ID:** Before opening a WebSocket connection, the client must include the chat ID within the query parameters of the URL. For example, if the chat ID is `123`, the URL would be `/ws?chat_id=123`.
2.  **Connection:** Send a GET request to the websocket endpoint with the provided URL. This will establish a persistent connection for real-time communication with the server.

**Sending Messages:**

1.  **JSON Payload:** Once the connection is established, the client sends messages to the server as JSON.
2.  **Message Format:** The JSON payload must contain a `message` key holding the content of the message. For instance:

    ```json
    {
      "message": "Hello everyone in the chat!"
    }
    ```

**Server-Side Processing:**

1.  **Message Handling:** Upon receiving a message, your server-side WebSocket class (`SocketChat`) processes the JSON payload.
2.  **Message Creation:** The server creates a new message in the database using your model, associating it with the relevant chat and sender.
3.  **Message Distribution:** The server then broadcasts the message to all other connected clients (participants) within the same chat. This ensures real-time message delivery to all members of the specified chat.


env
DATABASE_URL="sqlite:///test.db"
SECRET_KEY="your_secret_key"  # Use a complex, unique key
ALGORITHM="HS256"

API Documentation
API documentation can be accessed at:

Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc
(Replace 127.0.0.1:8000 with your application’s address)

Authentication
To access protected resources, the frontend application must send a POST request to /auth/login with a JSON body containing the user’s username and password. Upon successful authentication (status code 200), the server will set an access_token cookie containing the JWT. This cookie is then required for accessing protected resources. The access_token cookie is HttpOnly for security.

## License

This project is licensed under the [MIT License](LICENSE).