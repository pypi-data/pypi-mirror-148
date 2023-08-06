__all__ = [
    'CreateProviderOptionData', 'CreateProviderOptionSchema',
    'ProviderData', 'ProviderSchema', 'ProviderListData', 'ProviderListSchema',
    'ProviderCredentialData', 'ProviderCredentialSchema',
    'CreateDocumentOptionData', 'CreateDocumentOptionSchema',
    'UpdateDocumentOptionData', 'UpdateDocumentOptionSchema',
    'DocumentData', 'DocumentSchema'
]

from dataclasses import dataclass, field
from typing import Optional, List

import marshmallow_dataclass

from .users import UserData


@dataclass
class CreateProviderOptionData:
    name: str = field()
    type: str = field()
    credentials: str = field()


@dataclass
class ProviderData:
    id: str = field()
    name: str = field()
    type: str = field()


@dataclass
class ProviderListData:
    length: int = field()
    page: int = field()
    pages: int = field()
    items: List[ProviderData] = field(default_factory=list)


@dataclass
class ProviderCredentialData:
    id: str = field()
    name: str = field()
    type: str = field()
    salt: str = field()
    credentials: str = field()


@dataclass
class CreateDocumentOptionData:
    name: str = field()


@dataclass
class UpdateDocumentOptionData:
    name: str = field()


@dataclass
class DocumentData(UpdateDocumentOptionData):
    id: str = field()
    name: str = field()

    owner: Optional[UserData] = field()


CreateProviderOptionSchema = marshmallow_dataclass.class_schema(CreateProviderOptionData)()
ProviderSchema = marshmallow_dataclass.class_schema(ProviderData)()
ProviderListSchema = marshmallow_dataclass.class_schema(ProviderListData)()
ProviderCredentialSchema = marshmallow_dataclass.class_schema(ProviderCredentialData)()

CreateDocumentOptionSchema = marshmallow_dataclass.class_schema(CreateDocumentOptionData)()
UpdateDocumentOptionSchema = marshmallow_dataclass.class_schema(UpdateDocumentOptionData)()
DocumentSchema = marshmallow_dataclass.class_schema(DocumentData)()
