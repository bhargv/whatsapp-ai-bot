const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const express = require('express');
const axios = require('axios');

const app = express();
app.use(express.json());

const client = new Client({
    authStrategy: new LocalAuth({
        dataPath: '.wwebjs_auth'
    }),
    puppeteer: {
        headless: false,
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--no-first-run',
            '--no-zygote',
            '--single-process',
            '--disable-gpu'
        ],
        timeout: 60000
    }
});

let isReady = false;
let qrCodeData = null;

// QR Code generation
client.on('qr', (qr) => {
    console.log('QR Code received, scan with WhatsApp:');
    qrcode.generate(qr, { small: true });
    qrCodeData = qr;
});

client.on('ready', () => {
    console.log('WhatsApp client is ready!');
    isReady = true;
    qrCodeData = null;
});

client.on('authenticated', () => {
    console.log('WhatsApp authenticated successfully!');
});

client.on('auth_failure', (msg) => {
    console.error('Authentication failed:', msg);
});

client.on('disconnected', (reason) => {
    console.log('Client was disconnected:', reason);
});

client.on('loading_screen', (percent, message) => {
    console.log('Loading...', percent, message);
});

// Handle incoming messages - AUTO REPLY ENABLED
client.on('message', async (message) => {
    try {
        // Skip group messages and status updates
        if (message.from.includes('@g.us') || message.from === 'status@broadcast') {
            return;
        }

        console.log(`Message from ${message.from}: ${message.body}`);

        // Send message to Django backend for AI processing
        const response = await axios.post('http://localhost:8000/api/process-message/', {
            from: message.from,
            body: message.body,
            timestamp: message.timestamp
        });

        if (response.data.reply) {
            await message.reply(response.data.reply);
            console.log(`Auto-replied: ${response.data.reply}`);
        }
    } catch (error) {
        console.error('Error processing message:', error.message);
    }
});

// API endpoints
app.get('/status', (req, res) => {
    res.json({
        ready: isReady,
        qrCode: qrCodeData
    });
});

app.post('/send-message', async (req, res) => {
    const { number, message } = req.body;

    if (!isReady) {
        return res.status(503).json({ error: 'WhatsApp client not ready' });
    }

    try {
        const chatId = number.includes('@c.us') ? number : `${number}@c.us`;
        await client.sendMessage(chatId, message);
        res.json({ success: true });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Get all contacts
app.get('/contacts', async (req, res) => {
    if (!isReady) {
        return res.status(503).json({ error: 'WhatsApp client not ready' });
    }

    try {
        const contacts = await client.getContacts();
        const contactList = contacts
            .filter(contact => contact.isMyContact && !contact.isGroup)
            .map(contact => ({
                id: contact.id._serialized,
                name: contact.name || contact.pushname || contact.number,
                number: contact.number,
                pushname: contact.pushname,
                isMyContact: contact.isMyContact
            }));

        res.json({ contacts: contactList, count: contactList.length });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Get all chats
app.get('/chats', async (req, res) => {
    if (!isReady) {
        return res.status(503).json({ error: 'WhatsApp client not ready' });
    }

    try {
        const chats = await client.getChats();
        const chatList = chats
            .filter(chat => !chat.isGroup)
            .map(chat => ({
                id: chat.id._serialized,
                name: chat.name,
                lastMessage: chat.lastMessage ? {
                    body: chat.lastMessage.body,
                    timestamp: chat.lastMessage.timestamp
                } : null,
                unreadCount: chat.unreadCount
            }));

        res.json({ chats: chatList, count: chatList.length });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Reset/logout endpoint
app.post('/reset', async (req, res) => {
    try {
        console.log('Resetting WhatsApp connection...');

        // Destroy the client
        await client.destroy();

        // Delete auth folder
        const fs = require('fs');
        const path = require('path');
        const authPath = path.join(__dirname, '.wwebjs_auth');

        if (fs.existsSync(authPath)) {
            fs.rmSync(authPath, { recursive: true, force: true });
            console.log('Auth folder deleted');
        }

        // Reset state
        isReady = false;
        qrCodeData = null;

        // Reinitialize client
        setTimeout(() => {
            client.initialize();
            console.log('Client reinitialized');
        }, 2000);

        res.json({ success: true, message: 'WhatsApp connection reset successfully' });
    } catch (error) {
        console.error('Reset error:', error);
        res.status(500).json({ error: error.message });
    }
});

const PORT = process.env.WHATSAPP_SERVICE_PORT || 3000;
app.listen(PORT, () => {
    console.log(`WhatsApp service running on port ${PORT}`);
});

// Initialize with error handling
client.initialize().catch(err => {
    console.error('Failed to initialize WhatsApp client:', err);
    process.exit(1);
});
