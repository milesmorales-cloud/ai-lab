from ai_client import send_message


def main():
    messages = []
    last_model = None

    print("🤖 Hello! What can I help you with?")
    print("Type /help to see available commands.\n")

    while True:
        user_message = input("You: ")

        if user_message.lower() == "/help":
            print("\nAvailable commands:")
            print("/help   - Show available commands")
            print("/model  - Show the current model")
            print("/clear  - Clear conversation history")
            print("/exit   - Exit the application\n")
            continue

        if user_message.lower() == "/model":
            if last_model:
                print(f"\nCurrent model: {last_model}\n")
            else:
                print("\nNo model has been used yet.\n")
            continue

        if user_message.lower() == "/clear":
            messages.clear()
            print("\nConversation cleared.\n")
            continue

        if user_message.lower() == "/exit":
            print("Goodbye mate! 👋")
            break

        messages.append({
            "role": "user",
            "content": user_message
        })

        try:
            result = send_message(messages)
            last_model = result["model"]

            ai_message = result["message"]

            print("\nAI:", ai_message)
            print("Model:", result["model"])
            print()

            messages.append({
                "role": "assistant",
                "content": ai_message
            })

        except RuntimeError as error:
            print("\nError:", error)
            print()


if __name__ == "__main__":
    main()