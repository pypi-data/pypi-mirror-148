from magpylib._lib.fields.field_wrap_BH_level2 import getBH_level2


# ON INTERFACE
def getB(sources, observers, sumup=False, squeeze=True, **specs):
    """
    Compute B-field in [mT] for given sources and observers.

    Parameters
    ----------
    sources: source object, Collection or 1D list thereof
        Sources can be a single source object, a Collection or a 1D list of L source
        objects and/or collections.

    observers: array_like or Sensor or 1D list thereof
        Observers can be array_like positions of shape (N1, N2, ..., 3) where the field
        should be evaluated, can be a Sensor object with pixel shape (N1, N2, ..., 3) or
        a 1D list of K Sensor objects with similar pixel shape. All positions are given
        in units of [mm].

    sumup: bool, default=False
        If True, the fields of all sources are summed up.

    squeeze: bool, default=True
        If True, the output is squeezed, i.e. all axes of length 1 in the output (e.g. only
        a single sensor or only a single source) are eliminated.

    Returns
    -------
    B-field: ndarray, shape squeeze(L, M, K, N1, N2, ..., 3)
        B-field of each source (L) at each path position (M) for each sensor (K) and each
        sensor pixel position (N1,N2,...) in units of [mT]. Sensor pixel positions are
        equivalent to simple observer positions. Paths of objects that are shorter than
        M will be considered as static beyond their end.

    Notes
    -----
    This function automatically joins all sensor and position inputs together and groups
    similar sources for optimal vectorization of the computation. For maximal performance
    call this function as little as possible and avoid using it in loops.

    Examples
    --------

    Compute the B-field of a spherical magnet at a sensor positioned at (1,2,3):

    >>> import magpylib as mag3
    >>> source = mag3.magnet.Sphere(magnetization=(1000,0,0), diameter=1)
    >>> sensor = mag3.Sensor(position=(1,2,3))
    >>> B = mag3.getB(source, sensor)
    >>> print(B)
    [-0.62497314  0.34089444  0.51134166]

    Compute the B-field of a spherical magnet at five path positions as seen
    by an observer at position (1,2,3):

    >>> import magpylib as mag3
    >>> source = mag3.magnet.Sphere(magnetization=(1000,0,0), diameter=1)
    >>> source.move([(x,0,0) for x in [1,2,3,4,5]])
    >>> B = mag3.getB(source, (1,2,3))
    >>> print(B)
    [[-0.88894262  0.          0.        ]
     [-0.62497314 -0.34089444 -0.51134166]
     [-0.17483825 -0.41961181 -0.62941771]
     [ 0.09177028 -0.33037301 -0.49555952]
     [ 0.17480239 -0.22080302 -0.33120453]]

    Compute the B-field of two sources at two observer positions, with and without
    sumup:

    >>> import magpylib as mag3
    >>> src1 = mag3.current.Circular(current=15, diameter=2)
    >>> src2 = mag3.misc.Dipole(moment=(100,100,100))
    >>> obs_pos = [(1,1,1), (1,2,3)]
    >>> B = mag3.getB([src1,src2], obs_pos)
    >>> print(B)
    [[[0.93539608 0.93539608 0.40046672]
      [0.05387784 0.10775569 0.0872515 ]]
     [[3.06293831 3.06293831 3.06293831]
      [0.04340403 0.23872216 0.43404028]]]
    >>> B = mag3.getB([src1,src2], obs_pos, sumup=True)
    >>> print(B)
    [[3.99833439 3.99833439 3.46340502]
     [0.09728187 0.34647784 0.52129178]]

    """
    return getBH_level2(True, sources, observers, sumup, squeeze, **specs)


# ON INTERFACE
def getH(sources, observers, sumup=False, squeeze=True, **specs):
    """
    Compute H-field in [kA/m] for given sources and observers.

    Parameters
    ----------
    sources: source object, Collection or 1D list thereof
        Sources can be a single source object, a Collection or a 1D list of L source
        objects and/or collections.

    observers: array_like or Sensor or 1D list thereof
        Observers can be array_like positions of shape (N1, N2, ..., 3) where the field
        should be evaluated, can be a Sensor object with pixel shape (N1, N2, ..., 3) or
        a 1D list of K Sensor objects with similar pixel shape. All positions are given
        in units of [mm].

    sumup: bool, default=False
        If True, the fields of all sources are summed up.

    squeeze: bool, default=True
        If True, the output is squeezed, i.e. all axes of length 1 in the output (e.g. only
        a single sensor or only a single source) are eliminated.

    Returns
    -------
    H-field: ndarray, shape squeeze(L, M, K, N1, N2, ..., 3)
        H-field of each source (L) at each path position (M) for each sensor (K) and each
        sensor pixel position (N1,N2,...) in units of [kA/m]. Sensor pixel positions are
        equivalent to simple observer positions. Paths of objects that are shorter than
        M will be considered as static beyond their end.

    Notes
    -----
    This function automatically joins all sensor and position inputs together and groups
    similar sources for optimal vectorization of the computation. For maximal performance
    call this function as little as possible and avoid using it in loops.

    Examples
    --------
    Compute the H-field of a spherical magnet at a sensor positioned at (1,2,3):

    >>> import magpylib as mag3
    >>> source = mag3.magnet.Sphere(magnetization=(1000,0,0), diameter=1)
    >>> sensor = mag3.Sensor(position=(1,2,3))
    >>> H = mag3.getH(source, sensor)
    >>> print(H)
    [-0.49733782  0.27127518  0.40691277]

    Compute the H-field of a spherical magnet at five path positions as seen
    by an observer at position (1,2,3):

    >>> import magpylib as mag3
    >>> source = mag3.magnet.Sphere(magnetization=(1000,0,0), diameter=1)
    >>> source.move([(x,0,0) for x in [1,2,3,4,5]])
    >>> H = mag3.getH(source, (1,2,3))
    >>> print(H)
    [[-0.70739806  0.          0.        ]
     [-0.49733782 -0.27127518 -0.40691277]
     [-0.13913186 -0.33391647 -0.5008747 ]
     [ 0.07302847 -0.26290249 -0.39435373]
     [ 0.13910332 -0.17570946 -0.26356419]]

    Compute the H-field of two sources at two observer positions, with and without
    sumup:

    >>> import magpylib as mag3
    >>> src1 = mag3.current.Circular(current=15, diameter=2)
    >>> src2 = mag3.misc.Dipole(moment=(100,100,100))
    >>> obs_pos = [(1,1,1), (1,2,3)]
    >>> H = mag3.getH([src1,src2], obs_pos)
    >>> print(H)
    [[[0.74436455 0.74436455 0.31868129]
      [0.04287463 0.08574925 0.06943254]]
     [[2.43740886 2.43740886 2.43740886]
      [0.03453983 0.18996906 0.34539828]]]
    >>> H = mag3.getH([src1,src2], obs_pos, sumup=True)
    >>> print(H)
    [[3.18177341 3.18177341 2.75609015]
     [0.07741445 0.27571831 0.41483082]]

    """
    return getBH_level2(False, sources, observers, sumup, squeeze, **specs)
