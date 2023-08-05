from .vector import Vector
from .point import Point


class Plane:
    """
        Plane class
    """

    def __init__(self, **kwargs):
        """Initialize a plane with normal vector and a point on the plane.

            Params:
                normal (Vector): normal vector of the plane
                point (Point): point on the plane

            Returns:
                A plane class instance.

            Raises:
                ValueError if no arguments given
        """
        if kwargs is None:
            raise ValueError('No arguments given.')
        self.normal = kwargs.get('normal', Vector(x=0, y=0, z=0))
        self.point = kwargs.get('point', Point(x=0, y=0, z=0))
        self.a = self.normal.get('x')
        self.b = self.normal.get('y')
        self.c = self.normal.get('z')
        self.d = self.find_d(self.point)

    def find_d(self, point: Point) -> float:
        """
            Calculate the d value of the plane.

            Params:
                point (Point): point on the plane

            Returns:
                A float value of the d value.

            Raises:
                TypeError if point is not a Point
        """
        if not isinstance(point, Point):
            raise TypeError('point must be a Point')
        _sum = self.a * point.x + self.b * point.y + self.c * point.z
        d = -_sum
        return d

    def find_intersection(self, axis: str) -> Point:
        """
            Find the intersection of the plane with the given axis.

            Params:
                axis (str): axis of the plane

            Returns:
                A point on the plane.

            Raises:
                ValueError if axis is not 'x', 'y', or 'z'
        """
        if not axis in ['x', 'y', 'z']:
            raise ValueError('axis must be x, y, or z')
        d = self.find_d(self.point)
        v = -d / self.normal.get(axis)
        x_ = y_ = z_ = 0
        if axis == 'x':
            x_ = v
        if axis == 'y':
            y_ = v
        if axis == 'z':
            z_ = v
        return Point(x=x_, y=y_, z=z_)

    def symmetric_equation(self, **kwargs) -> str:
        """
            Return the symmetric equation of the plane.

            Params:
                point (Point): point on the plane
                decimals (int): number of decimals to round to
                fraction (bool): whether to return a fraction or not

            Returns:
                A string representation of the symmetric equation.

            Raises:
                TypeError if point is not a Point
                ValueError d must not be 0
        """
        point = kwargs.get('point', None)
        decimals = kwargs.get('decimals', 2)
        fraction = kwargs.get('fraction', False)
        if point and not isinstance(point, Point):
            raise TypeError('point must be a Point')
        d = -(self.find_d(point) if point else self.d)
        if d == 0:
            raise ValueError('d must not be 0')
        if fraction:
            return f'{self.a}x/{d} {self.b}y/{d} {self.c}z/{d} = 1'
        p = (self.a/-d).__round__(decimals)
        q = (self.b/-d).__round__(decimals)
        r = (self.c/-d).__round__(decimals)
        return f'x/{p} y/{q} z/{r} = 1'

    def __str__(self):
        """
            Return a string representation of the plane.

            Params:
                None

            Returns:
                A string representation of the plane.

            Raises:
                None
        """
        return f'π: {self.a}x {self.b}y {self.c}z {self.d} = 0'
