from dataclasses import dataclass

@dataclass
class EventItem:
    event_id: int
    title: str
    description: str
    article_ids: list[int]

@dataclass
class EventResult:
    case_id: int
    events: list[EventItem]