TOKEN = "1409852956:AAGw3jVo7hNI-9wLF7zOOct6w84LG__-hd0"

a = {
    "id": "2208104688201989159",
    "from": {
        "id": 514114435,
        "is_bot": False,
        "first_name": "Тимур",
        "username": "dyutin",
        "language_code": "ru",
    },
    "message": {
        "message_id": 903,
        "from": {
            "id": 1409852956,
            "is_bot": True,
            "first_name": "руззкий",
            "username": "ruzzkiy_bot",
        },
        "chat": {
            "id": 514114435,
            "first_name": "Тимур",
            "username": "dyutin",
            "type": "private",
        },
        "date": 1606600557,
        "text": "Привет! Пользователь @beneficium1 приглашает тебя сыграть в игру ОДИН НА ОДИН в @ruzzkiy_bot \n\nСкорее принимай приглашение!",
        "entities": [
            {"type": "mention", "offset": 21, "length": 12},
            {"type": "mention", "offset": 80, "length": 12},
        ],
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "Принять приглашение", "callback_data": "676733741"}]
            ]
        },
    },
    "chat_instance": "-2618453495629378967",
    "data": "676733741",
}

print(a["message"]["reply_markup"]["inline_keyboard"][0][0]["callback_data"])