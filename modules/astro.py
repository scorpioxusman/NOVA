class AstroLogic:
    def __init__(self, bot):
        self.bot = bot
        self.hub_id = 1122334455 # Your "Join to Create" ID
        self.active_rooms = {}

    async def manage_temp_channels(self, member, before, after):
        # Create Room
        if after.channel and after.channel.id == self.hub_id:
            category = after.channel.category
            room = await member.guild.create_voice_channel(f"🔊 {member.name}'s Room", category=category)
            await member.move_to(room)
            self.active_rooms[room.id] = member.id
            
        # Cleanup Empty Rooms
        if before.channel and before.channel.id in self.active_rooms:
            if len(before.channel.members) == 0:
                await before.channel.delete()
                del self.active_rooms[before.channel.id]
