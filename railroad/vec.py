import math
import numbers
import collections


class Vec(collections.namedtuple('Vec', ['x', 'y'])):
    def __new__(cls, *args, **kwargs):
        if len(args) == 0:
            x = y = 0
        elif len(args) == 1:
            x, y = args[0]
        elif len(args) == 2:
            x, y = args[0], args[1]
        else:
            raise ValueError
        if not isinstance(x, numbers.Number) or not isinstance(y, numbers.Number):
            raise TypeError('Vec coords must be numbers')
        return super().__new__(cls, x, y, **kwargs)

    def __add__(self, other):
        """ '+' operator, returns sum of two vectors. Ex.: Vec(2, 3) + Vec(1, -1) ==> Vec(3, 2) """

        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """ '-' operator, returns difference of two vectors. Ex.: Vec(2, 3) - Vec(3, 2) ==> Vec(-1, 1) """

        return self.__class__(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        """ '*' operator. Returns vector multiplied by scalar. Ex.: Vec(2, 3) * 2 ==> Vec(4, 6) """
        scalar = float(other)
        return self.__class__(self.x * scalar, self.y * scalar)

    def __truediv__(self, other):
        """ '/' operator. Returns vector divided by scalar. Ex.: Vec(2, 3) / 2 ==> Vec(1, 1.5) """
        return self * (1.0 / float(other))

    def __neg__(self):
        """ '-obj' operator. Returns reversed vector. Ex.: - Vec(2, 3) ==> Vec(-2, -3) """
        return self.__class__(-self.x, -self.y)
    
    @classmethod
    def dot(cls, v1, v2):
        """Returns dot product of 2 vectors. Ex.: Vec(2, 3).dot(Vec(3, 4)) ==> 18 """

        return v1.x * v2.x + v1.y * v2.y

    @property
    def length_sq(self):
        """ Returns vector's magnitude squared. More efficient than length, doesn't need to calculate square root. """

        return self.x ** 2 + self.y ** 2

    @property
    def length(self):
        """ Returns vector's magnitude (length). Ex.: Vec(3, 4).length ==> 5 """

        return math.sqrt(self.length_sq)

    @property
    def normalized(self):
        """ Returns normalized vector (unit vector). """
        
        length = self.length
        if length == 0:
            return Vec(0,0)
        return self.__class__(self.x / length, self.y / length)
    
    @property
    def angle(self):
        """ Returns counterclockwise angle between vector and x-axis in degrees """
        
        return math.degrees(math.atan2(self.y, self.x))
    
    @classmethod
    def from_angle(cls, angle, length=1):
        """ Returns a new instance constructed from angle in degrees """
        
        radians = math.radians(angle)
        return cls(math.cos(radians)*length, math.sin(radians)*length)

    def rotated(self, angle):
        """ Returns a new instance of the same length, rotated by angle in degrees, counterclockwise """

        radians = math.radians(angle)
        return self.__class__(
            self.x*math.cos(radians) - self.y*math.sin(radians),
            self.x*math.sin(radians) + self.y*math.cos(radians)
        )
