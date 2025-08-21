# main.py
from bot.bot_core import VKBot
from config import GROUP_TOKEN


def main():
    print("Запуск VKinder бота...")

    if not GROUP_TOKEN:
        print("❌ Ошибка: GROUP_TOKEN не установлен!")
        print("Получите токен группы в настройках сообщества -> Работа с API")
        return

    try:
        bot = VKBot(GROUP_TOKEN)
        bot.run()
    except Exception as e:
        print(f"❌ Ошибка запуска бота: {e}")


if __name__ == "__main__":
    main()