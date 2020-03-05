"""Tests for SSD class"""

import pytest
from OOP.inventory.app.models.resources_class import SSD


@pytest.fixture
def ssd_values():
    return {'name': 'Samsung 860 EVO', 'manufacturer': 'Samsung', 'total': 10, 'allocated': 3,
            'capacity_GB': 1000, 'interface': 'SATA III'}


@pytest.fixture
def ssd(ssd_values):
    return SSD(**ssd_values)


def test_create(ssd, ssd_values):
    for attr_name in ssd_values:
        assert getattr(ssd, attr_name) == ssd_values.get(attr_name)


def test_repr(ssd):
    assert ssd.category in repr(ssd)
    assert str(ssd.capacity_GB) in repr(ssd)
    assert ssd.interface in repr(ssd)
