from bs4 import BeautifulSoup
from ask_sdk_core.handler_input import HandlerInput
import xml.etree.ElementTree as ET  
import lxml
import time
def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    # print("on_launch requestId=" + launch_request['requestId'] +
    #       ", sessionId=" + session['sessionId'])
    # # Dispatch to your skill's launch
    return get_welcome_response()


#step through instructions
def readIngredients(intent, session):
    # with open('egg.xml') as fd:
    #     doc = xmltodict.parse(fd.read())

    card_title = ''
    session_attributes={}
    #specifies the category

    SpecificFood = intent['slots']['SpecificFood']['value']
    ingredientsList =[]
    speech_output=''
    if SpecificFood == 'boiled egg':
        ingredientsList=['one egg','salt','pepper']
    elif SpecificFood == 'fried egg':
        ingredientsList=['one egg','2 tablespoons of Butter','salt','pepper']
    elif SpecificFood == 'omelette':
        ingredientsList = ['two large eggs','three tablespoons of butter','two sprigs of basil','five cherry tomatoes','salt and pepper']
    else:
        speech_output = 'unknown food'
    
    for ingredient in ingredientsList:
        speech_output += ingredient+ ", "

    print(ingredientsList)

    speech_output += " say start cooking " + SpecificFood + " to begin"
    reprompt_text="retry that"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, False))


def readRecipesByCategory(intent, session):
    print("reached readRecipes by Category")
    card_title = ''

    session_attributes={}

    foodCategory = []

    category = intent['slots']['Category']['value']
    speech_output = ''
    if category == 'breakfast':
        foodCategory = ['fried egg', 'boiled egg', 'omelet']
    else:
        print('not breakfast')

    for food in foodCategory:
        speech_output+= food + ', '

    reprompt_text=""
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, False))

def readInstructions(intent, session):
    card_title = ''

    SpecificFood = intent['slots']['SpecificFood']['value']
    instructionList = []
    timingList = []
    speech_output=''
    if SpecificFood == 'boiled egg':
        instructionList =['Place your egg in a pot and cover with cold water by 1 inch. On medium-high heat, let the water boil.','Once boiled, cover and set aside','Drain and set aside in ice water. Peel your egg, slice in half, and season with salt and pepper. Enjoy']
        timingList=[10,8,5]
    elif SpecificFood == 'fried egg':
        instructionList=['Melt 2 tablespoons of butter over high heat on a nonstick skillet.','Next break your egg into the pan and turn the heat to low','Let cook until your egg white are completly set and the yolk starts to thicken. While cooking, season with salt and pepper to taste. This will take 1 minute.','Once your egg white are completly set and the yolk thickened, plate your egg with toast and you are good to go!']
        timingList=[1,0,1]
    elif SpecificFood == 'omelette':
        instructionList=['Crack your eggs into a mixing bowl and wisk til combined. Add salt and pepper to taste','Slice your cherry tomatoes in half and melt your two tablespoons of butter on medium-high heat.', 'Toss and fry the cherry tomato halves.', 'Turn the heat down to medium and sprinkle on your basil leaves. Add your eggs and move the pan around so the eggs are spread evenly.','Once the omelette starts to cook and firm up but the top is still raw, use a spatula to ease up the edges of the omelette. Fold it in half. When the omelette starts to turn golden brown on both sides, slide the omelette on to a plate. Eat immediately and enjoy!']
        timingList=[2,3,1,1,3]
    else:
        speech_output = 'unknown food'
    
    session_attributes=''
    for i in range(0, len(instructionList)-1):
        nextStep(intent, session, instructionList[i])
        count = session.attributes['count']
        count+=1
        session,attributes['count'] = count
        print(count)
        time.sleep(timingList[i]) 
        
    reprompt_text=""
    session_attributes = {"i":i}

    speech_output = "instruction"

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, False))

def nextStep(intent, session, instruction):
    speech_output = instruction
    session_attributes={}
    card_title=''
    reprompt_text=''
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, False))

# def get_Recipe_Types(intent, session):
#     card_title=intent['Recipe Type']
#     session_attributes = {0}
#     tree = ET.parse('egg.xml')  
#     root = tree.getroot()
#     ListA = []
#     for x in root.findall('Types'):
#         ListA.append(x.text)
#     return ListA

def get_Data_from(recipe, item):
#get_Data(roasted chicken, ingredient)

    ListB = []

    with open("food.json") as json_file:
        data = json.load(json_file, parse_float = decimal.Decimal)
        for x in data:
            listB.append(x[item])
            print("Adding :", x[item])

    return ListB

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText', 
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# def create_instrunction_length_attributes(index):
#     return {"index": index}

def get_welcome_response( session):
    card_title = "Welcome"
    speech_output = "What would you like to cook?"
    session.attributes['index']=0
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "What would you like to cook 2?"
    should_end_session = False

    print("welcome response")
    return build_response(session.attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "ChooseRecipeIntent":
        return readRecipesByCategory(intent, session)
    elif intent_name == "ChooseRecipe":
        return readIngredients(intent, session)
    elif intent_name == "StartInstructions":
        return readInstructions(intent, session)
    elif intent_name == "NextItem":
        return nextStep(intent, session)
    elif intent_name == "AddMissingToGroceryList":
        return get_welcome_response( session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response( session)
    else:
        raise ValueError("Invalid intent")

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])



def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response(session)


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here