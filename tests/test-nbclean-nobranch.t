  $ cat <<EOF >> $HGRCPATH
  > [ui]
  > username = test
  > slash = True
  > interactive = False
  > mergemarkers = detailed
  > promptecho = True
  > [extensions]
  > graphlog =
  > mmf_setup.nbclean = $MMF_SETUP/nbclean.py
  > strip =
  > [alias]
  > lga = glog --style=${MMF_SETUP}/_data/hgthemes/map-cmdline.lg -l20
  > [nbclean]
  > output_branch =
  > [defaults]
  > commit = -d "0 0"
  > ccommit = -d "0 0"
  > shelve = --date "0 0"
  > tag = -d "0 0"
  > glog = --template '{rev}: {author} {desc|strip|firstline} ({date|shortdate}) {branches} {boorkmarks} {tags}\n'
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
  cleaning N.ipynb
  A N.ipynb
  restoring output
  $ hg ccom -m '0'
  cleaning output
  cleaning N.ipynb
  created new head
  no output to commit
  restoring output
  $ hg cst
  cleaning output
  restoring output
  $ hg glog
  @  0: test 0 (1970-01-01)   tip
  

  $ cp ${TESTDIR}/_data/n1_clean.ipynb N.ipynb
  $ hg cst
  cleaning output
  cleaning N.ipynb
  M N.ipynb
  restoring output
  $ hg ccom -m '1'
  cleaning output
  cleaning N.ipynb
  created new head
  no output to commit
  restoring output
  $ hg glog
  @  1: test 1 (1970-01-01)   tip
  |
  o  0: test 0 (1970-01-01)
  

  $ cp ${TESTDIR}/_data/n1_dirty.ipynb N.ipynb
  $ hg st
  M N.ipynb
  $ hg cst
  cleaning output
  cleaning N.ipynb
  restoring output
  $ hg cdiff
  cleaning output
  cleaning N.ipynb
  restoring output
  $ hg st
  M N.ipynb

One can try to commit the dirty notebook.  Nothing has changed, but
the automatic output commit will appear.

  $ hg ccom -m '1'
  cleaning output
  cleaning N.ipynb
  nothing changed
  no output to commit
  restoring output
  $ hg glog
  o  2: test ...: Automatic commit with .ipynb output (*)   tip (glob)
  |
  @  1: test 1 (1970-01-01)
  |
  o  0: test 0 (1970-01-01)
  

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
  cleaning N.ipynb
  M N.ipynb
  restoring output
  $ hg cdiff
  cleaning output
  cleaning N.ipynb
  diff -r * N.ipynb (glob)
  --- a/N.ipynb	Thu Jan 01 00:00:00 1970 +0000
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
  cleaning N.ipynb
  created new head
  no output to commit
  restoring output

Update to a previous clean revision and check that things work.  This
was the source of failure for issue #2

  $ hg up -C 1
  1 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ hg cst
  cleaning output
  restoring output
  $ hg glog
  o  5: test ...: Automatic commit with .ipynb output (*)   tip (glob)
  |
  o  4: test 4: N2 (1970-01-01)
  |
  o  3: test 3: N1 (1970-01-01)
  |
  | o  2: test ...: Automatic commit with .ipynb output (*) (glob)
  |/
  @  1: test 1 (1970-01-01)
  |
  o  0: test 0 (1970-01-01)
  

Now update to revision 4 with the output from 5.

  $ hg update 4
  2 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg st
  $ hg cst
  cleaning output
  restoring output
  $ hg glog
  o  5: test ...: Automatic commit with .ipynb output (*)   tip (glob)
  |
  @  4: test 4: N2 (1970-01-01)
  |
  o  3: test 3: N1 (1970-01-01)
  |
  | o  2: test ...: Automatic commit with .ipynb output (*) (glob)
  |/
  o  1: test 1 (1970-01-01)
  |
  o  0: test 0 (1970-01-01)
  


  $ hg cupdate 4
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updating notebook outputs
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg st
  M N.ipynb
  $ hg diff -r 5
  $ hg cst
  cleaning output
  cleaning N.ipynb
  restoring output
  $ hg glog
  o  5: test ...: Automatic commit with .ipynb output (*)   tip (glob)
  |
  @  4: test 4: N2 (1970-01-01)
  |
  o  3: test 3: N1 (1970-01-01)
  |
  | o  2: test ...: Automatic commit with .ipynb output (*) (glob)
  |/
  o  1: test 1 (1970-01-01)
  |
  o  0: test 0 (1970-01-01)
  
