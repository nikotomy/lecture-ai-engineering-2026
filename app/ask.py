"""第1回: 素のLLMに質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする
    uv run python -m app.ask --interactive  # 会話履歴を保って続けて質問する

ツールは使わない「素の」呼び出し。対話モードでは同じ会話履歴を引き継ぐ。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def create_chat():
    client = genai.Client(api_key=get_api_key())
    chat = client.chats.create(
        model=MODEL,
        config={"temperature": 1},
    )
    return client, chat


def ask(question: str, chat=None) -> str:
    if chat is None:
        client, chat = create_chat()
    response = chat.send_message(question)

    usage = response.usage_metadata
    if usage is not None:
        print(
            f"[usage] input={usage.prompt_token_count} "
            f"output={usage.candidates_token_count} tokens"
        )

    return response.text


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="会話履歴を保って続けて質問する",
    )
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    try:
        if args.interactive:
            client, chat = create_chat()
            print("対話モードです。終了するには /exit を入力してください。")
            while True:
                try:
                    question = input("\n[質問] ")
                except EOFError:
                    break
                if question.strip().lower() == "/exit":
                    break
                if not question.strip():
                    continue
                print(ask(question, chat))
        else:
            print(f"[質問] {args.question}\n")
            print(ask(args.question))
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
