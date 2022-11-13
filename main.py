import os
import requests
from discord import app_commands, Intents, Client, Interaction

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
    print("Вы ввели некорректный токен.")

print("")
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
    print(f"Бот активирован.")
    print(f"{client.user} | {client.user.id}")
    print(" ")
    print(f"Ссылка для приглашения бота на сервер:")
    print(f"> https://discord.com/api/oauth2/authorize?client_id={client.user.id}&scope=applications.commands%20bot")
    print(" ")

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