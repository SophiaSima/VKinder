# main.py
"""
Главный файл приложения VKinder Bot.

"""
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import GROUP_TOKEN
from bot.message_handlers import MessageHandlers
from vk_tools.vk_tools import parse_user_input


def main():
    """Основная функция запуска бота"""
    print("🚀 Запуск VKinder Bot...")

    try:
        # Инициализируем VK API
        vk_session = vk_api.VkApi(token=GROUP_TOKEN)
        vk = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)

        # Инициализируем обработчики сообщений
        handlers = MessageHandlers(vk, {})

        print("✅ Бот успешно запущен и слушает сообщения...")

        # Основной цикл обработки сообщений
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                user_id = event.user_id
                message_text = event.text

                print(f"📩 Получено сообщение от {user_id}: {message_text}")

                # Парсим команду пользователя
                command = parse_user_input(message_text)

                # Обрабатываем команду
                if command == 'start':
                    handlers.handle_start(user_id)
                elif command == 'next':
                    handlers.show_next_profile(user_id)
                elif command == 'add_to_favorites':
                    handlers.handle_add_to_favorites(user_id)
                elif command == 'favorites':
                    handlers.handle_show_favorites(user_id)
                elif command == 'help':
                    handlers.handle_help(user_id)
                else:
                    # Неизвестная команда - показываем помощь
                    vk.messages.send(
                        user_id=user_id,
                        message="Не понимаю тебя 😕\nИспользуй кнопки или напиши «Помощь»",
                        random_id=0,
                        keyboard=handlers.create_main_keyboard().get_keyboard()
                    )

    except Exception as e:
        print(f"❌ Критическая ошибка при запуске бота: {e}")
        raise


if __name__ == "__main__":
    main()