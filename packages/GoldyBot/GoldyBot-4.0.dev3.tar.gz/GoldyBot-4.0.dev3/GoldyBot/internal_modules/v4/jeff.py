import GoldyBot

class JeffTheKiller(GoldyBot.Extenstion):
    """Just a test extenstion."""

    def __init__(self):
        super().__init__(self)
        
    def loader(self):

        @GoldyBot.command()
        async def jeff(self:JeffTheKiller, ctx):
            data = await self.database.find_one(self.FindGuilds.find_object_by_id(ctx.guild.id).database_collection_name, {"_id": ctx.author.id})
            await ctx.send("jiff")
            await ctx.send(str(data))

def load():
    """This is executed by Goldy Bot when this module is loaded."""
    JeffTheKiller()