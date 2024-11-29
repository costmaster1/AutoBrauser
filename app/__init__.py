
from flask import Flask
from flask import Blueprint



# Создаем blueprint для управления пользователями
user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/user/<username>')
def user_profile(username):
    return f'Profile page of user {username}'


 
app = Flask(__name__)
# Подключаем конфигурацию DevelopmentConfig
app.config.from_object('config.DevelopmentConfig')


# Импортируем маршруты
from app import routes


