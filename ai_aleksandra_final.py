from telethon import TelegramClient, events
import openai
import config

client = TelegramClient("session", config.API_ID, config.API_HASH)
openai.api_key = config.OPENAI_API_KEY

ASSISTANT_ID = "asst_dhKH6MYgkayW5twtGK6ydgkd"

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    user_input = event.message.message
    await event.respond("✍️ Думаю над ответом...")

    # Создание потока (thread)
    thread = openai.beta.threads.create()

    # Отправка сообщения ассистенту
    openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input
    )

    # Запрос ответа от ассистента
    run = openai.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID
    )

    # Ожидание завершения run
    while True:
        run_status = openai.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if run_status.status == "completed":
            break

    # Получение сообщения-ответа
    messages = openai.beta.threads.messages.list(thread_id=thread.id)
    reply = messages.data[0].content[0].text.value

    await event.respond(reply)

print("✅ AI Aleksandra запущена (финальная версия)")
client.start()
client.run_until_disconnected()
