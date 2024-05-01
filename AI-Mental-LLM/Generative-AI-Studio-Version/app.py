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
import google.generativeai as genai

load_dotenv() # load environment variable

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


# # Gemini Model config , Setting 
# generation_config = {
#     "max_output_tokens": 1024,
#     "temperature": 0.2,
#     "top_p": 0.8,
# }

# safety_settings = {
#     generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
#     generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
#     generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
#     generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
# }
# Set up the model
generation_config = {
  "temperature": 0.55,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]


# system instruction
textsi_1 = """
I am a mental health professional and I am here to help you.I am not a doctor, but I can provide you with some general information about mental health. If you are in crisis, please call 911 or go to the nearest emergency room. If you are in need of immediate help, please call the National"""

textsi_2 = """
I am a mental health professional and I am here to help you.I am not a doctor, but I can provide you with some general information about mental health."""

# sample for prompt instruction
testPrompt1 = """Is it have Depression or anxiety disorder or not, as below conversation?

    Context:"""

testPrompt2 = """I don't feel like doing much of anything todays?

    Context:"""

testPrompt3 = """If the phrase connotes a depressed emotion, assign a number 1 to the phrase. Otherwise, a number 0.

    Context:"""
    
testPrompt4 = """If the phrase connotes a anxiety emotion, assign a number 1 to the phrase. Otherwise, a number 0.

    Context:"""

testPrompt5 = """If the phrase connotes a depressed emotion, assign a number 1 to the phrase. if phrase connotes a anxiety emotion, assign a number 2 to the phrase.
                if phrase connotes both anxiety emotion and  depressed emotion, assign a number 3 to the phrase .Otherwise, a number 0.

    Context:"""

testPrompt6 = """Summarize the following conversation, What is the Emotion of the conversation?   

Context:"""


# Score for Depression and Anxiety initial value
if "depressCnt" not in st.session_state:
    st.session_state.depressCnt = 0

if "anxietyCnt" not in st.session_state:
    st.session_state.anxietyCnt = 0
  
if "depressAvg" not in st.session_state:
    st.session_state.depressAvg = 0.0

if "anxietyAvg" not in st.session_state:
    st.session_state.anxietyAvg = 0.0
  
if "dialogueTotalCnt" not in st.session_state:
    st.session_state.dialogueTotalCnt = 0
    
if "classifyResult" not in st.session_state:
    st.session_state.classifyResult= []
    
if "responseResult" not in st.session_state:
    st.session_state.responseResult= []

# Calculate Depression and Anxiety Average
def calculateDepressAnxietyAvg(result):
    if result == "0":
        print("Emotion: Not Depressed or Anxiety")
        st.session_state.depressAvg = st.session_state.depressCnt/st.session_state.dialogueTotalCnt
        st.session_state.anxietyAvg =  st.session_state.anxietyCnt/st.session_state.dialogueTotalCnt
        return
    elif result == "1":
        print("Emotion: Depressed")
        st.session_state.depressCnt += 1
        st.session_state.depressAvg = st.session_state.depressCnt/st.session_state.dialogueTotalCnt
        return
    
    elif result == "2":
        print("Emotion: Anxiety")
        st.session_state.anxietyCnt += 1
        st.session_state.anxietyAvg =  st.session_state.anxietyCnt/st.session_state.dialogueTotalCnt
        return
    elif result == "3":
        print("Emotion: Both Anxiety and Depressed")
        st.session_state.depressCnt += 1
        st.session_state.anxietyCnt += 1
        st.session_state.depressAvg = st.session_state.depressCnt/st.session_state.dialogueTotalCnt
        st.session_state.anxietyAvg =  st.session_state.anxietyCnt/st.session_state.dialogueTotalCnt
        return

# gen ai 
geminiModel =  "gemini-1.0-pro"
# geminiVisionModel = "gemini-vision-1.0-pro-002"

# Set up the model
model = genai.GenerativeModel(model_name=geminiModel,
                              generation_config=generation_config,
                              safety_settings=safety_settings,)
                              # system_instruction=textsi_2)


def initChatMode():
  convo = model.start_chat(history=[])
  return convo
# convo = model.start_chat(history=[])
convo= initChatMode()



# chat mode 
def singleChat(message):
  response = convo.send_message(
      [message],
      generation_config=generation_config,
      safety_settings=safety_settings
  )
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
  

def sendMessage(message):
    response = convo.send_message(message)
    return  response.text  #convo.last.text
  
def chatHistorySummary():
    print(convo.history)
    _, response = generateResponseInstr(testPrompt6, convo.history)
    # print(response.text)
    return response


# initialize out stremlit app
st.set_page_config(page_title="AI Mental Health Detection", page_icon="🧠", layout="centered", initial_sidebar_state="expanded")

st.header("Gemini LLM AI Mental Health Detection Application")

input1 = st.text_input("Enter your message here", key="input1", value="What is your feeling today?")
# input = st.text_area("Enter your message here", "I am feeling sad today")
submit = st.button("Chat")
chatHist = st.button("Chat History Emotion Summary")


    
# Check if the button is clicked
if submit:
    # response = generateResponse(input1)
    _, response = generateResponseInstr(testPrompt5, input1) # classifier for 
    responseChat = sendMessage(input1)
    print(response)
    st.session_state.classifyResult.append(response) # append result
    st.session_state.dialogueTotalCnt +=1
    calculateDepressAnxietyAvg(response) # calculate average Depress Ave
    print(f"Result: Depress Avg: { st.session_state.depressAvg:6.4f} Anxiety Avg:  {st.session_state.anxietyAvg:6.4f}  Total Dialogue: {st.session_state.dialogueTotalCnt}  Depress: {st.session_state.depressCnt} Anxiety: { st.session_state.anxietyCnt} ")
    st.subheader("AI Bot response is")
    st.write(responseChat)

if chatHist:
    st.subheader("Chat History Emotion Summary")
    response = chatHistorySummary()
    print(response)
    st.subheader("AI Bot response is")
    st.write(response)


