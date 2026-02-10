import os
import openai
import tiktoken
from dotenv import load_dotenv
from colorama import Fore

load_dotenv()
client = openai.OpenAI()
openai.api_key = os.getenv("OPENAI_API_KEY")

LANGUAGE_MODEL = "gpt-3.5-turbo-instruct"

def get_tokens(user_input: str) -> int: 
    
    encoding = tiktoken.get_encoding("cl100k_base")

    token_integers = encoding.encode(user_input)
    tokens_usage = len(token_integers)

    tokenized_input = list(
    # Following "map" takes some 'list' or 'Iterabble object' and 
    # apply a function to every single value inside of it  
        map(
            lambda x: encoding.decode_single_token_bytes(x).decode("utf-8"),
            encoding.encode(user_input),
        )
    )
    print(f"{encoding}: {tokens_usage} tokens")
    print(f"token integers: {tokens_usage}")
    print(f"token bytes: {tokenized_input}")


def start():
    print("MENU")
    print("====")
    print("[1]- Ask a question of your choice")
    print("[2]- Exit")
    choice = input("Enter your choice please! : ")
    if choice == "1":
        ask()
    elif choice == "2":
        exit()
    else:
        print("Invalid choice!")


def ask():
    "Ask any question and get a response from the model."
    instructions = (
        "Type your question and press ENTER. Type 'x' to go back to the MAIN MENU.\n"
    )
    print(Fore.BLUE + "\n\x1B[3m" + instructions + "\x1B[0m" + Fore.RESET)
    while True:
        user_input = input("Q: ")
    #   print(user_input)
        # Exit
        if user_input == "x":
            start()
        else:
            completion= client.completions.create(
                model=LANGUAGE_MODEL, 
                prompt=str(user_input),
                max_tokens=50,
                temperature=0
            )
            response = completion.choices[0].text
            get_tokens(response)
            
            print(Fore.BLUE + f"A: " + response + Fore.RESET)
            print(Fore.WHITE + "\n-------------------------------------------------")

if __name__ == "__main__":
    start()
