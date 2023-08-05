from typing import Optional, Any, List

import hyperscan as hs

from entityscan import Rule, Entity


class MatchHandler:
    def __init__(self, data: bytes, encoding: str, entities: List[Entity]):
        self.data = data
        self.encoding = encoding
        self.entities = entities

    def __call__(
        self,
        rule_id: int,
        start: int,
        end: int,
        flags: int,
        context: Optional[Any],
    ):
        text = self.data[start:end].decode(self.encoding)
        entity = Entity.from_rule(rule_id, text, start, end)
        self.entities.append(entity)


class PatternEngine:
    def __init__(self, encoding: str = None):
        self.encoding = encoding or "UTF-8"
        self.hyperscan_db = hs.Database()
        self.patterns = []
        self.ids = []
        self.flags = []
        self.is_active = False

    def encode_pattern(self, pattern: str, skip_boundaries: bool) -> bytes:
        if not skip_boundaries:
            pattern = fr"\b{pattern}\b"
        pattern = pattern.encode(self.encoding)
        return pattern

    def add_rule(self, rule: Rule):
        pattern = self.encode_pattern(rule.pattern, rule.skip_boundaries)
        self.patterns.append(pattern)
        self.ids.append(rule.id)
        flag = hs.HS_FLAG_SOM_LEFTMOST
        if not rule.case_sensitive:
            flag |= hs.HS_FLAG_CASELESS
        self.flags.append(flag)
        self.is_active = True

    def compile(self):
        if self.is_active:
            self.hyperscan_db.compile(
                expressions=self.patterns,
                ids=self.ids,
                elements=len(self.patterns),
                flags=self.flags,
            )

    def scan(self, text: str):
        entities = []
        if self.is_active:
            data: bytes = text.encode(self.encoding)
            handler = MatchHandler(data, self.encoding, entities)
            self.hyperscan_db.scan(data, match_event_handler=handler)
        return entities
