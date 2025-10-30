from enum import Enum
from typing import Any

from pydantic import BaseModel


class ExternalStageReference(BaseModel):
    name: str
    properties: dict[str, Any] | None = None


class StageReference(BaseModel):
    id: str | None = None
    name: str
    external: ExternalStageReference | None = None
    filter: str | None = None


class Action(BaseModel):
    name: str = "unknown"
    filter: str | None = None


class SetAction(Action):
    name: str = "set"
    set: dict[str, str | list[str]]


class DeleteAction(Action):
    name: str = "delete"
    delete: list[str]


class TranslateAction(Action):
    name: str = "translate"
    dictionary: dict[Any, Any]
    mapping: dict[str, str]
    fallback: Any | None = None


class Stage(BaseModel):
    description: str | None = None
    actions: list[SetAction | DeleteAction | TranslateAction]


class IntakeFormat(BaseModel):
    name: str
    pipeline: list[StageReference]
    stages: dict[str, Stage]


class CustomFieldType(str, Enum):
    KEYWORD = "keyword"
    BOOLEAN = "boolean"
    LONG = "long"
    INT = "int"
    FLOAT = "float"
    ARRAY = "array"
    DICT = "dict"
    IP = "ip"
    NUMBER = "number"
    OBJECT = "object"

    TEXT = "text"
    KEYWORDS = "keywords"
    DATE = "date"
    STRING = "string"
    LIST = "list"
    GEO_POINT = "geo_point"
    TRACKER = "tracker"
    BOOL = "bool"
    INTEGER = "integer"
    SHORT = "short"
    DATETIME = "datetime"
    DATE_NANOS = "date_nanos"


class CustomField(BaseModel):
    name: str
    description: str
    type: CustomFieldType
    observable: dict[str, str] | None = None


class SmartDescriptionCondition(BaseModel):
    field: str
    value: str | int | bool | None = None


class SmartDescriptionRelationship(BaseModel):
    source: str
    target: str
    type: str


class SmartDescription(BaseModel):
    value: str
    relationships: list[SmartDescriptionRelationship] | None = None
    conditions: list[SmartDescriptionCondition]


class TestFile(BaseModel):
    input: dict[str, Any]
    expected: dict[str, Any]


class ValidationError(BaseModel):
    message: str
    code: str
    file_path: str
    error: str | None = None

    def __dict__(self) -> dict[str, Any]:
        return self.model_dump(exclude_none=True, exclude_unset=True)

    def __str__(self) -> str:
        representation = [
            self.message,
            f"code=`{self.code}`",
        ]
        if self.file_path:
            representation.append(f"file_path=`{self.file_path}`")
        if self.error:
            representation.append(f"error=`{self.error}`")
        return " ".join(representation)


class CheckResult(BaseModel):
    name: str
    description: str
    warnings: list[str] = []
    errors: list[ValidationError] = []
    options: dict[str, Any] = dict()
