from .utils import make_request

class QuizClient:
    def __init__(self, api_key):
        """API Client

        Parameters
        ----------
        api_key : str
            QuizAPI.io API Key
        """
        self.api_key = api_key
        self.config = None
        self.endpoint = "https://quizapi.io/api/v1/questions"
        self._config_exist = False
        
        

    def make_config(self, category=None, difficulty=None, limit=None, tags=None):
        configs = {
                "category":category, 
                "difficulty":difficulty, 
                "limit":limit, 
                "tags":tags
            }

        newConfig = {}
        for config in configs:
            if configs[config] == None:
                continue
            else:
                newConfig[config] = configs[config]

        config = newConfig

        self.config = config
        self._config_exist = True


    def get_questions(self, use_config=False, category=None, difficulty=None, limit=None, tags=None):
        if use_config == True:
            if self.config == None:
                raise ValueError("No config defined on Client Object. Use the make_config method to make a configuration.")
            else:
                config = self.config
        else:
            configs = {
                "category":category, 
                "difficulty":difficulty, 
                "limit":limit, 
                "tags":tags
            }

            newConfig = {}
            for config in configs:
                if configs[config] == None:
                    continue
                else:
                    newConfig[config] = configs[config]

            config = newConfig

        response, content, status = make_request(self.api_key, self.endpoint, config)

        if status != 403:
            raise Exception(f"Error Code: {status}, {content['error']}")
        else:
            return content
