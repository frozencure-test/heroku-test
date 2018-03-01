from django.apps import apps
from urllib.parse import urlparse as parse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import os.path



def getTopQuestions(question_id, top=5):
    recommender_config = apps.get_app_config('recommender')
    sparseDf = recommender_config.sparseDf
    if parseQuestionUrl(question_id) is not False:
        question_id = parseQuestionUrl(question_id)
    try:
        num_Id = int(question_id)
    except ValueError:
        return False
    dict = sparseDf.getTopItemsCosineSim(num_Id, top=top)
    return dict


def parseQuestionUrl(url):
    val = URLValidator()
    try:
        val(url)
    except ValidationError:
        return False
    arr = parse(url)
    pathSections = arr.path.split('/')
    try:
        id = int(pathSections[2])
    except ValueError:
        return False
    return id

url = "https://stackoverflow.com/questions/3367194/configure-django-urls-py-to-keep-anchors-in-url-after-it-rewrites-it-with-a-end"
print(parseQuestionUrl(url))