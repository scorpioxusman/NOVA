import discord
import time

class WickHardened:
    def __init__(self, bot, state):
        self.bot = bot
        self.state = state  # Access to core/state.py
        self.heat = {}      # {user_id: {"score": 0, "last": 0}}

    async def check_security(self, message):
        """The Firewall: Processes every message before the bot reacts."""
        # Check Whitelist from State
        if self.state.is_whitelisted(message.author.id): 
            return True, None

        # 1. Spam/Heat Logic
        uid = message.author.id
        now = time.time()
        u_heat = self.heat.get(uid, {"score": 0, "last": now})
        
        # Decay heat over time (Cooling down)
        u_heat["score"] = max(0, u_heat["score"] - (now - u_heat["last"]) * 5)
        u_heat["score"] += 15 
        u_heat["last"] = now
        self.heat[uid] = u_heat

        if u_heat["score"] > 100:
            await self.apply_quarantine(message.author, "Auto-Mod: Spam Heat")
            return False, "User Quarantined for Spamming."

        return True, None

    async def apply_quarantine(self, member, reason):
        """Strips all roles and saves them to State."""
        old_roles = [r.id for r in member.roles if r.name != "@everyone"]
        self.state.set_quarantine(member.id, old_roles)
        
        try:
            await member.edit(roles=[], reason=f"Wick Quarantine: {reason}")
        except Exception as e:
            print(f"Security Error: Could not quarantine {member.name}: {e}")
