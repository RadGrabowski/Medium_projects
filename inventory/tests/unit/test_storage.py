"""Tests for Storage class."""

import pytest
from OOP.inventory.app.models.resources_class import Storage


@pytest.fixture
def storage_values():
    return {'name': 'Thumbdrive', 'manufacturer': 'Sandisk', 'total': 10, 'allocated': 3, 'capacity_GB': 512}


@pytest.fixture
def storage(storage_values):
    return Storage(**storage_values)


def test_create(storage_values, storage):
    for attr_name in storage_values:
        assert getattr(storage, attr_name) == storage_values.get(attr_name)


@pytest.mark.parametrize('gb, exception', [(10.5, TypeError), (-1, ValueError), (0, ValueError)])
def test_create_invalid_storage(gb, exception, storage_values):
    storage_values['capacity_GB'] = gb
    with pytest.raises(exception):
        Storage(**storage_values)


def test_repr(storage):
    assert storage.category in repr(storage)
    assert str(storage.capacity_GB) in repr(storage)