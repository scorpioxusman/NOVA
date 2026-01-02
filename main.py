import discord
from discord.ext import commands
import uuid
from core.state import GlobalState
from modules.wick import WickHardened
# Import your other modules here as you build them:
# from modules.astro import AstroLogic 

class NovaCore(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)
        
        # 0. Initialize Core State
        self.state = GlobalState()
        
        # 1. Initialize Wick Module
        self.wick = WickHardened(self, self.state)
        
        # Placeholders for Astro, Lara, TTS
        self.astro = None 
        self.lara = None

    async def on_ready(self):
        print(f"🛡️ Nova System Online: {self.user.name}")

    async def on_message(self, message):
        if message.author.bot: return

        # 1. WICK FIREWALL (Runs before everything)
        is_safe, reason = await self.wick.check_security(message)
        if not is_safe:
            return 

        # 2. PROCEED TO COMMANDS
        await self.process_commands(message)

    # --- WICK COMMAND SETS ---

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):
        """Auto Setup Wizard & Rescue Key Generation"""
        key = str(uuid.uuid4()).upper()[:13]
        
        # Save to Core State
        self.state.data["rescue_key"] = key
        self.state.save()
        
        embed = discord.Embed(title="🛡️ Wick Setup Wizard", color=0x2f3136)
        embed.add_field(name="Rescue Key", value=f"||{key}||", inline=False)
        embed.set_footer(text="SAVE THIS KEY. Required for Anti-Nuke recovery.")
        
        await ctx.author.send(embed=embed)
        await ctx.send("✅ **Wick Setup Complete.** Your rescue key has been sent to DMs.")

    @commands.command()
    async def permit(self, ctx, member: discord.Member):
        """Whitelists a user in the Core State"""
        if ctx.author.guild_permissions.administrator:
            if member.id not in self.state.data["whitelist"]:
                self.state.data["whitelist"].append(member.id)
                self.state.save()
                await ctx.send(f"🛡️ **Permit Issued:** {member.mention} added to whitelist.")

# --- START SYSTEM ---
if __name__ == "__main__":
    bot = NovaCore()
    # Note: Avoid hardcoding tokens in code for safety. 
    # Use environment variables in production.
    bot.run("MTQ1NjYxMDk1ODQzMTc1MjM1OQ.Gleu9-.ppRWYk1V3dZhWcImPeCJwEWcyjjvG1RYnnRYVA")
