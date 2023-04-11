from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import Conversation
import os
import openai
import toml

secrets_file = os.path.join(os.path.dirname(__file__), 'secrets.toml')
secrets = toml.load(secrets_file)
api_key = secrets['chatgpt']['api_key']

def generate_response(user_input, history=None):
    openai.api_key = api_key
    model_engine = "text-davinci-003"
    
    prompt = ""
    if history:
        prompt = f"{history}\n"
    prompt += f'Conversation with chatbot\n{user_input}\nBot: '
    
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()


def chat_view(request):
    context = {}
    if request.method == 'POST':
        user_input = request.POST['user_input']

        # Get the most recent conversation from the database
        previous_conversation = Conversation.objects.order_by('-timestamp').first()

        # Generate a response from the chatbot
        bot_response = generate_response(user_input, previous_conversation.bot_response)

        # Save the current conversation to the database
        conversation = Conversation(user_input=user_input, bot_response=bot_response)
        conversation.save()

        # Add the previous conversation to the context, if available
        if previous_conversation:
            context['previous_input'] = previous_conversation.user_input
            context['previous_response'] = previous_conversation.bot_response

        # Add the current conversation to the context
        context['user_input'] = user_input
        context['bot_response'] = bot_response

        # Return the context as JSON
        return JsonResponse(context)

    return render(request, 'chatgpt_app/chat.html')

