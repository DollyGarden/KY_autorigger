# ADVANCED ***************************************************************************
# content = assignment
#
# date    = 2022-01-07
# email   = contact@alexanderrichtertd.com
#************************************************************************************

"""
CUBE CLASS

1. CREATE an abstract class "Cube" with the functions:
   translate(x, y, z), rotate(x, y, z), scale(x, y, z) and color(R, G, B)
   All functions store and print out the data in the cube (translate, rotate, scale and color).

2. ADD an __init__(name) and create 3 cube objects.

3. ADD the function print_status() which prints all the variables nicely formatted.

4. ADD the function update_transform(ttype, value).
   "ttype" can be "translate", "rotate" and "scale" while "value" is a list of 3 floats.
   This function should trigger either the translate, rotate or scale function.

   BONUS: Can you do it without using ifs?

5. CREATE a parent class "Object" which has a name, translate, rotate and scale.
   Use Object as the parent for your Cube class.
   Update the Cube class to not repeat the content of Object.

"""

class Object:
    """
    Create Object class with a parameter name and 3 functions: translate, rotate and scale.
    """
   
    def __init__(self, name):
        self.name = name
        
    def translate(self, x, y, z):
        self.translation = [x, y, z]
        print("translation: ", (x), (y), (z))
    
    def rotate(self, x, y, z):
        self.rotation = [x, y, z]
        print("rotation: ", (x), (y), (z))

    def scale(self, x, y, z):
        self.scaling = [x, y, z]
        print("scaling: ", (x), (y), (z))


class Cube(Object):
    """
    Create Cube class parent to Object class, add 3 functions: color, print_status and update_transform
    """
    def __init__(self, name):
        super(Cube,self).__init__(name)

    def color(self, R, G, B):
        self.colors = [R, G, B]
        print("colors: ", (R), (G), (B))

    def update_transform(self, ttype, value):
        func_dic = {
                     "translate": self.translate,
                     "rotate": self.rotate,
                     "scale": self.scale
                     }
        func = func_dic.get(ttype)
        func(*value)

    def print_status(self):
        print("{} : translation {}".format(self.name, self.translation))
        print("{} : rotation {}".format(self.name, self.rotation))
        print("{} : scaling {}".format(self.name, self.scaling))
        print("{} : colors {}".format(self.name, self.colors))

        
# Create cube_a, cube_b and cube_c, set the translate, rotate, scale and color values, print the values
# Change the translate, rotate, scale and colors values.
cube_01 = Cube(name="cube_a")
cube_01.translate(0, 1, 0)
cube_01.rotate(0, 0, 0)
cube_01.scale(1, 0.5, 1)
cube_01.color(0 ,23 ,0)
cube_01.update_transform(ttype="translate", value=[1, 3.5, 4])
cube_01.print_status()

cube_02 = Cube(name="cube_b")
cube_02.translate(1, 1, 1)
cube_02.rotate(37, 45, 180)
cube_02.scale(1, 2, 1)
cube_02.color(255 ,255 ,255)
cube_02.update_transform(ttype="rotate", value=[5, 40, 98])
cube_02.print_status()

cube_03 = Cube(name="cube_c")
cube_03.translate(20, 15, 3)
cube_03.rotate(45, 135, 70)
cube_03.scale(3, 2, 6)
cube_03.color(100 ,45 ,78)
cube_03.update_transform(ttype="scale", value=[4, 0.3, 2])
cube_03.print_status()


        
        