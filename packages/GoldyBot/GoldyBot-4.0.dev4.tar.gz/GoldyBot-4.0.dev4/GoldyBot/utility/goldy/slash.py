import asyncio
import nextcord

Interaction = nextcord.Interaction
MISSING = nextcord.utils.MISSING

loop = asyncio.get_event_loop()

class InteractionToCtx():
    """This Goldy Bot class is used to convert interactions to ctx."""
    def __init__(self, interaction: Interaction):
        self.interaction = interaction

    @property
    def guild(self) -> Interaction.guild:
        return self.interaction.guild

    @property
    def author(self):
        return self.interaction.user

    async def send(self, text=None, embed=MISSING):
        await self.interaction.send(text, embed=embed)
        return Message(self.interaction)

class Message():
    def __init__(self, interaction: Interaction):
        self.interaction = interaction

    async def delete(self):
        await self.interaction.delete_original_message()

    async def edit(self, text=MISSING, embed=MISSING):
        #TODO: #29 Don't forget to add text to this.
        await self.interaction.edit_original_message(text, embed=embed)