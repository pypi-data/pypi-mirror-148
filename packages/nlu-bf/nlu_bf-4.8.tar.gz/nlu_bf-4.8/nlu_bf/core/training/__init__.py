import typing
from typing import Text, List, Optional, Union

if typing.TYPE_CHECKING:
    from nlu_bf.core.domain import Domain
    from nlu_bf.core.interpreter import NaturalLanguageInterpreter
    from nlu_bf.core.trackers import DialogueStateTracker
    from nlu_bf.core.training.structures import StoryGraph
    from nlu_bf.importers.importer import TrainingDataImporter


async def extract_story_graph(
    resource_name: Text,
    domain: "Domain",
    interpreter: Optional["NaturalLanguageInterpreter"] = None,
    use_e2e: bool = False,
    exclusion_percentage: int = None,
) -> "StoryGraph":
    from nlu_bf.core.interpreter import RegexInterpreter
    from nlu_bf.core.training.dsl import StoryFileReader
    from nlu_bf.core.training.structures import StoryGraph

    if not interpreter:
        interpreter = RegexInterpreter()
    story_steps = await StoryFileReader.read_from_folder(
        resource_name,
        domain,
        interpreter,
        use_e2e=use_e2e,
        exclusion_percentage=exclusion_percentage,
    )
    return StoryGraph(story_steps)


async def load_data(
    resource_name: Union[Text, "TrainingDataImporter"],
    domain: "Domain",
    remove_duplicates: bool = True,
    unique_last_num_states: Optional[int] = None,
    augmentation_factor: int = 50,
    tracker_limit: Optional[int] = None,
    use_story_concatenation: bool = True,
    debug_plots=False,
    exclusion_percentage: int = None,
) -> List["DialogueStateTracker"]:
    from nlu_bf.core.training.generator import TrainingDataGenerator
    from nlu_bf.importers.importer import TrainingDataImporter

    if resource_name:
        if isinstance(resource_name, TrainingDataImporter):
            graph = await resource_name.get_stories(
                exclusion_percentage=exclusion_percentage
            )
        else:
            graph = await extract_story_graph(
                resource_name, domain, exclusion_percentage=exclusion_percentage
            )

        g = TrainingDataGenerator(
            graph,
            domain,
            remove_duplicates,
            unique_last_num_states,
            augmentation_factor,
            tracker_limit,
            use_story_concatenation,
            debug_plots,
        )
        return g.generate()
    else:
        return []


def persist_data(trackers: List["DialogueStateTracker"], path: Text) -> None:
    """Dump a list of dialogue trackers in the story format to disk."""

    for t in trackers:
        t.export_stories_to_file(path)
