from .main import *

# PEP0440 compatible formatted version, see:
# https://www.python.org/dev/peps/pep-0440/
#
# Generic release markers:
#   X.Y
#   X.Y.Z   # For bugfix releases

import pkg_resources

__version__ = pkg_resources.get_distribution('pip').version
