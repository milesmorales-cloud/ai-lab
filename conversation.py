def generate_title(content):
    text = " ".join(content.split())
    if len(text) <= 30:
        return text
    cut = text[:30]
    last_space = cut.rfind(" ")
    if last_space > 0:
        cut = cut[:last_space]
    return cut


class Conversation:
    def __init__(self, title="", messages=None):
        self.title = title
        self.messages = messages if messages is not None else []

    @property
    def is_empty(self):
        return not self.messages

    def add_message(self, message):
        self.messages.append(message)
        if message.get("role") == "user" and not self.title:
            self.title = generate_title(message["content"])

    def reset(self):
        self.title = ""
        self.messages.clear()


class ConversationStore:
    def __init__(self):
        self.conversations = []
        self.active = Conversation()

    @property
    def visible(self):
        return [conv for conv in self.conversations if not conv.is_empty]

    def save_active(self):
        if not self.active.is_empty and self.active not in self.conversations:
            self.conversations.append(self.active)

    def clear_active(self):
        self.active = Conversation()

    def select(self, index):
        visible = self.visible
        if 1 <= index <= len(visible):
            self.active = visible[index - 1]
            return self.active
        return None

    def delete(self, index):
        visible = self.visible
        if index < 1 or index > len(visible):
            return False
        conversation = visible[index - 1]
        self.conversations.remove(conversation)
        if self.active is conversation:
            self.active = Conversation()
        return True
