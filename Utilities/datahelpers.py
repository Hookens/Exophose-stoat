# Copyright (C) 2026 Hookens
# See the LICENSE file in the project root for details.

from datetime import datetime
from dataclasses import dataclass
from typing import Any, Generic, TypeVar, Iterable, Type

T = TypeVar("T")


class Parameter(Generic[T]):
    def __init__(
        self,
        name: str,
        value: Any,
        expected_type: Type[T],
        required: bool = False,
        min: int | None = None,
        max: int | None = None,
        match: Iterable[T] | None = None,
    ):
        self.name = name
        self.value = value
        self.expected_type = expected_type
        self.required = required
        self.min = min
        self.max = max
        self.match = match


class ExoRole:
    def __init__(self, id: str, server_id: str):
        self.id: str = id
        self.server_id = server_id


class CreatedRole(ExoRole):
    def __init__(self, id: str, server_id: str, user_id: str, created_date: datetime):
        super().__init__(id, server_id)
        self.user_id = user_id
        self.created_date = created_date


class AllowedRole(CreatedRole):
    def __init__(
        self,
        id: str,
        server_id: str,
        user_id: str,
        max_roles: int,
        allow_badges: bool,
        allow_gradients: bool,
        created_date: datetime,
        updated_user_id: str,
        updated_date: datetime,
    ):
        super().__init__(id, server_id, user_id, created_date)
        self.max_roles = max_roles
        self.allow_badges = allow_badges
        self.allow_gradients = allow_gradients
        self.updated_user_id = updated_user_id
        self.updated_date = updated_date
        self.is_everyone = id == server_id


class Bundle:
    def __init__(self, id: int, server_id: str, name: str):
        self.id = int(id)
        self.server_id = server_id
        self.name = name


class BundleRole:
    def __init__(self, bundle_id: int, id: str, server_id: str):
        self.id = id
        self.bundle_id = int(bundle_id)
        self.server_id = server_id
