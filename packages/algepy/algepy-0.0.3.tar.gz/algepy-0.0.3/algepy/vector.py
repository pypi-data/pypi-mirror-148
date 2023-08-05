import math


class Vector:
    """
        Vector class
        Supported operators:
            +: add two vectors
            -: subtract two vectors
            *: scalar multiplication
            /: scalar division
            ==: check if two vectors are equal
    """

    def __init__(self, **kwargs):
        """Initialize a vector with x, y and z coordinates.

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
            self.null()
        else:
            self.axes = ['x', 'y', 'z']
            self.dimension = kwargs.get('dimension', 3)
            self.check_axes(kwargs)

    def check_axes(self, kwargs: dict) -> None:
        """
            Check if the axes are valid.

            Params:
                kwargs: dictionary with the axes.

            Returns:
                None

            Raises:
                None
        """
        for axis in self.axes:
            if axis in kwargs:
                setattr(self, axis, kwargs[axis])
            else:
                setattr(self, axis, 0)

    def null(self) -> None:
        """
            Set all the coordinates to 0.

            Params:
                None

            Returns:
                None
        """
        for axis in self.axes[0: self.dimension]:
            setattr(self, axis, 0)

    def get(self, axis: str) -> float:
        """
            Get the value of the axis.

            Params:
                axis: axis to get the value.

            Returns:
                Value of the axis as a float.

            Raises:
                ValueError if the axis is not valid.
        """
        if axis not in self.axes:
            raise ValueError('Axis must be x, y or z')
        return getattr(self, axis)

    def magnitude(self) -> float:
        """
            Calculate the magnitude of the vector.

            Params:
                None

            Returns:
                Magnitude of the vector as a float.

            Raises:
                None
        """
        _sum = 0
        for axis in self.axes[0: self.dimension]:
            _sum += getattr(self, axis) ** 2
        return math.sqrt(_sum) if _sum > 0 else 0

    def midpoint(self) -> 'Vector':
        """
            Calculate the midpoint of the vector.

            Params:
                None

            Returns:
                Midpoint of the vector as a vector.

            Raises:
                ValueError if the vector is null.
        """
        if self.isnull():
            raise ValueError('Cannot calculate midpoint with null vector')
        return self / 2

    def opposite(self) -> 'Vector':
        """
            Return the opposite vector.

            Params:
                None

            Returns:
                A vector with the opposite coordinates of the original vector.

            Raises:
                ValueError if the vector is null.
        """
        if self.isnull():
            raise ValueError('Cannot calculate opposite with null vector')
        x, y, z = -self.get('x'), -self.get('y'), -self.get('z')
        return Vector(x=x, y=y, z=z, dimension=self.dimension)

    def isnull(self) -> bool:
        """
            Check if the vector is null.

            Params:
                None

            Returns:
                True if the vector is null, False otherwise.

            Raises:
                None
        """
        return self.magnitude() >= 0 and self.magnitude() == 0

    def direction_cosine(self, axis: str, degrees: bool = False, decimals: int = 2) -> float:
        """
            Calculate the direction cosine of the vector.

            Params:
                axis (str): axis to calculate the direction cosine.
                degrees (bool): if True, return the result in degrees.
                decimals (int): number of decimals to round the result.

            Returns:
                Direction cosine of the vector as a radian or degree.

            Raises:
                ValueError if the axis is not valid.
        """
        if axis not in self.axes:
            raise ValueError('Axis must be x, y or z')
        value = getattr(self, axis)
        radians = math.acos(value/self.magnitude())
        return math.degrees(radians).__round__(decimals) if degrees else radians

    def perpendicular(self, other: 'Vector') -> bool:
        """
            Check if the vector is perpendicular to the other vector.

            Params:
                other (Vector): other vector to check.

            Returns:
                True if the vector is perpendicular to the other vector, False otherwise.

            Raises:
                ValueError if the vector is null or the dimensions are not equal.
        """
        if self.dimension != other.dimension:
            raise ValueError('Dimensions must be equal')
        if other.isnull() or self.isnull():
            raise ValueError('Cannot calculate perpendicular with null vector')
        return self * other == 0

    def angle(self, other: 'Vector', degrees: bool = False, decimals: int = 2) -> float:
        """
            Calculate the angle between the vectors.

            Params:
                other (Vector): other vector to calculate the angle.
                degrees (bool): if True, return the result in degrees.
                decimals (int): number of decimals to round the result.

            Returns:
                Angle between the vectors as a radian or degree.

            Raises:
                ValueError if the vector is null or the dimensions are not equal.
        """
        if self.dimension != other.dimension:
            raise ValueError('Dimensions must be equal')
        if other.isnull() or self.isnull():
            raise ValueError('Cannot calculate angle with null vector')
        radians = math.acos(
            self * other / (self.magnitude() * other.magnitude()))
        return math.degrees(radians).__round__(decimals) if degrees else radians

    def projection(self, other: 'Vector') -> ['self->other', 'other->self']:
        """
            Calculate the projection of the vector on the other vector.

            Params:
                other (Vector): other vector to calculate the projection.

            Returns:
                A tuple with the projection:
                    - self->other: projection of the vector on the other vector.
                    - other->self: projection of the other vector on the vector.

            Raises:
                ValueError if the vector is null or the dimensions are not equal.
        """
        if self.dimension != other.dimension:
            raise ValueError('Dimensions must be equal')
        if other.isnull() or self.isnull():
            raise ValueError('Cannot calculate proyection with null vector')
        product_scalar = self * other
        other_magnitude = other.magnitude() ** 2
        projection_magnitude = product_scalar / other_magnitude
        projection = other * projection_magnitude
        return projection, self - projection

    def cross(self, other: 'Vector') -> 'Vector':
        """
            Calculate the cross product with the other vector.

            Params:
                other (Vector): other vector to calculate the cross product.

            Returns:
                A vector with the cross product.

            Raises:
                ValueError if the vector is null or the dimensions are not equal.
        """
        if self.dimension != other.dimension:
            raise ValueError('Dimensions must be equal')
        if other.isnull() or self.isnull():
            raise ValueError('Cannot calculate cross product with null vector')
        x = self.get('y') * other.get('z') - self.get('z') * other.get('y')
        y = self.get('x') * other.get('z') - self.get('z') * other.get('x')
        z = self.get('x') * other.get('y') - self.get('y') * other.get('x')
        return Vector(x=x, y=-y, z=z, dimension=self.dimension)

    def triple(self, other: 'Vector', third: 'Vector') -> float:
        """
            Calculate the triple product of the vectors.

            Params:
                other (Vector): other vector to calculate the triple product.
                third (Vector): third vector to calculate the triple product.

            Returns:
                Triple product of the vectors as a float.

            Raises:
                ValueError if the vector is null or the dimensions are not equal.
        """
        if self.dimension != other.dimension or self.dimension != third.dimension:
            raise ValueError('Dimensions must be equal')
        if other.isnull() or self.isnull() or third.isnull():
            raise ValueError(
                'Cannot calculate triple product with null vector')
        cross = other.cross(third)
        return self * cross

    def __eq__(self, other: 'Vector') -> bool:
        """
            Check if the vectors are equal.

            Params:
                other: other vector to check.

            Returns:
                True if the vectors are equal, False otherwise.

            Raises:
                ValueError if the dimensions are not equal.
        """
        if self.dimension != other.dimension:
            raise ValueError('Dimensions must be equal')
        for axis in self.axes[0: self.dimension]:
            if getattr(self, axis) != getattr(other, axis):
                return False
        return True

    def __str__(self) -> str:
        """
            Return the vector as a string.

            Params:
                None

            Returns:
                Vector as a string in the form of (x, y, z).

            Raises:
                None
        """
        values = '('
        for axis in self.axes[0: self.dimension]:
            values += f'{getattr(self, axis)},'
        return values[:-1] + ')'

    def __repr__(self) -> str:
        """
            Return the vector as a string.

            Params:
                None

            Returns:
                Vector as a string in the form of Vector(x, y, z).

            Raises:
                None
        """
        return f'Vector({self.get("x")}, {self.get("y")}, {self.get("z")})'

    def __add__(self, other: 'Vector') -> 'Vector':
        """
            Add two vectors.

            Params:
                other: other vector to add.

            Returns:
                A vector with the sum of the two vectors.

            Raises:
                ValueError if the dimensions are not equal.
        """
        if self.dimension != other.dimension:
            raise ValueError('Dimensions must be equal')
        vec = Vector(dimension=self.dimension)
        for axis in self.axes[0: self.dimension]:
            setattr(vec, axis, getattr(self, axis) + getattr(other, axis))
        return vec

    def __sub__(self, other: 'Vector') -> 'Vector':
        """
            Subtract two vectors.

            Params:
                other: other vector to subtract.

            Returns:
                A vector with the difference of the two vectors.

            Raises:
                ValueError if the dimensions are not equal.
        """
        if self.dimension != other.dimension:
            raise ValueError('Dimensions must be equal')
        vec = Vector(dimension=self.dimension)
        for axis in self.axes[0: self.dimension]:
            setattr(vec, axis, getattr(self, axis) - getattr(other, axis))
        return vec

    def __mul__(self, other: 'Vector' or float) -> 'Vector':
        """
            Multiply a vector by a scalar or another vector.

            Params:
                other: scalar or vector to multiply.

            Returns:
                A vector with the product of the vector and the scalar or a vector.

            Raises:
                ValueError if the dimensions are not equal.
        """
        if isinstance(other, Vector):
            if self.dimension != other.dimension:
                raise ValueError('Dimensions must be equal')
            if other.isnull() or self.isnull():
                return x
            x = self.get('x') * other.get('x')
            y = self.get('y') * other.get('y')
            z = self.get('z') * other.get('z')
            return x + y + z
        vec = Vector(dimension=self.dimension)
        for axis in self.axes[0: self.dimension]:
            setattr(vec, axis, getattr(self, axis) * other)
        return vec

    def __truediv__(self, scalar: float) -> 'Vector':
        """
            Divide a vector by a scalar.

            Params:
                scalar: scalar to divide.

            Returns:
                A vector with the division of the vector by the scalar.
        """
        vec = Vector(dimension=self.dimension)
        for axis in self.axes[0: self.dimension]:
            setattr(vec, axis, getattr(self, axis) / scalar)
        return vec
