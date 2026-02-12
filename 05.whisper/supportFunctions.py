import os
import whisper
import openai
from dotenv import load_dotenv

# Load the environment variables present in .env file
load_dotenv()

# Set the OpenAI API key defined in .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create OpenAI client
client = openai.OpenAI()

# Function to save the translate and transcrit files to a folder
def save_file(text, file_name):
    if not os.path.exists("transcriptions"):
        os.makedirs("transcriptions")

    # Open the file in write mode and write the content
    with open(file_name, "w") as file:
        file.write(str(text))

    print(f"DEBUG : SupportFunction file_name :  Content saved to {file_name}")



# Function to transscribe the file  ="SampleAudios/sample-0.mp3" 
def speech_to_text(audio_path):
    try:
        if not os.path.exists(audio_path):
            raise FileNotFoundError("File not found")

        # Initialize the Whisper's base ASR (Automatic Speach Recognition) model
        model = whisper.load_model("base")

        # Your code to transcribe the audio
        result = model.transcribe(audio_path,fp16=False)

        # Extract the transcript text from the result
        return result["text"]

    except Exception as e:
        print(f"EXCEPTION :  An error occurred during transcription: {e}")

# Function to translate the audio into english
def speech_to_translation(audio_path):
    print("DEBUG : SupportFunction  audio_path  "+ audio_path)
    try:
        if not os.path.exists(audio_path):
            raise FileNotFoundError("File not found")

        # Initialize the Whisper  base Automatic Speach Recognition model
        model = whisper.load_model("base")

        # Your code to transcribe the audio
        result = model.transcribe(audio_path, language="en", fp16=False)

        # Extract the transcript text from the result
        return result["text"]
    except Exception as e:
        print(f"EXCEPTION :  An error occurred during transcription: {e}")