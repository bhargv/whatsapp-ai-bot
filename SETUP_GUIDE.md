# WhatsApp AI Bot - Complete Setup Guide

## 🚀 Quick Start (3 Easy Steps!)

### Step 1: Start the Application

Run the startup script:
```bash
cd C:\Users\Lenovo\whatsapp-ai-bot
start_services.bat
```

This will open two windows:
- Django Server (Port 8000)
- WhatsApp Service (Port 3000)

### Step 2: Open the Setup Page

Open your browser and go to:
```
http://localhost:8000/
```

### Step 3: Follow the Setup Wizard

The setup wizard will guide you through:

1. **Configure API Key**
   - Enter your Google Gemini API key
   - Don't have one? Get it free at: https://aistudio.google.com/app/apikey
   - Click "Save & Continue"

2. **Connect WhatsApp**
   - A QR code will appear
   - Open WhatsApp on your phone
   - Go to Settings → Linked Devices → Link a Device
   - Scan the QR code
   - Wait for connection confirmation

3. **Done!**
   - You'll be redirected to the dashboard
   - Your bot is now ready to use!

## 📱 Using the Dashboard

Once setup is complete, you can:

- **View Connection Status**: See if WhatsApp is connected
- **Send Messages**: Send messages to any WhatsApp number
- **View Conversations**: See all bot conversations with message counts
- **Monitor Activity**: Real-time status updates

## 🔧 Features

- **Automatic AI Responses**: Bot automatically replies to incoming WhatsApp messages using Gemini AI
- **Conversation History**: All messages are saved in the database
- **Context Awareness**: Bot remembers conversation context (last 20 messages)
- **Easy Configuration**: Web-based setup, no manual file editing needed
- **Real-time Status**: Dashboard updates every 5 seconds

## 📝 API Endpoints

- `GET /` - Setup wizard
- `GET /dashboard/` - Main dashboard
- `GET /api/status/` - Check WhatsApp connection status
- `POST /api/save-api-key/` - Save Gemini API key
- `GET /api/check-config/` - Check if configured
- `POST /api/process-message/` - Process incoming messages (used by WhatsApp service)
- `GET /api/conversations/` - List all conversations
- `GET /api/history/<phone_number>/` - Get conversation history

## 🛠️ Troubleshooting

### Services not starting?
- Make sure ports 8000 and 3000 are not in use
- Check if Python and Node.js are installed

### WhatsApp not connecting?
- Make sure the WhatsApp service is running (check port 3000)
- Try refreshing the QR code by restarting the WhatsApp service

### API key not working?
- Make sure you copied the full API key (starts with "AIza")
- Get a new key from Google AI Studio if needed

### Messages not being sent?
- Check if WhatsApp is connected (green indicator)
- Make sure phone number includes country code (no + or spaces)

## 🎯 Next Steps

After setup, you can:
1. Test the bot by sending a message from another WhatsApp account
2. Send messages through the dashboard
3. View conversation history
4. Monitor bot activity in real-time

## 📞 Support

For issues or questions, check the README.md file or the project documentation.

---

**Enjoy your WhatsApp AI Bot! 🤖**
