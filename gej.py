import discord
from discord.ext import commands
from discord import app_commands
import random
import os

# === BOT SETUP ===
intents = discord.Intents.default()
intents.message_content = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="/", intents=intents)
        self.synced = False

    async def setup_hook(self):
        # Dodajemy komendy do drzewa
        self.tree.add_command(kiss)
        self.tree.add_command(hug)
        self.tree.add_command(love)
        self.tree.add_command(slap)
        self.tree.add_command(smash)
        self.tree.add_command(cry)
        if not self.synced:
            await self.tree.sync()
            self.synced = True

bot = MyBot()

@bot.event
async def on_ready():
    print(f"✅ Zalogowano jako {bot.user} (ID: {bot.user.id})")

# === GIF ===
def get_random_gif(folder_name):
    gif_folder = os.path.join("gifs", folder_name)
    if not os.path.exists(gif_folder):
        return None
    gif_files = [f for f in os.listdir(gif_folder) if f.endswith('.gif')]
    if not gif_files:
        return None
    return os.path.join(gif_folder, random.choice(gif_files))

# === TEKSTY ===
def generate_random_text(action, user1, user2):
    messages = {
        'kiss': [f"**{user1}** *całuje* **{user2}** 🥰", f"**{user1}** *daje całusa* **{user2}** 💋"],
        'hug': [f"**{user1}** *przytula* **{user2}** 🤗", f"**{user1}** *obejmuje* **{user2}** ❤️"],
        'love': [f"**{user1}** *kocha* **{user2}** 💖", f"**{user1}** *wyznaje miłość* **{user2}** 💞"],
        'slap': [f"**{user1}** *spoliczkował/a* **{user2}** 😵", f"**{user1}** *uderza* **{user2}** 💥"],
        'smash': [f"**{user1}** *rozbił/a* **{user2}** 💣", f"**{user1}** *zniszczył/a* **{user2}** 🔨"],
        'cry': [f"**{user1}** *płacze z powodu* **{user2}** 😢", f"**{user1}** *łka* przez **{user2}** 😭"],
    }
    return random.choice(messages.get(action, []))

# === UNIWERSALNA KOMENDA ===
async def handle_interaction(interaction: discord.Interaction, action: str, title: str, color: discord.Color, target: discord.User = None):
    await interaction.response.defer()
    user1 = interaction.user.display_name
    user2 = target.display_name if target else "kogoś"
    message = generate_random_text(action, user1, user2)
    gif_path = get_random_gif(action)

    if gif_path:
        with open(gif_path, 'rb') as f:
            file = discord.File(f, filename=os.path.basename(gif_path))
            embed = discord.Embed(title=title, description=message, color=color)
            embed.set_image(url=f"attachment://{file.filename}")
            await interaction.followup.send(embed=embed, file=file)
    else:
        await interaction.followup.send("❌ Nie udało się znaleźć gifa.")

# === KOMENDY ===

@app_commands.command(name="kiss", description="Pocałuj kogoś!")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(target="Osoba, którą chcesz pocałować")
async def kiss(interaction: discord.Interaction, target: discord.User = None):
    await handle_interaction(interaction, "kiss", "💋 Pocałunek", discord.Color.red(), target)

@app_commands.command(name="hug", description="Przytul kogoś!")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(target="Osoba, którą chcesz przytulić")
async def hug(interaction: discord.Interaction, target: discord.User = None):
    await handle_interaction(interaction, "hug", "🤗 Przytulas", discord.Color.green(), target)

@app_commands.command(name="love", description="Wyznaj komuś miłość!")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(target="Osoba, którą kochasz")
async def love(interaction: discord.Interaction, target: discord.User = None):
    await handle_interaction(interaction, "love", "💖 Miłość", discord.Color.pink(), target)

@app_commands.command(name="slap", description="Spoliczkuj kogoś!")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(target="Osoba, którą chcesz uderzyć")
async def slap(interaction: discord.Interaction, target: discord.User = None):
    await handle_interaction(interaction, "slap", "👋 Policzek", discord.Color.orange(), target)

@app_commands.command(name="smash", description="Zniszcz kogoś!")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(target="Osoba, którą chcesz zmiażdżyć")
async def smash(interaction: discord.Interaction, target: discord.User = None):
    await handle_interaction(interaction, "smash", "💥 Smash!", discord.Color.blurple(), target)

@app_commands.command(name="cry", description="Płacz przez kogoś!")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(target="Osoba, przez którą płaczesz")
async def cry(interaction: discord.Interaction, target: discord.User = None):
    await handle_interaction(interaction, "cry", "😭 Płacz", discord.Color.blue(), target)

# === START ===
bot.run('MTM5NTg5ODU2NzAzMzQ4NzQ2MA.GXh7Xx.6zT2DqcuLFTT4Q0dSz57ohPw5P0UKQuGYKrimI')
