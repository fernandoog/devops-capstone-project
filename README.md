# DevOps Capstone Project - RESTful Service

This project implements a RESTful Account Service using Flask and Test-Driven Development (TDD) principles.

## Project Structure

```
devops-capstone-project/
├── service/
│   ├── __init__.py
│   ├── models.py          # Account model and database operations
│   ├── routes.py          # Flask routes and REST API endpoints
│   └── status.py          # HTTP status codes
├── tests/
│   ├── __init__.py
│   └── test_routes.py     # Unit tests for REST API endpoints
├── setup.cfg              # Test configuration
├── requirements.txt       # Python dependencies
├── run.py                 # Simple server runner
├── start_server.py       # Server with detailed instructions
├── demo_rest_api.py      # Demonstration script
└── README.md             # This file
```

## Features

### REST API Endpoints

| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|-------------|
| POST | `/accounts` | Create a new account | 201 Created |
| GET | `/accounts` | List all accounts | 200 OK |
| GET | `/accounts/{id}` | Get account by ID | 200 OK / 404 Not Found |
| PUT | `/accounts/{id}` | Update account by ID | 200 OK / 404 Not Found |
| DELETE | `/accounts/{id}` | Delete account by ID | 204 No Content |
| GET | `/health` | Health check | 200 OK |

### Account Model

The Account model includes the following fields:
- `id` (Integer, Primary Key)
- `name` (String, Required)
- `email` (String, Required, Unique)
- `address` (String, Optional)
- `phone_number` (String, Optional)
- `date_joined` (DateTime, Auto-generated)

## Installation and Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Tests:**
   ```bash
   python -m pytest tests/ -v --cov=service
   ```

3. **Start the Server:**
   ```bash
   python start_server.py
   ```

4. **Run Demonstration:**
   ```bash
   python demo_rest_api.py
   ```

## Usage Examples

### Create Account
```bash
curl -X POST http://127.0.0.1:5000/accounts \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@doe.com","address":"123 Main St","phone_number":"555-1212"}'
```

### List All Accounts
```bash
curl -X GET http://127.0.0.1:5000/accounts
```

### Get Account by ID
```bash
curl -X GET http://127.0.0.1:5000/accounts/1
```

### Update Account
```bash
curl -X PUT http://127.0.0.1:5000/accounts/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"John Updated","email":"john.updated@doe.com","address":"456 New St","phone_number":"555-9999"}'
```

### Delete Account
```bash
curl -X DELETE http://127.0.0.1:5000/accounts/1
```

### Health Check
```bash
curl -X GET http://127.0.0.1:5000/health
```

## Test-Driven Development

This project follows TDD principles:

1. **Write Tests First:** Each endpoint has comprehensive unit tests
2. **Red-Green-Refactor:** Tests are written before implementation
3. **High Coverage:** Aim for 95%+ test coverage
4. **Continuous Testing:** Tests run automatically during development

### Test Categories

- **Happy Path Tests:** Normal operation scenarios
- **Error Handling Tests:** Edge cases and error conditions
- **Data Validation Tests:** Input validation and constraints
- **HTTP Status Code Tests:** Correct status code responses

## Database

The application uses SQLite for simplicity and includes:
- Automatic table creation
- Database migrations support
- Transaction management
- Connection pooling

## Error Handling

The service includes comprehensive error handling:
- **404 Not Found:** When account doesn't exist
- **405 Method Not Allowed:** Invalid HTTP methods
- **400 Bad Request:** Invalid JSON or missing fields
- **500 Internal Server Error:** Server-side errors

## Development Guidelines

### Code Quality
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for all functions
- Maintain 95%+ test coverage

### REST API Best Practices
- Use proper HTTP methods
- Return appropriate status codes
- Include meaningful error messages
- Follow RESTful URL patterns
- Use JSON for data exchange

## Sprint Review

### Completed User Stories
✅ Set up development environment  
✅ Create account endpoint  
✅ List accounts endpoint  
✅ Read account endpoint  
✅ Update account endpoint  
✅ Delete account endpoint  
✅ Error handling  
✅ Test coverage (95%+)  

### Evidence
- All REST API endpoints working correctly
- Comprehensive test suite with high coverage
- Proper error handling and status codes
- Clean, maintainable code structure

## Next Steps

1. **Deployment:** Deploy to cloud platform (OpenShift)
2. **Monitoring:** Add logging and metrics
3. **Security:** Implement authentication and authorization
4. **Documentation:** Add API documentation (Swagger)
5. **Performance:** Add caching and optimization

## Technologies Used

- **Flask:** Web framework
- **SQLAlchemy:** ORM for database operations
- **SQLite:** Database
- **pytest:** Testing framework
- **coverage:** Code coverage analysis
- **unittest:** Unit testing framework

## Author

Developed as part of the IBM DevOps and Software Engineering Professional Certificate Capstone Project.
