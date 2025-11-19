# TestRetry Backend API

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Navigate to the backend directory:
   ```bash
   cd backend
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up the environment variables:
   - Copy the `.env.example` file to `.env`.
   - Update the variables with your values (e.g., `DATABASE_URL`, `SECRET_KEY`).

6. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

7. Access the API at:
   - Swagger UI: `http://127.0.0.1:8000/docs`
   - Redoc: `http://127.0.0.1:8000/redoc`

## API Endpoints

### Authentication
- **POST** `/register`: Register a new user.
- **POST** `/token`: Generate a JWT token for authentication.

### Leads
- **POST** `/generate-lead`: Create a new lead.
- **GET** `/leads`: Retrieve leads for a specific user.

### Health Check
- **GET** `/health`: Check the health of the API.

## Database Schema
- **User**:
  - `id`: Integer, Primary Key
  - `username`: String, Unique
  - `email`: String, Unique
  - `hashed_password`: String
  - `created_at`: DateTime

- **Lead**:
  - `id`: Integer, Primary Key
  - `user_id`: Integer, Foreign Key
  - `name`: String
  - `email`: String
  - `phone`: String
  - `message`: String
  - `created_at`: DateTime

## License
This project is licensed under the MIT License.