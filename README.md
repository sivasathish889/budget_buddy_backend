# BudgetBuddy Backend

A Django REST API backend for a personal expense tracking application that helps users manage their finances, track expenses, and set budget goals.

## Features

- **User Management**
  - User registration with email verification
  - Secure authentication with JWT tokens
  - Password reset functionality
  - Profile management
  - Account deletion

- **Expense Tracking**
  - Add, view, and delete expenses
  - Categorize expenses
  - Recent expense history (last 2 months)
  - Expense filtering by date range

- **Security**
  - Password hashing with bcrypt
  - JWT token-based authentication
  - Email OTP verification
  - Secure password reset

## Tech Stack

- **Framework**: Django 5.2.6
- **API**: Django REST Framework 3.16.1
- **Database**: MySQL (via mysqlclient 2.2.7)
- **Authentication**: JWT (PyJWT 2.10.1)
- **Password Hashing**: bcrypt 4.3.0
- **Email**: Django's built-in email system
- **Environment**: python-dotenv 1.1.1

## Project Structure

```
budget_buddy_backend/
├── budget_buddy_app/
│   ├── migrations/          # Database migrations
│   ├── utils/
│   │   ├── bcrypt.py       # Password hashing utilities
│   │   └── jwt.py          # JWT token utilities
│   ├── models.py           # Database models
│   ├── views.py            # API endpoints
│   ├── serializer.py       # Data serializers
│   ├── urls.py             # URL routing
│   └── middleware.py       # Custom middleware
├── budget_buddy_backend/
│   ├── certs/              # SSL certificates
│   ├── settings.py         # Django settings
│   └── urls.py             # Main URL configuration
├── requirements.txt        # Python dependencies
└── manage.py              # Django management script
```

## Database Models

### Users
- Personal information (name, email, phone, DOB)
- Budget goals
- Secure password storage
- Account timestamps

### Expense
- Amount and description
- Category association
- Date tracking
- User association

### Category
- Expense categorization system

### Social
- Social authentication support

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd budget_buddy_backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your_django_secret_key
   DEBUG=True
   DATABASE_NAME=your_database_name
   DATABASE_USER=your_database_user
   DATABASE_PASSWORD=your_database_password
   DATABASE_HOST=localhost
   DATABASE_PORT=3306
   EMAIL_HOST_USER=your_email@gmail.com
   EMAIL_HOST_PASSWORD=your_email_password
   ```

5. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Superuser** (Optional)
   ```bash
   python manage.py createsuperuser
   ```

7. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

## Configuration

### Database
The project is configured to use MySQL. Update your database settings in `settings.py` or use environment variables.

### Email Configuration
Configure SMTP settings for email functionality (OTP verification, password reset).

### JWT Configuration
JWT tokens are used for authentication. Configure token expiration and secret keys as needed.

## Security Features

- **Password Security**: All passwords are hashed using bcrypt
- **JWT Authentication**: Secure token-based authentication
- **Email Verification**: OTP-based email verification
- **Input Validation**: Comprehensive input validation and sanitization
- **CORS Protection**: Configured for secure cross-origin requests

## API Response Format

All API responses follow a consistent format:
```json
{
  "message": "Response message",
  "success": true/false,
  "data": {}, // Optional data payload
  "Token": "jwt_token" // For authentication endpoints
}
```

## Error Handling

The API includes comprehensive error handling with appropriate HTTP status codes:
- `200` - Success
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `500` - Internal Server Error

## Development

### Adding New Features
1. Create models in `models.py`
2. Create serializers in `serializer.py`
3. Implement views in `views.py`
4. Add URL patterns in `urls.py`
5. Run migrations

### Testing
Run tests using Django's test framework:
```bash
python manage.py test
```

## Deployment

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure production database
- [ ] Set up proper email backend
- [ ] Configure static files serving
- [ ] Set up SSL certificates
- [ ] Configure environment variables
- [ ] Set up logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support or questions, please contact [your-email@example.com]

## Changelog

### Version 1.0.0
- Initial release
- User authentication system
- Expense tracking functionality
- Category management
- Email verification system