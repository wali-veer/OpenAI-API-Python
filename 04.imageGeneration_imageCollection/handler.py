import openai
import os
import requests
import ssl
from dotenv import load_dotenv
from PIL import Image

# Specify the gallary directory path
folder_path = "gallery"

load_dotenv()
client = openai.OpenAI()


def downloadFile(user_input, url):
    #Download a file from a URL and save it to the gallary directory 

    try:
        # Recommended to verify SSL certificates
        ssl._create_default_https_context = ssl._create_unverified_context
        r = requests.get(url, allow_redirects=True)
        r.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)

        # Create the image save directory path
        file_path = os.path.join(
            "gallery", os.path.basename("image_" + user_input.replace(" ", "_")) + ".png"
        )

        with open(file_path, "wb") as f:
            f.write(r.content)
        return f"File downloaded successfully and saved to {file_path}"

    except requests.RequestException as e:
        print(f"An error occurred while downloading the file: {e}")

#Get all image files in the gallery folder
def get_files():
    # List all files in the folder
    files = os.listdir(folder_path)
    images = []
    # Filter out image files (assuming JPEG and PNG formats)
    image_files = [f for f in files if f.endswith(".jpg") or f.endswith(".png")]

    # Display every image
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        image = Image.open(image_path)
        images.append({"file": image, "title": image_file})
    return images

#Generate the image from a user's prompt (text)
def generate_image(user_input="Universe"):
    response = client.images.generate(
        model="dall-e-3",
        prompt=user_input,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url
