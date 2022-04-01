from discord.ext import commands

from .helpers.pag import Pag

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cmds_per_page = 5

    def get_command_signature(self, command: commands.Command, ctx: commands.Context):
        aliases = " or "+command.aliases[0]+" or " if len(command.aliases) > 1 else ""
        aliases += " or ".join(command.aliases[1:]) if len(command.aliases) > 1 else ""
        cmd_invoke = f"?[{command.name}{aliases}]" if command.aliases else command.name

        full_invoke = command.qualified_name.replace(command.name, "")

        signature = f"{full_invoke}{cmd_invoke} {command.signature}"
        return signature

    async def return_filtered_commands(self, walkable, ctx):
        filtered = []

        for c in walkable.walk_commands():
            try:
                if c.hidden or c.parent:
                    continue

                await c.can_run(ctx)
                filtered.append(c)

            except commands.CommandError:
                continue

        return sorted(filtered, key=lambda c: c.name)

    async def setup_help_pag(self, ctx, command=None, title=None):
        command = command or self.bot
        title = title or self.bot.description

        pages = []

        if isinstance(command, commands.Command):
            filtered_commands = (
                list(set(command.all_commands.values())) if hasattr(command, "all_commands")
                else []
            )

            filtered_commands.insert(0, command)

        else:
            filtered_commands = await self.return_filtered_commands(command, ctx)

        for i in range(0, len(filtered_commands), self.cmds_per_page):
            next_commands = filtered_commands[i : i + self.cmds_per_page]
            commands_entry = ""

            for cmd in next_commands:
                desc = cmd.help or "No description"
                signature = self.get_command_signature(cmd, ctx)
                subcommand = "Has subcommands" if hasattr(cmd, "all_commands") else ""

                commands_entry += (
                    f"• **`{cmd.name}`**\n```\n{signature}\n```\n{desc}\n"
                    if isinstance(command, commands.Command)
                    else f"• **`{cmd.name}`**\n{desc}\n    {subcommand}\n"
                )
            pages.append(commands_entry)

        await Pag(title=title, color=0xCE2029, entries=pages, length=1).start(ctx)

    @commands.command(name="help", aliases=["h", "commands"])
    async def help_command(self, ctx, *, command=None):
        """The help command"""
        if not command:
            await self.setup_help_pag(ctx)

        else:
            cog = self.bot.get_cog(command)
            if cog:
                await self.setup_help_pag(ctx, cog, f"{cog.qualified_name}'s commands")

            else:
                command = self.bot.get_command(command)
                if command:
                    await self.setup_help_pag(ctx, command, command.name)

                else:
                    await ctx.send("Command not found")

def setup(bot):
    bot.add_cog(Help(bot))