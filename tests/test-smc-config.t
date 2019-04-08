  $ export PATH="$RUNTESTDIR/../bin/:$PATH"
  $ mmf_initial_setup --help
  Usage: mmf_initial_setup [options] dir1 dir2 ...
  
  Creates symlinks to files in the specified config directories (default "./").
  
  Options:
    -h, --help         show this help message and exit
    --home=<home>      use <home> rather than ~ for installation.(Used to
                       replace '~' in dest strings.)
    -v, --verbose      print lots of information
    -n, --no-action    don't do anything:only print commands that would be
                       executed
    -i, --interactive  prompt before taking action
    -a, --abs-path     Use absolute symlinks (defaults are relative to ~)
  
  Run from the desired config directory, and files with a second line like
  "dest = ~/.bashrc"  will be symlinked to the specified location.  If a file
  already exists, it will be backed up (copied to a file with a .bak extension).
  Existing symlinks will be overwritten.
  $ SRC="$RUNTESTDIR/../mmf_setup/_data/config_files/smc"
  $ mkdir home
  $ touch home/.bash_aliases
  $ mmf_initial_setup -n --home="./home" "${SRC}"
  backup('./home/.bash_aliases')
  os.symlink('*/config_files/smc/bash_aliases', './home/.bash_aliases') (glob)
  os.symlink('*/config_files/smc/hgignore', './home/.hgignore') (glob)
  os.symlink('*/config_files/smc/hgrc', './home/.hgrc') (glob)
  os.symlink('*/config_files/smc/inputrc', './home/.inputrc') (glob)
  $ mmf_initial_setup --home="./home" "${SRC}"
  $ ls -aF ./home
  ./
  ../
  .bash_aliases@
  .bash_aliases.bak
  .hgignore@
  .hgrc@
  .inputrc@
  $ mmf_initial_setup -v --home="./home" "${SRC}"
  Using <home> = ./home
  Using dir = */mmf_setup/_data/config_files/smc (glob)
  Symlink ./home/.bash_aliases exists.
  os.remove('./home/.bash_aliases')
  os.symlink('*/config_files/smc/bash_aliases', './home/.bash_aliases') (glob)
  Symlink ./home/.hgrc exists.
  os.remove('./home/.hgrc')
  os.symlink('*/config_files/smc/hgrc', './home/.hgrc') (glob)
  Symlink ./home/.hgignore exists.
  os.remove('./home/.hgignore')
  os.symlink('*/config_files/smc/hgignore', './home/.hgignore') (glob)
  Symlink ./home/.inputrc exists.
  os.remove('./home/.inputrc')
  os.symlink('*/config_files/smc/inputrc', './home/.inputrc') (glob)
  $ ls -aF ./home
  ./
  ../
  .bash_aliases@
  .bash_aliases.bak
  .hgignore@
  .hgrc@
  .inputrc@
