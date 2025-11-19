# Test Suite for TestRetry Application

## Running the Tests

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the tests:
   ```bash
   pytest
   ```

3. Run tests with coverage:
   ```bash
   pytest --cov=app
   ```

## Test Structure
- `test_api.py`: Unit tests for backend API endpoints.
- `test_auth.py`: Unit tests for authentication logic.
- `test_models.py`: Unit tests for database models.
- `test_integration.py`: Integration test for the main workflow.
- `conftest.py`: Pytest configuration and fixtures.

## Additional Notes
- Ensure the application is properly configured before running integration tests.
- Update the `requirements.txt` file if additional dependencies are introduced.