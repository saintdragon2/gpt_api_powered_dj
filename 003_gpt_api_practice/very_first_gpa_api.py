import openai

openai.api_key = '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'

def ask_to_gpt_35_turbo(user_input):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        temperature=0.5,
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': user_input},
        ]
    )

    return response.choices[0].message.content



answer = ask_to_gpt_35_turbo('너에 대한 소개를 해줘')
print(answer)