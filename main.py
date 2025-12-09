import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from config import system_prompt
from call_function import call_function, available_functions

# Loading API key
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("GEMINI_API_KEY not found")

client = genai.Client(api_key=api_key)

# Parser to incorporate user input as a prompt
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
# Now we can access `args.prompt`

messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]
prompt = messages


def main():
    try:
        for _ in range(0, 20):
            generated_content = generate_content(client, messages, args.verbose)
            if not generated_content.candidates and generated_content.text:
                break
        print(generated_content.text)
    except Exception as error:
        return f"Error: {str(error)}"


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    candidates = response.candidates
    for candidate in candidates:
        messages.append(candidate.content)

    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    # Instructions for --verbose flag
    if verbose:
        print(f"User prompt: {args.prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    function_responses = []
    if not response.function_calls:
        print("Response:")
        r = types.Content(
            parts=[types.Part(text=response.text)],
            role="user",
        )
        messages.append(r)

    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)

        # validate structure
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")

        part = function_call_result.parts[0]

        if verbose:
            print(f"-> {part.function_response.response}")

        function_responses.append(part)

    if not function_responses:
        raise Exception("no function responses generated, exiting.")

    response_list = types.Content(
        parts=function_responses,
        role="user",
    )

    messages.append(response_list)
    return response


if __name__ == "__main__":
    main()
