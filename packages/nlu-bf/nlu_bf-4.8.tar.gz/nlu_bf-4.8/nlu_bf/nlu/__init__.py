import logging

import nlu_bf
from nlu_bf.nlu.train import train
from nlu_bf.nlu.test import run_evaluation as test
from nlu_bf.nlu.test import cross_validate
from nlu_bf.nlu.training_data import load_data

logging.getLogger(__name__).addHandler(logging.NullHandler())

__version__ = nlu_bf.__version__
