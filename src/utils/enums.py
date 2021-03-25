from enum import Enum


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple(map(lambda format_type: (format_type.name, format_type.value), cls))
