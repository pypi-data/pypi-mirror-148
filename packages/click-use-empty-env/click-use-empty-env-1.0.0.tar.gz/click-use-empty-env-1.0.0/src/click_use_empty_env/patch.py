import os
from typing import Optional

import click
from click import Context

_PATCH_INSTALLED = False


def parameter_resolve_envvar_value(self, ctx: Context) -> Optional[str]:
    if self.envvar is None:
        return None

    if isinstance(self.envvar, str):
        rv = os.environ.get(self.envvar)

        if rv is not None:
            return rv
    else:
        for envvar in self.envvar:
            return os.environ.get(envvar)

    return None


def option_resolve_envvar_value(self, ctx: Context) -> Optional[str]:
    rv = super(click.Option, self).resolve_envvar_value(ctx)

    if rv is not None:
        return rv

    if (
        self.allow_from_autoenv
        and ctx.auto_envvar_prefix is not None
        and self.name is not None
    ):
        envvar = f"{ctx.auto_envvar_prefix}_{self.name.upper()}"
        return  os.environ.get(envvar)

    return None


def install_patch():
    global _PATCH_INSTALLED
    if _PATCH_INSTALLED:
        return
    click.Parameter.resolve_envvar_value = parameter_resolve_envvar_value
    click.Option.resolve_envvar_value = option_resolve_envvar_value
    _PATCH_INSTALLED = True

