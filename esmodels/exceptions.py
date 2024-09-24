"""Exceptions for esmodels."""

from collections.abc import Sequence


class ESMException(Exception):
    pass


class VarNotInModel(ESMException):

    def __init__(self, name: str, synonyms: None | str | Sequence[str] = None):
        self.name = name
        self.synonyms = synonyms

    def __str__(self):
        msg = f"The variable {self.name} "
        if self.synonyms is not None:
            msg += "nor its synonyms {self.synonyms} "
        msg += " are present in this model."
        return msg


class ParsingError(ESMException):

    def __init__(self, model: str, name: str, expression: str):
        self.model = model
        self.name = name
        self.expression = expression

    def __str__(self):
        msg = f"Error parsing expression: model={self.model} variable={self.name} expression='{self.expression}'"
        return msg
