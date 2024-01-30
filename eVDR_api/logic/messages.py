import os
import json
from django.conf import settings
import requests

from eVDR_api.models import Indizi, SystemDescription


def evaluate_vdr(vdr):
    # Recupera l'ultima descrizione del sistema dal database
    try:
        system_desc = SystemDescription.objects.latest('last_updated')
        system_description = system_desc.description
    except SystemDescription.DoesNotExist:
        return "Bot non disponibile..."

    # Recupera l'ultima entry di Indizi
    last_indizi = Indizi.objects.last()
    if last_indizi:
        solution = last_indizi.solution
    else:
        solution = "Nessuna soluzione disponibile."

    messages = [{
        "role": "system",
        "content": system_description + "\n\n" + solution
    }]
    messages.append({"role": "user", "content": vdr})

    headers = {
        'Authorization': f'Bearer {settings.OPENAI_API_KEY}'
    }

    # print(settings.OPENAI_API_KEY)

    data = {
        'model': 'gpt-4',
        'messages': messages,
        'temperature': 1,
        'max_tokens': 1000,
        'top_p': 1,
        'frequency_penalty': 0,
        'presence_penalty': 0
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)
        response.raise_for_status()  # Assicurati che la richiesta sia andata a buon fine
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print("Si è verificato un errore:", e)
        return "Bot non disponibile..."