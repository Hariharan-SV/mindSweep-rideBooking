# Uvicorn Guide - Running FastAPI Application

## Table of Contents
1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Development Mode](#development-mode)
4. [Production Mode](#production-mode)
5. [Configuration Options](#configuration-options)
6. [Advanced Usage](#advanced-usage)
7. [Deployment](#deployment)
8. [Troubleshooting](#troubleshooting)

---

## Installation

### Install Uvicorn with Standard Dependencies
```bash
pip install uvicorn[standard]
```

### What's Included in [standard]?
- `uvloop` - Ultra fast asyncio event loop
- `httptools` - Fast HTTP parsing
- `websockets` - WebSocket support
- `watchfiles` - File change detection for auto-reload
- `python-dotenv` - Environment variable support

### Minimal Installation (Not Recommended)
```bash
pip install uvicorn
```

---

## Basic Usage

### Method 1: Using Python Script (Recommended for Development)

**run.py:**
```python
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
```

Run with:
```bash
python run.py
```

### Method 2: Command Line

**Basic:**
```bash
uvicorn app.main:app
```

**With options:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Method 3: From Python Code

```python
import uvicorn
from app.main import app

uvicorn.run(app, host="127.0.0.1", port=8000)
```

---

## Development Mode

### Auto-Reload on File Changes
```bash
uvicorn app.main:app --reload
```

**In Python:**
```python
uvicorn.run("app.main:app", reload=True)
```

### Specify Reload Directories
```bash
uvicorn app.main:app --reload --reload-dir app --reload-dir config
```

### Reload with Specific File Extensions
```bash
uvicorn app.main:app --reload --reload-include "*.py" --reload-include "*.yaml"
```

### Debug Mode with Detailed Logging
```bash
uvicorn app.main:app --reload --log-level debug
```

**In Python:**
```python
uvicorn.run(
    "app.main:app",
    host="0.0.0.0",
    port=8000,
    reload=True,
    log_level="debug"
)
```

---

## Production Mode

### Basic Production Setup
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Production with All Options
```bash
uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --log-level info \
    --access-log \
    --no-use-colors \
    --proxy-headers \
    --forwarded-allow-ips "*"
```

### Production Python Script

**run_production.py:**
```python
import uvicorn
import multiprocessing

if __name__ == "__main__":
    # Calculate workers based on CPU cores
    workers = multiprocessing.cpu_count() * 2 + 1
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        workers=workers,
        log_level="info",
        access_log=True,
        proxy_headers=True,
        forwarded_allow_ips="*"
    )
```

---

## Configuration Options

### Host and Port

```bash
# Listen on all interfaces
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Listen on localhost only
uvicorn app.main:app --host 127.0.0.1 --port 8000

# Custom port
uvicorn app.main:app --port 3000
```

### Workers (Multi-Processing)

```bash
# Specific number of workers
uvicorn app.main:app --workers 4

# Auto-calculate based on CPU cores
uvicorn app.main:app --workers $(nproc)
```

**Note:** Workers are separate processes, not threads. Each worker can handle multiple concurrent requests.

### Logging Levels

```bash
# Critical errors only
uvicorn app.main:app --log-level critical

# Errors
uvicorn app.main:app --log-level error

# Warnings
uvicorn app.main:app --log-level warning

# Info (recommended for production)
uvicorn app.main:app --log-level info

# Debug (development only)
uvicorn app.main:app --log-level debug

# Trace (very verbose)
uvicorn app.main:app --log-level trace
```

### Access Logging

```bash
# Enable access logs
uvicorn app.main:app --access-log

# Disable access logs (better performance)
uvicorn app.main:app --no-access-log

# Custom access log format
uvicorn app.main:app --access-log --log-config logging_config.yaml
```

### SSL/TLS (HTTPS)

```bash
uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 443 \
    --ssl-keyfile ./key.pem \
    --ssl-certfile ./cert.pem
```

**In Python:**
```python
uvicorn.run(
    "app.main:app",
    host="0.0.0.0",
    port=443,
    ssl_keyfile="./key.pem",
    ssl_certfile="./cert.pem"
)
```

### Proxy Headers (Behind Nginx/Apache)

```bash
uvicorn app.main:app --proxy-headers --forwarded-allow-ips "*"
```

This enables proper handling of:
- `X-Forwarded-For`
- `X-Forwarded-Proto`
- `X-Forwarded-Host`

---

## Advanced Usage

### Using Unix Domain Sockets

```bash
uvicorn app.main:app --uds /tmp/uvicorn.sock
```

### Limiting Concurrent Connections

```bash
uvicorn app.main:app --limit-concurrency 100
```

### Limiting Max Requests per Worker

```bash
# Restart worker after 1000 requests (prevents memory leaks)
uvicorn app.main:app --limit-max-requests 1000
```

### Custom Timeout

```bash
# Timeout for keep-alive connections (seconds)
uvicorn app.main:app --timeout-keep-alive 5

# Timeout for graceful shutdown (seconds)
uvicorn app.main:app --timeout-graceful-shutdown 30
```

### Custom Headers

```bash
uvicorn app.main:app --header "X-Custom-Header:Value"
```

### Environment-Based Configuration

**config.py:**
```python
import os
from typing import Optional

class UvicornConfig:
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    WORKERS: int = int(os.getenv("WORKERS", "4"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
    RELOAD: bool = os.getenv("RELOAD", "false").lower() == "true"
    
config = UvicornConfig()
```

**run_with_config.py:**
```python
import uvicorn
from config import config

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=config.HOST,
        port=config.PORT,
        workers=config.WORKERS,
        log_level=config.LOG_LEVEL,
        reload=config.RELOAD
    )
```

**.env:**
```
HOST=0.0.0.0
PORT=8000
WORKERS=4
LOG_LEVEL=info
RELOAD=false
```

---

## Deployment

### Development Server
```bash
# Windows
python run.py

# Linux/Mac
python3 run.py
```

### Production - Systemd Service (Linux)

**Create service file:** `/etc/systemd/system/cab-booking-api.service`

```ini
[Unit]
Description=Cab Booking FastAPI Application
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/mindSweepRideBooking
Environment="PATH=/var/www/mindSweepRideBooking/venv/bin"
ExecStart=/var/www/mindSweepRideBooking/venv/bin/uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --log-level info \
    --access-log

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable cab-booking-api
sudo systemctl start cab-booking-api
sudo systemctl status cab-booking-api
```

### Production - Docker

**Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

**Build and run:**
```bash
docker build -t cab-booking-api .
docker run -d -p 8000:8000 cab-booking-api
```

### Production - Docker Compose

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - LOG_LEVEL=info
      - WORKERS=4
    restart: unless-stopped
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Run:**
```bash
docker-compose up -d
```

### Production - Behind Nginx

**Nginx configuration:**
```nginx
upstream fastapi_backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://fastapi_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Run Uvicorn:**
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 4 --proxy-headers
```

### Production - Gunicorn + Uvicorn Workers

**Install:**
```bash
pip install gunicorn
```

**Run:**
```bash
gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --access-logfile - \
    --error-logfile -
```

---

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000

# Kill the process
# Windows
taskkill /PID <PID> /F

# Linux/Mac
kill -9 <PID>
```

### Module Not Found Error
```bash
# Make sure you're in the correct directory
cd e:\Programming\Hackathon\mindSweepRideBooking

# Activate virtual environment
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Auto-Reload Not Working
```bash
# Ensure watchfiles is installed
pip install watchfiles

# Specify reload directory
uvicorn app.main:app --reload --reload-dir app
```

### Workers Not Starting
```bash
# Check if port is available
# Try with single worker first
uvicorn app.main:app --workers 1

# Check logs
uvicorn app.main:app --workers 4 --log-level debug
```

### SSL Certificate Errors
```bash
# Generate self-signed certificate for testing
openssl req -x509 -newkey rsa:4096 -nodes \
    -out cert.pem -keyout key.pem -days 365

# Use with uvicorn
uvicorn app.main:app --ssl-keyfile key.pem --ssl-certfile cert.pem
```

---

## Performance Tips

### Optimal Worker Count
```python
import multiprocessing

# CPU-bound applications
workers = multiprocessing.cpu_count()

# I/O-bound applications (recommended for FastAPI)
workers = (multiprocessing.cpu_count() * 2) + 1
```

### Production Checklist
- ✅ Use `--workers` for multi-processing
- ✅ Disable `--reload` in production
- ✅ Set appropriate `--log-level` (info or warning)
- ✅ Enable `--access-log` for monitoring
- ✅ Use `--proxy-headers` if behind reverse proxy
- ✅ Set `--limit-concurrency` to prevent overload
- ✅ Use `--limit-max-requests` to prevent memory leaks
- ✅ Monitor with tools like Prometheus/Grafana

### Monitoring
```bash
# Enable access logs
uvicorn app.main:app --access-log

# Custom log format with timestamps
uvicorn app.main:app --access-log --log-config logging_config.yaml
```

---

## Quick Reference

### Development
```bash
python run.py
# or
uvicorn app.main:app --reload --log-level debug
```

### Production (Simple)
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Production (Full)
```bash
uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --log-level info \
    --access-log \
    --proxy-headers \
    --limit-concurrency 100 \
    --timeout-keep-alive 5
```

---

## Additional Resources

- **Uvicorn Documentation:** https://www.uvicorn.org/
- **FastAPI Deployment:** https://fastapi.tiangolo.com/deployment/
- **ASGI Specification:** https://asgi.readthedocs.io/

---

## For This Project

### Development
```bash
# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python run.py
```

### Production
```bash
# Run with 4 workers
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4 --log-level info
```

### Access
- **API:** http://localhost:8000
- **Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health:** http://localhost:8000/api/v1/health
