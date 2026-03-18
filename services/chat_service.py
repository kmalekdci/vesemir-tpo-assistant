import tiktoken
from config import client, MODEL, SYSTEM_PROMPT
from storage.chat_repository import (
    save_message,
    load_messages,
    set_title
)


def count_tokens(text):

    enc = tiktoken.get_encoding("cl100k_base")

    return len(enc.encode(text))


def build_messages(chat_id):

    rows = load_messages(chat_id)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for m in rows:
        messages.append(m)

    return messages


def generate_title(first_message):

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Create a very short chat title (max 5 words)."},
            {"role": "user", "content": first_message}
        ]
    )

    return completion.choices[0].message.content.strip()


def stream_chat(chat_id, user_message, stop_flag):

    user_tokens = count_tokens(user_message)

    save_message(chat_id, "user", user_message, user_tokens)

    messages = build_messages(chat_id)

    print(messages)

    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=True
    )

    response = ""

    for chunk in stream:

        if stop_flag["stop"]:
            break

        delta = chunk.choices[0].delta.content or ""
        response += delta

        yield response

    tokens = count_tokens(response)

    save_message(chat_id, "assistant", response, tokens)

    # title generation
    if len(messages) == 2:
        title = generate_title(user_message)
        set_title(chat_id, title)
