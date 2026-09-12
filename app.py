from ai_client import send_message


def main():
    messages = []

    print("🤖 AI Client")
    print("Type 'exit' to quit.\n")

    while True:
        user_message = input("You: ")

        if user_message.lower() == "exit":
            print("Goodbye mate! 👋")
            break

        messages.append({
            "role": "user",
            "content": user_message
        })

        try:
            result = send_message(messages)

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