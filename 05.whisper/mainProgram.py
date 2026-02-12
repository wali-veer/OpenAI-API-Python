import streamlit as st
import os
import tempfile
from dotenv import load_dotenv
from supportFunctions import speech_to_text, speech_to_translation, save_file

# Streamlit Application 
# Add a application / page title 
st.title("Audio clips - transcriptions & translations service")  


# User's input - Option to select the audio file and provide a button to upload it
with st.form("file_upload_form", clear_on_submit=True):
    uploaded_file = st.file_uploader("Select a file present on your computer")
    submit_button = st.form_submit_button(label="Submit")

# Following block is to process the uploaded file
if submit_button and uploaded_file is not None:
    with st.spinner("Transcribing...", show_time=True):
    
        # Save the uploaded file into a temporary location - tempfile module renames the file as well.

        # Create a temp file
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=os.path.splitext(uploaded_file.name)[1]
        ) as temp_file:
            print("DEBUG : main program : temp_file : " + str(temp_file))

            #write the uploaded file content into temp file
            temp_file.write(uploaded_file.getvalue())
            #print("DEBUG : main program : uploaded_file.getvalue : " + str(uploaded_file.getvalue()))

            temp_file_path = temp_file.name
            print("DEBUG : main program : temp_file_path : "+ temp_file_path )

            filename = temp_file_path.split("\\")[-1]
            print("DEBUG : main program : filename : "+ filename )

            original_transcript = speech_to_text(temp_file_path)
            translated_transcript = speech_to_translation(temp_file_path)
            
            save_file(original_transcript, f"transcriptions/{uploaded_file.name}.txt")
            save_file(
                translated_transcript,
                f"transcriptions/{uploaded_file.name}_translated.txt",
            )

            st.success("File transcribed successfully!")

            st.divider()
            # Dsplay transcribed test streamlit GUI
            st.markdown(f":blue[{original_transcript}]")
            
            st.divider()
            # Dsplay traslated test streamlit GUI
            st.markdown(f":green[{translated_transcript}]")

            # Dsplay option to play the audio on streamlit GUI
            st.audio(temp_file_path)