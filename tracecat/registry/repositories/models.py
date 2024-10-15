from pydantic import BaseModel

from tracecat.registry.actions.models import RegistryActionRead


class RegistryRepositoryRead(BaseModel):
    origin: str
    actions: list[RegistryActionRead]


class RegistryRepositoryReadMinimal(BaseModel):
    origin: str


class RegistryRepositoryCreate(BaseModel):
    origin: str


class RegistryRepositoryUpdate(BaseModel):
    name: str | None = None
    include_base: bool = True
    include_remote: bool = True
    include_templates: bool = True