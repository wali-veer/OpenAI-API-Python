import openai
from dotenv import load_dotenv
from colorama import Fore

# define main variable 
SYSTEM_MESSAGE = "You are an helpful assistant"
MODEL_ENGINE = "gpt-3.5-turbo"
messages = [{"role": "system", "content": SYSTEM_MESSAGE}]

# Load environment variables present in the .env file
load_dotenv()
client = openai.OpenAI()  # Create an openAPI client object

def generate_chat_completion(user_input=""):
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.9,
        max_tokens=100,
    )
    message = response.choices[0].message # refer the below JSON sameple output to parse the "message" feild
    messages.append(message)
    print(Fore.GREEN + "Bot: " + message.content.replace("\n", ""))
'''
{
  "id": "chatcmpl-8o4sq3sSzGVqS0aQyjlXuuEGVZnSj",
  "object": "chat.completion",
  "created": 1721722200,
  "model": "gpt-4o-2024-05-13",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "In moonlit shadows soft they prowl,\nWith eyes aglow in night's dark cowl."
      },
      "finish_reason": "stop",
      "logprobs": null
    }
  ],
  "usage": {
    "completion_tokens": 34,
    "prompt_tokens": 14,
    "total_tokens": 48
  }
}

'''

def main():
    while True:
        print("\n")
        print("----------------------------------------\n")
        print("      WELCOME TO MY OPEN- AI CHATBOT     ")
        print("\n----------------------------------------")
        print("\n================ MENU ================\n")
        print("[1]- Start Chat")
        print("[2]- Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            start_chat()
        elif choice == "2":
            exit()
        else:
            print("Invalid choice")


def start_chat():
    print("to end chat, type 'x'")
    print("\n")
    print("      NEW CHAT       ")
    print("---------------------")
    generate_chat_completion()

    while True:
        user_input = input(Fore.WHITE + "You: ")

        if user_input.lower() == "x":
            main()
            break
        else:
            generate_chat_completion(user_input)

if __name__ == "__main__":
    main()