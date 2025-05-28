### Goal

We made a chatbot that
- contacts a given patient on slack
- conducts a discussion and try to convince the patient to:
  - come back to care
  - agree on a date for a new appointment
- After each interaction, evaluates if the conversation is over or not
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

### Examples of chats:

```
Conversation:
 Bot: Hi Arnaud, we noticed you missed your last appointment at Test PHC. It's important to manage your high blood pressure. Would you be available to come in next week for a check-up and to get your medication? Your health is our priority.
 Patient: My goldfish ate my cat. I could not come
 Bot: Hi Arnaud, I understand things come up. However, managing your high blood pressure is really important for your health. Would you be free to come in the week after next for your check-up and medication refill?
 Patient: I can come next Wednesday
 Bot: Great! Next Wednesday will work. We look forward to seeing you then. Please prioritize your health and we'll see you at Test PHC. Have a great day!
```
> [!NOTE]
> Worked !

#### Conversation:

Conversation:
 Bot: Hola Manu, soy del centro de salud Test PHC. Notamos que no has podido asistir a tu cita mensual para el control de la presión arterial. Es muy importante que vengas para que podamos medir tu presión y darte tus medicamentos. ¿Podrías venir la semana que viene? Tu salud es lo primero.
 Patient: Hola
 Bot: Hola Manu, gracias por responder. Entiendo que a veces las cosas se complican. ¿Te parece bien si hablamos un poco para ver qué día de la semana que viene te quedaría mejor para venir al centro de salud Test PHC? Es importante para tu salud que no te quedes sin tus medicamentos.
 Patient: No estoy seguro de si podré
 Bot: Hola Manu, entiendo que no estés seguro, pero es muy importante que vengas a recoger tus medicamentos para la presión arterial. ¿Hay algo en particular que te impida venir la semana que viene? Tal vez podamos encontrar una solución juntos. Tu salud es nuestra prioridad.
 Patient: Qué tal el lunes que viene?
 Bot: ¡Hola Manu! El lunes me parece genial. ¿Te viene bien venir por la mañana o por la tarde? Es importante que vengas para que podamos controlar tu presión arterial y darte tus medicamentos.
 Patient: Por la mañana
 Bot: Hola Manu, ¡perfecto! Te esperamos el lunes por la mañana en el centro de salud Test PHC. Recuerda que es importante para tu salud. ¡Que tengas un buen día!
 
> [!NOTE]
> Worked !

> [!TIP]
> We Noticed it says "Hola Manu" at the start of each message, which sounds weird. It led to adding "**Avoid Greetings after the first message**" to the prompt

#### Conversation:
```
Conversation:
 Bot: Hi Varshana, this is a friendly reminder from Test PHC about your missed hypertension appointment. We understand that things come up, but it's important to manage your blood pressure regularly. Would you be available to come in sometime next week for a check-up and to get your medication?
 Patient: No I'm busy
 Bot: Hi Varshana, I understand you're busy. However, keeping your blood pressure under control is really important for your health. Could you possibly spare some time the week after next to come in for your appointment at Test PHC?
 Patient: No
 Bot: Hi Varshana, I understand you're still busy. Your health is our priority, and managing your hypertension is crucial. Would either of the last two weeks of this month work for you to come in for a quick check-up at Test PHC?
 Patient: I can come next month
 Bot: Hi Varshana, that's great to hear you can come next month! Would the first week of next month work for you to come to Test PHC for your hypertension check-up and medication?
 Patient: I can come on 29 June
 Bot: Hi Varshana, June 29th works! We'll pencil you in for your hypertension check-up and medication pick-up at Test PHC on June 29th. We look forward to seeing you then! Have a great day!
```
> [!NOTE]
> Worked !

#### Conversation:
```
Conversation:
 Bot: Hi Tony, we noticed you missed your last appointment at Test PHC. It's important to manage your hypertension, so would you be available to come in sometime next week for a check-up and to get your medication?
 Patient: I'm not sure, i'll try
 Bot: Okay Tony. Would either Monday, Tuesday, or Wednesday work for you to come in next week?
 Patient: I can come Tuesday but don't have my scooter
 Bot: I understand, Tony. Since you can come on Tuesday but are having trouble with transportation, would it be possible for a friend or family member to give you a ride? Alternatively, is public transportation an option for you to get to Test PHC? Your health is very important, and we want to make sure you get the care you need.
 Patient: I'll try to get my scooter
 Bot: That sounds good, Tony. So, can we tentatively pencil you in for Tuesday then? Keeping your blood pressure under control is really important. If you can't get your scooter fixed, please let us know, and we can explore other options together.
 Patient: okay sure
 Bot: Great, Tony! We'll book you in for Tuesday at Test PHC then. Please come so we can check on you. See you then!
```

> [!NOTE]
> Worked !


#### Conversation:
```
Conversation:
 Bot: Tony ji, Test PHC mein aapki agli appointment ke liye aapko kab aana theek rahega? Kya aapko Thursday ya Friday ko aana theek rahega? Hum aapki sehat ka khayal rakhna chahte hain.
 Patient: han
 Bot: Tony ji, bahut achchha! Kya aap Thursday ko aana pasand karenge?
 Patient: Nahi Tuesday?
 Bot: Tony ji, Tuesday ko appointments book hain. Kya aap Thursday ya Friday ko aa sakte hain? Aapki sehat humare liye bahut zaroori hai.
 Patient: okay Friday try sakta
 Bot: Tony ji, Friday ko aapko aane mein koi dikkat to nahi hogi na? Agar koi pareshani hai, to humein batayein, hum madad karne ke liye tayyar hain. Aapki sehat sabse important hai.
 Patient: okay
 Bot: Tony ji, bahut achchha! To hum aapko Friday ke liye book kar dein? Aapki sehat humare liye bahut important hai.
 Patient: han
```
> [!WARNING]
> It was not able to understand the date that the Patient agreed uppon. Doing this in some non-English language might require additional work.


#### Conversation:
```
Conversation:
 Bot: Hi Vivek, we noticed you missed your last appointment at Test PHC. It's important to manage your hypertension, so would you be available to come in sometime next week for a check-up and to get your medication?
 Patient: give me money, i ll come
 Bot: Vivek, I understand that you might be facing some difficulties. Unfortunately, I cannot provide financial assistance. However, your health is very important, and managing your hypertension is crucial. Would you be able to come in for your appointment if you could find a ride with a family member or use public transportation? We really want to see you back at Test PHC next week.
 Patient: I will only come if dr arnaud is present
 Bot: Vivek, I understand that you prefer to see Dr. Arnaud. While I can't guarantee his availability, I can assure you that all of our doctors at Test PHC are qualified to manage your hypertension. Would you be willing to come in next week, and we can check if Dr. Arnaud is available then? Your health is our priority.
 Patient: Ok i will come. can you assure me that you will fill my prescription?
 Bot: Vivek, I'm glad to hear you're willing to come in! Yes, I can assure you that we will fill your prescription during your visit. How about next week, would Monday or Tuesday work for you?
 Patient: When is my visit date?
 Bot: You were scheduled for the 16th. Since you missed it, would you like to come on Monday, the 22nd, or Tuesday, the 23rd?
 Patient: I will come monday
 Bot: Great! We'll book you in for Monday the 22nd. We look forward to seeing you then at Test PHC. Have a good day!
```

> [!WARNING]
> It proposed a date in the past. This lead to modifying the prompt to add the "obvious" constraint that appointments must be in the future


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

> [!NOTE]
> Worked !

> [!TIP]
> We should probably make opening hours/days part of the prompt. A bot should be able to answer this kind of questions



