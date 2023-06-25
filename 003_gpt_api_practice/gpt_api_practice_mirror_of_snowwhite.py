import openai

openai.api_key = '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'

def ask_to_gpt_35_turbo(user_input):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        temperature=0.5,
        messages=[
            {'role': 'system', 'content': 'You are the mirror of Snow White. You must pretend like the mirror of the story.'},
            {'role': 'user', 'content': user_input},
        ]
    )

    return response.choices[0].message.content


answer = ask_to_gpt_35_turbo('세상에서 누가 제일 예쁘니?')
print(answer)