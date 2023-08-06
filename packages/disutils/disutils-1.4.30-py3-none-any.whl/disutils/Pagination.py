from typing import List, Literal
import discord
import asyncio


class v1_x_Paginator:
    def __init__(self, ctx, pages: List[discord.Embed], auto_footer: bool = False, commands: dict = {"⏮️": "first", "⏪": "previous", "⏹": "stop", "⏩": "next", "⏭️": "last"}, timeout: float = 60.0, on_stop: Literal["remove_reactions", "delete_message", None] = None, start_page: int = 0):
        self.ctx = ctx
        self.bot = ctx.bot
        self.pages = pages
        self.auto_footer = auto_footer
        self.commands = commands
        self.timeout = timeout
        self.on_stop = on_stop
        self.current_page = start_page

    async def run(self):
        if self.auto_footer:
            for page in self.pages:
                page.set_footer(
                    text=f"Page {self.pages.index(page) + 1} of {len(self.pages)}")

        self.message = await self.ctx.send(embed=self.pages[self.current_page])

        for command in self.commands:
            await self.message.add_reaction(command)

        def check(reaction, user):
            return user == self.ctx.author and reaction.message.id == self.message.id and str(reaction.emoji) in self.commands.keys()

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=self.timeout, check=check)
                command = self.commands[str(reaction.emoji)]

                if command == "stop":
                    return await self.stop()

                elif command == "first":
                    self.current_page = 0

                elif command == "previous":
                    if self.current_page > 0:
                        self.current_page -= 1

                elif command == "next":
                    if self.current_page < len(self.pages) - 1:
                        self.current_page += 1

                elif command == "last":
                    self.current_page = len(self.pages) - 1

                elif command.startswith("page"):
                    try:
                        page = int(command.split("page")[1])
                        if page > 0 and page <= len(self.pages):
                            self.current_page = page - 1
                    except:
                        raise ValueError("Invalid page number")

                await self.message.remove_reaction(str(reaction.emoji), user)
                await self.message.edit(embed=self.pages[self.current_page])

            except asyncio.TimeoutError:
                return await self.stop()

    async def stop(self):
        if self.on_stop == "remove_reactions":
            await self.message.clear_reactions()
        elif self.on_stop == "delete_message":
            await self.message.delete()


# TODO do it with 2.0 discord.View
class v2_x_Paginator(v1_x_Paginator):
    pass


if discord.version_info.major == 1:
    Paginator = v1_x_Paginator
elif discord.version_info.major == 2:
    Paginator = v2_x_Paginator
