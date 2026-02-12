# https://developers.openai.com/api/docs/guides/function-calling/#handling-function-calls

import openai
from colorama import Fore
from dotenv import load_dotenv
import json
from supportFunctions import get_current_weather

load_dotenv()

# https://developers.openai.com/api/docs/guides/function-calling/#defining-functions
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {
                        "type": "string", 
                        "enum": ["celsius", "fahrenheit"]
                        },
                },
                "required": ["location", "unit"],
            },
        },
    }
]


# Variables - constants 
MODEL_ENGINE = "gpt-3.5-turbo"
messages = [{"role": "system", "content": "You are an expert assistant"}]

# Initiate openAI client
client = openai.OpenAI()

def generate_response(user_input):
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=tools,
        tool_choice="auto",  # https://developers.openai.com/api/docs/guides/function-calling#additional-configurations
    )
    messages.append(response.choices[0].message)  
    print("\n DEBUG : GENERATE RESPONSE FUNC : --response.choices --" + str(response.choices))  
    #DEBUG : GENERATE RESPONSE FUNC : --response.choices --[Choice(finish_reason='tool_calls', index=0, logprobs=None, message=ChatCompletionMessage(content=None, refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=[ChatCompletionMessageFunctionToolCall(id='call_pOXxOzgZz6KflrAhkjyJFeNL', function=Function(arguments='{"location":"Hyderabad","unit":"celsius"}', name='get_current_weather'), type='function')]))]
    
    print("\n DEBUG : GENERATE RESPONSE FUNC : -- response.choices[0].message -- " + str(response.choices[0].message))
    #DEBUG : GENERATE RESPONSE FUNC : -- response.choices[0].message -- ChatCompletionMessage(content=None, refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=[ChatCompletionMessageFunctionToolCall(id='call_pOXxOzgZz6KflrAhkjyJFeNL', function=Function(arguments='{"location":"Hyderabad","unit":"celsius"}', name='get_current_weather'), type='function')])
    
    print("\n DEBUG : GENERATE RESPONSE FUNC : -- messages --" + str(messages))
    # DEBUG : GENERATE RESPONSE FUNC : -- response.choices[0].message -- ChatCompletionMessage(content=None, refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=[ChatCompletionMessageFunctionToolCall(id='call_pOXxOzgZz6KflrAhkjyJFeNL', function=Function(arguments='{"location":"Hyderabad","unit":"celsius"}', name='get_current_weather'), type='function')])

    return response.choices[0].message


available_functions = {
    "get_current_weather": get_current_weather,
}  # only one function in this example, but you can have multiple


def call_function(tool_calls):
    if tool_calls:
        # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                location=function_args.get("location"),
                unit=function_args.get("unit"),
            )

            print(function_response)
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response


def main():
    print(
        Fore.CYAN
        + "Bot: Hello, I am a helpful assistant. Type 'exit' to quit."
        + Fore.RESET
    )

    while True:
        user_input = input("You: ")

        if user_input == "exit":
            print("Have a good day!")
            break

        # Step 1: send the conversation and available functions to GPT
        message_response = generate_response(user_input)
        print("\n DEBUG : MAIN program : message_response " + str(message_response))
        # DEBUG : MAIN program : message_response ChatCompletionMessage(content=None, refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=[ChatCompletionMessageFunctionToolCall(id='call_pOXxOzgZz6KflrAhkjyJFeNL', function=Function(arguments='{"location":"Hyderabad","unit":"celsius"}', name='get_current_weather'), type='function')])

        # Step 2: check if GPT wanted to call a function and generate an extended response. See the above mentioned comment
        if message_response.tool_calls is None:
            print("Bot: " + message_response.content)
            continue

        # Step 3: call the function
        call_function(message_response.tool_calls)

        # Step 4: send the info on the function call and function response to GPT
        # extend conversation with assistant's reply
        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
        )  # get a new response from the model where it can see the function response
        print("\n DEBUG : MAIN program : second_response " + str(second_response))
        # DEBUG : MAIN program : second_response ChatCompletion(id='chatcmpl-D8Ui4cWWGrTqY9fTUISdP5X1wSTCD', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='The current temperature in Hyderabad, India is 21°C with scattered clouds.', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None))], created=1770917044, model='gpt-3.5-turbo-1106', object='chat.completion', service_tier='default', system_fingerprint='fp_208565f510', usage=CompletionUsage(completion_tokens=15, prompt_tokens=82, total_tokens=97, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)))

        print("\n DEBUG : MAIN program : second_response.choices " + str(second_response.choices))
        # DEBUG : MAIN program : second_response.choices [Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='The current temperature in Hyderabad, India is 21°C with scattered clouds.', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None))]

        print("\n DEBUG : MAIN program : second_response.choices[0].message.content " + str(second_response.choices[0].message.content))
        #DEBUG : MAIN program : second_response.choices[0].message.content The current temperature in Hyderabad, India is 21°C with scattered clouds. 

        print("Bot: " + second_response.choices[0].message.content)


if __name__ == "__main__":
    main()