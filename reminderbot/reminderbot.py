from google import genai
from json import JSONEncoder
import jsonpickle
import json
import os

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
## Loads the patient. TODO : take it from an interface
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
print(currentPrompt)



###
## Gets the first message to be sent to the patient
###
response = client.models.generate_content(
    model="gemini-2.0-flash", contents=currentPrompt
)



print(response.text)

response = input()


