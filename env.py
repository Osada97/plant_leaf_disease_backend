import os
from dotenv import load_dotenv


class Environment():
    def getBaseEnv():
        load_dotenv()
        return os.getenv('BASE_URL')
