import os
import requests
from discord import app_commands, Intents, Client, Interaction

# цветовые коды
class ConsoleColors:
    Success = '\033[92m'
    Warning = '\033[93m'
    Error = '\033[91m'
    Reset = '\033[0m'

# Проверка на корректность введённого токена
def CheckTokenValidity(token: str) -> dict:
    response = requests.get("https://discord.com/api/v10/users/@me", headers = {"Authorization": f"Bot {token}"})
    return response.json()

print("Добро пожаловать.")

while True:
    token = input("Введите токен вашего бота > ")
    data = CheckTokenValidity(token)

    if data.get("id", None):
        break

    print("")
    print(ConsoleColors.Warning + "Вы ввели некорректный токен." + ConsoleColors.Reset)

print("")
print(ConsoleColors.Success + "Введён валидный токен." + ConsoleColors.Reset)
print("Не закрывайте программу...")
print("")

# клиент бота
class Badge(Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents = intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        await self.tree.sync(guild = None)

client = Badge(intents = Intents.none())

# активация бота
@client.event
async def on_ready():
    print(ConsoleColors.Success + f"Бот успешно активирован." + ConsoleColors.Reset)
    print(f"{client.user} | {client.user.id}")
    print(" ")
    print(f"Ссылка для приглашения бота на сервер:")
    print(f"> https://discord.com/api/oauth2/authorize?client_id={client.user.id}&scope=applications.commands%20bot")
    print(" ")

# ошибка при выполнении
@client.event
async def on_error():
    print(ConsoleColors.Error + "Во время выполнения произошла ошибка.")
    print("Возможные причины проблемы:")
    print(" - Отсутствие подключения к интернету.")
    print(" - Нестабильное подключение к интернету.")
    print(" - Проблемы на серверах Discord.")
    print(" - Некорректная версия Discord.py или Requests.")
    print(ConsoleColors.Reset)
    print("Если вы не смогли решить проблему, откройте issue в репозитории бота: https://github.com/oqo0/discord-badge")

    os._exit(0)

# глобальная команда /getbadge
@client.tree.command()
async def getbadge(interaction: Interaction):
    print(f"Команда была использована пользователем {interaction.user}.")

    await interaction.response.send_message("\n".join([
        f"Приветствую, **{interaction.user}**, спасибо за использование этого бота.",
        "",
        "__**Когда я смогу получить значок?**__",
        "Получение доступа к значку занимает до 24 часов, т.к. проверка происходит раз в сутки.",
        "",
        "__**Как забрать значок**__",
        "После того как прошло 24 часа нужно перейти по ссылке: https://discord.com/developers/active-developer и заполнить форму.",
        "Если вы сделали всё правильно значок автоматически появится у вас в аккаунте.",
        "",
        "Если этот бот был полезен для вас, пожалуйста, поставьте звёзду репозиторию с ботом.",
    ]))
    
    await interaction.client.close()
    await interaction.client.clear()
    os._exit(0)

client.run(token)