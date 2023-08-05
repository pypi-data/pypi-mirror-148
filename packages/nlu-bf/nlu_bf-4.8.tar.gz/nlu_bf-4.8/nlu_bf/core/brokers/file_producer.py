from nlu_bf.constants import DOCS_URL_EVENT_BROKERS
from nlu_bf.core.brokers.file import FileEventBroker
from nlu_bf.utils.common import raise_warning


class FileProducer(FileEventBroker):
    raise_warning(
        "The `FileProducer` class is deprecated, please inherit from "
        "`FileEventBroker` instead. `FileProducer` will be removed in "
        "future Rasa versions.",
        FutureWarning,
        docs=DOCS_URL_EVENT_BROKERS,
    )
