from dataclasses import dataclass

@dataclass
class Article:
    id: int
    cluster_id: int
    title: str
    content: str

@dataclass
class Cluster:
    id: int
    is_relevant: bool = None

