import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types



def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    resp = client.models.generate_content(model="gemini-2.5-flash", contents=messages)
    if resp is None or resp.usage_metadata is None:
        raise Excption("AI client failed to respond")

    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {resp.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {resp.usage_metadata.candidates_token_count}")
    print("Response")
    print(resp.text)

if __name__ == "__main__":
    main()
