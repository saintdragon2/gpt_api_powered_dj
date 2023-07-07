import openai

openai.api_key = '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'

def ask_to_gpt_35_turbo(messages):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        temperature=0.5,
        messages=messages
    )

    return response.choices[0].message.content

def main():
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
    ]

    while True:
        user_input = input('You: ')

        if user_input.lower() == 'quit':
            break

        messages.append(
            {'role': 'user', 'content': user_input},
        )

        response = ask_to_gpt_35_turbo(messages)

        messages.append(
            {'role': 'assistant', 'content': response},
        )

        print(response)


if __name__ == "__main__":
    main()