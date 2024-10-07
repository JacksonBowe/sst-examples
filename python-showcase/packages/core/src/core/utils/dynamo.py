from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar, Self

from aws_lambda_powertools.utilities.parser import BaseModel
from core.utils import collapse_dict


class SimpleEntity(BaseModel, ABC):
    """
    An entity with only a Hash key
    """

    _primary_index_keys: ClassVar[list] = ["PK"]
    _raw_item: dict = None

    class Config:
        populate_by_name = True

    @property
    @abstractmethod
    def PK(self):
        """
        This is an abstract property that must be implemented by any subclass.
        """
        pass

    def _update_attribute(self, current_object, attribute_parts, value):
        """
        Helper method to recursively update an attribute with a given value.

        Args:
            current_object: Current object being processed.
            attribute_parts (list): List of attribute parts (nested keys).
            value: New value for the attribute.
        """
        if len(attribute_parts) == 1:
            # Reached the final part of the attribute, set the value
            if isinstance(current_object, dict):
                # If the current object is a dictionary, set the value using dict[key] syntax
                current_object[attribute_parts[0]] = value
            elif isinstance(current_object, BaseModel):
                # Otherwise, use setattr for class instances
                setattr(current_object, attribute_parts[0], value)
            else:
                raise Exception(f"Unsupported update type: {current_object}")
        else:
            # Move deeper into the nested structure
            nested_object = getattr(current_object, attribute_parts[0], None)

            if nested_object is None:
                # Create a new nested object if it doesn't exist
                nested_object = {}
                setattr(current_object, attribute_parts[0], nested_object)

            # Recursively update the nested attribute
            self._update_attribute(nested_object, attribute_parts[1:], value)

    def update(self, values):
        """
        Update attributes with values from the given dictionary.

        Args:
            values (dict): Dictionary of attribute values.
        """
        values = collapse_dict(values)
        for key, value in values.items():
            attribute_parts = key.split(".")
            # Start the recursive update from the current instance
            self._update_attribute(self, attribute_parts, value)

    def serialize(self) -> dict:
        raw = self.model_dump(exclude_none=True)
        [raw.update({key: getattr(self, key) for key in self._primary_index_keys})]
        return raw

    @classmethod
    def deserialize(cls, data: dict) -> Self:
        raw_item = data.copy()
        [data.pop(key) for key in cls._primary_index_keys]
        entity = cls(**data)
        entity._raw_item = raw_item
        return entity


class CompositeEntity(SimpleEntity):
    """
    An entity with both Hash and Sort keys
    """

    _primary_index_keys: ClassVar[list] = ["PK", "SK"]

    @property
    @abstractmethod
    def SK(self):
        """
        This is an abstract property that must be implemented by any subclass.
        """
        pass
