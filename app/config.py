import dotenv, os
from fastapi.templating import Jinja2Templates

dotenv.load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

templates = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=templates + '/templates')
