"""BaseGeo class code"""

from magpylib._lib.display import display

# ALL METHODS ON INTERFACE
class BaseDisplayRepr:
    """ Provides the display(self) and self.repr methods for all objects

    Properties
    ----------

    Methods
    -------
    - display(self, **kwargs)
    - repr
    """
    def __init__(self):
        self.object_type = None

    # ------------------------------------------------------------------
    # INTERFACE
    def display(
        self,
        markers=[(0,0,0)],
        axis=None,
        show_direction=False,
        show_path=True,
        size_sensors=1,
        size_direction=1,
        size_dipoles=1):
        """
        Display object graphically using matplotlib 3D plotting.

        Parameters
        ----------
        markers: array_like, shape (N,3), default=[(0,0,0)]
            Display position markers in the global CS. By default a marker is placed
            in the origin.

        axis: pyplot.axis, default=None
            Display graphical output in a given pyplot axis (must be 3D). By default a new
            pyplot figure is created and displayed.

        show_direction: bool, default=False
            Set True to show magnetization and current directions.

        show_path: bool or int, default=True
            Options True, False, positive int. By default object paths are shown. If
            show_path is a positive integer, objects will be displayed at multiple path
            positions along the path, in steps of show_path.

        size_sensor: float, default=1
            Adjust automatic display size of sensors.

        size_direction: float, default=1
            Adjust automatic display size of direction arrows.

        size_dipoles: float, default=1
            Adjust automatic display size of dipoles.

        Returns
        -------
        None: NoneType

        Examples
        --------

        Display Magpylib objects graphically using Matplotlib:

        >>> import magpylib as mag3
        >>> obj = mag3.magnet.Sphere(magnetization=(0,0,1), diameter=1)
        >>> obj.move([(.2,0,0)]*50, increment=True)
        >>> obj.rotate_from_angax(angle=[10]*50, axis='z', anchor=0, start=0, increment=True)
        >>> obj.display(show_direction=True, show_path=10)
        --> graphic output

        Display figure on your own 3D Matplotlib axis:

        >>> import matplotlib.pyplot as plt
        >>> import magpylib as mag3
        >>> my_axis = plt.axes(projection='3d')
        >>> obj = mag3.magnet.Box(magnetization=(0,0,1), dimension=(1,2,3))
        >>> obj.move([(x,0,0) for x in [0,1,2,3,4,5]])
        >>> obj.display(axis=my_axis)
        >>> plt.show()
        --> graphic output

        """
        #pylint: disable=dangerous-default-value
        display(
            self,
            markers=markers,
            axis=axis,
            show_direction=show_direction,
            show_path=show_path,
            size_direction=size_direction,
            size_sensors=size_sensors,
            size_dipoles=size_dipoles)

    # ------------------------------------------------------------------
    # INTERFACE
    def __repr__(self) -> str:
        return f'{self.object_type}(id={str(id(self))})'
