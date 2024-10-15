from typing import Annotated

from pydantic import BaseModel, StringConstraints, model_validator

SecretName = Annotated[str, StringConstraints(pattern=r"[a-z0-9_]+")]
"""Validator for a secret name. e.g. 'aws_access_key_id'"""

SecretKey = Annotated[str, StringConstraints(pattern=r"[a-zA-Z0-9_]+")]
"""Validator for a secret key. e.g. 'access_key_id'"""


class RegistrySecret(BaseModel):
    name: SecretName
    keys: list[SecretKey] | None = None
    optional_keys: list[SecretKey] | None = None

    @model_validator(mode="after")
    def validate_keys(cls, v):
        if v.keys is None and v.optional_keys is None:
            raise ValueError(
                "At least one of 'keys' or 'optional_keys' must be specified"
            )
        return v