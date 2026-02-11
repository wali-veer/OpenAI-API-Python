import openai
from dotenv import load_dotenv
from colorama import Fore

load_dotenv()
client = openai.OpenAI()

# Constants
#PERSONA = "You are a skilled assistant having knowledge about health and healthy life style, you are able to prvide the helpful tips and guidance when asked anything about human health, healthy life style and living healthy"
MODEL_ENGINE = "gpt-3.5-turbo"
MESSAGE_SYSTEM = " You are a skilled assistant having knowledge about health and healthy life style with a skill of giving advises in the form of 3 to 4 bullet points"
messages = [{"role": "system", "content": MESSAGE_SYSTEM}]

def print_messages(messages):
    messages = [message for message in messages if message["role"] != "system"]
    for message in messages:
        role = "Bot" if message["role"] == "assistant" else "You"
        print(Fore.BLUE + role + ": " + message["content"])
    return messages

def to_dict(message_obj):
    return {
        "role": message_obj.role,
        "content": message_obj.content,
    }

#https://developers.openai.com/api/reference/python/resources/chat/subresources/completions/methods/create

def generate_chat_completion(user_input=""):
    messages.append({"role": "user", "content": user_input})
    completion = client.chat.completions.create(
        model=MODEL_ENGINE,
        messages=messages, 
        temperature=0.9, 
        max_tokens=500
    )
    message = completion.choices[0].message
    messages.append(to_dict(message))
    print_messages(messages)  #to print on the IDE terminal not on the browser run by streamlit
    return message.content 