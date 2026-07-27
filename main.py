import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("API key is not found! Enter API key.")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args  = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    response = client.chat.completions.create(model="openrouter/free", messages=messages,
    tools=available_functions,
    )

    # print extra detailed information while running
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    
    message = response.choices[0].message

    if message.tool_calls is not None :
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)
            if result_message["content"] is None or result_message["content"] == "":
                raise Exception("Error: Content is empty")
            if args.verbose:
                print(f"-> {result_message['content']}")

    else:
        print(message.content)



    if response.usage is None:
        raise RuntimeError


if __name__ == "__main__":
    main()
