import re

from conversation import ConversationStore
from provider_client import send_message
from ui import (
    Spinner,
    print_header,
    render_assistant,
    render_error,
    render_user,
    rule,
    style,
    wrap_text,
)

SELECT_RE = re.compile(r"^\d+$")
DELETE_RE = re.compile(r"^[dD](\d+)$")

INPUT_PROMPT = "› "


def show_help():
    print()
    print(style("Available commands", "bold"))
    print(style("Normal chatting is the primary experience.", "dim"))
    print()
    commands = [
        ("/help", "Show available commands"),
        ("/model", "Show the current model"),
        ("/history", "Show conversation history"),
        ("/clear", "Clear the current conversation"),
        ("/select", "Open a conversation by number"),
        ("D<n>", "Delete conversation number n"),
        ("/exit", "Exit the application"),
    ]
    for name, description in commands:
        print(f"  {style(f'{name:<10}', 'cyan')} - {description}")
    print()


def show_history(store):
    visible = store.visible
    print()
    print(style("Conversation history", "bold"))
    print()
    if not visible:
        print("No saved conversations yet.")
        print()
        print("Enter a number to open a conversation, or D<n> to delete.")
        print()
        return
    for index, conversation in enumerate(visible, start=1):
        print(f"{index}. {conversation.title}")
    print()
    print("Enter a number to open a conversation, or D<n> to delete.")
    print()


def show_conversation(store, index):
    conversation = store.select(index)
    if conversation is None:
        print(f"No conversation found at index {index}.")
        print()
        return
    print()
    print(style(f"Conversation {index}: {conversation.title}", "bold"))
    print()
    for message in conversation.messages:
        role = message["role"]
        label = role.capitalize()
        color = "cyan" if role == "user" else "magenta"
        print(f"{style(label, color)}: {wrap_text(message['content'])}")
    print()


def delete_conversation(store, index):
    visible = store.visible
    if index < 1 or index > len(visible):
        print(f"No conversation found at index {index}.")
        print()
        return
    conversation = visible[index - 1]
    confirm = input(
        f"Type 'y' to confirm deleting '{conversation.title}' "
        "(cannot be undone): "
    )
    if confirm.strip().lower() != "y":
        print("Deletion cancelled.")
        print()
        return
    store.delete(index)
    print(f"Deleted conversation '{conversation.title}'.")
    print()


def show_model(last_model):
    print()
    if last_model:
        print(f"Current model: {last_model}")
    else:
        print("No model has been used yet.")
    print()


def clear_conversation(store):
    store.clear_active()
    print("Conversation cleared. A new conversation has started.")
    print()


def handle_chat(store, user_message):
    render_user(user_message)

    active = store.active
    active.add_message({"role": "user", "content": user_message})
    store.save_active()

    try:
        with Spinner("Thinking"):
            result = send_message(active.messages)
    except RuntimeError as error:
        render_error(str(error))
        return None

    render_assistant(result["message"], result["model"])
    rule()

    active.add_message({"role": "assistant", "content": result["message"]})
    return result["model"]


def main():
    store = ConversationStore()
    last_model = None

    print_header(model=last_model or "—")
    print(style("🤖 AI-Lab is ready. Type /help for commands.", "dim"))
    print()

    while True:
        try:
            user_message = input(style(INPUT_PROMPT, "cyan"))
        except EOFError:
            print()
            break

        command = user_message.strip()
        lowered = command.lower()

        if lowered == "/help":
            show_help()
            continue

        if lowered == "/model":
            show_model(last_model)
            continue

        if lowered == "/history":
            show_history(store)
            continue

        if lowered == "/clear":
            clear_conversation(store)
            continue

        if lowered == "/exit":
            print("Good bye!")
            break

        delete_match = DELETE_RE.match(command)
        if delete_match:
            delete_conversation(store, int(delete_match.group(1)))
            continue

        if SELECT_RE.match(command):
            show_conversation(store, int(command))
            continue

        if not command:
            continue

        model = handle_chat(store, command)
        if model:
            last_model = model


if __name__ == "__main__":
    main()
