import os
from dotenv import load_dotenv
from google import genai


def main():
    #print("Hello from ai-tester!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    resp = client.models.generate_content(model="gemini-2.5-flash",
                                          contents=prompt)
    if resp is None or resp.usage_metadata is None:
        raise Excption("AI client failed to respond")
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {resp.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {resp.usage_metadata.candidates_token_count}")
    print("Response")
    print(resp.text)

if __name__ == "__main__":
    main()
