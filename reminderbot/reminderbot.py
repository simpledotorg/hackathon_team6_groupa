from google import genai
from json import JSONEncoder
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

###
## Connects to Google Gemini. TODO: make it an interface
###
client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

###
## This loads the template for the prompt
###
with open("./prompt.base.txt", 'r') as file:
    file_content = file.read()


###
## Loads the patient. TODO : take it from an interface, ideally from a list
###
test_patient = Patient()
test_patient.name ="Arnaud"
test_patient.age = 43
test_patient.sex= "male"
test_patient.prefered_language="English"
test_patient.facilityName="Test PHC"

###
## Generate customized first prompt for the patient
###
currentPrompt = file_content.replace("__PATIENT_DATA__", jsonpickle.encode(test_patient))

###
## Loops until satisfied. Max is 5
###

for i in range(5):
    ###
    ## Gets the message to be sent to the patient
    ###
    chatbot_message = client.models.generate_content(
        model="gemini-2.0-flash", contents=currentPrompt
    )

    ###
    ## Gets the answer from the patient 
    ###
    print(chatbot_message.text)
    patient_response = input()

    ###
    ## Prepares the message for next round
    ###
    currentPrompt = currentPrompt + "HISTORY of Message: \n " + "BOT: " + chatbot_message.text +" \nPATIENT: "+ patient_response






