import gradio as gr

from storage.chat_repository import (
    init_db,
    create_chat,
    list_chats,
    delete_chat,
    load_messages
)

from services.chat_service import stream_chat


init_db()

stop_flag = {"stop": False}


# -----------------------------
# Helpers
# -----------------------------

def sidebar_choices():
    """Return (label, value) pairs for sidebar."""
    chats = list_chats()
    return [(title, chat_id) for chat_id, title in chats]


# -----------------------------
# Chat logic
# -----------------------------

def chat(message, history, chat_id):

    if not chat_id:
        chat_id = create_chat()

    stop_flag["stop"] = False

    history = history or []

    # dodaj user
    history.append({"role": "user", "content": message})

    # placeholder assistant
    history.append({"role": "assistant", "content": ""})

    for chunk in stream_chat(chat_id, message, stop_flag):

        history[-1]["content"] = chunk

        yield history, chat_id


def stop():
    stop_flag["stop"] = True


# -----------------------------
# Sidebar actions
# -----------------------------

def new_chat():

    chat_id = create_chat()

    return (
        [],
        chat_id,
        gr.update(choices=sidebar_choices(), value=chat_id)
    )


def select_chat(chat_id):

    if not chat_id:
        return [], None

    rows = load_messages(chat_id)

    history = [
        {"role": m["role"], "content": m["content"]}
        for m in rows
    ]

    return history, chat_id


def delete_current(chat_id):

    if chat_id:
        delete_chat(chat_id)

    return (
        [],
        None,
        gr.update(choices=sidebar_choices(), value=None)
    )


# -----------------------------
# UI
# -----------------------------

with gr.Blocks(css="""
#sidebar {background:#f7f7f8; padding:10px}
""") as demo:

    chat_id_state = gr.State()

    with gr.Row():

        # SIDEBAR
        with gr.Column(scale=1, elem_id="sidebar"):

            new_btn = gr.Button("➕ New Chat")

            chat_list = gr.Radio(
                choices=sidebar_choices(),
                label=None
            )

            delete_btn = gr.Button("🗑 Delete Chat")

        # MAIN CHAT
        with gr.Column(scale=4):

            chatbot = gr.Chatbot(height=600)

            msg = gr.Textbox(
                placeholder="Message",
                show_label=False
            )

            with gr.Row():

                send = gr.Button("Send")
                stop_btn = gr.Button("Stop")


    # -----------------------------
    # Events
    # -----------------------------

    send.click(
        chat,
        [msg, chatbot, chat_id_state],
        [chatbot, chat_id_state]
    ).then(
        lambda: "",
        None,
        msg
    )

    msg.submit(
        chat,
        [msg, chatbot, chat_id_state],
        [chatbot, chat_id_state]
    ).then(
        lambda: "",
        None,
        msg
    )

    stop_btn.click(stop)

    new_btn.click(
        new_chat,
        None,
        [chatbot, chat_id_state, chat_list]
    )

    chat_list.change(
        select_chat,
        chat_list,
        [chatbot, chat_id_state]
    )

    delete_btn.click(
        delete_current,
        chat_id_state,
        [chatbot, chat_id_state, chat_list]
    )


demo.launch(inbrowser=True)
