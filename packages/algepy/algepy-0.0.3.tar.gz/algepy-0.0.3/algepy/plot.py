from matplotlib import pyplot as plt
import numpy as np
from .vector import Vector
from .point import Point
from .plane import Plane


class Plot:
    """
        Plot class, uses matplotlib.
        Only supports 3d projection for now.
    """

    def __init__(self, **kwargs):
        """
            Initialize a Plot object.

            Params:
                name (str): name of the plot
                projection (str): projection of the plot. Default is 3d
                range list(float): range of the plot. Default is [0, 5]

            Returns:
                A plot class instance.

            Raises:
                ValueError if no arguments given
        """
        if kwargs is None:
            raise ValueError('No arguments given.')
        self.name = kwargs.get('name', 'Plot')
        self.projection = kwargs.get('projection', '3d')
        self.range = kwargs.get('range', [0, 5])
        self.prepare()

    def prepare(self):
        """
            Prepare the plot.

            Params:
                None

            Returns:
                None

            Raises:
                None
        """
        self.ax = plt.axes(projection=self.projection)
        self.ax.set_title(self.name)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_zlabel('z')
        self.ax.set_xlim(self.range)
        self.ax.set_ylim(self.range)
        self.ax.set_zlim(self.range)

    def add_vector(self, vector: Vector, origin: Point, color: str = 'black') -> None:
        """
            Add a vector to the plot.

            Params:
                vector (Vector): vector to add
                origin (Point): origin of the vector
                color (str): color of the vector. Default is black

            Returns:
                None

            Raises:
                TypeError if vector is not a Vector
                ValueError if dimension is not equal or not origin given
        """
        if not isinstance(vector, Vector):
            raise TypeError('vector must be a Vector')
        if not isinstance(origin, Point):
            raise TypeError('origin must be a Point')
        if self.projection == '3d' and vector.dimension != 3:
            raise ValueError('Dimension must be 3 for 3d projection')
        if not origin:
            raise ValueError('not origin given')
        self.ax.quiver(origin.x, origin.y, origin.z, vector.get(
            'x'), vector.get('y'), vector.get('z'), color=color)

    def add_point(self, point: Point, color: str = 'black') -> None:
        """
            Add a point to the plot.

            Params:
                point (Point): point to add
                color (str): color of the point. Default is black

            Returns:
                None

            Raises:
                TypeError if point is not a Point
                ValueError if dimension is not equal or not point given
        """
        if not isinstance(point, Point):
            raise TypeError('point must be a Point')
        if self.projection == '3d' and point.dimension != 3:
            raise ValueError('Dimension must be 3 for 3d projection')
        if not point:
            raise ValueError('not point given')
        self.ax.scatter(point.x, point.y, point.z, color=color)

    def add_plane(self, plane: Plane, color: str = 'black') -> None:
        """
            Add a plane to the plot.

            Params:
                plane (Plane): plane to add
                color (str): color of the plane. Default is black

            Returns:
                None

            Raises:
                TypeError if plane is not a Plane
                ValueError if dimension is not equal or not plane given
        """
        if not isinstance(plane, Plane):
            raise TypeError('plane must be a Plane')
        if not plane:
            raise ValueError('not plane given')
        # point = np.array([plane.point.x, plane.point.y, plane.point.z])
        normal = np.array(
            [plane.normal.get('x'), plane.normal.get('y'), plane.normal.get('z')])
        d = plane.d
        xx, yy = np.meshgrid(range(self.range[1]), range(self.range[1]))
        z = (-normal[0] * xx - normal[1] * yy - d) * 1. / normal[2]
        self.ax.plot_surface(xx, yy, z, color=color)

    def clear(self) -> None:
        """
            Clear the plot.

            Params:
                None

            Returns:
                None

            Raises:
                None
        """
        self.ax.clear()

    def show(self) -> None:
        """
            Show the plot.

            Params:
                None

            Returns:
                None

            Raises:
                None
        """
        plt.show()

    def save(self, path: str) -> None:
        """
            Save the plot.

            Params:
                path (str): path to save the plot

            Returns:
                None

            Raises:
                None
        """
        plt.savefig(path)
