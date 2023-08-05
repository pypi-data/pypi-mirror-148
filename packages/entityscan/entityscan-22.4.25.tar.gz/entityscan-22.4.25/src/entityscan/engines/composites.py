import re
from collections import defaultdict
from functools import reduce
from string import punctuation
from typing import Iterable, List, Optional, Dict

from entityscan import Rule, Entity

# https://stackoverflow.com/a/64303618
Trie = lambda: defaultdict(Trie)


class CompositeFinder:
    def __init__(self, engine: "CompositeEngine", text: str, entities: list):
        self.engine = engine
        self.text = text
        self.entities = entities
        self.composites = []
        self.curr_prefixes = []
        self.next_prefixes = []

    def find(self):
        for this in self.entities:
            if self.engine.is_prefix((this,)):
                self.next_prefixes.append((this,))

            for prefix in self.curr_prefixes:
                t_start, p_end = this.start, prefix[-1].end

                # span clean is without the punctuation
                span_exact = self.text[slice(p_end, t_start)]
                span_clean = span_exact.strip(punctuation)
                span_exact = span_exact.strip()
                span_clean = span_clean.strip()

                dist = len(span_clean)

                if dist <= self.engine.max_dist:
                    self.next_prefixes.append(prefix)

                    self.process_prefix(prefix, span_exact, this)
                    if span_exact and (span_clean != span_exact):
                        self.process_prefix(prefix, span_clean, this)

            self.curr_prefixes = self.next_prefixes
            self.next_prefixes = []

        for prefix in self.curr_prefixes:
            for trail, label in self.engine.get_trail_text(prefix).items():
                last_end = prefix[-1].end
                if trail == self.text[slice(last_end, last_end + len(trail))]:
                    self.push_composite(label, prefix + (trail,))

            # handle singleton composites
            label = self.engine.get_end(prefix)
            if label:
                self.push_composite(label, prefix)

        return self.composites

    def process_prefix(self, prefix: tuple, span: str, this: dict):
        if span:
            prefix += (span,)

        prefix += (this,)

        if self.engine.is_prefix(prefix):
            self.next_prefixes.append(prefix)

        label = self.engine.get_end(prefix)
        if label:
            self.push_composite(label, prefix)

    def push_composite(self, label, prefix):
        entities = [item for item in prefix if isinstance(item, Entity)]
        start, end = entities[0].start, entities[-1].end

        if isinstance(prefix[-1], str):
            end += len(prefix[-1])

        text = self.text[start:end]
        meta = Entity.collapse_meta(entities)
        composite = Entity(
            text=text,
            label=label,
            start=start,
            end=end,
            name=text,
            meta=meta,
            entities=entities,
        )
        self.composites.append(composite)


class CompositeEngine:

    # trie helpers

    END = object()

    def __init__(self):
        self.trie = Trie()
        self.max_dist = 1

    def __contains__(self, item):
        return item in self.trie

    def __getitem__(self, part: str):
        return self.trie.get(part)

    def __setitem__(self, parts: tuple, label):
        parts = [p.label if isinstance(p, Entity) else p for p in parts]
        val = reduce(dict.__getitem__, parts, self.trie)
        val[self.END] = label

    def is_prefix(self, parts: tuple):
        val = self.reduce(parts)
        prefix_keys = val and (val.keys() - {self.END})
        return len(prefix_keys or []) > 0

    def get_end(self, parts: tuple) -> Optional[str]:
        val = self.reduce(parts)
        return val and val.get(self.END)

    def get_trail_text(self, parts: tuple) -> Dict[str, str]:
        val = self.reduce(parts)
        prefix_keys = val and (val.keys() - {self.END})
        trails = {}
        for key in prefix_keys:
            label = val.get(key, {}).get(self.END)
            if label:
                trails[key] = label
        return trails

    def reduce(self, parts: tuple):
        parts = [p.label if isinstance(p, Entity) else p for p in parts]

        trie = self.trie
        for part in parts:
            # need to check first, because getting creates
            if part in trie:
                trie = trie.get(part)

            # if invalid, return None
            else:
                return None

        return trie

    # add composite pattern

    def add_rule(self, rule: Rule):
        parts, this_max_dist = self.to_parts(
            rule.pattern, rule.ignore_punctuation
        )
        self[parts] = rule.label
        self.max_dist = max(self.max_dist, this_max_dist)

    re_labels = re.compile(r"(@[A-Z_]+)")
    re_punctuation = re.compile(r"")

    @classmethod
    def to_parts(cls, pattern: str, ignore_punctuation: bool) -> tuple:
        parts = []
        prev = None
        max_dist = 0
        pattern = pattern.strip()

        for match in cls.re_labels.finditer(pattern):
            # remove leading @
            label = match.group()[1:]

            # current
            curr = dict(start=match.start(), end=match.end(), label=label)

            # if not first
            if prev:
                span = pattern[prev["end"] : curr["start"]]
                max_dist = max(max_dist, len(span))
                if span and ignore_punctuation:
                    span = span.strip(punctuation)
                span = span.strip()
                if span:
                    parts.append(span)

            parts.append(curr["label"])
            prev = curr

        if prev:
            span = pattern[prev["end"] :]
            max_dist = max(max_dist, len(span))
            if span and ignore_punctuation:
                span = span.strip(punctuation)
            span = span.strip()
            if span:
                parts.append(span)

        return tuple(parts), max_dist

    # scan

    def process(self, text: str, entities: Iterable) -> List[Entity]:
        keep_going = True

        while keep_going:
            keep_going = False
            entities = Entity.sort_filter(entities)
            composites = CompositeFinder(self, text, entities).find()

            if composites:
                entities = self.filter_sub_entities(composites, entities)
                keep_going = True

        return entities

    @classmethod
    def filter_sub_entities(cls, composites, entities):
        next_entities = []
        composites = Entity.sort_filter(composites)
        seen_offsets = set()

        for composite in composites:
            off = set(range(composite.start, composite.end + 1))

            if seen_offsets.isdisjoint(off):
                seen_offsets.update(off)
                next_entities.append(composite)

        for entity in entities:
            if entity.start not in seen_offsets:
                next_entities.append(entity)

        return next_entities

    @classmethod
    def to_pattern(cls, text: str, entities: List[Entity]):
        """Helper function to generate pattern from text and entities."""
        if entities:
            last = -1
            pattern = ""
            for entity in entities:
                if entity.start > last:
                    pattern += text[max(0, last):entity.start]
                    pattern += f"@{entity.label}"
                    last = entity.end
            pattern += text[last:]
            return pattern
