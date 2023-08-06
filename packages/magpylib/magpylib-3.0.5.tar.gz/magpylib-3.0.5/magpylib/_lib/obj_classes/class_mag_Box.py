"""Magnet Box class code"""

import numpy as np
from magpylib._lib.obj_classes.class_BaseGeo import BaseGeo
from magpylib._lib.obj_classes.class_BaseDisplayRepr import BaseDisplayRepr
from magpylib._lib.obj_classes.class_BaseGetBH import BaseGetBH
from magpylib._lib.obj_classes.class_BaseExcitations import BaseHomMag
from magpylib._lib.config import Config
from magpylib._lib.input_checks import check_vector_format, check_vector_init, check_vector_type

# init for tool tips
a=b=c=None
mx=my=mz=None

# ON INTERFACE
class Box(BaseGeo, BaseDisplayRepr, BaseGetBH, BaseHomMag):
    """
    Cuboid magnet with homogeneous magnetization.

    Local object coordinates: The geometric center of the Box is located
    in the origin of the local object coordinate system. Box sides are
    parallel to the local basis vectors. Local (Box) and global CS coincide when
    position=(0,0,0) and orientation=unit_rotation.

    Parameters
    ----------
    magnetization: array_like, shape (3,)
        Magnetization vector (mu0*M, remanence field) in units of [mT] given in
        the local CS of the Box object.

    dimension: array_like, shape (3,)
        Dimension/Size of the Box with sides [a,b,c] in units of [mm].

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
    Box object: Box

    Examples
    --------
    By default a Box is initialized at position (0,0,0), with unit rotation:

    >>> import magpylib as mag3
    >>> magnet = mag3.magnet.Box(magnetization=(100,100,100), dimension=(1,1,1))
    >>> print(magnet.position)
    [0. 0. 0.]
    >>> print(magnet.orientation.as_quat())
    [0. 0. 0. 1.]

    Boxs are magnetic field sources. Below we compute the H-field [kA/m] of the above Box at the
    observer position (1,1,1),

    >>> H = magnet.getH((1,1,1))
    >>> print(H)
    [2.4844679 2.4844679 2.4844679]

    or at a set of observer positions:

    >>> H = magnet.getH([(1,1,1), (2,2,2), (3,3,3)])
    >>> print(H)
    [[2.4844679  2.4844679  2.4844679 ]
     [0.30499798 0.30499798 0.30499798]
     [0.0902928  0.0902928  0.0902928 ]]

    The same result is obtained when the Box moves along a path,
    away from the observer:

    >>> magnet.move([(-1,-1,-1), (-2,-2,-2)], start=1)
    >>> H = magnet.getH((1,1,1))
    >>> print(H)
    [[2.4844679  2.4844679  2.4844679 ]
     [0.30499798 0.30499798 0.30499798]
     [0.0902928  0.0902928  0.0902928 ]]
    """

    def __init__(
            self,
            magnetization = (mx,my,mz),
            dimension = (a,b,c),
            position = (0,0,0),
            orientation = None):

        # inherit
        BaseGeo.__init__(self, position, orientation)
        BaseDisplayRepr.__init__(self)
        BaseHomMag.__init__(self, magnetization)

        # set attributes
        self.dimension = dimension
        self.object_type = 'Box'


    # properties ----------------------------------------------------

    @property
    def dimension(self):
        """ Object dimension attribute getter and setter.
        """
        return self._dimension

    @dimension.setter
    def dimension(self, dim):
        """ Set Box dimension (a,b,c), shape (3,), [mm].
        """
        # input type and init check
        if Config.CHECK_INPUTS:
            check_vector_type(dim, 'dimension')
            check_vector_init(dim, 'dimension')

        # input type -> ndarray
        dim = np.array(dim,dtype=float)

        # input format check
        if Config.CHECK_INPUTS:
            check_vector_format(dim, (3,), 'dimension')

        self._dimension = dim
