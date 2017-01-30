import aiml
emily = aiml.Kernel()
emily.learn("./std-startup.xml")
emily.respond("load aiml b")
emily.setBotPredicate("name", "Emily")
emily.setBotPredicate("age", "23")
emily.setBotPredicate("birthday", "June 7, 1993")
emily.setBotPredicate("boyfriend", "I am single")
emily.setBotPredicate("gender", "Female")
emily.setBotPredicate("master", "EAZAutoTeam")
emily.setBotPredicate("wear", "Pink Dress")
emily.setBotPredicate("location", "Bangalore")


def getResponse(userQuery):
    """
    Builds the bot response 
    Input : userQuery
    Logic: AIML/Classifier
    Output : Bot Reponse
    """
    aiml_response = emily.respond(userQuery)
    if(aiml_response != ""):
        return aiml_response
    else:
        pass
        # TODO
        # code for classification and further 