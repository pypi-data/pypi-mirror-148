import pytest

from nlu_bf.nlu.config import RasaNLUModelConfig
from nlu_bf.nlu.training_data import load_data
from nlu_bf.nlu.train import Trainer, Interpreter
from nlu_bf.utils.tensorflow.constants import EPOCHS


@pytest.mark.parametrize(
    "pipeline",
    [
        [
            {"name": "WhitespaceTokenizer"},
            {"name": "CountVectorsFeaturizer"},
            {"name": "ResponseSelector", EPOCHS: 1},
        ]
    ],
)
def test_train_selector(pipeline, component_builder, tmpdir):
    # use data that include some responses
    td = load_data("data/examples/nlu_bf/demo-nlu_bf.md")
    td_responses = load_data("data/examples/nlu_bf/demo-nlu_bf-responses.md")
    td = td.merge(td_responses)
    td.fill_response_phrases()

    nlu_config = RasaNLUModelConfig({"language": "en", "pipeline": pipeline})

    trainer = Trainer(nlu_config)
    trainer.train(td)

    persisted_path = trainer.persist(tmpdir)

    assert trainer.pipeline

    loaded = Interpreter.load(persisted_path, component_builder)

    assert loaded.pipeline
    assert loaded.parse("hello") is not None
