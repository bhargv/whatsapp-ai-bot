# WhatsApp AI Bot - Usage Guide

## Features Added ✓

### 1. **Automatic AI Replies**
- The bot now automatically replies to ALL incoming messages
- No manual intervention needed
- Skips group messages and status updates
- Uses AI (Gemini) to generate contextual responses

### 2. **View All Contacts**
- New contacts page at `http://localhost:8000/contacts/`
- Shows all your WhatsApp contacts
- Displays recent chats
- Search functionality to find contacts quickly
- Real-time statistics

### 3. **Enhanced Dashboard**
- View all conversations
- Send manual messages
- Monitor connection status
- Track message history

## How to Start the Bot

### Step 1: Start WhatsApp Service
Open a terminal and run:
```bash
cd C:\Users\Lenovo\whatsapp-ai-bot
npm start
```

Scan the QR code with your WhatsApp mobile app.

### Step 2: Start Django Server
Open another terminal and run:
```bash
cd C:\Users\Lenovo\whatsapp-ai-bot
python manage.py runserver
```

### Step 3: Configure API Key
1. Go to `http://localhost:8000/`
2. Enter your Gemini API key
3. Complete the setup

## Access the Bot

- **Setup Page**: http://localhost:8000/
- **Dashboard**: http://localhost:8000/dashboard/
- **Contacts Page**: http://localhost:8000/contacts/ ← **NEW!**

## What Happens Now

1. **Someone sends you a message** → Bot receives it
2. **AI processes the message** → Generates smart reply
3. **Bot sends reply automatically** → No action needed from you
4. **Conversation continues** → AI maintains context

## API Endpoints

- `GET /api/contacts/` - Get all WhatsApp contacts
- `GET /api/chats/` - Get all recent chats
- `GET /api/conversations/` - Get AI conversation history
- `POST /api/process-message/` - Process incoming messages
- `GET /api/status/` - Check WhatsApp connection status

## Important Notes

⚠️ **Auto-Reply is ALWAYS ON** - The bot will reply to every message automatically
⚠️ **Group messages are ignored** - Only responds to individual chats
⚠️ **Keep both services running** - WhatsApp service (port 3000) and Django (port 8000)

## Troubleshooting

**Bot not replying?**
- Check if both services are running
- Verify WhatsApp is connected (green status)
- Check Gemini API key is configured

**Can't see contacts?**
- Make sure WhatsApp service is connected
- Wait a few seconds for contacts to load
- Refresh the page

**Connection lost?**
- Restart the WhatsApp service
- Scan QR code again
