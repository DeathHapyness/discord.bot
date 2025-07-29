import discord
from discord.ext import commands


TOKEN = "..."

#
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

last_welcome_message = None

# Classe com os botões
class GamesView(discord.ui.View):
    def __init__(self, message_ref_callback):
        super().__init__()
        self.message_ref_callback = message_ref_callback

    async def handle_role(self, interaction, role_name, cargo_nome):
        role = discord.utils.get(interaction.guild.roles, name=role_name)
        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"Cargo **{cargo_nome}** adicionado com sucesso!", ephemeral=True)
            # Log de de registros
            log_channel = discord.utils.get(interaction.guild.text_channels, name="log-do-servidor")
            if log_channel:
                await log_channel.send(f"[LOG] {interaction.user.mention} recebeu o cargo **{cargo_nome}** pelo botão.")
            msg = self.message_ref_callback()
            if msg:
                await discord.utils.sleep_until(discord.utils.utcnow() + discord.timedelta(seconds=20))
                try:
                    await msg.delete()
                except Exception:
                    pass

    @discord.ui.button(label="Ark", style=discord.ButtonStyle.primary)
    async def ark_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_role(interaction, "Ark", "Ark")

    @discord.ui.button(label="night-crows", style=discord.ButtonStyle.primary)
    async def night_crows_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_role(interaction, "night-crows", "night-crows")

    @discord.ui.button(label="poe", style=discord.ButtonStyle.primary)
    async def poe_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_role(interaction, "poe", "poe")

    @discord.ui.button(label="throne-and-liberty", style=discord.ButtonStyle.primary)
    async def throne_and_liberty_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_role(interaction, "throne-and-liberty", "throne-and-liberty")


# Evento de boas-vindas 

@bot.event
async def on_member_join(member):
    global last_welcome_message
    guild = member.guild
    role = discord.utils.get(guild.roles, name="comunidade")
    if role:
        await member.add_roles(role)
   
    channel = discord.utils.get(guild.text_channels, name="registro")
    if channel:
       
        try:
            async for message in channel.history(limit=None):
                await message.delete()
        except Exception:
            pass

        def get_last_msg():
            return last_welcome_message
        view = GamesView(get_last_msg)
        msg = await channel.send(
            f"Olá! Seja bem-vindo(a) ao servidor!\n"
            f"{member.mention}! Por favor, escolha um jogo abaixo para receber o cargo correspondente e liberar os demais canais:",
            view=view
        )
        last_welcome_message = msg



@bot.event
async def on_ready():
    print(f"Bot {bot.user} está online!")

bot.run(TOKEN)
