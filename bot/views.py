from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
from .models import Message, Conversation
import requests

genai.configure(api_key=settings.GEMINI_API_KEY)

@api_view(['POST'])
def process_message(request):
    """Process incoming WhatsApp message and generate AI reply"""
    phone_number = request.data.get('from')
    message_text = request.data.get('body')

    if not phone_number or not message_text:
        return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

    # Save incoming message
    message = Message.objects.create(
        phone_number=phone_number,
        message_text=message_text
    )

    # Get or create conversation context
    conversation, created = Conversation.objects.get_or_create(
        phone_number=phone_number,
        defaults={'context': []}
    )

    # Build conversation history for Gemini
    conversation.context.append({
        'role': 'user',
        'parts': [message_text]
    })

    # Keep only last 20 messages for context
    if len(conversation.context) > 20:
        conversation.context = conversation.context[-20:]

    try:
        # Generate AI response using Gemini 2.5 Flash
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Convert context to Gemini format
        history = []
        for i, msg in enumerate(conversation.context[:-1]):
            role = 'user' if msg['role'] == 'user' else 'model'
            history.append({
                'role': role,
                'parts': msg['parts']
            })

        chat = model.start_chat(history=history)
        response = chat.send_message(message_text)
        ai_reply = response.text

        # Save AI response
        message.ai_response = ai_reply
        message.save()

        # Update conversation context
        conversation.context.append({
            'role': 'model',
            'parts': [ai_reply]
        })
        conversation.save()

        return Response({'reply': ai_reply}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def whatsapp_status(request):
    """Check WhatsApp service status"""
    try:
        response = requests.get('http://localhost:3000/status', timeout=5)
        return Response(response.json(), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e), 'ready': False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(['GET'])
def conversation_history(request, phone_number):
    """Get conversation history for a phone number"""
    messages = Message.objects.filter(phone_number=phone_number).order_by('-timestamp')[:50]
    data = [{
        'message': msg.message_text,
        'reply': msg.ai_response,
        'timestamp': msg.timestamp
    } for msg in messages]

    return Response(data, status=status.HTTP_200_OK)

def dashboard(request):
    """Render the dashboard UI"""
    return render(request, 'bot/dashboard.html')

def setup(request):
    """Render the setup UI"""
    return render(request, 'bot/setup.html')

def contacts(request):
    """Render the contacts UI"""
    return render(request, 'bot/contacts.html')

@api_view(['GET'])
def list_conversations(request):
    """List all recent conversations"""
    conversations = Conversation.objects.all().order_by('-updated_at')[:20]

    data = []
    for conv in conversations:
        messages = Message.objects.filter(phone_number=conv.phone_number).order_by('-timestamp')[:1]
        last_message = messages[0] if messages else None

        data.append({
            'phone_number': conv.phone_number,
            'last_message': last_message.message_text if last_message else '',
            'last_reply': last_message.ai_response if last_message else '',
            'timestamp': last_message.timestamp if last_message else conv.updated_at,
            'message_count': Message.objects.filter(phone_number=conv.phone_number).count()
        })

    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
@csrf_exempt
def save_api_key(request):
    """Save Gemini API key to .env file"""
    api_key = request.data.get('api_key')

    if not api_key:
        return Response({'error': 'API key is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        import os
        from pathlib import Path

        # Get the base directory
        base_dir = Path(__file__).resolve().parent.parent
        env_file = base_dir / '.env'

        # Read existing .env content
        env_content = {}
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        env_content[key.strip()] = value.strip()

        # Update API key
        env_content['GEMINI_API_KEY'] = api_key

        # Write back to .env
        with open(env_file, 'w') as f:
            for key, value in env_content.items():
                f.write(f'{key}={value}\n')

        # Update settings
        settings.GEMINI_API_KEY = api_key
        genai.configure(api_key=api_key)

        return Response({'success': True, 'message': 'API key saved successfully'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def check_config(request):
    """Check if API key is configured"""
    api_key = settings.GEMINI_API_KEY
    configured = bool(api_key and api_key.strip())

    return Response({'configured': configured}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_contacts(request):
    """Get all WhatsApp contacts"""
    try:
        response = requests.get('http://localhost:3000/contacts', timeout=10)
        return Response(response.json(), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(['GET'])
def get_chats(request):
    """Get all WhatsApp chats"""
    try:
        response = requests.get('http://localhost:3000/chats', timeout=10)
        return Response(response.json(), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(['POST'])
def reset_whatsapp(request):
    """Reset WhatsApp connection and clear session"""
    try:
        response = requests.post('http://localhost:3000/reset', timeout=30)
        return Response(response.json(), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
