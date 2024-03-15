import requests

OPENAI_API_KEY = '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'
OPENAI_API_URL = 'https://api.openai.com/v1/chat/completions'

def get_chat_response(prompt):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }
    data = {
        'model': 'gpt-3.5-turbo-0125',  # Update the model to one that is available
        'messages': [
            {'role': 'user', 'content': prompt}
        ]
    }
    response = requests.post(OPENAI_API_URL, headers=headers, json=data)
    print(response.json())
    return response.json()['choices'][0]['message']['content'].strip()
    
    
