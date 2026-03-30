# WhatsApp AI Bot

Django application with WhatsApp Web integration and AI-powered auto-replies using Claude.

## Features
- QR code login for WhatsApp Web
- AI-powered message responses using Claude API
- Conversation history tracking
- REST API for message processing

## Setup

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install Node.js Dependencies
```bash
npm install
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env` and add your Anthropic API key:
```bash
ANTHROPIC_API_KEY=your_actual_api_key_here
```

### 4. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Django Admin User (Optional)
```bash
python manage.py createsuperuser
```

## Running the Application

### Start WhatsApp Service (Terminal 1)
```bash
npm start
```
Scan the QR code with your WhatsApp mobile app.

### Start Django Server (Terminal 2)
```bash
python manage.py runserver
```

## How It Works

1. WhatsApp service connects via QR code
2. Incoming messages are sent to Django API
3. Claude AI generates contextual replies
4. Responses are sent back through WhatsApp

## API Endpoints

- `POST /api/process-message/` - Process incoming WhatsApp messages
- `GET /api/status/` - Check WhatsApp connection status
- `GET /api/history/<phone_number>/` - Get conversation history

## Admin Panel

Access at `http://localhost:8000/admin/` to view messages and conversations.
