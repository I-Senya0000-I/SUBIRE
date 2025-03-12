import g4f
from g4f.client import Client


client = Client()


def answerpls(history, message):
    response = client.chat.completions.create(
        model="gpt-4",
        provider=g4f.Provider.Ai4Chat,
        messages=[{"role": "system", "content": "you will receive chemical reactions. answer only result of them"},
        ]+history+{"role": "user", "content": message},
        # Add any other necessary parameters
    )
    return response.choices[0].message.content
