from unittest.mock import patch

import app
from conversation import ConversationStore


def test_show_help_lists_all_commands(capsys):
    app.show_help()
    output = capsys.readouterr().out
    assert "/help" in output
    assert "/model" in output
    assert "/history" in output
    assert "/clear" in output
    assert "/exit" in output
    assert "/select" in output
    assert "D<n>" in output


def test_show_history_empty(capsys):
    store = ConversationStore()
    app.show_history(store)
    output = capsys.readouterr().out
    assert "No saved conversations yet." in output


def test_show_history_lists_titles(capsys):
    store = ConversationStore()
    store.active.add_message({"role": "user", "content": "First topic"})
    store.save_active()
    store.clear_active()
    store.active.add_message({"role": "user", "content": "Second topic"})
    store.save_active()

    app.show_history(store)
    output = capsys.readouterr().out
    assert "1. First topic" in output
    assert "2. Second topic" in output


def test_show_conversation_prints_messages(capsys):
    store = ConversationStore()
    store.active.add_message({"role": "user", "content": "Hello"})
    store.save_active()

    app.show_conversation(store, 1)
    output = capsys.readouterr().out
    assert "Conversation 1: Hello" in output
    assert "User: Hello" in output


def test_show_conversation_invalid_index(capsys):
    store = ConversationStore()
    app.show_conversation(store, 1)
    output = capsys.readouterr().out
    assert "No conversation found at index 1." in output


def test_show_conversation_sets_active(capsys):
    store = ConversationStore()
    store.active.add_message({"role": "user", "content": "Topic A"})
    store.save_active()
    store.clear_active()
    store.active.add_message({"role": "user", "content": "Topic B"})
    store.save_active()

    app.show_conversation(store, 1)
    capsys.readouterr()
    assert store.active is store.visible[0]


def test_delete_conversation_confirmed(monkeypatch, capsys):
    store = ConversationStore()
    store.active.add_message({"role": "user", "content": "To delete"})
    store.save_active()
    monkeypatch.setattr("builtins.input", lambda prompt="": "y")

    app.delete_conversation(store, 1)
    output = capsys.readouterr().out
    assert "Deleted conversation 'To delete'" in output
    assert len(store.visible) == 0


def test_delete_conversation_cancelled(monkeypatch, capsys):
    store = ConversationStore()
    store.active.add_message({"role": "user", "content": "Keep me"})
    store.save_active()
    monkeypatch.setattr("builtins.input", lambda prompt="": "n")

    app.delete_conversation(store, 1)
    output = capsys.readouterr().out
    assert "Deletion cancelled" in output
    assert len(store.visible) == 1


def test_delete_conversation_invalid_index(capsys):
    store = ConversationStore()
    app.delete_conversation(store, 1)
    output = capsys.readouterr().out
    assert "No conversation found at index 1." in output


@patch("app.send_message")
def test_main_full_flow(mock_send_message, monkeypatch, capsys):
    inputs = iter([
        "Hello",
        "/history",
        "1",
        "D1",
        "y",
        "/exit",
    ])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    mock_send_message.return_value = {"model": "fake-model", "message": "Hi there!"}

    app.main()
    output = capsys.readouterr().out

    assert "1. Hello" in output
    assert "User: Hello" in output
    assert "Assistant: Hi there!" in output
    assert "Deleted conversation 'Hello'" in output
    mock_send_message.assert_called_once()


@patch("app.send_message")
def test_main_clear_preserves_saved_history(mock_send_message, monkeypatch, capsys):
    inputs = iter([
        "First topic",
        "/clear",
        "/history",
        "/exit",
    ])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    mock_send_message.return_value = {"model": "m", "message": "reply"}

    app.main()
    output = capsys.readouterr().out

    assert "1. First topic" in output
    assert "Conversation cleared" in output
    mock_send_message.assert_called_once()


@patch("app.send_message")
def test_main_select_then_continue_chatting(mock_send_message, monkeypatch, capsys):
    inputs = iter([
        "Hello",
        "/history",
        "1",
        "Tell me more",
        "/history",
        "1",
        "/exit",
    ])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    mock_send_message.return_value = {"model": "m", "message": "Hi there!"}

    app.main()
    output = capsys.readouterr().out

    assert "1. Hello" in output
    assert output.count("User: Hello") == 2
    assert output.count("Assistant: Hi there!") == 3
    assert "User: Tell me more" in output
    assert mock_send_message.call_count == 2
