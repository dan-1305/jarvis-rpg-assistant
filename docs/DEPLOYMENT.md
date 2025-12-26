# Jarvis RPG Assistant - Production Deployment Guide

## Webhook Setup for Render/Heroku

### 1. Environment Variables

Set these in your deployment platform:

```bash
TELEGRAM_BOT_TOKEN=your_actual_bot_token
USE_WEBHOOK=true
WEBHOOK_URL=https://your-app.onrender.com
PORT=8443
ADMIN_CHAT_IDS=your_admin_chat_id
GOOGLE_API_KEY=your_google_api_key
```

### 2. Render Deployment

**render.yaml:**
```yaml
services:
  - type: web
    name: jarvis-bot
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python -m jarvis_core.telegram_webhook
    envVars:
      - key: PYTHON_VERSION
        value: 3.10.0
      - key: USE_WEBHOOK
        value: true
```

### 3. Heroku Deployment

**Procfile:**
```
web: python -m jarvis_core.telegram_webhook
```

**Deploy commands:**
```bash
heroku create your-app-name
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set USE_WEBHOOK=true
heroku config:set WEBHOOK_URL=https://your-app.herokuapp.com
git push heroku main
```

### 4. Local Development

Use polling mode:
```bash
# .env
USE_WEBHOOK=false
```

Run:
```bash
python -m jarvis_core.telegram_webhook
```

### 5. Testing Webhook

Test your webhook is working:
```bash
curl https://your-app.onrender.com/webhook/YOUR_BOT_TOKEN
```

### 6. Error Monitoring

Errors are automatically sent to admin users via Telegram.

Configure in `.env`:
```bash
ADMIN_CHAT_IDS=123456789,987654321
```

## Database Sync

The bot automatically:
1. Pulls latest DB changes before updates
2. Commits and pushes after changes
3. Uses transaction locks to prevent conflicts

## Testing

Run tests locally:
```bash
./run_tests.bat    # Windows
./run_tests.sh     # Linux/Mac
```

Minimum 80% coverage required.
