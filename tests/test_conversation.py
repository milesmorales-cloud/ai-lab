from conversation import Conversation, ConversationStore, generate_title


def test_generate_title_short():
    assert generate_title("Hello") == "Hello"


def test_generate_title_collapses_whitespace():
    assert generate_title("  Hello   world  ") == "Hello world"


def test_generate_title_truncates_long_messages():
    text = "Explain quantum computing and why it matters"
    title = generate_title(text)
    assert len(title) <= 30
    assert text.startswith(title)


def test_add_message_sets_title_from_first_user_message():
    conversation = Conversation()
    conversation.add_message({"role": "user", "content": "Say hello"})
    assert conversation.title == "Say hello"


def test_add_message_does_not_override_existing_title():
    conversation = Conversation()
    conversation.add_message({"role": "user", "content": "First message"})
    conversation.add_message({"role": "user", "content": "Second message"})
    assert conversation.title == "First message"


def test_assistant_message_does_not_set_title():
    conversation = Conversation()
    conversation.add_message({"role": "assistant", "content": "AI reply"})
    assert conversation.title == ""
    assert conversation.is_empty is False


def test_reset_clears_title_and_messages():
    conversation = Conversation()
    conversation.add_message({"role": "user", "content": "Hello"})
    assert conversation.is_empty is False
    conversation.reset()
    assert conversation.is_empty is True
    assert conversation.title == ""


def test_store_save_active_adds_non_empty_conversation():
    store = ConversationStore()
    assert store.visible == []
    store.active.add_message({"role": "user", "content": "Hi"})
    store.save_active()
    assert len(store.visible) == 1
    assert store.active in store.conversations


def test_store_save_active_is_idempotent():
    store = ConversationStore()
    store.active.add_message({"role": "user", "content": "Hi"})
    store.save_active()
    store.save_active()
    assert len(store.visible) == 1


def test_store_clear_active_preserves_saved_history():
    store = ConversationStore()
    store.active.add_message({"role": "user", "content": "Old conversation"})
    store.save_active()
    assert len(store.visible) == 1
    store.clear_active()
    assert store.active.is_empty is True
    assert len(store.visible) == 1


def test_store_select_opens_and_sets_active_conversation():
    store = ConversationStore()
    store.active.add_message({"role": "user", "content": "First"})
    store.save_active()
    store.clear_active()
    store.active.add_message({"role": "user", "content": "Second"})
    store.save_active()

    selected = store.select(1)
    assert selected is store.visible[0]
    assert store.active is selected


def test_store_select_invalid_index_returns_none():
    store = ConversationStore()
    assert store.select(1) is None
    assert store.select(99) is None


def test_store_delete_removes_conversation():
    store = ConversationStore()
    store.active.add_message({"role": "user", "content": "To delete"})
    store.save_active()
    assert len(store.visible) == 1
    assert store.delete(1) is True
    assert len(store.visible) == 0
    assert store.active.is_empty is True


def test_store_delete_active_creates_new_active():
    store = ConversationStore()
    store.active.add_message({"role": "user", "content": "To delete"})
    store.save_active()
    active = store.active
    store.delete(1)
    assert store.active is not active
    assert store.active.is_empty is True


def test_store_delete_invalid_index_returns_false():
    store = ConversationStore()
    assert store.delete(1) is False
