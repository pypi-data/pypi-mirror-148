from .vector import Vector


class Point:
    """
        Point class
        Supported operators:
            +: add two points
            ==: check if two points are equal
    """

    def __init__(self, **kwargs):
        """
            Initialize a Point object.

            Params:
                x: x coordinate
                y: y coordinate
                z: z coordinate
                dimension: dimension of the vector. Default is 3

            Returns:
                A vector class instance.

            Raises:
                None
        """
        if kwargs is None:
            raise ValueError('No arguments given.')
        self.x = kwargs.get('x', 0)
        self.y = kwargs.get('y', 0)
        self.z = kwargs.get('z', 0)
        self.dimension = kwargs.get('dimension', 3)

    def midpoint(self, other: 'Point') -> 'Vector':
        """
            Calculate the midpoint between two points.

            Params:
                other: another point

            Returns:
                A vector class instance.

            Raises:
                None
        """

        if not isinstance(other, Point):
            raise TypeError('other must be a Point')
        if self.dimension != other.dimension:
            raise ValueError('Dimensions must be equal')
        x = (self.x + other.x) / 2
        y = (self.y + other.y) / 2
        z = (self.z + other.z) / 2
        return Vector(x=x, y=y, z=z)

    def find_vector(self, other: 'Point') -> Vector:
        """
            Calculate the vector between two points.

            Params:
                other (Point): another point

            Returns:
                A vector class instance.

            Raises:
                TypeError if other is not a Point
                ValueError if dimensions are not equal
        """
        if not isinstance(other, Point):
            raise TypeError('other must be a Point')
        if self.dimension != other.dimension:
            raise ValueError('Dimensions must be equal')
        return Vector(x=other.x - self.x, y=other.y - self.y, z=other.z - self.z)

    def __str__(self) -> str:
        """
            Return a string representation of the point.
        """
        return f'({self.x}, {self.y}, {self.z})'

    def __repr__(self) -> str:
        """
            Return a string representation of the point.
        """
        return f'Point({self.x}, {self.y}, {self.z})'

    def __eq__(self, other: 'Point') -> bool:
        """
            Check if two points are equal.

            Params:
                other (Point): another point

            Returns:
                True if points are equal, False otherwise.

            Raises:
                TypeError if other is not a Point
                ValueError if dimensions are not equal
        """
        if not isinstance(other, Point):
            raise TypeError('other must be a Point')
        if self.dimension != other.dimension:
            raise ValueError('Dimensions must be equal')
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __add__(self, other: 'Point') -> Vector:
        """
            Add two points.

            Params:
                other (Point): another point

            Returns:
                A vector class instance.

            Raises:
                TypeError if other is not a Point
                ValueError if dimensions are not equal
        """
        if not isinstance(other, Point):
            raise TypeError('other must be a Point')
        if self.dimension != other.dimension:
            raise ValueError('Dimensions must be equal')
        return Vector(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z)
