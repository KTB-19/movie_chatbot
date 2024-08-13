import openai

def get_chatgpt_response(prompt):
    openai.api_key = "YOUR_API_KEY"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']