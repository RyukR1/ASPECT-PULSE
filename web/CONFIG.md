# Aspect-Pulse Web Configuration Guide

## Environment Configuration

### Development Environment

Create a `.env` file in the `web/` directory:

```env
FLASK_ENV=development
FLASK_APP=app.py
DEBUG=True
SECRET_KEY=your-secret-key-here
MAX_TEXT_LENGTH=5000
```

### Production Environment

For production deployment:

```env
FLASK_ENV=production
DEBUG=False
SECRET_KEY=generate-a-strong-secret-key
MAX_CONTENT_LENGTH=16777216
```

## Server Configuration

### Local Development
```python
# In app.py
app.run(
    debug=True,
    host='0.0.0.0',
    port=5000
)
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Production with uWSGI
```bash
pip install uwsgi
uwsgi --http :5000 --wsgi-file app.py --callable app --processes 4
```

## Database Configuration

Currently the app uses in-memory storage. For persistent storage:

```python
# In app.py - Add database configuration
import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your-password',
    'database': 'aspect_pulse'
}

# Create connection pool for better performance
```

## API Rate Limiting

To prevent abuse, add rate limiting:

```bash
pip install Flask-Limiter
```

```python
from flask_limiter import Limiter

limiter = Limiter(app)

@app.route('/analyze', methods=['POST'])
@limiter.limit("30 per minute")
def analyze():
    # ... analysis code
```

## CORS Configuration

If your frontend is on a different domain:

```bash
pip install flask-cors
```

```python
from flask_cors import CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

## Security Headers

Add security headers to responses:

```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

## SSL/TLS Configuration

For HTTPS in production:

```bash
pip install pyopenssl
```

Use a reverse proxy like Nginx:

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Logging Configuration

```python
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## Performance Optimization

### Caching
```python
from functools import wraps

def cache(timeout=300):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Implement caching logic
            pass
        return wrapper
    return decorator
```

### Compression
```bash
pip install flask-compress
```

```python
from flask_compress import Compress
Compress(app)
```

### CDN Configuration

Update template URLs for CDN:

```html
<!-- Development -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>

<!-- Production (use a CDN with caching) -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
```

## Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

Build and run:

```bash
docker build -t aspect-pulse-web .
docker run -p 5000:5000 aspect-pulse-web
```

## Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    volumes:
      - ./:/app
  mysql:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=root
      - MYSQL_DATABASE=aspect_pulse
    ports:
      - "3306:3306"
```

## Monitoring & Logging

### Application Monitoring
```bash
pip install flask-monitoringdashboard
```

### Error Tracking
```bash
pip install sentry-sdk
```

```python
import sentry_sdk
sentry_sdk.init("your-sentry-url")
```

## Testing Configuration

Create `test_config.py`:

```python
class TestConfig:
    TESTING = True
    DEBUG = True
    MAX_CONTENT_LENGTH = 1024 * 1024  # 1MB for testing
    
class DevelopmentConfig:
    DEBUG = True
    
class ProductionConfig:
    DEBUG = False
```

## Environment Variables Summary

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | development | Environment mode |
| `DEBUG` | True | Debug mode |
| `SECRET_KEY` | None | Session encryption key |
| `MAX_TEXT_LENGTH` | 5000 | Max input characters |
| `MODEL_CACHE_SIZE` | 1 | ML model cache size |
| `LOG_LEVEL` | INFO | Logging level |

## Quick Start Commands

```bash
# Development
python app.py

# Production (Gunicorn)
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Production (uWSGI)
uwsgi --http :5000 --wsgi-file app.py --callable app --processes 4

# Docker
docker-compose up -d

# Testing
python -m pytest
```

## Support

For configuration issues, refer to Flask documentation:
- https://flask.palletsprojects.com/
- https://werkzeug.palletsprojects.com/
