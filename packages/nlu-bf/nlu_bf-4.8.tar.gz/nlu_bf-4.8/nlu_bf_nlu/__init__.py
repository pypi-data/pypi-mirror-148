import nlu_bf.nlu
import sys
import warnings

# this makes sure old code can still import from `rasa_nlu`
# although the package has been moved to `nlu_bf.nlu`
sys.modules["rasa_nlu"] = nlu_bf.nlu

warnings.warn(
    "The 'rasa_nlu' package has been renamed. You should change "
    "your imports to use 'nlu_bf.nlu' instead.",
    UserWarning,
)
