from __future__ import annotations
            _("Error: {message}").format(message=self.format_message()),
            file=file,
            color=self.show_color,
        )




class UsageError(ClickException):
    """An internal exception that signals a usage error.  This typically
    aborts any further handling.


    :param message: the error message to display.
    :param ctx: optionally the context that caused this error.  Click will
                fill in the context automatically in some situations.
    """


    exit_code = 2


    def __init__(self, message: str, ctx: Context | None = None) -> None:
        super().__init__(message)
        self.ctx = ctx
        self.cmd: Command | None = self.ctx.command if self.ctx else None


    def show(self, file: t.IO[t.Any] | None = None) -> None:
        if file is None:
            file = get_text_stderr()
        color = None
        hint = ""
        if self.ctx is not None:
            help_option = self.ctx.command.get_help_option(self.ctx)

            if help_option is not None:
                help_option_names = set(help_option.opts)
                hint_option = next(
                    (
                        name
                        for name in self.ctx.help_option_names
                        if name in help_option_names
                    ),
                    help_option.opts[0],
                )

                hint = _("Try '{command} {option}' for help.").format(
                    command=self.ctx.command_path, option=hint_option
                )
                hint = f"{hint}\n"
        if self.ctx is not None:
            color = self.ctx.color
            echo(f"{self.ctx.get_usage()}\n{hint}", file=file, color=color)
        echo(
            _("Error: {message}").format(message=self.format_message()),
            file=file,
            color=color,
        )




class BadParameter(UsageError):
    """An exception that formats out a standardized error message for a
    bad parameter.  This is useful when thrown from a callback or type as
    Click will attach contextual information to it (for instance, which
    parameter it is).


    .. versionadded:: 2.0


    :param param: the parameter object that caused this error.  This can
                  be left out, and Click will attach this info itself
                  if possible.
    :param param_hint: a string that shows up as parameter name.  This
                       can be used as alternative to `param` in cases
                       where custom validation should happen.  If it is
                       a string it's used as such, if it's a list then
                       each item is quoted and separated.
    """


    def __init__(
        self,
        message: str,
        ctx: Context | None = None,
        param: Parameter | None = None,
        param_hint: cabc.Sequence[str] | str | None = None,
    ) -> None:
        super().__init__(message, ctx)
        self.param = param
        self.param_hint = param_hint
