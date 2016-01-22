  $ cat <<EOF >> $HGRCPATH
  > [extensions]
  > mmf_setup.nbclean = $MMF_SETUP/nbclean.py
  > strip =
  > [nbclean]
  > output_branch =
  > [defaults]
  > ccommit = -d "0 0"
  > 
  > %include $MMF_SETUP/_data/hgrc
  > EOF

Test that nothing happens with a clean and completely empty repository:

  $ hg init
  $ hg cst
  cleaning output
  restoring output
  $ hg cdiff
  cleaning output
  restoring output
  $ hg ccom
  cleaning output
  nothing changed
  no output to commit
  restoring output


Now do a more comprehensive test:

  $ cp ${TESTDIR}/_data/n0_clean.ipynb N.ipynb
  $ hg cst
  cleaning output
  ? N.ipynb
  restoring output
  $ hg add N.ipynb
  $ hg cst
  cleaning output
  A N.ipynb
  restoring output
  $ hg ccom -m '0'
  cleaning output
  created new head
  no output to commit
  restoring output
  $ hg cst
  cleaning output
  restoring output
  $ hg lg
  @  0:d test 0 (1970-01-01)  tip
  

  $ cp ${TESTDIR}/_data/n1_clean.ipynb N.ipynb
  $ hg cst
  cleaning output
  M N.ipynb
  restoring output
  $ hg ccom -m '1'
  cleaning output
  created new head
  no output to commit
  restoring output
  $ hg lg
  @  1:d test 1 (1970-01-01)  tip
  |
  o  0:d test 0 (1970-01-01)
  

  $ cp ${TESTDIR}/_data/n1_dirty.ipynb N.ipynb
  $ hg st
  M N.ipynb
  $ hg cst
  cleaning output
  restoring output
  $ hg cdiff
  cleaning output
  restoring output
  $ hg st
  M N.ipynb
One can try to commit the dirty notebook.  Nothing hasmchanged, but
the automatic output commit will appear.

  $ hg ccom -m '1'
  cleaning output
  nothing changed
  automatic commit of output
  restoring output
  $ hg lg
  o  2:d test ...: Automatic commit with .ipynb output (* ago)  tip (glob)
  |
  @  1:d test 1 (1970-01-01)
  |
  o  0:d test 0 (1970-01-01)
  


  $ cp ${TESTDIR}/_data/n2_dirty.ipynb N.ipynb

Commit a dirty notebook

  $ cp ${TESTDIR}/_data/n1_dirty.ipynb N1.ipynb
  $ hg add N1.ipynb
  $ hg com N1.ipynb -m '3: N1'
  created new head
  $ hg st
  M N.ipynb
  $ hg cst
  cleaning output
  M N.ipynb
  restoring output
  $ hg cdiff
  cleaning output
  diff -r * N.ipynb (glob)
  --- a/N.ipynb	* (glob)
  +++ b/N.ipynb	* (glob)
  @@ -17,6 +17,17 @@
      "source": [
       "1+1"
      ]
  +  },
  +  {
  +   "cell_type": "code",
  +   "execution_count": null,
  +   "metadata": {
  +    "collapsed": false
  +   },
  +   "outputs": [],
  +   "source": [
  +    "2+2"
  +   ]
     }
    ],
    "metadata": {
  restoring output
  $ hg ccom -m '4: N2'
  cleaning output
  created new head
  automatic commit of output
  restoring output

Update to a previous clean revision and check that things work.  This
was the source of failure for issue #2

  $ hg up -C 1
  1 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ hg cst
  cleaning output
  restoring output
  $ hg lg
  o  5:d test ...: Automatic commit with .ipynb output (* ago)  tip (glob)
  |
  o  4:d test 4: N2 (1970-01-01)
  |
  o  3:d test 3: N1 (1970-01-01)
  |
  | o  2:d test ...: Automatic commit with .ipynb output (* ago) (glob)
  |/
  @  1:d test 1 (1970-01-01)
  |
  o  0:d test 0 (1970-01-01)
  
