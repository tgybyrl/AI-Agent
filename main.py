import os, sys, argparse
from dotenv import load_dotenv
from openai import OpenAI
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



    for _ in range(20):
        #call the model
        response = client.chat.completions.create(model="openrouter/free", messages=messages, tools=available_functions,)
        
        #grab the message from the response
        message = response.choices[0].message

        #assistant message
        messages.append(message)


        if message.tool_calls:
            
            # print extra detailed information while running
            if args.verbose:
                print(f"User prompt: {args.user_prompt}")
                print(f"Prompt tokens: {response.usage.prompt_tokens}")
                print(f"Response tokens: {response.usage.completion_tokens}")

            for tool_call in message.tool_calls:

                result_message = call_function(tool_call, args.verbose)
                
                #results of any function calls model requested
                messages.append(result_message)
                
                if result_message["content"] is None or result_message["content"] == "":
                    raise Exception("Error: Content is empty")
                
                if args.verbose:
                    print(f"-> {result_message['content']}")
        
        if not message.tool_calls:
            print(message.content)
            break
        
    else:
        print("Reached maximum number of iterations")
        sys.exit(1)


if __name__ == "__main__":
    main()
