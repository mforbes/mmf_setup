  $ cat <<EOF >> $HGRCPATH
  > %include $TESTDIR/hgrc
  > EOF

  $ hg init
  $ touch A
  $ hg add A
  $ hg com -m "Added A"
  $ echo "A" >> A
  $ cat <<EOF >> .hg/hgrc
  > [hooks]
  > pre-commit = false
  > EOF
  $ hg ccom -m "Modified A"
  cleaning output
  nothing changed
  no output to commit
  restoring output
  $ hg lg
  o  0:d test Added A (1970-01-01) (glob)

If the commit failed, then the modified files should still be there.
Issue #18 was that the file was removed.

  $ hg st
  M A.py
  $ cat A.py
  A

# Another possible result (if pre-commit hooks are ignored) is:
$ hg lg
@  1:d test Modified A (1970-01-01)  tip (glob)
|
o  0:d test Added A (1970-01-01) (glob)



