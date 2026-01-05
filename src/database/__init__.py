from enum import Enum

class ArticleFilter(Enum):
    ANY = 'any'
    ENCODED = 'encoded'
    NON_ENCODED = 'non-encoded'