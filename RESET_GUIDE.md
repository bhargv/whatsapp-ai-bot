# WhatsApp Connection Reset Guide

## When to Reset

Reset your WhatsApp connection when:
- You logged out from WhatsApp on your phone
- The bot stops responding to messages
- You see "Execution context was destroyed" errors
- You want to connect a different WhatsApp account

## Method 1: Using the Web UI (Recommended)

1. Open your browser and go to: `http://localhost:8000/setup`
2. Navigate to Step 2 (Connect WhatsApp)
3. Click the **"🔄 Reset WhatsApp Connection"** button
4. Confirm the reset
5. Wait for the new QR code to appear
6. Scan the QR code with your WhatsApp mobile app

## Method 2: Using Command Line

### Windows:
```bash
cd whatsapp-ai-bot
reset_whatsapp.bat
```

### Linux/Mac:
```bash
cd whatsapp-ai-bot
node reset_whatsapp.js
```

After running the command:
1. Go to `http://localhost:8000/setup`
2. Scan the new QR code

## Method 3: Manual Reset

If the above methods don't work:

1. Stop all services (close the terminal windows)
2. Delete the `.wwebjs_auth` folder:
   ```bash
   cd whatsapp-ai-bot
   rm -rf .wwebjs_auth
   ```
3. Restart the services:
   ```bash
   start_services.bat
   ```
4. Go to `http://localhost:8000/setup` and scan the QR code

## Troubleshooting

### "Cannot connect to WhatsApp service"
- Make sure the WhatsApp service is running on port 3000
- Check if you started the services with `start_services.bat`

### QR Code Not Appearing
- Wait 10-15 seconds after reset
- Refresh the page
- Check the terminal for any error messages

### Still Having Issues?
- Restart both services completely
- Delete `.wwebjs_auth` and `.wwebjs_cache` folders
- Run `start_services.bat` again

## Notes

- Resetting will disconnect your current WhatsApp session
- You'll need to scan the QR code again to reconnect
- All conversation history in the database will be preserved
- The reset only affects the WhatsApp connection, not your API key
