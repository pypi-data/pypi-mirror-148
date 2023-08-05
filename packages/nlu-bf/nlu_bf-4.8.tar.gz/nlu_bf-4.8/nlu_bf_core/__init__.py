import nlu_bf.core
import sys
import warnings

# this makes sure old code can still import from `rasa_core`
# although the package has been moved to `nlu_bf.core`
sys.modules["rasa_core"] = nlu_bf.core

warnings.warn(
    "The 'rasa_core' package has been renamed. You should change "
    "your imports to use 'nlu_bf.core' instead.",
    UserWarning,
)
