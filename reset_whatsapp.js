#!/usr/bin/env node

const axios = require('axios');

console.log('🔄 Resetting WhatsApp connection...\n');

axios.post('http://localhost:3000/reset')
    .then(response => {
        console.log('✅ Success:', response.data.message);
        console.log('\nYou can now scan a new QR code at: http://localhost:8000/setup');
        process.exit(0);
    })
    .catch(error => {
        if (error.response) {
            console.error('❌ Error:', error.response.data.error || error.message);
        } else if (error.request) {
            console.error('❌ Cannot connect to WhatsApp service on port 3000');
            console.error('   Make sure the service is running with: node whatsapp_service.js');
        } else {
            console.error('❌ Error:', error.message);
        }
        process.exit(1);
    });
