from django.apps import AppConfig
from .SparseDataframe import SparseDataframe
from .preprocessor import decompress

class RecommenderConfig(AppConfig):

    name = 'recommender'


    def __init__(self, app_name, app_module):
        super(RecommenderConfig, self).__init__(app_name, app_module)
        self.sparseDf = None

    def ready(self):
        path = decompress()
        if self.sparseDf is None:
            print('hello')
            self.sparseDf = SparseDataframe(greaterThan=30, csvPath=path)
