from enum import Enum


class Lifecycle(Enum):
    BETA = "beta"
    PRODUCTION = "production"
    DEPRECATED = "deprecated"
    DISCONTINUED = "discontinued"


class Impact(Enum):
    PROFIT = "profit"
    CUSTOMERS = "customers"
    EMPLOYEES = "employees"


class SentryIssueCategory(Enum):
    STALE = "stale"
    DECAYING = "decaying"
    SPOILED = "spoiled"
    FRESH = "fresh"


class EnviromentType(Enum):
    GITLAB = "gitlab"
    ZOO = "zoo"
