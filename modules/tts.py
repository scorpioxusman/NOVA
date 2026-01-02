from gtts import gTTS
import os

class TTSManager:
    async def play_speech(self, message, text):
        tts = gTTS(text=text, lang='en')
        tts.save("output.mp3")
        vc = await message.author.voice.channel.connect()
        vc.play(discord.FFmpegPCMAudio("output.mp3"), after=lambda e: os.remove("output.mp3"))
        # Disconnect logic here...
