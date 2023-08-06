import unittest
import numpy as np
from scipy.spatial.transform import Rotation as R
from magpylib._lib.obj_classes.class_BaseGeo import BaseGeo
from magpylib._lib.exceptions import (MagpylibBadUserInput,
    MagpylibBadInputShape)
import magpylib as mag3

a3 = np.array([1,2,3])
a2 = np.array([1,2])
a234 = np.array([[[1,2]]*3]*4)
r0 = R.from_quat((0,0,0,1))

# BAD BASEGEO INPUTS --------------------------------------
def badInput_BaseGeo1():
    """ bad pos input type"""
    BaseGeo(123, r0)

def badInput_BaseGeo2():
    """ bad pos input format1"""
    BaseGeo(a2, r0)

def badInput_BaseGeo3():
    """ bad pos input format2"""
    BaseGeo(a234, r0)

def badInput_BaseGeo4():
    """ bad rot input type"""
    BaseGeo(a3, 123)


# BAD BASEGEO .MOVE INPUT--------------------------------------------------
def badInput_move1():
    """ bad displacement input type"""
    bg = BaseGeo(a3, r0)
    bg.move(123)

def badInput_move2():
    """ bad start input type"""
    bg = BaseGeo(a3, r0)
    bg.move([1,2,3], start=1.1)

def badInput_move3():
    """ bad increment input type"""
    bg = BaseGeo(a3, r0)
    bg.move([1,2,3], increment=5)

def badInput_move4():
    """ bad displacement input format1"""
    bg = BaseGeo(a3, r0)
    bg.move([1,2])

def badInput_move5():
    """ bad displacement input format2"""
    bg = BaseGeo(a3, r0)
    bg.move([[[1,2,3]]*3]*4)


# BAD BASEGEO .ROTATE INPUT------------------------------------------------
def badInput_rotate1():
    """ bad rot input type"""
    bg = BaseGeo(a3, r0)
    bg.rotate(123)

def badInput_rotate2():
    """ bad anchor input type"""
    bg = BaseGeo(a3, r0)
    bg.rotate(r0, anchor=123)

def badInput_rotate3():
    """ bad start input type"""
    bg = BaseGeo(a3, r0)
    bg.rotate(r0, start=1.23)

def badInput_rotate4():
    """ bad increment input type"""
    bg = BaseGeo(a3, r0)
    bg.rotate(r0, increment=1)

def badInput_rotate5():
    """ bad anchor input format"""
    bg = BaseGeo(a3, r0)
    bg.rotate(r0, anchor=(1,2,3,4))


# BAD BASEGEO .ROTATE_FROM_ANGAX INPUT-----------------------------------------
def badInput_rotate_from_angax1():
    """ bad ang input type"""
    bg = BaseGeo(a3, r0)
    bg.rotate_from_angax('123', (1,2,3))

def badInput_rotate_from_angax2():
    """ bad axis input type"""
    bg = BaseGeo(a3, r0)
    bg.rotate_from_angax(123, 1)

def badInput_rotate_from_angax3():
    """ bad anchor input type"""
    bg = BaseGeo(a3, r0)
    bg.rotate_from_angax(123, (1,2,3), anchor=1)

def badInput_rotate_from_angax4():
    """ bad start input type"""
    bg = BaseGeo(a3, r0)
    bg.rotate_from_angax(123, (1,2,3), start=1.1)

def badInput_rotate_from_angax5():
    """ bad increment input type"""
    bg = BaseGeo(a3, r0)
    bg.rotate_from_angax(123, (1,2,3), increment=None)

def badInput_rotate_from_angax6():
    """ bad degrees input type"""
    bg = BaseGeo(a3, r0)
    bg.rotate_from_angax(123, (1,2,3), degrees=None)

def badInput_rotate_from_angax7():
    """ bad angle input format"""
    bg = BaseGeo(a3, r0)
    bg.rotate_from_angax([[1,2,3]]*2, (1,2,3))

def badInput_rotate_from_angax8():
    """ bad axis input format"""
    bg = BaseGeo(a3, r0)
    bg.rotate_from_angax([1,2,3], [1,2,3,4])

def badInput_rotate_from_angax9():
    """ bad axis input format"""
    bg = BaseGeo(a3, r0)
    bg.rotate_from_angax(123, [0,0,0])


# EXCITATIONS -----------------------------------------

def badMag_input1():
    """bad magnetization input type"""
    mag3.magnet.Box(magnetization='woot', dimension=a3)

def badMag_input2():
    """bad magnetization input format"""
    mag3.magnet.Box(magnetization=(1,2,3,4), dimension=a3)

def badMag_input3():
    """no magnetization input"""
    mag3.magnet.Box(dimension=a3)

def badCurrent_input1():
    """bad current input type"""
    mag3.current.Circular(current='1', diameter=1)

def badCurrent_input2():
    """missing current input"""
    mag3.current.Circular(diameter=1)

# DIMENSIONS --------------------------------------------

def bad_dim_input1():
    """box dim type"""
    mag3.magnet.Box(magnetization=a3, dimension=1)
def bad_dim_input2():
    """box dim init"""
    mag3.magnet.Box(magnetization=a3)
def bad_dim_input3():
    """box dim format"""
    mag3.magnet.Box(magnetization=a3, dimension=(1,2))

def bad_dim_input4():
    """cylinder dim type"""
    mag3.magnet.Cylinder(magnetization=a3, dimension=1)
def bad_dim_input5():
    """cylinder dim init"""
    mag3.magnet.Cylinder(magnetization=a3)
def bad_dim_input6():
    """cylinder dim format"""
    mag3.magnet.Cylinder(magnetization=a3, dimension=(1,2,3))

def bad_dim_input7():
    """Sphere dim type"""
    mag3.magnet.Sphere(magnetization=a3, diameter=(1,1))
def bad_dim_input8():
    """Sphere dim init"""
    mag3.magnet.Sphere(magnetization=a3)

def bad_dim_input9():
    """Circular dim type"""
    mag3.current.Circular(current=1, diameter=(1,1))
def bad_dim_input10():
    """Circular dim init"""
    mag3.current.Circular(current=1)



# MISC SOURCE ------------------------------------------------------------

def bad_misc_input1():
    """Sensor pixel type"""
    mag3.Sensor(pixel=1)
def bad_misc_input2():
    """Sensor pixel format"""
    mag3.Sensor(pixel=[[1,2]]*3)

def bad_misc_input3():
    """Line vertex type"""
    mag3.current.Line(1, '1')
def bad_misc_input4():
    """Line vertex format 1"""
    mag3.current.Line(1, [(1,2,3)])
def bad_misc_input5():
    """Line vertex format 2"""
    mag3.current.Line(1, [[(1,2,3)]*2]*2)
def bad_misc_input6():
    """Line vertex format 3"""
    mag3.current.Line(1, [(1,2)]*2)


# OBSERVER ------------------------------------------------------------

src = mag3.current.Circular(current=1, diameter=1)
sens = mag3.Sensor()
def bad_observer_input1():
    """getBH observer format"""
    mag3.getB(src, a234)
def bad_observer_input2():
    """getBH observer format"""
    mag3.getB(src, [sens, [(1,2),(1,2)]])
def bad_observer_input3():
    """getBH observer format"""
    mag3.getB(src, [(1,2),(1,2)])
def bad_observer_input4():
    """bad observer type"""
    mag3.getB(src, 123)

class TestExceptions(unittest.TestCase):
    """ test class for exception testing """

    def test_BaseGeo(self):
        """ bad BG inputs"""
        self.assertRaises(MagpylibBadUserInput, badInput_BaseGeo1)
        self.assertRaises(MagpylibBadInputShape, badInput_BaseGeo2)
        self.assertRaises(MagpylibBadInputShape, badInput_BaseGeo3)
        self.assertRaises(MagpylibBadUserInput, badInput_BaseGeo4)

    def test_move(self):
        """ bad .move inputs"""
        self.assertRaises(MagpylibBadUserInput, badInput_move1)
        self.assertRaises(MagpylibBadUserInput, badInput_move2)
        self.assertRaises(MagpylibBadUserInput, badInput_move3)
        self.assertRaises(MagpylibBadInputShape, badInput_move4)
        self.assertRaises(MagpylibBadInputShape, badInput_move5)

    def test_rotate(self):
        """ bad .rotate inputs"""
        self.assertRaises(MagpylibBadUserInput, badInput_rotate1)
        self.assertRaises(MagpylibBadUserInput, badInput_rotate2)
        self.assertRaises(MagpylibBadUserInput, badInput_rotate3)
        self.assertRaises(MagpylibBadUserInput, badInput_rotate4)
        self.assertRaises(MagpylibBadInputShape, badInput_rotate5)

    def test_rotate_from_angax(self):
        """ bad .rotate_from_angax inputs"""
        self.assertRaises(MagpylibBadUserInput, badInput_rotate_from_angax1)
        self.assertRaises(MagpylibBadUserInput, badInput_rotate_from_angax2)
        self.assertRaises(MagpylibBadUserInput, badInput_rotate_from_angax3)
        self.assertRaises(MagpylibBadUserInput, badInput_rotate_from_angax4)
        self.assertRaises(MagpylibBadUserInput, badInput_rotate_from_angax5)
        self.assertRaises(MagpylibBadUserInput, badInput_rotate_from_angax6)
        self.assertRaises(MagpylibBadInputShape, badInput_rotate_from_angax7)
        self.assertRaises(MagpylibBadInputShape, badInput_rotate_from_angax8)
        self.assertRaises(MagpylibBadUserInput, badInput_rotate_from_angax9)

    def test_magnetization_input(self):
        """ bad magnetization inputs"""
        self.assertRaises(MagpylibBadUserInput, badMag_input1)
        self.assertRaises(MagpylibBadInputShape, badMag_input2)
        self.assertRaises(MagpylibBadUserInput, badMag_input3)
        self.assertRaises(MagpylibBadUserInput, badCurrent_input1)
        self.assertRaises(MagpylibBadUserInput, badCurrent_input2)

    def test_dim_inputs(self):
        """ bad dimension inputs"""
        self.assertRaises(MagpylibBadUserInput, bad_dim_input1)
        self.assertRaises(MagpylibBadUserInput, bad_dim_input2)
        self.assertRaises(MagpylibBadInputShape, bad_dim_input3)
        self.assertRaises(MagpylibBadUserInput, bad_dim_input4)
        self.assertRaises(MagpylibBadUserInput, bad_dim_input5)
        self.assertRaises(MagpylibBadInputShape, bad_dim_input6)
        self.assertRaises(MagpylibBadUserInput, bad_dim_input7)
        self.assertRaises(MagpylibBadUserInput, bad_dim_input8)
        self.assertRaises(MagpylibBadUserInput, bad_dim_input9)
        self.assertRaises(MagpylibBadUserInput, bad_dim_input10)

    def test_misc_source_inputs(self):
        """ bad misc source inputs"""
        self.assertRaises(MagpylibBadUserInput, bad_misc_input1)
        self.assertRaises(MagpylibBadInputShape, bad_misc_input2)
        self.assertRaises(MagpylibBadUserInput, bad_misc_input3)
        self.assertRaises(MagpylibBadInputShape, bad_misc_input4)
        self.assertRaises(MagpylibBadInputShape, bad_misc_input5)
        self.assertRaises(MagpylibBadInputShape, bad_misc_input6)

    def test_observer_inputs(self):
        """ bad observer inputs"""
        self.assertRaises(MagpylibBadInputShape, bad_observer_input1)
        self.assertRaises(MagpylibBadInputShape, bad_observer_input2)
        self.assertRaises(MagpylibBadInputShape, bad_observer_input3)
        self.assertRaises(MagpylibBadUserInput, bad_observer_input4)
