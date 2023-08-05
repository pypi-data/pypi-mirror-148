from itertools import chain
from typing import Generator

from dawg import BytesDAWG

from entityscan import Rule, Entity


class LiteralDAWG:
    def __init__(self, case_sensitive: bool):
        self.case_sensitive = case_sensitive
        self.data = []
        self.dawg = None

    def normalize(self, term: str):
        return term.lower() if not self.case_sensitive else term

    def add_data(self, term: str, rule_id: int):
        norm = self.normalize(term)
        bytes_id = rule_id.to_bytes(8, "little", signed=False)
        self.data.append((norm, bytes_id))

    def compile(self):
        self.dawg = BytesDAWG(self.data)

    def is_prefix(self, term: str):
        norm = self.normalize(term)
        for _ in self.dawg.iterkeys(norm):
            return True
        return False

    def iter_entities(
        self,
        term: str,
        start: int = None,
        end: int = None,
    ) -> Generator[Entity, None, None]:
        norm = self.normalize(term)
        for bytes_id in self.dawg.get(norm) or []:
            bytes_id = bytes_id[:-1]  # DAWG appending '>' to ints?
            rule_id = int.from_bytes(bytes_id, "little", signed=False)
            start = start or 0
            end = end or len(term)
            yield Entity.from_rule(rule_id, term, start, end)

    def scan(self, text: str) -> Generator[Entity, None, None]:
        last = 0
        curr = 0
        prefixes = []
        for right in chain(text, "\0"):
            if not right.isalnum():
                next_prefixes = []
                for left in chain([last], prefixes):
                    term = text[left:curr]

                    yield from self.iter_entities(term, left, curr)

                    if self.is_prefix(term):
                        next_prefixes.append(left)

                prefixes = next_prefixes
                curr += 1
                last = curr

            else:
                curr += 1


class LiteralEngine:
    def __init__(self):
        self.dawgs = {
            True: LiteralDAWG(case_sensitive=True),
            False: LiteralDAWG(case_sensitive=False),
        }

    def add_rule(self, rule: Rule):
        dawg = self.dawgs.get(bool(rule.case_sensitive))

        dawg.add_data(rule.name, rule.id)
        for synonym in rule.synonyms or []:
            dawg.add_data(synonym, rule.id)

    def compile(self):
        for dawg in self.dawgs.values():
            dawg.compile()

    def scan(self, text: str) -> Generator[Entity, None, None]:
        for dawg in self.dawgs.values():
            yield from dawg.scan(text)
