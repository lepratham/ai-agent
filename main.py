import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("GEMINI_API_KEY not found")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
# Now we can access `args.prompt`


def main():
    messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]
    prompt = messages
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    if args.verbose:
        print(f"User prompt: {args.prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
