### Goal

We need a chatbot that will
- contact a given patient on slack
- conduct a discussion and try to convince the patient to:
  - come back to care
  - agree on a date for a new appointment
- After each interaction, evaluate if the conversation is over or not
- Once the conversation is over, output a machine-usable json document containing:
  -  nextAppointmentSet (true/false)
  -  nextApppointmentDate (date of next appointment)

### Out of scope
Given the limited time for this POC, we tried to keep the scope minimal and focused on the AI driven chatbot. Input and output integration has been abstracted as follows

#### Input
Fetching the patient information is out of scope, we'll use `json` files (`patient.XXX.json`) as as substitute. This is given as a command line argument to the script.


```
{
    "email": "ademarcq@resolvetosavelives.org",
    "name": "Arnaud",
    "age": 43,
    "sex": "male",
    "prefered_language": "English",
    "facilityName": "Test PHC"
}
```
> [!TIP]
> Note that the `prefered_language` is respected. We tried English, French, Spanish, Hindi, Hindi with English letters (parsing prompt performed poorly and was not able to get the dates)


#### Output
Processing the output is out of scope as well. Output behaviour will be something like 
- if the patient agreed to visit, create a new appointment and mark the patient as "agreed to visit"
- if not, flag the patient as needing to be called by a human HCW

An successful discussion will output something like that
```
{
    "conversationOver": true,
    "nextAppointmentSet": true,
    "nextApppointmentDate": "2025-06-04"
}
```

An unsuccessful discussion will output something like that
```
{
    "conversationOver": true,
    "nextAppointmentSet": false,
    "nextApppointmentDate": null
}
```

### Technical stack
- Script is developped in Python
   - Script is relatively small =>  150 lines including comments !
- Web API for **Google Gemini** is used
- Web API for **Slack** is used

### AI involvement
We've got two prompts:
- one prompt for the dicussion
- one for analysing the discussion and generating the output, that's aimed at answering these 3 questions:
    - is the conversation over ? (stop condition)
    - has the patient agreed to visit ?
    - when ?

### Examples of conversation:


#### Conversation:
```
 Bot: Hi Daniel, we noticed you missed your last appointment at Test PHC. It's important to manage your hypertension, so would you be available to come in sometime next week for a check-up and to get your medication?
 Patient: Sorry, I'm busy
 Bot: Daniel, I understand you're busy. However, keeping your blood pressure under control is really important. Would you be able to come in the week after next instead? It's crucial for your health.
 Patient: Yes, is it possible to get help with the bus fare?
 Bot: Daniel, I understand your concern about the bus fare. Unfortunately, I'm not able to help with that directly. Would it be possible for a family member or friend to help you with transportation, or perhaps you could explore public transportation options to Test PHC? It's very important to come in for your check-up and medication refill the week after next to manage your hypertension.
 Patient: Ok, I'll come in at 6pm to Test PHC, after work. Will it be open?
 Bot: Daniel, I'm glad to hear you're planning to come in! However, I don't have access to the exact opening hours. Could you call Test PHC to confirm they're open until 6 PM that day? Also, what day the week after next works best for you to come in?
 Patient: Tuesday or Wednesday
 Bot: Great! Would Tuesday or Wednesday be best for you the week after next to come for your appointment? Please confirm which day, and remember to call Test PHC to confirm they're open until 6 PM if you plan to come that late.
 Patient: Yes
 Bot: Daniel, thank you for confirming. Please let me know if Tuesday or Wednesday works best so we can note it down. Also, please call Test PHC to confirm they are open until 6 PM if you plan to come that late.
 Patient: Tuesday
 Bot: Perfect Daniel. So Tuesday it is. Please make sure to call Test PHC beforehand to confirm they are open until 6 PM. See you then!
```


