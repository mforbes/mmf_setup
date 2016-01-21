"""Mercurial extension for committing clean Jupyter notebooks.
"""

from mercurial import cmdutil, commands
from mercurial.util import Abort
from mercurial.i18n import _    # International support


cmdtable = {}
command = cmdutil.command(cmdtable)

testedwith = '3.6.3'


######################################################################
# Helpers
@command(
    'checkpoint',               # name
    [                           # options
        ('v', 'verbose', False, _('enable additional output'))
    ],
    _(''))                      # synopsis
def checkpoint(ui, repo):
    try:
        commands.commit(ui, repo, quiet=True,
                        message="CHK: auto checkpoint")
        commands.tag(ui, repo, '_c_new', force=True, local=True, quiet=True)
    except Abort:
        pass
    finally:
        commands.tag(ui, repo, '_c_new', force=True, local=True, quiet=True)


@command(
    'nbclean',                  # name
    [                           # options
        ('v', 'verbose', False, _('enable additional output'))
    ],
    _(''))                      # synopsis
def nbclean(ui, repo, **opts):
    """Strip added or modified notebooks of their output."""
