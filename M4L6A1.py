import requests
from colorama import Fore, Style, init
from config import HF_API_KEY

# Initialize colorama
init(autoreset=True)

# Default model
DEFAULT_MODEL = "facebook/bart-large-cnn"


# ================== AI SUMMARIZER FUNCTION ==================

def summarize_text(text, min_length, max_length, model_name=DEFAULT_MODEL):

    api_url = f"https://router.huggingface.co/hf-inference/models/{model_name}"

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Accept": "application/json"
    }

    payload = {
        "inputs": text,
        "parameters": {
            "min_length": min_length,
            "max_length": max_length
        },
        "options": {
            "wait_for_model": True
        }
    }

    print(Fore.BLUE + f"\n🤖 Using model: {model_name}")

    try:
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=120
        )

        print(Fore.CYAN + "\nStatus Code:", response.status_code)
        print(Fore.YELLOW + "Raw Response:")
        print(response.text)

        # Handle request failure
        if response.status_code != 200:
            print(Fore.RED + "❌ Request failed")
            return None

        # Handle empty response
        if not response.text.strip():
            print(Fore.RED + "❌ Empty response from API")
            return None

        result = response.json()

        # Normal summarization output
        if isinstance(result, list) and len(result) > 0:

            if "summary_text" in result[0]:
                return result[0]["summary_text"]

            if "generated_text" in result[0]:
                return result[0]["generated_text"]

        # API error
        if isinstance(result, dict) and "error" in result:
            print(Fore.RED + f"❌ API Error: {result['error']}")
            return None

        print(Fore.RED + "❌ Unexpected response format:")
        print(result)
        return None

    except Exception as e:
        print(Fore.RED + f"❌ Error: {e}")
        return None


# ================== MAIN PROGRAM ==================

print(Fore.YELLOW + Style.BRIGHT + "👋 Hi there! What's your name?")
user_name = input("Your name: ").strip()

if not user_name:
    user_name = "User"

print(Fore.GREEN + f"\nWelcome, {user_name}! Let's summarize your text ✨")

# Input text
print(Fore.YELLOW + "\nEnter text to summarize:")
user_text = input("> ").strip()

if not user_text:
    print(Fore.RED + "❌ No text provided. Exiting.")
    exit()

# Model selection
print(Fore.YELLOW + "\nEnter model name (press Enter for default):")
model_choice = input("Model: ").strip()

if not model_choice:
    model_choice = DEFAULT_MODEL

# Style selection
print(Fore.YELLOW + "\nChoose summarization style:")
print("1. Standard (short)")
print("2. Enhanced (detailed)")

choice = input("Enter 1 or 2: ").strip()

if choice == "2":
    min_length = 80
    max_length = 200
    print(Fore.BLUE + "🚀 Enhanced mode selected")
else:
    min_length = 50
    max_length = 150
    print(Fore.BLUE + "⚡ Standard mode selected")

# Run summarizer
summary = summarize_text(
    user_text,
    min_length,
    max_length,
    model_name=model_choice
)

# Output result
if summary:
    print(Fore.GREEN + Style.BRIGHT + f"\n📝 Summary for {user_name}:\n")
    print(Fore.GREEN + summary)
else:
    print(Fore.RED + "❌ Failed to generate summary")