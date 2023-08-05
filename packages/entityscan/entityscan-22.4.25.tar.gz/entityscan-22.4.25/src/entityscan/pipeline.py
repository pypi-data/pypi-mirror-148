from typing import List, Dict, Iterable

from entityscan import Entity


class PipelineStep:

    each_labels = {}

    def __call__(self, text: str, entities: Iterable[Entity]):
        entities = self.process_all(text, entities)
        for entity in entities:
            if entity.label in self.each_labels:
                yield from self.process_each(text, entity)
            else:
                yield entity

    # noinspection PyMethodMayBeStatic
    def process_all(self, text: str, entities: Iterable[Entity]):
        yield from entities

    # noinspection PyMethodMayBeStatic
    def process_each(self, text: str, entity: Entity):
        yield entity


class Pipeline:

    __pipelines: Dict[str, List[PipelineStep]] = None

    @classmethod
    def get_pipeline_steps(cls, name: str) -> Iterable[PipelineStep]:
        if Pipeline.__pipelines is None:
            Pipeline.__pipelines = {}
            for subclass in cls.__subclasses__():
                kw = vars(subclass)
                name = kw.get("name")
                if name:
                    Pipeline.__pipelines[name] = [
                        val
                        for val in kw.values()
                        if isinstance(val, PipelineStep)
                    ]

        return Pipeline.__pipelines.get(name, [])

    @classmethod
    def run(cls, pipeline_name: str, text: str, entities: List[Entity]):
        steps = Pipeline.get_pipeline_steps(pipeline_name)
        for step in steps:
            entities = step(text, entities)
        return entities
