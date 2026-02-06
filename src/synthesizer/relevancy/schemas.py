from dataclasses import dataclass

@dataclass
class RelevancyInput:
    query: str
    document: str

@dataclass
class RelevancyResult:
    is_relevant: bool

