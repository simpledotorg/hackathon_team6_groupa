from google import genai
from json import JSONEncoder
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse
from threading import Event
import jsonpickle
import json
import os
import time
import sys

###
## Creates the patient clas. TODO: should be in a different script/package
###

class Patient:
    email:str = None
    name = None
    age = None
    sex = None
    prefered_language= "English"
    facilityName= None
    def dumpPatient(self) -> str:
        return jsonpickle.encode(self)


class Message:
    author:str
    messageText:str
    def __init__(self, author, messageText):
        self.author= author
        self.messageText=messageText


class Conversation:
    patient: None
    messages= []
    def __init__(self, patient):
        self.patient= patient
    def dumpConversation(self) -> str:
        returnString= ' '
        for currentMessage in self.messages:
            returnString = returnString + currentMessage.author +  ': '  +  currentMessage.messageText + '\n '
        return returnString
    
class ConversationAnalyseResult:
    def __init__(self, d=None):
        print(d)
        if d is not None:
            for key, value in d.items():
                print(key)
                print(value)
                if value is not None and key is not None:
                 setattr(self, key, value)
    conversationOver:bool
    nextAppointmentSet:bool
    nextApppointmentDate:str



###
## Slack client. Todo: make it an interface
###
slackClient = WebClient(token=os.environ.get('SLACK_TOKEN'))

###
## Connects to Google Gemini. TODO: make it an interface
###
client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

###
## This loads the template for the prompt
###
with open("./prompt.base.txt", 'r') as file:
    discussion_prompt_file_content = file.read()

with open("./prompt.analyse.txt", 'r') as file:
    analyse_prompt_file_content = file.read()

###
## Loads the patient. TODO : take it from an interface, ideally from a list
###
with open(sys.argv[1]) as patient_file:
  file_content = patient_file.read()
patient_dict = json.loads(file_content)
currentConversation = Conversation(patient_dict);
slack_user_id = slackClient.users_lookupByEmail(email=patient_dict["email"])["user"]["id"]

print(str(patient_dict))
###
## Defines a few helper functions
###
def getDiscussionPrompt() -> str:
    returnString: str =  discussion_prompt_file_content.replace("__PATIENT_DATA__", str(patient_dict))
    returnString = returnString.replace("__CONVERSATION__", currentConversation.dumpConversation())
    return returnString

def getAnalysePrompt() -> str:
    returnString: str =  analyse_prompt_file_content.replace("__PATIENT_DATA__", str(patient_dict))
    returnString = returnString.replace("__CONVERSATION__", currentConversation.dumpConversation())
    returnString = returnString.replace("__CURRENT_DATE__", datetime.now().strftime("%Y-%m-%d"))
    return returnString

def getConversationAnalyseResult() -> ConversationAnalyseResult:
    analysePrompt = getAnalysePrompt()
    analyseResponse = client.models.generate_content(
        model="gemini-2.0-flash", contents=analysePrompt
    ).text.replace("```json", "").replace("```","")
    print(analyseResponse)
    
    return ConversationAnalyseResult(json.loads(analyseResponse))

###
## Loops until satisfied. Max is 5
###
for i in range(10):
    ## Generate customized prompt for the patient
    currentPrompt = getDiscussionPrompt()
    ## Gets the message to be sent to the patient
    chatbot_message = client.models.generate_content(
        model="gemini-2.0-flash", contents=currentPrompt
    ).text.strip("\n ")
    slackResponse = slackClient.chat_postMessage(
            channel=slack_user_id,
            text=chatbot_message)
    print(slackResponse)
    dmChannelId = slackResponse["channel"]
    ## Checks if we should continue or not
    currentConversation.messages.append( Message ('Bot', chatbot_message))
    if (len(currentConversation.messages) > 1):
        currentResult: ConversationAnalyseResult = getConversationAnalyseResult()
        if (currentResult.conversationOver):
            break
    ## Gets the answer from the patient 
    print(chatbot_message)
    patient_response= None
    while (patient_response is None):
        slackPatientAnswer = slackClient.conversations_history(
            channel=dmChannelId,
            inclusive=True,
            limit=1
            )
        lastMessage = slackPatientAnswer["messages"][0]
        if(lastMessage["user"] == slack_user_id) :
            patient_response = lastMessage["text"]
            print(lastMessage)
        else:
            time.sleep(3)
    currentConversation.messages.append( Message ('Patient', patient_response))


print(getDiscussionPrompt())



