from pathlib import Path
from typing import Iterable, List
from itertools import chain
import json

from pony import orm

from entityscan import (
    Connection,
    Pipeline,
    Rule,
    Doc,
    Entity,
    engines,
    timelog,
    logger,
)


class Scanner:
    def __init__(self, connection: Connection = None, encoding: str = None):
        self.connection = connection
        self.encoding = encoding or "UTF-8"
        self.patterns = engines.PatternEngine(encoding=self.encoding)
        self.composites = engines.CompositeEngine()
        self.literals = engines.LiteralEngine()

    @orm.db_session
    def load_rules(self, rules_jsonl: Path):
        assert rules_jsonl.suffix == ".jsonl", "Only supports JSONL files."
        for line in rules_jsonl.open("r"):
            line = line.strip()
            if line and line.startswith("{"):
                try:
                    kw = json.loads(line)
                    Rule(**kw)
                except json.JSONDecodeError:
                    logger.exception(f"JSON Fail: {line[:30]}...{line[-30:]}")
                    raise

    @orm.db_session
    @timelog("compile")
    def compile(self):
        for rule in Rule.select():
            if rule.is_pattern:
                self.patterns.add_rule(rule)
            elif rule.is_composite:
                self.composites.add_rule(rule)
            elif rule.is_literal:
                self.literals.add_rule(rule)
            else:
                raise ValueError(f"Invalid rule: {rule.id}")

        self.patterns.compile()
        self.literals.compile()

        return self

    @orm.db_session
    def scan_expressions(self, text: str) -> List[Entity]:
        p_entities = self.patterns.scan(text)
        l_entities = self.literals.scan(text)
        return Entity.sort_filter(chain(p_entities, l_entities))

    def scan(self, text: str, pipeline: str = None) -> List[Entity]:
        # expressions
        entities = self.scan_expressions(text=text)
        if pipeline:
            entities = Pipeline.run(pipeline, text, entities)
        entities = Entity.sort_filter(entities)

        # composites
        entities = self.composites.process(text, entities)
        entities = Entity.sort_filter(entities)
        if pipeline:
            entities = Pipeline.run(pipeline, text, entities)
            entities = Entity.sort_filter(entities)

        return entities

    def parse(self, text: str, pipeline: str = None) -> Doc:
        entities = self.scan(text=text, pipeline=pipeline)
        return Doc(text=text, entities=entities)

    def find(self, text: str, labels: Iterable[str] = None) -> List[Entity]:
        entities = self.scan(text)
        if labels:
            labels = set(labels)
            entities = [ent for ent in entities if ent.label in labels]
        return entities

    def find_one(self, text: str, labels: Iterable[str] = None):
        entities = self.find(text=text, labels=labels)
        return entities[0] if len(entities) == 1 else None
