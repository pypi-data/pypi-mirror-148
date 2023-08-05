import logging

import nlu_bf

from nlu_bf.core.train import train
from nlu_bf.core.test import test
from nlu_bf.core.visualize import visualize

logging.getLogger(__name__).addHandler(logging.NullHandler())

__version__ = nlu_bf.__version__
