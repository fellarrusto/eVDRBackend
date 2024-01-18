import os
from django.conf import settings
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)

system_description = ""
solution = ""

system = {
            "role": "system",
            "content": system_description + "\n\n" + solution
         }

def evaluate_vdr(vdr):
    # Aggiunge il nuovo messaggio dell'utente alla conversazione
    messages = system
    messages.append({"role": "user", "content": vdr})

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=1,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        # Estrai e restituisci solo il testo della risposta
        return response.choices[0].message.content
    except Exception as e:
        # Gestisci qui l'errore
        print("Si è verificato un errore:", e)
        return None