import json
from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property
from typing import List, Iterable, Optional

from entityscan import Rule, get_rule


class MetaDict:
    def __init__(self, data: dict):
        self._data = data or {}

    def __getattr__(self, key):
        return self._data.get(key)


@dataclass
class Entity:
    text: str
    label: str
    start: int = 0
    end: int = 0
    name: Optional[str] = None
    synonyms: Optional[List[str]] = None
    entities: Optional[List["Entity"]] = None
    meta: Optional[dict] = None

    def __lt__(self, other: "Entity"):
        return self._sort_key < other._sort_key

    def __hash__(self):
        return hash((self.text, self.label, self.start, self.end))

    def iter_descendents(self):
        for entity in self.entities or []:
            yield entity
            yield from entity.iter_descendents()

    def dict(self, keep_null=False):
        data = dict(
            (k, v)
            for k, v in vars(self).items()
            if keep_null or (v is not None) and k[0] != "_"
        )
        if self.entities:
            data["entities"] = [
                e.dict(keep_null=keep_null) for e in self.entities
            ]
        return data

    def json(self, indent=4):
        return json.dumps(self.dict(), indent=indent)

    @cached_property
    def _m(self):
        return MetaDict(self.meta or {})
    
    @cached_property
    def _is_synonym(self):
        return self.text.lower() != self.name.lower()

    @cached_property
    def _sort_key(self):
        # +start, -end, -sub entity count, -is_synonym
        end_desc = -1 * self.end
        sub_desc = -1 * len(self.entities or [])
        is_synonym = any(e._is_synonym for e in (self.entities or []))
        is_synonym = is_synonym or self._is_synonym
        return self.start, end_desc, sub_desc, is_synonym

    @classmethod
    def from_rule(cls, rule_id: int, text: str, start: int, end: int):
        rule: Rule = get_rule(rule_id)
        groups = rule.get_groups(text)
        meta = {**(rule.meta or {}), **(groups or {})} or None

        return cls(
            label=rule.label,
            text=text,
            start=start,
            end=end,
            meta=meta,
            name=rule.name or text,
            synonyms=rule.synonyms,
        )

    @classmethod
    def sort_filter(cls, entities: Iterable["Entity"]) -> List["Entity"]:
        """
        Sorting is based on Entity._sort_key

        Filtering follows the following logic:
            - Composites cause sub-entities to be removed
            - Entities of the same label that overlap goes to the longer
        """

        entities = sorted(entities)
        max_end = defaultdict(int)
        filtered = []

        for entity in entities:
            if max_end[entity.label] < entity.end:
                max_end[entity.label] = max(max_end[entity.label], entity.end)

                for child in entity.iter_descendents():
                    max_end[child.label] = max(max_end[child.label], child.end)

                filtered.append(entity)

        return filtered

    @classmethod
    def collapse_meta(cls, entities: List["Entity"]):
        meta = defaultdict(list)

        for entity in entities:
            prefix = entity.label.lower()
            meta[prefix].append(entity.name)
            for k, v in (entity.meta or {}).items():
                meta[f"{prefix}_{k}"].append(v)

        return dict((k, v[0] if len(v) == 1 else v) for k, v in meta.items())


@dataclass
class Doc:
    text: str
    entities: Optional[List["Entity"]] = None
