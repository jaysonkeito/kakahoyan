import json
from groq import Groq
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import ChatSession, ChatMessage, FAQItem

SYSTEM_PROMPT = """You are Kaka, the friendly virtual assistant for Kakahoyan — an exclusive event venue in Sta. Catalina, Negros Oriental, Philippines.

About Kakahoyan:
- Location: Purok 2, Brgy. Caranoche, Sta. Catalina, Negros Oriental, 6220
- Contact: 0920 611 2718
- Indoor venue: Fully air-conditioned Glass Pavilion — seats up to 250 guests
- Outdoor: Lawn and outdoor platform also available
- Events catered: weddings, birthdays, reunions, graduation parties, company events, seminars, socials
- Always open (by appointment)
- Facebook: Kakahoyan

Your job:
- Answer questions about the venue, capacity, events, booking, and location
- Help clients understand how to set an appointment (they can book through this website)
- For appointments: the manager meets clients at Kakahoyan or at a client-specified location between Sta. Catalina and Bayawan City, or via phone call
- If someone wants to book or needs a formal quote, guide them to the Appointment Booking page on this website
- Be warm, professional, and helpful. Speak in a friendly Filipino-English tone.
- If you don't know the answer to something specific (like exact pricing), honestly say it and suggest they book an appointment or call 0920 611 2718.
- Keep responses concise and helpful. Do not make up information.
- IMPORTANT: Only answer questions related to Kakahoyan — the venue, events, booking, location, packages, or appointments. If the user asks about anything unrelated (e.g., recipes, math, general knowledge, other businesses), politely decline and redirect them back to Kakahoyan topics. Example: "I'm only able to help with questions about Kakahoyan! Is there anything about our venue or bookings I can assist you with?" """


def get_or_create_session(request):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    session, _ = ChatSession.objects.get_or_create(session_key=session_key)
    return session


@require_POST
def chat_message(request):
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        if not user_message:
            return JsonResponse({'error': 'Empty message'}, status=400)

        session = get_or_create_session(request)
        ChatMessage.objects.create(session=session, role='user', content=user_message)

        # Build message history (last 10 for context)
        history = session.messages.order_by('-created_at')[:10]
        messages_payload = [{'role': m.role, 'content': m.content} for m in reversed(history)]

        api_key = getattr(settings, 'GROQ_API_KEY', '')
        if not api_key:
            reply = "I'm currently unavailable. Please call 0920 611 2718."
        else:
            client = Groq(api_key=api_key)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # free and fast
                max_tokens=500,
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages_payload,
            )
            reply = response.choices[0].message.content

        ChatMessage.objects.create(session=session, role='assistant', content=reply)
        return JsonResponse({'reply': reply})

    except Exception as e:
        return JsonResponse({
            'reply': f'Sorry, I had a problem. Please call 0920 611 2718 or message us on Facebook!'
        })


def get_faqs(request):
    faqs = FAQItem.objects.filter(is_active=True).values('question', 'answer')
    return JsonResponse({'faqs': list(faqs)})