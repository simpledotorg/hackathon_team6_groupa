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



