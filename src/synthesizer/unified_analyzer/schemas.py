from dataclasses import dataclass

@dataclass
class EventItem:
    event_id: int
    title: str
    description: str
    article_ids: list[int]

@dataclass
class AnalysisResult:
    is_relevant: bool
    name: str
    categories: list[str]
    events: list[EventItem]