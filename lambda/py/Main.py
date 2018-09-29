from bs4 import BeautifulSoup

infile = open("egg.xml","r")
contents = infile.read()
soup = BeautifulSoup(contents,'xml')


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


# fulfilled recipe
def setRecipeFromList(intent, session):
    recipeName = intent['slots']['AMAZON.Food']['value']
    return(readInstructions(recipeName))

#step through instructions
def readInstructions(recipe):
    session_attributes = {}
    card_title = ''
    #specifies the category
    titles = soup.recipe.find_all('Instructions')
    speach_output =''
    for title in titles:
        speach_output += title.get_text()+", "
    reprompt_text=""
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, False))


def readRecipesByCategory(intent, session):
    session_attributes = {}
    card_title = ''
    infile = open("egg.xml","r")
    contents = infile.read()
    soup = BeautifulSoup(contents,'xml')
    #specifies the category
    titles = soup.intent['slots']['FoodCategory']['value'].find_all('Name')
    speach_output =''
    for title in titles:
        speach_output += title.get_text()+", "
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
    reprompt_text = "What would you like to cook?"
    should_end_session = False
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
        return setRecipeFromList(intent, session)
    elif intent_name == "AddMissingToGroceryList":
        return get_welcome_response()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    else:
        raise ValueError("Invalid intent")