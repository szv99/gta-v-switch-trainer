"""Static vehicle catalog and validation helpers."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Mapping

_CATALOG_PATH = Path(__file__).with_name("vehicles.json")
SUPPORTED_CATEGORIES = frozenset(
    {"compact", "muscle", "motorcycle", "off-road", "sports", "super", "suv"}
)
_ID_PATTERN = re.compile(r"^vehicle\.[a-z0-9]+(?:-[a-z0-9]+)*$")
_RUNTIME_STATUSES = frozenset({"tested", "unconfirmed"})


class CatalogError(ValueError):
    """Raised when a vehicle catalog is missing or violates its schema."""


def validate_catalog(catalog: Mapping[str, Any]) -> None:
    """Validate a decoded catalog, raising :class:`CatalogError` on bad data."""
    if not isinstance(catalog, Mapping):
        raise CatalogError("catalog must be an object")
    if catalog.get("schema_version") != 1:
        raise CatalogError("schema_version must be 1")
    vehicles = catalog.get("vehicles")
    if not isinstance(vehicles, list) or not vehicles:
        raise CatalogError("vehicles must be a non-empty array")

    names: set[str] = set()
    ids: set[str] = set()
    for index, vehicle in enumerate(vehicles):
        if not isinstance(vehicle, Mapping):
            raise CatalogError(f"vehicles[{index}] must be an object")
        for field in ("id", "name", "label", "category", "runtime"):
            if field not in vehicle:
                raise CatalogError(f"vehicles[{index}] missing {field}")
        vehicle_id, name, label, category = (
            vehicle["id"], vehicle["name"], vehicle["label"], vehicle["category"]
        )
        if not isinstance(vehicle_id, str) or not _ID_PATTERN.fullmatch(vehicle_id):
            raise CatalogError(f"vehicles[{index}].id is not a stable id")
        if vehicle_id in ids:
            raise CatalogError(f"duplicate vehicle id: {vehicle_id}")
        ids.add(vehicle_id)
        if not isinstance(name, str) or not name or name != name.lower():
            raise CatalogError(f"vehicles[{index}].name must be canonical lowercase")
        if name in names:
            raise CatalogError(f"duplicate vehicle name: {name}")
        names.add(name)
        if not isinstance(label, str) or not label.strip():
            raise CatalogError(f"vehicles[{index}].label must be non-empty")
        if category not in SUPPORTED_CATEGORIES:
            raise CatalogError(f"unsupported vehicle category: {category}")
        runtime = vehicle["runtime"]
        if not isinstance(runtime, Mapping) or runtime.get("availability") not in _RUNTIME_STATUSES:
            raise CatalogError(
                f"vehicles[{index}].runtime.availability must be tested or unconfirmed"
            )
        # IDs deliberately remain explicit data, so renaming a display/model field
        # cannot silently change an integration key.


def load_catalog(path: str | Path | None = None) -> dict[str, Any]:
    """Load and validate the static catalog; return its decoded mapping."""
    source = Path(path) if path is not None else _CATALOG_PATH
    try:
        with source.open(encoding="utf-8") as handle:
            catalog = json.load(handle)
    except (OSError, json.JSONDecodeError) as error:
        raise CatalogError(f"could not read catalog {source}: {error}") from error
    validate_catalog(catalog)
    return catalog


__all__ = ["CatalogError", "SUPPORTED_CATEGORIES", "load_catalog", "validate_catalog"]
