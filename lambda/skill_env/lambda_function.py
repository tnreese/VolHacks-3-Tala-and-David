from bs4 import BeautifulSoup
import lxml
import xmltodict

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


#step through instructions
def readIngredients(intent, session):
    # with open('egg.xml') as fd:
    #     doc = xmltodict.parse(fd.read())

    session_attributes = {}
    card_title = ''
    #specifies the category

    food = intent['slots']['SpecificFood']['value']

    ingredientsList = ["eggs", "bacon", "grease"]
    speech_output = ""
    for ingredient in ingredientsList:
        speech_output += ingredient + " "

    speech_output += " say I want to start cooking to begin"
    reprompt_text="retry that"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, False))


def readRecipesByCategory(intent, session):
    print("reached readRecipes by Category")
    session_attributes = {}
    card_title = ''
    # infile = open("egg.xml","r")
    # contents = infile.read()
    # soup = BeautifulSoup(contents,'xml')
    # #specifies the category
    # titles = soup.Breakfast.find_all('Name')
    speech_output = intent['slots']['Category']['value']
    # for title in titles:
    #     speech_output += title.get_text()+", "
    reprompt_text=""
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, False))

def readInstructions(intent, session):
    session_attributes = {}
    card_title = ''

    instructionList = ["boil", "let sit", "salt" "serve"]

    speech_output = instructionList[0]
    # session_attributes[0]++
    reprompt_text=""
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, False))

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


def get_welcome_response():
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "What would you like to cook?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "What would you like to cook 2?"
    should_end_session = False
    print("welcome response")
    return build_response(session_attributes, build_speechlet_response(
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
    elif intent_name == "AddMissingToGroceryList":
        return get_welcome_response()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    else:
        raise ValueError("Invalid intent")

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    # print("event.session.application.applicationId=" +
    #       event['session']['application']['applicationId'])

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
    return get_welcome_response()


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here
