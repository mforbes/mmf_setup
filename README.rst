.. -*- rst -*- -*- restructuredtext -*-

.. This file should be written using the restructure text
.. conventions.  It will be displayed on the bitbucket source page and
.. serves as the documentation of the directory.

.. include:: .links.rst

Python Setup
============
This meta-project collects all of the python tools I typically use.  It also
serves as a fairly minimal example of setting up a package the |pip|_ can
install, and specifying dependencies.

Quick Start
===========
If you are impatient and courageous, here is the exceutive summary:

* Install |EPD|_, git_, and GSL_.

.. code:: bash

   pip install virtualenv
   virtualenv --system-site-packages --distribute ~/.python_environments/epd
   virtualenv --no-site-packages --distribute ~/.python_environments/clean
   virtualenv -p /usr/bin/python --system-site-packages --distribute \
              ~/.python_environments/sys

   cat >> ~/.bashrc <<EOF
   alias v.epd=". ~/.python_environments/epd/bin/activate"
   alias v.sys=". ~/.python_environments/sys/bin/activate"
   alias v.clean=". ~/.python_environments/clean/bin/activate"
   v.epd
   EOF

   pip install hg

   mkdir -p ~/src/python/git
   cd ~/src/python/git
   git clone http://github.com/gldnspud/virtualenv-pythonw-osx.git
   cd virtualenv-pythonw-osx
   python install_pythonw.py /Users/mforbes/.python_environments/epd

Then choose the set of requirements and:

.. code:: bash

   pip install -r all.txt

Requirements
============
Here is a list of the various requirements.  These are all disjoint, so you can
pick and choose.

``doc.txt`` :
   Various documentation tools like Sphinx_ and associated packages.  I use this
   for both my code documentation and for things like my website.
``emacs.txt`` :
   Various tools for setting up my development environment (I use emacs)
   including checking tools.
``debug.txt`` : 
   Debugging tools, including remote debuggers.
``profile.txt`` :
   Profiling tools for optimizing code.
``testing.txt`` :
   Testing tools including code coverage.
``vc.txt`` :
   Version control tools like mercurial and extensions
``misc.txt`` :
   Odds and ends.
``mmf.txt`` :
   My source packages for projects.  These will be installed as source
   distributions.
``all.txt`` :
   All of the above.

Here are some additional requirement files:

``EPD.txt`` :
   The list of requirements frozen from a fresh EPD_ install.
``freeze.txt`` :
   Snapshot of my system by running ``pip freeze > freeze.txt``
``bleeding-edge.txt`` :
   Installs NumPy_, SciPy_, and matplotlib_ from source.  Note: this does not
   work for some reason because |pip|_ fails to install some compiled
   libraries.  (The NumPy_ install will look fine, but SciPy_ will then fail.)
   Here is `a discussion.`__  To deal with this, first use |pip| to install this
   developmental version of NumPy_.  This will install the source.  Then go into
   the source directory and run ``python setup.py install
   --prefix=/path/to/virtualenv``.  I.e.::

      pip install --upgrade -r bleading-edge.txt
      cd ~/.python_environments/epd/src/numpy
      python setup.py install --prefix=~/.python_environments/epd

__ http://stackoverflow.com/questions/12574604/scipy-install-on-mountain-lion-failing


Details
=======
To use it do the following:

1) Install a version of python.  Many systems have a version preinstalled, so
   this step is optional.  However, if you plan to do serious development, then
   I strongly recommend installing the |EPD|_.  There is a free version, and an
   almost full featured free version for academic use: You can also pay for a
   comercial version and recieve support.  The EPD_ is very complete, and just
   works on most common platforms and I highly recommend it.  Make sure you can
   run the version of python you desire.

   If you install the EPD_, then it will typically add something like the
   following to your ``~/.bash_login`` or ``~/.profile`` files::

      # Setting PATH for EPD-7.3-2
      # The orginal version is saved in .bash_login.pysave
      PATH="/Library/Frameworks/Python.framework/Versions/Current/bin:${PATH}"
      export PATH
      
      MKL_NUM_THREADS=1
      export MKL_NUM_THREADS

   (If you want to use a multithreaded version of ``numpy``, you will need to
   change the value of ``MKL_NUM_THREADS``.  See `this discussion`__.)

__ http://stackoverflow.com/q/5260068/1088938

2) Create a virtualenv_.  This will allow you to install new packages in a
   controlled manner that will not mess with the system version (or the EPD_
   version).  You can create multiple virtual environments for different
   projects or associated with different versions of python.  Again, this is
   highly recommended.  There are several ways of doing this. 

   .. note:: Methods 1) and 2) will install virtualenv_ to the location 
      specified by the current version of python.  This means that you might
      need root access, and it will slightly "muck up" you pristine system
      install. This is generally not a problem, but if it bothers you see step
      3).

   1) If you have |pip|_ (the new python packageing system), then you can use it
      to install virtualenv_ as follows::

         pip install virtualenv
   
   2) If you do not have |pip|_, you might have ``easy_install``::
   
         easy_install virtualenv

   3) If you do not want to muck up your system version of python at all, then
      you can simply download the file |virtualenv.py|_.  In the commands that
      follow, replace ``virtualenv`` with ``python virtualenv.py``.

3) Setup a virtual environment for your work.  You can have many differen
   environments, so you will need to choose a meaningful name.  I use "epd" for
   the EPD_ version of python, "sys" for the system version of python, and
   "clean" for a version using EPD_ but without the site-packages::

       virtualenv --system-site-packages --distribute ~/.python_environments/epd
       virtualenv --no-site-packages --distribute ~/.python_environments/clean
       virtualenv -p /usr/bin/python --system-site-packages --distribute \
                  ~/.python_environments/sys

   Once this virtualenv_ is activated, install packages with pip_ will place all
   of the installed files in the ``~/.python_environments/epd`` directory.  (You
   can change this to any convenient location).  The ``--system-site-packages``
   option allows the virtualenv_ access to the system libraries (in my case, all
   of the EPD_ goodies).  If you want to test a system for deployment, making
   sure that it does not have any external dependencies, then you would use the
   ``--no-site-packages`` option instead.  Run ``virtualenv --help`` for more
   information.

4) Add some aliases to help you activate virtualenv_ sessions.  I include the
   following in my ``.bashrc`` file::

      # Some virtualenv related macros
      alias v.epd=". ~/.python_environments/epd/bin/activate"
      alias v.sys=". ~/.python_environments/sys/bin/activate"
      alias v.clean=". ~/.python_environments/clean/bin/activate"
      v.epd

   You can activate your chosen environment with one of the commands ``v.epd``,
   ``v.clean``, or ``v.sys``.  The default activation script will insert "(epd)"
   etc. to your prompt::

      ~ mforbes$ v.epd
      (epd)~ mforbes$ v.sys
      (sys)~ mforbes$ deactivate
      ~ mforbes$

   To get out of the environments, just type ``deactivate`` as shown above.
   
   .. note:: If you have an older version of IPython_ (pre 0.13), then you may
      need to call ``ipython`` from a `function like this`__::

         # Remap ipython if VIRTUAL_ENV is defined
         function ipython {
           if [ -n "${VIRTUAL_ENV}" -a -x "${VIRTUAL_ENV}/bin/python" ]; then
             START_IPYTHON='\
               import sys; \
               from IPython.frontend.terminal.ipapp import launch_new_instance;\
               sys.exit(launch_new_instance())'
              "${VIRTUAL_ENV}/bin/python" -c "${START_IPYTHON}" "$@"
            else
              command ipython "$*"
            fi
         }


      This deals with issues that IPython_ was not virtualenv_ aware.  The
      recommended solution is still to install IPython_ in the virtualenv_ using
      ``pip install ipython``, but then you will need one in each environment.
      As of IPython_ 0.13, this support is included. (See `this PR`__.)

      If you have not used IPython_ before, then you should have a look.  It has
      some fantastic features like ``%paste`` and the `IPython notebook`_
      interface.

__ http://igotgenes.blogspot.fr/2010/01/interactive-sandboxes-using-ipython.html
__ https://github.com/ipython/ipython/pull/1388/

5) Install mercurial_.  You may already have this (try ``hg --version``).  If
   not, either install a native distribution (which might have some GUI tools)
   or install with::

      pip install hg

6) Install git_.  This may not be as easy, but some packages are only available
   from github_.

7) On Mac OS X you may need to install ``pythonw`` for some GUI applications
   (like RunSnakeRun_).  You an do this using `this solution`__::
   
      mkdir -p ~/src/python/git
      cd ~/src/python/git
      git clone http://github.com/gldnspud/virtualenv-pythonw-osx.git
      cd virtualenv-pythonw-osx
      python install_pythonw.py /Users/mforbes/.python_environments/epd

   You will have to do this in each virtualenv_ you want to use the GUI apps
   from.

__ https://github.com/gldnspud/virtualenv-pythonw-osx

8) Non-python prerequisites.  These need to be installed outside of the python
   environment for some of the required libraries to work.

   * GSL_: This is needed for pygsl_.


9) Install various requirements as follows::

      pip install -r requirements/all.txt


Using |pip|_
============
Here are some notes about using |pip|_ that I did not find obvious.

Version Control
---------------
It is clear from the `documentation about requirements`__ that you can specify
version controlled repositories with |pip|_, however, the exact syntax for
specifying revisions etc. is not so clear.  Examining `the source`__ shows that
you can specify revisions, tags, etc. as follows::

   # Get the "tip"
   hg+http://bitbucket.org/mforbes/pymmf#egg=pymmf

   # Get the revision with tag "v1.0" or at the tip of branch "v1.0"
   hg+https://bitbucket.org/mforbes/pymmf@v1.0#egg=pymmf

   # Get the specified revision exactly
   hg+https://bitbucket.org/mforbes/pymmf@633be89a#egg=pymmf

What appears after the "@" sign is any valid revision (for mercurial see ``hg
help revision`` for various options).  Unfortunately, I see no way of specifying
something like ">=1.1", or ">=633be89a" (i.e. a descendent of a particular
revision).  (See `issue 782`__)

__ http://www.pip-installer.org/en/latest/requirements.html
__ https://github.com/pypa/pip/blob/develop/pip/vcs/mercurial.py
__ https://github.com/pypa/pip/issues/728

Using the MKL
=============
The EPD_ is build using the Intel MKL_.  Here are some instructions on how to
compile your own version of `NumPy and SciPy with the MKL`__.

__ http://software.intel.com/en-us/articles/numpyscipy-with-intel-mkl

* Checkout the source code::

     pip install --no-install -e git+http://github.com/numpy/numpy#egg=numpy-dev
     pip install --no-install -e git+http://github.com/scipy/scipy#egg=scipy-dev

* Setup the environment to use the `Intel compilers`_::

     . /usr/local/bin/intel64.sh
     . /opt/intel/Compiler/11.1/069/mkl/tools/environment/mklvarsem64t.sh

* Edit the ``site.cfg`` file in the NumPy_ source directory.  I am not sure
  exactly which libraries to include. See these discussions:

     * http://software.intel.com/en-us/articles/numpyscipy-with-intel-mkl
     * Check the ``site.cfg`` in your EPD_ installation.

  .. code::

     cd ~/.python_environments/epd/src/numpy
     cp site.cfg.example site.cfg
     vi site.cfg

  Here is what I used::

     [mkl]
     library_dirs = /opt/intel/Compiler/11.1/069/mkl/lib/em64t/
     include_dirs = /opt/intel/Compiler/11.1/069/mkl/include
     lapack_libs = mkl_lapack95_lp64
     mkl_libs = mkl_def, mkl_intel_lp64, mkl_intel_thread, mkl_core, mkl_mc

  I also needed to modify ``numpy/distutils/intelccompiler.py`` as follows::

          cc_args = "-fPIC"
          def __init__ (self, verbose=0, dry_run=0, force=0):
              UnixCCompiler.__init__ (self, verbose,dry_run, force)
     -        self.cc_exe = 'icc -m64 -fPIC'
     +        self.cc_exe = 'icc -O3 -g -openmp -m64 -fPIC'
              compiler = self.cc_exe
              self.set_executables(compiler=compiler,
                                   compiler_so=compiler,

* Build both NumPy_ and SciPy_ with the following::

     cd ~/.python_environments/epd/src/numpy
     python setup.py config --compiler=intelem --fcompiler=intelem\
                 build_clib --compiler=intelem --fcompiler=intelem\
                 build_ext --compiler=intelem --fcompiler=intelem\
                 install
     cd ~/.python_environments/epd/src/scipy

* Run and check the build configuration::

     $ python -c "import numpy;print numpy.__file__;print numpy.show_config()"
     /phys/users/mforbes/.python_environments/epd/lib/python2.7/site-packages/numpy/__init__.pyc
     lapack_opt_info:
         libraries = ['mkl_lapack95_lp64', 'mkl_def', 'mkl_intel_lp64', 'mkl_intel_thread', 'mkl_core', 'mkl_mc', 'pthread']
         library_dirs = ['/opt/intel/Compiler/11.1/069/mkl/lib/em64t/']
         define_macros = [('SCIPY_MKL_H', None)]
         include_dirs = ['/opt/intel/Compiler/11.1/069/mkl/include']
     blas_opt_info:
         libraries = ['mkl_def', 'mkl_intel_lp64', 'mkl_intel_thread', 'mkl_core', 'mkl_mc', 'pthread']
         library_dirs = ['/opt/intel/Compiler/11.1/069/mkl/lib/em64t/']
         define_macros = [('SCIPY_MKL_H', None)]
         include_dirs = ['/opt/intel/Compiler/11.1/069/mkl/include']
     lapack_mkl_info:
         libraries = ['mkl_lapack95_lp64', 'mkl_def', 'mkl_intel_lp64', 'mkl_intel_thread', 'mkl_core', 'mkl_mc', 'pthread']
         library_dirs = ['/opt/intel/Compiler/11.1/069/mkl/lib/em64t/']
         define_macros = [('SCIPY_MKL_H', None)]
         include_dirs = ['/opt/intel/Compiler/11.1/069/mkl/include']
     blas_mkl_info:
         libraries = ['mkl_def', 'mkl_intel_lp64', 'mkl_intel_thread', 'mkl_core', 'mkl_mc', 'pthread']
         library_dirs = ['/opt/intel/Compiler/11.1/069/mkl/lib/em64t/']
         define_macros = [('SCIPY_MKL_H', None)]
         include_dirs = ['/opt/intel/Compiler/11.1/069/mkl/include']
     mkl_info:
         libraries = ['mkl_def', 'mkl_intel_lp64', 'mkl_intel_thread', 'mkl_core', 'mkl_mc', 'pthread']
         library_dirs = ['/opt/intel/Compiler/11.1/069/mkl/lib/em64t/']
         define_macros = [('SCIPY_MKL_H', None)]
         include_dirs = ['/opt/intel/Compiler/11.1/069/mkl/include']
     None

  .. note:: You will need to setup the environment to run with the MKL_
     libraries.  The EPD_ avoids this by distributing the libraries.  I suggest
     that you add the following to the activation script::

        cat >> ~/.python_environments/epd/bin/activate <<EOF
        
        # This adds the MKL libraries to the path for use with my custom numpy
        # and scipy builds.
        . /usr/local/bin/intel64.sh
        . /opt/intel/Compiler/11.1/069/mkl/tools/environment/mklvarsem64t.sh
        EOF


See also:

  * http://math.nju.edu.cn/help/mathhpc/doc/intel/mkl/mklgs_lnx.htm
  * http://blog.sun.tc/2010/11/numpy-and-scipy-with-intel-mkl-on-linux.html
  * http://www.scipy.org/Installing_SciPy/Linux

    This suggests maybe using the runtime libraries instead (just ``mkl_libs =
    mkl_rt``).  I have not yet tried this.

  * http://cournape.github.com/Bento/
  
    It looks like it might be easier to use Bento_ rather than distutils
