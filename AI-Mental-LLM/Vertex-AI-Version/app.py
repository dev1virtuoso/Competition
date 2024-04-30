"""
AI Mental detection/classification UI using Vertex AI (Gemini Model)
------------------------
Require install vertexai
!pip install vertexai
------------------------
Require install google-cloud-aiplatform
!pip install -U google-cloud-aiplatform "shapely<2" # workaround for the issue
------------------------
Require install streamlit for UI 
!pip install streamlit


"""

import streamlit as st  # import stremlit
import os
from dotenv import load_dotenv # load environment variable
import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models
import google.auth 
google.auth.default()  # get google default credentials , when gcloud init completed


load_dotenv() # load environment variable


# Gemini Model config , Setting 
generation_config = {
    "max_output_tokens": 1024,
    "temperature": 0.2,
    "top_p": 0.8,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}


textsi_1 = """
I am a mental health professional and I am here to help you.I am not a doctor, but I can provide you with some general information about mental health. If you are in crisis, please call 911 or go to the nearest emergency room. If you are in need of immediate help, please call the National"""

googleProjectID="gdg-vertex-ai-workshop-curl"
location="us-central1"
# vertex ai 
vertexai.init(project=googleProjectID, location="us-central1")
geminiModel =  "gemini-1.0-pro-002"
geminiVisionModel = "gemini-vision-1.0-pro-002"

model = GenerativeModel(
    geminiModel,
    system_instruction=[textsi_1]
  )
chat = model.start_chat() # chat model 


# chat mode 
def singleChat(message):
  response = chat.send_message(
      [message],
      generation_config=generation_config,
      safety_settings=safety_settings
  )
#   print(response)
  return response.text


# Generate response function with Instruction Prompt Template for Generate Contenct 
def generateResponseInstr(prompTemp,message):
    response = model.generate_content(f"""
    {prompTemp}
    {message}""")
    # print(response.text)
    return response, response.text

def generateResponse(message):
    response = model.generate_content(f"""
    {message}""")
    # print(response.text)
    return response.text


# initialize out stremlit app
st.set_page_config(page_title="AI Mental Health Detection", page_icon="🧠", layout="centered", initial_sidebar_state="expanded")

st.header("Gemini LLM AI Mental Health Detection Application")

input1 = st.text_input("Enter your message here", key="input1", value="What is your feeling today?")
# input = st.text_area("Enter your message here", "I am feeling sad today")
submit = st.button("Chat")


# Check if the button is clicked
if submit:
    response = generateResponse(input1)
    st.subheader("AI Mental Bot response is")
    st.write(response)




