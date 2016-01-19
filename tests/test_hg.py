import subprocess
import tempfile
import os
import shutil

import pytest
from bash import bash
from fnmatch import fnmatch


class Shell(object):
    """Class to execute shell commands and check the result."""
    def __init__(self, tmpdir=None):
        self._tmpdir = tmpdir

    def __enter__(self):
        self.tmpdir = self._tmpdir
        if self.tmpdir is None:
            self.tmpdir = tempfile.mkdtemp()
        else:
            if os.path.exists(self.tmpdir):
                shutil.rmtree(self.tmpdir)
            os.makedirs(self.tmpdir)

        self.prevdir = os.getcwd()
        self.tstdir = os.path.dirname(__file__)
        os.chdir(os.path.expanduser(self.tmpdir))
        return self

    def __exit__(self, type, value, traceback):
        os.chdir(self.prevdir)
        if self._tmpdir is None:
            shutil.rmtree(self.tmpdir)

    @staticmethod
    def match(s1, s2):
        s1 = s1.strip()
        s2 = s2.strip()
        return s1 == s2 or fnmatch(s1, s2)

    def __call__(self, cmd, out='', err=''):
        """Run the command, replacing {tmpdir} and then check out and err"""
        res = bash(cmd.format(tstdir=self.tstdir, tmpdir=self.tmpdir))
        assert self.match(res.stderr, err)
        assert self.match(res.stdout, out)


class TestHG(object):
    @pytest.yield_fixture
    def sh(self):
        with Shell('_tmp') as sh:
            yield sh

    def _test_empty(self, sh):
        """Test command on an empty repo"""
        sh("hg init")
        sh("hg cst")
        sh("hg cdiff")
        sh("hg ccom", "nothing changed")

    def _test_hg(self, sh):
        """Test command on a clean repo"""
        sh("hg init")
        sh("cp {tstdir}/_data/n0_clean.ipynb N.ipynb")
        sh("hg cst", "? N.ipynb")
        sh("hg add N.ipynb", )
        sh("hg cst", "A N.ipynb")
        sh("hg ccom -m '0: Clean'", "created new head")
        sh("hg cst")

        _lg = "\n".join([
            "@  0:d * 0: Clean (* ago)  tip"
        ])
        sh("hg lg", _lg)
        sh("cp {tstdir}/_data/n1_clean.ipynb N.ipynb")
        sh("hg cst", "M N.ipynb")
        sh("hg ccom -m '1: Clean'", "created new head")

        _lg = "\n".join([
            "@  1:d * 1: Clean (* ago)  tip",
            "|",
            "o  0:d * 0: Clean (* seconds ago)"])
        sh("hg lg", _lg)
        sh("cp {tstdir}/_data/n1_dirty.ipynb N.ipynb")
        sh("hg st", "M N.ipynb")
        sh("hg cst")            # Only output differs
        sh("hg cdiff")
        sh("hg st", "M N.ipynb")

        # One can try to commit the dirty notebook.  Nothing has
        # changed, but the automatic output commit will appear.
        sh("hg ccom -m '1: Dirty'", "nothing changed")

        _lg = "\n".join([
            "o  2:d * ...: Automatic commit with .ipynb output (* ago)  tip",
            "|",
            "@  1:d * 1: Clean (* seconds ago)",
            "|",
            "o  0:d * 0: Clean (* seconds ago)",
        ])
        sh("hg lg", _lg)

        sh("cp {tstdir}/_data/n2_dirty.ipynb N.ipynb")

        # Commit a dirty notebook
        sh("cp {tstdir}/_data/n1_dirty.ipynb N1.ipynb")
        sh("hg add N1.ipynb")
        sh("hg com N1.ipynb -m 'N1: Dirty'", "created new head")
        sh("hg st", "M N.ipynb")
        sh("hg cst", "M N.ipynb")

        _diff = "\n".join([
            'diff --git a/N.ipynb b/N.ipynb',
            '--- a/N.ipynb',
            '+++ b/N.ipynb',
            '@@ -17,6 +17,17 @@',
            '    "source": [',
            '     "1+1"',
            '    ]',
            '+  },',
            '+  {',
            '+   "cell_type": "code",',
            '+   "execution_count": null,',
            '+   "metadata": {',
            '+    "collapsed": false',
            '+   },',
            '+   "outputs": [],',
            '+   "source": [',
            '+    "2+2"',
            '+   ]',
            '   }',
            '  ],',
            '  "metadata": {'])
        sh("hg cdiff", _diff)
        sh("hg ccom -m 'N2: Dirty'", "created new head")

        # Update to a previous clean revision and check that things
        # work.  This was the source of failure for issue #2
        _up = "1 files updated, 0 files merged, 1 files removed, 0 files unresolved"
        sh("hg up -C 1", _up)
        sh("hg cst")
        _lg = "\n".join([
            "o  5:d * ...: Automatic commit with .ipynb output (* ago)  tip",
            "|",
            "o  4:d * N2: Dirty (* seconds ago)",
            "|",
            "o  3:d * N1: Dirty (* seconds ago)",
            "|",
            "| o  2:d * ...: Automatic commit with .ipynb output (* seconds ago)",
            "|/",
            "@  1:d * 1: Clean (* seconds ago)",
            "|",
            "o  0:d * 0: Clean (* seconds ago)"])
        sh("hg lg", _lg)

    def test_hg_output_branch(self, sh):
        """Test command on a clean repo"""
        sh("hg init")
        sh("cp {tstdir}/_data/n0_clean.ipynb N.ipynb")
        sh("hg cst", "\n".join([
            "cleaning output",
            "? N.ipynb",
            "restoring output"]))
        sh("hg add N.ipynb", )
        sh("hg cst", "\n".join([
            "cleaning output",
            "A N.ipynb",
            "restoring output"]))
        sh("hg ccom -m '0: Clean'", "\n".join([
            "cleaning output",
            "created new head",
            "no output to commit",
            "restoring output"]))
        sh("hg cst", "\n".join([
            "cleaning output",
            "restoring output"]))

        _lg = "\n".join([
            "@  0:d * 0: Clean (* ago)  tip"
        ])
        sh("hg lg", _lg)
        sh("cp {tstdir}/_data/n1_clean.ipynb N.ipynb")
        sh("hg cst", "\n".join([
            "cleaning output",
            "M N.ipynb",
            "restoring output"]))

        sh("hg ccom -m '1+1'", "\n".join([
            "cleaning output",
            "created new head",
            "no output to commit",
            "restoring output"]))
        _lg = "\n".join([
            "@  1:d * 1+1 (* ago)  tip",
            "|",
            "o  0:d * 0: Clean (* seconds ago)"])
        sh("hg lg", _lg)

        # Try another commit - should do nothing.
        sh("hg ccom -m '1+1'", "\n".join([
            "cleaning output",
            "nothing changed",
            "no output to commit",
            "restoring output"]))
        sh("cp {tstdir}/_data/n1_dirty.ipynb N.ipynb")
        sh("hg st", "M N.ipynb")
        sh("hg cst", "\n".join([    # Only output differs
            "cleaning output",
            "restoring output"]))
        sh("hg cdiff", "\n".join([  # Only output differs
            "cleaning output",
            "restoring output"]))
        sh("hg st", "M N.ipynb")

        # One can try to commit the dirty notebook.  Nothing has
        # changed, but the automatic output commit will appear.
        sh("hg ccom -m '1+1'", "\n".join([
            "cleaning output",
            "nothing changed",
            "marked working directory as branch auto_output",
            "(branches are permanent and global, did you want a bookmark?)",
            "automatic commit of output",
            "restoring output"]))

        _lg = "\n".join([
            "o  2:d * ...: Automatic commit with * (* ago) auto_output tip",
            "|",
            "@  1:d * 1+1 (* seconds ago)",
            "|",
            "o  0:d * 0: Clean (* seconds ago)",
        ])
        sh("hg lg", _lg)

        # Commit the same notebook but with different output.
        sh("cp {tstdir}/_data/n1_dirty2.ipynb N.ipynb")
        sh("hg ccom -m '1+1'", "\n".join([
            "cleaning output",
            "nothing changed",
            "automatic commit of output",
            "restoring output"]))

        _lg = "\n".join([
            "o  3:d * ...: Automatic commit * (* ago) auto_output tip",
            "|",
            "o  2:d * ...: Automatic commit * (* ago) auto_output",
            "|",
            "@  1:d * 1+1 (* seconds ago)",
            "|",
            "o  0:d * 0: Clean (* seconds ago)",
        ])
        sh("hg lg", _lg)

        # Commit another dirty notebook on top
        sh("cp {tstdir}/_data/n2_dirty.ipynb N.ipynb")
        sh("cp {tstdir}/_data/n1_dirty.ipynb N1.ipynb")
        sh("hg add N1.ipynb")
        sh("hg com N1.ipynb -m 'second 1+1'")  # No new head with branches.
        sh("hg st", "M N.ipynb")
        sh("hg cst", "\n".join([
            "cleaning output",
            "M N.ipynb",
            "restoring output"]))

        _diff = "\n".join([
            'diff --git a/N.ipynb b/N.ipynb',
            '--- a/N.ipynb',
            '+++ b/N.ipynb',
            '@@ -17,6 +17,17 @@',
            '    "source": [',
            '     "1+1"',
            '    ]',
            '+  },',
            '+  {',
            '+   "cell_type": "code",',
            '+   "execution_count": null,',
            '+   "metadata": {',
            '+    "collapsed": false',
            '+   },',
            '+   "outputs": [],',
            '+   "source": [',
            '+    "2+2"',
            '+   ]',
            '   }',
            '  ],',
            '  "metadata": {'])
        sh("hg cdiff", "\n".join([
            "cleaning output",
            _diff,
            "restoring output"]))

        sh("hg ccom -m '2+2'", "\n".join([
            "cleaning output",
            "created new head",
            "automatic commit of output",
            "restoring output"]))

        # Update to a previous clean revision and check that things
        # work.  This was the source of failure for issue #2
        _up = "1 files updated, 0 files merged, 1 files removed, 0 files unresolved"
        sh("hg up -C 1", _up)
        sh("hg cst", "\n".join([
            "cleaning output",
            "restoring output"]))
        _lg = "\n".join([
            "o    6:d * ...: Automatic commit * (* ago) auto_output tip",
            "|\\",
            "| o  5:d * 2+2 (* ago)",
            "| |",
            "| o  4:d * second 1+1 (* ago)",
            "| |",
            "o |  3:d * ...: Automatic commit * (* ago) auto_output",
            "| |",
            "o |  2:d * ...: Automatic commit * (* ago) auto_output",
            "|/",
            "@  1:d * 1+1 (* ago)",
            "|",
            "o  0:d * 0: Clean (* ago)"])
        sh("hg lg", _lg)


"""
hg init
echo "0" > A
hg add A
hg com -m "0"
hg tag -l t0
hg up 00000
hg branch "other"
hg com -m "Added other branch"
hg up default
echo "1" >> A
hg com -m "1"
hg tag -l t1
hg up other
hg merge t1 --tool :other
hg revert --all -r t0   # Removes file
hg revert --all -r t0   # Adds file back
"""
