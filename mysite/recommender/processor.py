from django.apps import apps



def getTopQuestions(question_id, top=5, voteCountsUnder=500):
    recommender_config = apps.get_app_config('recommender')
    sparseDf = recommender_config.sparseDf
    dict = sparseDf.getTopItems(top, question_id, voteCountsUnder=voteCountsUnder)
    return dict
