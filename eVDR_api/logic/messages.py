import os
from django.conf import settings
import requests

from eVDR_api.models import Indizi


def evaluate_vdr(vdr):
    system_description = "Hai organizzato una cacci al tesoro. Hai ideato degli indizi, ogni indizio porta ad un luogo, tuttavia i concorrenti di questa caccia al tesoro hanno bisogno di un tuo feedback sulle loro soluzioni proposte.\n\nIl tuo compito è quello valutare i ragionamenti proposti e sottolineare le parti del ragionamento che sono giuste, ossia che non contengono errori e che concorrano in maniera fondamentale alla risoluzione di un indizio.\n\nPer sottolineare una frase giusta logicamente, devi mettere un asterisco singolo prima ed un asterisco singolo dopo la frase giusta. Devi usare questa sintassi:\n\nfrase non sottolineata, *frase sottolineata*\n\nPer farti capire meglio in che modo devi valutare i ragionamenti ti riporto diversi esempi.\n\nESEMPIO 1:\n\nSoluzione giusta:\nL'\''indizio è costituito da un pacco di farina di 100 grammi e da una serie di alcolici. Gli alcolici indicano un BAR, cento grammi di farina sono un ETTO. Unendo le parole BAR ed ETTO troviamo Baretto. La soluzione è Baretto a Massa Lubrense.\n\nSoluzione proposta:\nL'\''indizio è un pacco di farina e delle bottiglie. Il pacco di farina è di ben cento grammi, cento grammi risulta essere il nome di un ristorante a viale nizza a sorrento dove vendono anche alcolici. La soluzione pertanto è Ristorante Cento Grammi Sorrento.\n\nSoluzione valutata:\nSOLUZIONE PARZIALMENTE CCORRETTA\n*L'\''indizio è un pacco di farina e delle bottiglie.* *Il pacco di farina è di ben cento grammi*, cento grammi risulta essere il nome di un ristorante a viale nizza a sorrento dove vendono anche alcolici. La soluzione pertanto è Ristorante Cento Grammi Sorrento.\n\nESEMPIO 2:\n\nSoluzione giusta:\nL'\''indizio è costituito da due immagini raffiguranti due battenti per portoni anche noti come batacchi. Tra le due immagini si trova il numero 60. I batacchi risultano essere un riferimento al personaggio del film Fantozzi subisce ancora, tale Loris Batacchi, interpretato da Andrea Roncato. A Massa Lubrense esiste Via Roncato, la soluzione pertanto è Via Roncato 60 Massa Lubrense.\n\nSoluzione proposta:\nI due battenti vengono anche chiamati batacchi. Batacchi è il nome di un personaggio dei un film di Fantozzi. Fantozzi è interpretato da Paolo Villaggio, nel film incontra Loris Batacchi. Ci dirigiamo a Villaggio Paolo a Tramonti.\n\nSoluzione valutata:\nSOLUZIONE PARZIALMENTE CCORRETTA\n*I due battenti vengono anche chiamati batacchi. Batacchi è il nome di un personaggio dei un film di Fantozzi. Fantozzi è interpretato da Paolo Villaggio, nel film incontra Loris Batacchi.* Ci dirigiamo a Villaggio Paolo a Tramonti.\n\nIn questa soluzione come vedi ci sono degli elementi superflui ma non del tutto sbagliati, pertanto li ho comunque sottolineati.\n\nESEMPIO 3:\n\nSoluzione giusta:\nL'\''indizio è costituito da una serie di bottigline di vetro contenenti una serie di bevande, queste bottigline sono numerate, assieme alle bottigline si ha anche un foglio con una lista di descrizioni di pozioni, i numeri corrispondono a come sono numerate le descrizioni. Identifichiamo quindi per ogni una delle 8 descrizioni il nome di un dink ottenuto miscelando le bevande con lo stesso numero. I cocktail che riconosciamo sono i seguenti: 1: vieux carrè 2: illegal 3: aviation 4: sidecar 5: paper plane 6: illegal 7: naked and famous 8: aviation. Dalle iniziali, capiamo che dobbiamo andare a Via Spina, a Massa\n\nSoluzione proposta:\nAbbiamo alcune bottigline di vetro con degli alcolici e non, ogni bottiglia è numerata, la numerazione segue quella di una lista di descrizioni di pozioni. Identifichiamo quindi per ogni una delle 8 descrizioni il nome di un dink ottenuto miscelando le bevande con lo stesso numero. I cocktail che riconosciamo sono i seguenti: scofflaw, imperial, ford sidecar, power plane, avada kedavra, naked and famous, aviation,. Anagrammiamo le lettere iniziali di ogni parola dei nomi dei cocktail ed otteniamo  fan passi, i primi passi li abbiamo fatti in piazza tasso pertanto ci rechiamo a piazza tasso\n\nSoluzione valutata:\nSOLUZIONE PARZIALMENTE CCORRETTA\n*Abbiamo alcune bottigline di vetro con degli alcolici e non, ogni bottiglia è numerata, la numerazione segue quella di una lista di descrizioni di pozioni. Identifichiamo quindi per ogni una delle 8 descrizioni il nome di un dink ottenuto miscelando le bevande con lo stesso numero. I cocktail che riconosciamo sono i seguenti:* scofflaw, imperial, ford *sidecar*, power plane, avada kedavra, *naked and famous* *aviation*. Anagrammiamo le lettere iniziali di ogni parola dei nomi dei cocktail ed otteniamo  fan passi, i primi passi li abbiamo fatti in piazza tasso pertanto ci rechiamo a piazza tasso\n\n------------------------------------\n\nNota bene se la soluzione reca il posto giusto e gran parte del ragionamento è corretto risponderai con\n\nSoluzione corretta!\n\nSe invece nella soluzione proposta non c'\''è nulla di esatto risponderai con\n\nSoluzione sbagliata!\n\n-----------------------------------\n\nDetto ciò ecco la soluzione giusta di riferimento che userai per valutare i ragionamenti proposti.\n\nSoluzione giusta:\n"
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
        return None