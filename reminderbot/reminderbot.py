from google import genai
from json import JSONEncoder
from datetime import datetime
import jsonpickle
import json
import os

###
## Creates the patient clas. TODO: should be in a different script/package
###

class Patient:
    eggs = None
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
    patient: Patient
    messages= []
    def __init__(self, patient):
        self.patient= patient
    def dumpConversation(self) -> str:
        returnString= ''
        for currentMessage in self.messages:
            returnString = returnString + currentMessage.author +  ': '  +  currentMessage.messageText + '\n '
        return returnString
    
class ConversationAnalyseResult:
    conversationOver:bool
    nextAppointmentSet:bool
    nextApppointmentDate:str




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
test_patient = Patient()
test_patient.name ="Arnaud"
test_patient.age = 43
test_patient.sex= "male"
test_patient.prefered_language="English"
test_patient.facilityName="Test PHC"
currentConversation = Conversation(test_patient);


###
## Defines a few helper functions
###
def getDiscussionPrompt() -> str:
    returnString: str =  discussion_prompt_file_content.replace("__PATIENT_DATA__", test_patient.dumpPatient())
    returnString = returnString.replace("__CONVERSATION__", currentConversation.dumpConversation())
    return returnString

def getAnalysePrompt() -> str:
    returnString: str =  analyse_prompt_file_content.replace("__PATIENT_DATA__", test_patient.dumpPatient())
    returnString = returnString.replace("__CONVERSATION__", currentConversation.dumpConversation())
    returnString = returnString.replace("__CURRENT_DATE__", datetime.now().strftime("%Y-%m-%d"))
    return returnString



###
## Loops until satisfied. Max is 5
###
for i in range(5):
    ## Generate customized prompt for the patient
    currentPrompt = getDiscussionPrompt()
    ## Gets the message to be sent to the patient
    chatbot_message = client.models.generate_content(
        model="gemini-2.0-flash", contents=currentPrompt
    )
    currentConversation.messages.append( Message ('Bot', chatbot_message.text))
    ## Analyse the current State for the conversation
    analysePrompt = getAnalysePrompt()
    analyseResponse = client.models.generate_content(
        model="gemini-2.0-flash", contents=analysePrompt
    )
    print(analyseResponse.text)
    ## Gets the answer from the patient 
    print(chatbot_message.text)
    patient_response = input()
    currentConversation.messages.append( Message ('Patient', patient_response))


print(getDiscussionPrompt())



