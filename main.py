import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

MAX_ITERATIONS = 20

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    user_prompt = args.user_prompt

    for _ in range(MAX_ITERATIONS):
        try:
            final_resp = generate_content(client, user_prompt, messages, args)
            if final_resp:
                print(f'Final response: {final_resp}')
                break
        except Exception as e:
            print(f'Error: {e}')
    else:
        print(f'Max iterations ({MAX_ITERATIONS} reached.')
        sys.exit(1)

    """
    resp = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0,
            tools=[available_functions],
        ),
    )
    if resp is None or resp.usage_metadata is None:
        raise Exception("AI client failed to respond")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {resp.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {resp.usage_metadata.candidates_token_count}")
    print("Response")
    if not resp.function_calls is None:
        function_results = []
        for func in resp.function_calls:
            # print(f"Calling function: {func.name}({func.args})")
            function_call_result = call_function(func, args.verbose)
            if len(function_call_result.parts) == 0:
                raise Exception(f"Error: Are you sure the function {func.name} was really called?")
            if function_call_result.parts[0].function_response is None:
                raise Exception(f"Error: Frightful mess in the return data from calling {func.name}")
            if function_call_result.parts[0].function_response.response is None:
                raise Exception(f"Error: Crikey, nothing came back from {func.name}!")
            function_results.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

    else:
        print(resp.text)
    """

def generate_content(client, user_prompt, messages, args):
    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions],
        ),
    )
    if resp is None or resp.usage_metadata is None:
        raise Exception("AI client failed to respond")

    if resp.candidates:
        for c in resp.candidates:
            messages.append(c.content)

    if args.verbose:
        print(f'Prompt tokens: {resp.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {resp.usage_metadata.candidates_token_count}')

    if not resp.function_calls:
        return resp.text

    function_results = []
    for func in resp.function_calls:
        function_call_result = call_function(func, args.verbose)
        if len(function_call_result.parts) == 0:
            raise Exception(f"Error: Are you sure the function {func.name} was really called?")
        if function_call_result.parts[0].function_response is None:
            raise Exception(f"Error: Frightful mess in the return data from calling {func.name}")
        if function_call_result.parts[0].function_response.response is None:
            raise Exception(f"Error: Crikey, nothing came back from {func.name}!")
        function_results.append(function_call_result.parts[0])

    if not function_results:
        raise Exception("No function responses generated")

    messages.append(types.Content(role="tool", parts=function_results))

    return None


if __name__ == "__main__":
    main()
