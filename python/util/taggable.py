from typing import Set, List, Optional


class Taggable:
    tags: Optional[Set[str]] = None

    def has_tag(self, tag: str):
        if not self.tags:
            self.tags = set()
        return tag in self.tags

    def add_tag(self, tag: str):
        if not self.tags:
            self.tags = set()
        self.tags.add(tag)

    def add_tags(self, tags: List[str]):
        if not self.tags:
            self.tags = set()
        for tag in tags:
            self.add_tag(tag)

    def remove_tag(self, tag: str):
        if not self.tags:
            self.tags = set()
        if tag in self.tags:
            self.tags.remove(tag)
