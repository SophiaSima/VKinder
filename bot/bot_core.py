# bot/bot_core.py
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import GROUP_TOKEN
from bot.message_handlers import handle_message
from bot.keyboard_utils import get_main_keyboard
import traceback


class VKBot:
    def __init__(self, group_token):
        self.vk = vk_api.VkApi(token=group_token)
        self.longpoll = VkLongPoll(self.vk)
        self.api = self.vk.get_api()

    def send_message(self, user_id, message, keyboard=None, attachment=None):
        """Отправляет сообщение пользователю"""
        params = {
            'user_id': user_id,
            'message': message,
            'random_id': 0
        }

        if keyboard:
            params['keyboard'] = keyboard

        if attachment:
            params['attachment'] = attachment

        try:
            result = self.api.messages.send(**params)
            print(f"✅ Сообщение отправлено: {message[:50]}...")
            return result
        except Exception as e:
            print(f"❌ Ошибка отправки сообщения: {e}")
            print(traceback.format_exc())

    def run(self):
        """Запускает бота"""
        print("Бот запущен... Ожидание сообщений")

        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                user_id = event.user_id
                message_text = event.text

                print(f"📩 Получено сообщение от {user_id}: '{message_text}'")

                try:
                    # Обрабатываем сообщение
                    result = handle_message(user_id, message_text)

                    # Отправляем ответ
                    if len(result) == 2:
                        message, keyboard = result
                        self.send_message(user_id, message, keyboard)
                    elif len(result) == 3:
                        message, keyboard, attachment = result
                        self.send_message(user_id, message, keyboard, attachment)
                    else:
                        print(f"❌ Неверный формат ответа: {result}")

                except Exception as e:
                    error_msg = f"❌ Ошибка обработки сообщения: {e}"
                    print(error_msg)
                    print(traceback.format_exc())
                    self.send_message(user_id, "Произошла ошибка 😢 Попробуйте позже.")