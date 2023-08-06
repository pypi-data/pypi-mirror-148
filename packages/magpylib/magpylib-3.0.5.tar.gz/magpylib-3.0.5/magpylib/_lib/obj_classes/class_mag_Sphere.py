"""Magnet Sphere class code"""

from magpylib._lib.obj_classes.class_BaseGeo import BaseGeo
from magpylib._lib.obj_classes.class_BaseDisplayRepr import BaseDisplayRepr
from magpylib._lib.obj_classes.class_BaseGetBH import BaseGetBH
from magpylib._lib.obj_classes.class_BaseExcitations import BaseHomMag
from magpylib._lib.config import Config
from magpylib._lib.input_checks import check_scalar_init, check_scalar_type

# init for tool tips
mx=my=mz=None

# ON INTERFACE
class Sphere(BaseGeo, BaseDisplayRepr, BaseGetBH, BaseHomMag):
    """
    Spherical magnet with homogeneous magnetization.

    Local object coordinates: The Sphere center is located in the origin of
    the local object coordinate system. Local (Sphere) and global CS coincide when
    position=(0,0,0) and orientation=unit_rotation.

    Parameters
    ----------
    magnetization: array_like, shape (3,)
        Magnetization vector (mu0*M, remanence field) in units of [mT] given in
        the local CS of the Sphere object.

    diameter: float
        Diameter of the Sphere in units of [mm].

    position: array_like, shape (3,) or (M,3), default=(0,0,0)
        Object position (local CS origin) in the global CS in units of [mm].
        For M>1, the position represents a path. The position and orientation
        parameters must always be of the same length.

    orientation: scipy Rotation object with length 1 or M, default=unit rotation
        Object orientation (local CS orientation) in the global CS. For M>1
        orientation represents different values along a path. The position and
        orientation parameters must always be of the same length.

    Returns
    -------
    Sphere object: Sphere

    Examples
    --------
    By default a Sphere is initialized at position (0,0,0), with unit rotation:

    >>> import magpylib as mag3
    >>> magnet = mag3.magnet.Sphere(magnetization=(100,100,100), diameter=1)
    >>> print(magnet.position)
    [0. 0. 0.]
    >>> print(magnet.orientation.as_quat())
    [0. 0. 0. 1.]

    Spheres are magnetic field sources. Below we compute the H-field [kA/m] of the
    above Sphere at the observer position (1,1,1),

    >>> H = magnet.getH((1,1,1))
    >>> print(H)
    [1.27622429 1.27622429 1.27622429]

    or at a set of observer positions:

    >>> H = magnet.getH([(1,1,1), (2,2,2), (3,3,3)])
    >>> print(H)
    [[1.27622429 1.27622429 1.27622429]
     [0.15952804 0.15952804 0.15952804]
     [0.04726757 0.04726757 0.04726757]]

    The same result is obtained when the Sphere object moves along a path,
    away from the observer:

    >>> magnet.move([(-1,-1,-1), (-2,-2,-2)], start=1)
    >>> H = magnet.getH((1,1,1))
    >>> print(H)
    [[1.27622429 1.27622429 1.27622429]
     [0.15952804 0.15952804 0.15952804]
     [0.04726757 0.04726757 0.04726757]]
    """

    def __init__(
            self,
            magnetization = (mx,my,mz),
            diameter = None,
            position = (0,0,0),
            orientation = None):

        # inherit base_geo class
        BaseGeo.__init__(self, position, orientation)
        BaseDisplayRepr.__init__(self)
        BaseHomMag.__init__(self, magnetization)

        # set attributes
        self.diameter = diameter
        self.object_type = 'Sphere'

    @property
    def diameter(self):
        """ Object diameter attribute getter and setter.
        """
        return self._diameter

    @diameter.setter
    def diameter(self, dia):
        """ Set Sphere diameter, float, [mm].
        """
        # input type and init check
        if Config.CHECK_INPUTS:
            check_scalar_init(dia, 'diameter')
            check_scalar_type(dia, 'diameter')

        self._diameter = float(dia)
