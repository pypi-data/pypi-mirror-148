import logging
import typing
from typing import Dict, Text

from nlu_bf.cli.utils import print_warning
from nlu_bf.constants import DOCS_BASE_URL
from nlu_bf.core.lock_store import LockStore

logger = logging.getLogger(__name__)

if typing.TYPE_CHECKING:
    from nlu_bf.core.agent import Agent


def run(
    model: Text,
    endpoints: Text,
    connector: Text = None,
    credentials: Text = None,
    **kwargs: Dict,
):
    """Runs a Rasa model.

    Args:
        model: Path to model archive.
        endpoints: Path to endpoints file.
        connector: Connector which should be use (overwrites `credentials`
        field).
        credentials: Path to channel credentials file.
        **kwargs: Additional arguments which are passed to
        `nlu_bf.core.run.serve_application`.

    """
    import nlu_bf.core.run
    import nlu_bf.nlu.run
    from nlu_bf.core.utils import AvailableEndpoints
    import nlu_bf.utils.common as utils

    _endpoints = AvailableEndpoints.read_endpoints(endpoints)

    if not connector and not credentials:
        connector = "rest"
        print_warning(
            "No chat connector configured, falling back to the "
            "REST input channel. To connect your bot to another channel, "
            "read the docs here: {}/user-guide/"
            "messaging-and-voice-channels".format(DOCS_BASE_URL)
        )

    kwargs = utils.minimal_kwargs(kwargs, nlu_bf.core.run.serve_application)
    nlu_bf.core.run.serve_application(
        model,
        channel=connector,
        credentials=credentials,
        endpoints=_endpoints,
        **kwargs,
    )


def create_agent(model: Text, endpoints: Text = None) -> "Agent":
    from nlu_bf.core.tracker_store import TrackerStore
    from nlu_bf.core.utils import AvailableEndpoints
    from nlu_bf.core.agent import Agent
    from nlu_bf.core.brokers.broker import EventBroker

    _endpoints = AvailableEndpoints.read_endpoints(endpoints)

    _broker = EventBroker.create(_endpoints.event_broker)
    _tracker_store = TrackerStore.create(_endpoints.tracker_store, event_broker=_broker)
    _lock_store = LockStore.create(_endpoints.lock_store)

    return Agent.load(
        model,
        generator=_endpoints.nlg,
        tracker_store=_tracker_store,
        lock_store=_lock_store,
        action_endpoint=_endpoints.action,
    )
