import subprocess
import sys


def test_set_path_hgroot():
    HGROOT = subprocess.check_output(['hg', 'root']).strip()
    while HGROOT not in sys.path:
        sys.path.remove(HGROOT)
    import mmf_setup.set_path.hgroot
    assert HGROOT == sys.path[0]
    assert mmf_setup.HGROOT == HGROOT
    

    
