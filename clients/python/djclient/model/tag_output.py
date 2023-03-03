# coding: utf-8

"""
    DJ server

    A DataJunction metrics layer  # noqa: E501

    The version of the OpenAPI document: 0.0.post1.dev1+gd8cb070
    Generated by: https://openapi-generator.tech
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from djclient import schemas  # noqa: F401


class TagOutput(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Output tag model.
    """


    class MetaOapg:
        required = {
            "tag_type",
            "name",
            "description",
        }
        
        class properties:
            description = schemas.StrSchema
            name = schemas.StrSchema
            tag_type = schemas.StrSchema
            tag_metadata = schemas.DictSchema
            display_name = schemas.StrSchema
            __annotations__ = {
                "description": description,
                "name": name,
                "tag_type": tag_type,
                "tag_metadata": tag_metadata,
                "display_name": display_name,
            }
    
    tag_type: MetaOapg.properties.tag_type
    name: MetaOapg.properties.name
    description: MetaOapg.properties.description
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["description"]) -> MetaOapg.properties.description: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["tag_type"]) -> MetaOapg.properties.tag_type: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["tag_metadata"]) -> MetaOapg.properties.tag_metadata: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["display_name"]) -> MetaOapg.properties.display_name: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["description", "name", "tag_type", "tag_metadata", "display_name", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["description"]) -> MetaOapg.properties.description: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["tag_type"]) -> MetaOapg.properties.tag_type: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["tag_metadata"]) -> typing.Union[MetaOapg.properties.tag_metadata, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["display_name"]) -> typing.Union[MetaOapg.properties.display_name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["description", "name", "tag_type", "tag_metadata", "display_name", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        tag_type: typing.Union[MetaOapg.properties.tag_type, str, ],
        name: typing.Union[MetaOapg.properties.name, str, ],
        description: typing.Union[MetaOapg.properties.description, str, ],
        tag_metadata: typing.Union[MetaOapg.properties.tag_metadata, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        display_name: typing.Union[MetaOapg.properties.display_name, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'TagOutput':
        return super().__new__(
            cls,
            *_args,
            tag_type=tag_type,
            name=name,
            description=description,
            tag_metadata=tag_metadata,
            display_name=display_name,
            _configuration=_configuration,
            **kwargs,
        )
