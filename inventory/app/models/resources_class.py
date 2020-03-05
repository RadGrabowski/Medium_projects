"""Inventory models"""
from OOP.inventory.tests.unit.test_validators import validate_integer


class Resources:
    """Base class for resources."""

    def __init__(self, name: str, manufacturer: str, total: int, allocated: int):
        """

        Args:
            name (str): display name of resource
            manufacturer (str): resource manufacturer
            total (int): current total amount of resources
            allocated (int): current count of in-use resources

        Notes:
            'allocated' cannot exceed 'total'
        """
        self._name = name
        self._manufacturer = manufacturer

        validate_integer('total', total, 0)
        self._total = int(total)

        validate_integer('allocated', allocated, 0, total,
                         custom_max_message='Allocated inventory cannot exceed total inventory')
        print(allocated, total)
        self._allocated = int(allocated)

    @property
    def name(self):
        """
        Returns:
            str: the resource name
        """
        return self._name

    @property
    def manufacturer(self):
        """
        Returns:
            str: the resource manufacturer
        """
        return self._manufacturer

    @property
    def total(self):
        """
        Returns:
            int: the total inventory count
        """
        return self._total

    @property
    def allocated(self):
        """
        Returns:
            int: number of resources in use
        """
        return self._allocated

    @property
    def category(self):
        """
        Returns:
            str: the resource category
        """
        return self.__class__.__name__.lower()

    @property
    def available(self):
        """
        Returns:
            int: number of resources available for use
        """
        return self.total - self.allocated

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'name: {self.name}, category: {self.category}, manufacturer: {self.manufacturer},' \
               f' total: {self._total}, allocated: {self._allocated}'

    def claim(self, n: int):
        """
        Claim n inventory items (if available).
        Args:
            n (int): number of inventory items to claim
        """
        validate_integer('n', n, 1, self.available,
                         custom_max_message='Cannot claim more than available')
        self._allocated += n

    def free_up(self, n: int):
        """
        Return an inventory item to the available pool.

        Args:
            n (int): Number of items to return (cannot exceed number in use)
        """
        validate_integer('n', n, 1, self.allocated,
                         custom_max_message='Cannot return more than allocated')
        self._allocated -= n

    def died(self, n: int):
        """
        Number of items to deallocate and remove from the inventory pool altogether.

        Args:
            n (int): number of items that have died
        """
        validate_integer('n', n, 1, self.allocated,
                         custom_max_message='Cannot retire more than allocated')
        self._total -= n
        self._allocated -= n

    def purchased(self, n: int):
        """
        Add new inventory to the pool.

        Args:
            n (int): number of items to add to the pool
        """
        validate_integer('n', n, 1)
        self._total += n


class CPU(Resources):
    def __init__(self, name, manufacturer, total, allocated, cores: int, socket: str, power_watts: int):
        """

        Args:
            name (str): display name of resource
            manufacturer (str): resource manufacturer
            total (int): current total amount of resources
            allocated (int): current count of in-use resources
            cores (int): number of cores
            socket (str): CPU socket type
            power_watts (int): CPU rated wattage
        """
        super().__init__(name, manufacturer, total, allocated)

        validate_integer('cores', cores, 1)
        self._cores = cores

        self._socket = socket

        validate_integer('power_watts', power_watts, 1)
        self._power_watts = power_watts

    @property
    def cores(self):
        """
        Number of cores.
        Returns:
            int
        """
        return self._cores

    @property
    def socket(self):
        """
        The socket type for this CPU.
        Returns:
            str
        """
        return self._socket

    @property
    def power_watts(self):
        """
        The rated wattage of this CPU.
        Returns:
            int
        """
        return self._power_watts

    def __repr__(self):
        return f'{self.category}: {self.name} ({self.socket} - x{self.cores})'
    

class Storage(Resources):
    """
    A base class for storage devices - probably not used directly.
    """
    def __init__(self, name, manufacturer, total, allocated, capacity_GB):
        """
        Args:
            name (str): display name of resource
            manufacturer (str): resource manufacturer
            total (int): current total amount of resources
            allocated (int): current count of in-use resources
            capacity_GB (int): storage capacity (in GB)
        """
        super().__init__(name, manufacturer, total, allocated)
        validate_integer('capacity_GB', capacity_GB, 1)
        self._capacity_GB = capacity_GB

    @property
    def capacity_GB(self):
        """
        Indicates the capacity (in GB) of the storage device.
        Returns:
            int
        """
        return self._capacity_GB

    def __repr__(self):
        return f'{self.category}: {self.capacity_GB} GB'


class HDD(Storage):
    """
    Class used for HDD type resources
    """
    def __init__(self, name, manufacturer, total, allocated, capacity_GB, size: int, rpm: int):
        """
        Args:
            name (str): display name of resource
            manufacturer (str): resource manufacturer
            total (int): current total amount of resources
            allocated (int): current count of in-use resources
            capacity_GB (int): storage capacity (in GB)
            size (str): indicates the device size (must be either 2.5" or 3.5")
            rpm (int): disk rotation speed (in rmp)
        """
        super().__init__(name, manufacturer, total, allocated, capacity_GB)

        allowed_size = ['2.5"', '3.5"']
        if size not in allowed_size:
            raise ValueError(f'Invalid HDD size. Must be one of {", ".join(allowed_size)}')
        self._size = size

        validate_integer('rpm', rpm, 1000, 50000)
        self._rpm = rpm

    @property
    def size(self):
        """
        The HDD size (2.5" / 3.5")
        Returns:
            str
        """
        return self._size

    @property
    def rpm(self):
        """
        The HDD spin speed (rpm)
        Returns:
            int
        """
        return self._rpm

    def __repr__(self):
        s = super().__repr__()
        return f'{s} ({self.size}, {self.rpm} rpm)'


class SSD(Storage):
    """
    Class used for SSD type resources
    """
    def __init__(self, name, manufacturer, total, allocated, capacity_GB, interface):
        """
        Args:
            name (str): display name of resource
            manufacturer (str): resource manufacturer
            total (int): current total amount of resources
            allocated (int): current count of in-use resources
            capacity_GB (int): storage capacity (in GB)
            interface (str): indicates the device interface (e.g. PCIe NVMe 3.0 x4)
        """
        super().__init__(name, manufacturer, total, allocated, capacity_GB)

        self._interface = interface

    @property
    def interface(self):
        """
        Interface used by SSD (e.g. PCIe NVMe 3.0 x4)
        Returns:
            str
        """
        return self._interface

    def __repr__(self):
        s = super().__repr__()
        return f'{s} ({self.interface})'
