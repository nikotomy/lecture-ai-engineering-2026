from types import SimpleNamespace

from app import ask as ask_module


class FakeChat:
    def __init__(self, response):
        self.response = response
        self.messages = []

    def send_message(self, message):
        self.messages.append(message)
        return self.response


def _response():
    return SimpleNamespace(
        text="回答",
        usage_metadata=SimpleNamespace(
            prompt_token_count=12,
            candidates_token_count=34,
        ),
    )


def test_ask_prints_input_and_output_token_counts(monkeypatch, capsys):
    chat = FakeChat(_response())
    request = {}

    class FakeClient:
        def __init__(self, api_key):
            self.chats = SimpleNamespace(
                create=lambda **kwargs: request.update(kwargs) or chat,
            )

    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(ask_module.genai, "Client", FakeClient)

    assert ask_module.ask("質問") == "回答"
    assert request == {"model": ask_module.MODEL, "config": {"temperature": 0}}
    assert chat.messages == ["質問"]
    assert capsys.readouterr().out == "[usage] input=12 output=34 tokens\n"


def test_interactive_mode_reuses_chat_for_follow_up_questions(monkeypatch, capsys):
    client = object()
    chat = FakeChat(_response())
    questions = iter(["LoRAとは？", "さっきの説明を短くして", "/exit"])
    monkeypatch.setattr(ask_module, "create_chat", lambda: (client, chat))
    monkeypatch.setattr("builtins.input", lambda prompt: next(questions))
    monkeypatch.setattr("sys.argv", ["app.ask", "--interactive"])

    ask_module.main()

    assert chat.messages == ["LoRAとは？", "さっきの説明を短くして"]
    assert capsys.readouterr().out.count("回答") == 2