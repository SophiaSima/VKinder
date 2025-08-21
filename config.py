# config.py
# Файл для хранения всех констант и токенов
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Токен для доступа к API VK
USER_TOKEN = os.getenv('USER_TOKEN')

# Токен группы (для ответов бота) - ВСТАВЬТЕ ВАШ ТОКЕН
GROUP_TOKEN = os.getenv('GROUP_TOKEN')

APP_ID = os.getenv('APP_ID')
API_VERSION = os.getenv('API_VERSION')
DATABASE_URL = os.getenv('DATABASE_URL')
SEARCH_COUNT = os.getenv('SEARCH_COUNT')
SEARCH_OFFSET = os.getenv('SEARCH_OFFSET')