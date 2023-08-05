import logging

from nlu_bf import version

# define the version before the other imports since these need it
__version__ = version.__version__

from nlu_bf.run import run
from nlu_bf.train import train
from nlu_bf.test import test

logging.getLogger(__name__).addHandler(logging.NullHandler())
