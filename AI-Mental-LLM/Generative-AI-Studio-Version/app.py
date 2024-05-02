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
import plotly.express as px  # pip install plotly-express
import os, json, re, random
import pandas as pd
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
if "textsi_1" not in st.session_state: 
    st.session_state.textsi_1 = """
I am a mental health professional and I am here to help you.I am not a doctor, but I can provide you with some general information about mental health. If you are in crisis, please call 911 or go to the nearest emergency room. If you are in need of immediate help, please call the National"""
if "textsi_2" not in st.session_state: 
    st.session_state.textsi_2 = """
I am a mental health professional and I am here to help you.I am not a doctor, but I can provide you with some general information about mental health."""

# sample for prompt instruction
if "testPrompt1" not in st.session_state: 
    st.session_state.testPrompt1 = """Is it have Depression or anxiety disorder or not, as below conversation?

    Context:"""
if "testPrompt2" not in st.session_state: 
    st.session_state.testPrompt2 = """I don't feel like doing much of anything todays?

    Context:"""
if "testPrompt3" not in st.session_state:    
    st.session_state.testPrompt3 = """If the phrase connotes a depressed emotion, assign a number 1 to the phrase. Otherwise, a number 0.

    Context:"""
if "testPrompt4" not in st.session_state:    
    st.session_state.testPrompt4 = """If the phrase connotes a anxiety emotion, assign a number 1 to the phrase. Otherwise, a number 0.

    Context:"""
if "testPrompt5" not in st.session_state:
    st.session_state.testPrompt5 = """If the phrase connotes a depressed emotion, assign a number 1 to the phrase. if phrase connotes a anxiety emotion, assign a number 2 to the phrase.
                if phrase connotes both anxiety emotion and  depressed emotion, assign a number 3 to the phrase .Otherwise, a number 0.

    Context:"""
if "testPrompt6" not in st.session_state:
    st.session_state.testPrompt6 = """Summarize the following conversation, What is the Emotion of the conversation?   

Context:"""
if "testPrompt7" not in st.session_state:
    st.session_state.testPrompt7 = """Classify Emotion into depressed, anxiety , both anxiety and depressed , not anxiety and not depressed from as below context.

    Context:"""

if "testPrompt8" not in st.session_state:
    st.session_state.testPrompt8 = """
    For each phrase, read the phrase carefully and assign a number based on the emotion it connotes:

1: If the phrase connotes a depressed emotion (e.g. sadness, despair, hopelessness)
2: If the phrase connotes an anxiety emotion (e.g. fear, worry, nervousness)
3: If the phrase connotes both anxiety and depressed emotions
0: If the phrase does not connote either anxiety or depressed emotions (e.g. neutral, happy, excited).

Output format in JSON with text and emtion , without explanation the reason for the emotion.
Context: """

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

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
if "depressHist" not in st.session_state:
    st.session_state.depressHist = [] # {}
    
if "anxietyHist" not in st.session_state:
    st.session_state.anxietyHist = [] # {}

# Calculate Depression and Anxiety Average
def calculateDepressAnxietyAvg(result):
    output = ""
    if result == "0":
        output = "Emotion: Not Depressed or Anxiety"
        print(output)
 
    elif result == "1":
        output = "Emotion: Depressed"
        print(output)
        st.session_state.depressCnt += 1
    
    elif result == "2":
        output = "Emotion: Anxiety"
        print(output)
        st.session_state.anxietyCnt += 1
  
    elif result == "3":
        output = "Emotion: Both Anxiety and Depressed"
        print(output)
        st.session_state.depressCnt += 1
        st.session_state.anxietyCnt += 1
    
    st.session_state.depressAvg = st.session_state.depressCnt/st.session_state.dialogueTotalCnt
    st.session_state.anxietyAvg =  st.session_state.anxietyCnt/st.session_state.dialogueTotalCnt
    st.session_state.depressHist.append(st.session_state.depressAvg)
    st.session_state.anxietyHist.append(st.session_state.anxietyAvg)
    return output

# gen ai 
# geminiModel =  "gemini-1.0-pro"
# geminiVisionModel = "gemini-vision-1.0-pro-002"

# Set up the model
st.session_state.model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings,)
                              # system_instruction=textsi_2)


# def initChatMode():
#   st.session_state.convo = st.session_state.model.start_chat(history=[])
#   return st.session_state.convo
# convo = model.start_chat(history=[])
st.session_state.convo= st.session_state.model.start_chat(history=[])



# chat mode 
def singleChat(message):
  response = st.session_state.convo.send_message(
      [message],
      generation_config=generation_config,
      safety_settings=safety_settings
  )
  return response.text


# Generate response function with Instruction Prompt Template for Generate Contenct 
def generateResponseInstr(prompTemp, message):
    response = st.session_state.model.generate_content(f"""
    {prompTemp}
    {message}""")
    # print(response.text)
    return response, response.text

def generateResponse(message):
    response = st.session_state.model.generate_content(f"""
    {message}""")
    # print(response.text)
    return response.text
  

def sendMessage(message):
    response = st.session_state.convo.send_message(message)
    return  response.text  #convo.last.text
  
def chatHistorySummary():
    # print(st.session_state.chat_history)
    _, response = generateResponseInstr(st.session_state.testPrompt6, st.session_state.chat_history)
    # print(response.text)
    return response

def generateIntervention():
    selectedInterventionList = [1, 2, 5,6,8,7,8]
    selectedIntervention = random.choice(selectedInterventionList)
    print(f"Selected Intervention: {selectedIntervention}")
    if st.session_state.depressAvg >= 0.5 and st.session_state.anxietyAvg <= 0.5:
        return "Recommend A"
    elif st.session_state.anxietyAvg <= 0.5 and st.session_state.depressAvg >= 0.5:
        return "Recommend B"
    elif st.session_state.anxietyAvg >= 0.5 and st.session_state.depressAvg >= 0.5:
        return "Recommend C"
    elif st.session_state.anxietyAvg <= 0.5 and st.session_state.depressAvg <= 0.5:
        return "Recommend D"
    elif st.session_state.anxietyAvg >= 0.5 and st.session_state.depressAvg <= 0.5:
        return "Recommend E"

# initialize out stremlit app
st.set_page_config(page_title="AI Mental Health Detection", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

st.header("Gemini LLM AI Mental Health Detection Application")
left_column, right_column = st.columns(2)
input1 = left_column.text_input("Enter your message here about your feel and thinking", key="input1", value="What is your feeling today?")
# input = st.text_area("Enter your message here", "I am feeling sad today")
submit = left_column.button("Chat")
chatHist = left_column.button("Chat History Emotion Summary")
intervent = left_column.button("Generate Intervention")
exportEmotion = right_column.button("Export Emotion History")

    
# Check if the button is clicked
if submit:
    # response = generateResponse(input1)
    _, response = generateResponseInstr(st.session_state.testPrompt5, input1) # classifier for 
    st.session_state.chat_history.append(("user", input1))
    responseChat = sendMessage(input1)
    st.session_state.chat_history.append(("Bot", responseChat))
    # print(response)
    st.session_state.classifyResult.append(response) # append result
    st.session_state.dialogueTotalCnt +=1
    st.session_state.emotion = calculateDepressAnxietyAvg(response) # calculate average Depress Ave
    print(f"Result: Depress Avg: { st.session_state.depressAvg:6.4f} Anxiety Avg:  {st.session_state.anxietyAvg:6.4f}  Total Dialogue: {st.session_state.dialogueTotalCnt}  Depress: {st.session_state.depressCnt} Anxiety: { st.session_state.anxietyCnt} ")
    left_column.subheader("AI Bot response is")
    left_column.write(responseChat)
    df1 = pd.DataFrame(st.session_state.depressHist, columns=["depression"])
    df2 = pd.DataFrame(st.session_state.anxietyHist, columns=["anxiety"])
    # print("Depress Hist: \n", df1.head())
    # print("Anxiety Hist: \n", df2.head())
    st.session_state.df3 = pd.concat([df1, df2], axis=1) #combine two dataframe for ploting 
    print("Combine Hist: \n", st.session_state.df3.head())
    st.session_state.figDepress = px.line(st.session_state.df3, x=st.session_state.df3.index, y=["depression","anxiety"], title="Depression and Anxiety Score In Dialogues", 
                                          labels={"x":"Dialogue Count", "y":"Score"}, line_shape="spline", render_mode="svg", color_discrete_sequence=["blue", "green"], 
                                          template="plotly_dark", symbol_map={"depression":"circle", "anxiety":"circle"}) 
    st.session_state.figDepress.update_layout(yaxis_range=[-0.2, 1.2] , 
                                              xaxis_title="Dialogue Count", yaxis_title="Score", 
                                              title="Depression and Anxiety Score In Dialogues",
                                              xaxis_tickformat="d", yaxis_tickformat=".2f")
    right_column.plotly_chart(st.session_state.figDepress) # update the i
    right_column.write(f"Last {st.session_state.emotion}")
    

if chatHist:
    left_column.subheader("Chat History Emotion Summary")
    response = chatHistorySummary()
    print(response)
    left_column.subheader("AI Bot response is")
    left_column.write(response)


if exportEmotion:
    if "df3" not in st.session_state:
        right_column.write("Not Emotion History can export!")
    else:   
        st.session_state.df3.to_csv("emotion_history.csv", index=False)
        right_column.write("Export Emotion History to CSV file")


if intervent:
    left_column.subheader("Generate Intervention:")
    recommend = generateIntervention()
    left_column.write(recommend)