"""
Tests for Resources class
"""
import pytest
from OOP.inventory.app.models.resources_class import Resources


@pytest.fixture
def resource_values():
    return {'name': 'parrot', 'manufacturer': 'Pirates A-Hoy', 'total': 100, 'allocated': 50}


@pytest.fixture
def resource(resource_values):
    return Resources(**resource_values)


def test_create_resources(resource_values, resource):
    for name_attr in resource_values:
        assert getattr(resource, name_attr) == resource_values.get(name_attr)


def test_create_invalid_total_type():
    with pytest.raises(TypeError):
        Resources('Parrot', 'Pirates A-Hoy', 10.5, 50)


def test_create_invalid_total_value():
    with pytest.raises(ValueError):
        Resources('Parrot', 'Pirates A-Hoy', -10, 50)


def test_create_invalid_allocated_type():
    with pytest.raises(TypeError):
        Resources('Parrot', 'Pirates A-Hoy', 10, 50.5)


@pytest.mark.parametrize('total,allocated', [(10, -5), (10, 20)])
def test_create_invalid_allocated_value(total, allocated):
    with pytest.raises(ValueError):
        Resources('Parrot', 'Pirates A-Hoy', total, allocated)


def test_available(resource):
    assert resource.available == resource.total - resource.allocated


def test_category(resource):
    assert resource.category == 'resources'


def test_str(resource):
    assert str(resource) == resource.name


def test_repr(resource):
    assert repr(resource) == f'name: {resource.name}, category: {resource.category},' \
                             f' manufacturer: {resource.manufacturer},' \
                             f' total: {resource._total}, allocated: {resource._allocated}'


def test_claim(resource):
    n = 2
    original_total = resource.total
    original_allocated = resource.allocated
    resource.claim(n)
    assert resource.total == original_total
    assert resource.allocated == original_allocated + n


@pytest.mark.parametrize('value', [-1, 0, 1000])
def test_claim_invalid(resource, value):
    with pytest.raises(ValueError):
        resource.claim(value)


def test_free_up(resource):
    n = 2
    original_total = resource.total
    original_allocated = resource.allocated
    resource.free_up(n)
    assert resource.allocated == original_allocated - n
    assert resource.total == original_total


@pytest.mark.parametrize('value', [-1, 0, 1000])
def test_free_up_invalid(resource, value):
    with pytest.raises(ValueError):
        resource.free_up(value)


def test_died(resource):
    n = 2
    original_total = resource.total
    original_allocated = resource.allocated
    resource.died(n)
    assert resource.allocated == original_allocated - n
    assert resource.total == original_total - n


@pytest.mark.parametrize('value', [-1, 0, 1000])
def test_died_invalid(resource, value):
    with pytest.raises(ValueError):
        resource.died(value)


def test_purchased(resource):
    n = 2
    original_total = resource.total
    original_allocated = resource.allocated
    resource.purchased(n)
    assert resource.allocated == original_allocated
    assert resource.total == original_total + n


@pytest.mark.parametrize('value', [-1, 0])
def test_purchased_invalid(resource, value):
    with pytest.raises(ValueError):
        resource.purchased(value)






