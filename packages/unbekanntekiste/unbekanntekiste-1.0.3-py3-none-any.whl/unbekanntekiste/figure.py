
from itertools import permutations

from math import dist
from math import atan2
from math import pi

from typing import Union
from typing import Iterable
from typing import Tuple
from typing import NewType

# === class point definition ===

FigureType = NewType(
    'Figure', 
    Tuple[Union[int,float],Union[int,float]]
    )

class Figure(object):
    '''
    
    '''

    # === should be described for dump ===
    @classmethod
    def to_dict(cls, obj:FigureType) -> dict:
        return {}

    # === should be described for load ===
    @classmethod
    def to_instance(cls, dict_:dict) -> FigureType:
        return cls()

# === class point definition ===

PointType = NewType(
    'Point', 
    Tuple[Union[int,float],Union[int,float]]
    )

class Point(Figure):
    '''
    
    '''

    _x = None
    _y = None

    def __init__(self, x:float=None, y:float=None):
        
        self._x = x
        self._y = y

    def __str__(self) -> str:
        return '{}<x:{},y:{}>'.format(
            self.__class__.__name__,
            self._x,
            self._y
            )

    def __repr__(self) -> str:
        return '{}<x:{},y:{}>'.format(
            self.__class__.__name__,
            self._x,
            self._y
            )
        
    def __getitem__(self, index:int) -> int:
        if index == 0:
            return self._x
        
        elif index == 1:
            return self._y

        raise IndexError(
            'only index 0 and 1 stands for x and y.'
            )

    def __hash__(self) -> int:
        return hash((self._x, self._y,))

    def __eq__(self, point:PointType) -> bool:
        if not isinstance(point, self.__class__):
            return False
        else:
            return (self._x == point._x) and \
                (self._y == point._y)
    
    def __lt__(self, point:PointType) -> bool:
        if not isinstance(point, self.__class__):
            raise TypeError(
                '"<" not supported with instance "{}"'.format(
                    type(point)
                    )
                )
        else:
            yi = point.y - point.x
            return self._y > self._x + yi
    
    def __le__(self, point:PointType) -> bool:
        if not isinstance(point, self.__class__):
            raise TypeError(
                '"<=" not supported with instance "{}"'.format(
                    type(point)
                    )
                )
        else:
            if self == point:
                return True
            
            else:
                yi = point.y - point.x
                return self._y >= self._x + yi
    
    def __gt__(self, point:PointType) -> bool:
        if not isinstance(point, self.__class__):
            raise TypeError(
                '">" not supported with instance "{}"'.format(
                    type(point)
                    )
                )
        else:
            if self == point:
                return True

            else:
                yi = point.y - point.x
                return self._y <= self._x + yi
    
    def __ge__(self, point:PointType) -> bool:
        if not isinstance(point, self.__class__):
            raise TypeError(
                '">=" not supported with instance "{}"'.format(
                    type(point)
                    )
                )
        else:
            yi = point.y - point.x
            return self._y < self._x + yi

    def __iter__(self) -> Iterable[Union[int,float]]:
        return iter((self._x, self._y,))

    @classmethod
    def to_dict(cls, obj:PointType) -> dict:
        return {
            'cls' : obj.__class__.__name__,
            'x' : obj._x,
            'y' : obj._y,
            }

    @classmethod
    def to_instance(cls, dict_:dict) -> PointType:
        return cls(
            x=dict_[0] if isinstance(dict_, cls) \
                else dict_['x'],
            y=dict_[1] if isinstance(dict_, cls) \
                else dict_['y'],
            )

    @property
    def x(self) -> Union[int,float]:
        return self._x

    @property
    def y(self) -> Union[int,float]:
        return self._y

    @classmethod
    def _distance(cls, point1:PointType, point2:PointType) -> float:
        return dist(point1, point2)
        
    @classmethod
    def _degree2(cls, point1:PointType, point2:PointType) -> float:
        a1 = atan2(point1[1], point1[0])
        a2 = atan2(point2[1], point2[0])

        return (a1-a2) * 180/pi

    @classmethod
    def _degree3(cls, point1:PointType, point2:PointType, point3:PointType) -> float:
        _point1 = Point(point1[0]-point2[0], point1[1]-point2[1])
        _point2 = Point(point3[0]-point2[0], point3[1]-point2[1])

        return (cls._degree2(_point1, _point2) + 360) % 360

    @classmethod
    def _degree4(cls, point1:PointType, point2:PointType, point3:PointType, point4:PointType) -> float:
        _point1 = Point(point1[0]-point2[0], point1[1]-point2[1])
        _point2 = Point(point3[0]-point4[0], point3[1]-point4[1])

        return (cls._degree2(_point1, _point2) + 360) % 360

    @classmethod
    def _has_aligned(cls, *points:Iterable[PointType]) -> bool:
        degrees = []
        length = len(points)

        for index in range(length):
            degree = Point._degree3(
                points[index-1], 
                points[index],
                points[index+1 if index+1 < length else 0]
                )

            degrees.append(int(degree))
        
        return 180 in degrees or 0 in degrees

    def distance(self, point:PointType) -> float:
        return self._distance(
            point1=self,
            point2=point
            )
    
    def degree(self, point1:PointType, point2:PointType) -> float:
        return self._degree3(
            point1=point1,
            point2=self,
            point3=point2
            )

    def has_aligned(self, *points:Iterable[PointType]) -> bool:
        degrees = []
        length = len(points)

        for index in range(length):
            degree = Point._degree3(
                points[index], 
                self,
                points[index+1 if index+1 < length else 0]
                )

            degrees.append(int(degree))
        
        return 180 in degrees or 0 in degrees

# === class line definition ===

LineType = NewType(
    'Line',
    Tuple[PointType,PointType]
    )

class Line(Figure):
    '''
    
    '''

    _point1 = None
    _point2 = None

    def __init__(self, point1:PointType=None, point2:PointType=None):

        self._point1 = point1 if isinstance(point1, Point) \
            else Point(*point1)

        self._point2 = point2 if isinstance(point2, Point) \
            else Point(*point2)

        # raise unavailable point
        if len({self._point1, self._point2}) == 1:
            raise ValueError(
                'should be consisted of 2 independent points.'
                )

    def __str__(self) -> str:
        return '{}<p1:{},p2:{}>'.format(
            self.__class__.__name__,
            self._point1,
            self._point2
            )

    def __repr__(self) -> str:
        return '{}<p1:{},p2:{}>'.format(
            self.__class__.__name__,
            self._point1,
            self._point2
            )

    def __getitem__(self, index:int) -> PointType:
        if index == 0:
            return self._point1
        
        elif index == 1:
            return self._point2

        raise IndexError(
            'only index 0 and 1 stands for point1 and point2.'
            )

    def __hash__(self) -> int:
        return hash((self._point1, self._point2,))

    def __eq__(self, line:LineType) -> bool:
        if not isinstance(line, self.__class__):
            return False
        else:
            return (self._point1 == line._point1) and \
                (self._point2 == line._point2)
    
    def __iter__(self) -> Iterable[PointType]:
        return iter((self._point1, self._point2,))

    @classmethod
    def to_dict(cls, obj:LineType) -> dict:
        return {
            'cls' : obj.__class__.__name__,
            'point1' : Point.to_dict(obj._point1),
            'point2' : Point.to_dict(obj._point2),
            }

    @classmethod
    def to_instance(cls, dict_:dict) -> LineType:
        return cls(
            point1= Point.to_instance(dict_[0])\
                if isinstance(dict_, cls) \
                else Point.to_instance(dict_['point1']), 
            point2= Point.to_instance(dict_[1])\
                if isinstance(dict_, cls) \
                else Point.to_instance(dict_['point2']), 
            )

    @property
    def point1(self) -> PointType:
        return self._point1

    @property
    def point2(self) -> PointType:
        return self._point2

    @property
    def center(self) -> PointType:
        return Point(
            (self._point1[0]+self._point2[0])/2,
            (self._point1[1]+self._point2[1])/2
            )

    @property
    def distance(self) -> float:
        return dist(self._point1, self._point2)

    @classmethod
    def _determinant(cls, point1:PointType, point2:PointType) -> float:
        return point1[0]*point2[1] - point1[1]*point2[0]

    @classmethod
    def _direct(cls, point1:PointType, point2:PointType, point3:PointType) -> float:
        x1 = point2[0] - point1[0]
        y1 = point2[1] - point1[1]
        x2 = point3[0] - point1[0]
        y2 = point3[1] - point1[1]

        return cls._determinant(
            point1=(x1,y1,),
            point2=(x2,y2,)
            )

    @classmethod
    def _direction_point(cls, point1:PointType, point2:PointType, point3:PointType) -> int:
        det = cls._direct(
            point1=point1,
            point2=point2,
            point3=point3
           )
        
        return 1 if det > 0 \
            else 0 if det == 0 \
            else -1

    @classmethod
    def _direction_line(cls, line1:LineType, line2:LineType) -> Tuple[int,int]:
        return (
            cls._direction_point(
                point1=line1[0],
                point2=line2[0],
                point3=line2[1]
                ),
            cls._direction_point(
                point1=line1[1],
                point2=line2[0],
                point3=line2[1]
                ),
            )
    
    @classmethod
    def _contacted_point(cls, line1:LineType, line2:LineType) -> Union[PointType,None]:
        px = Point(
            line1[0][0] - line1[1][0],
            line2[0][0] - line2[1][0]
            )

        py = Point(
            line1[0][1] - line1[1][1],
            line2[0][1] - line2[1][1]
            )

        div = cls._determinant(px, py)

        if div == 0:
            return None

        pd = Point(
            cls._determinant(line1[0], line1[1]),
            cls._determinant(line2[0], line2[1])
            )

        return Point(
            cls._determinant(pd, px) / div,
            cls._determinant(pd, py) / div
            )

    @classmethod
    def _contacted_degree(cls, line1:LineType, line2:LineType) -> float:
        contacted_point = cls._contacted_point(
            line1,
            line2
            )

        if contacted_point is None:
            return 0

        return contacted_point.degree(
            line1.center,
            line2.center
            )

    @classmethod
    def _straddled(cls, line1:LineType, line2:LineType) -> bool:
        d1, d2 = cls._direction_line(line1, line2)
        d3, d4 = cls._direction_line(line2, line1)

        return (d1*d2 < 0) and (d3*d4 < 0)

    @classmethod
    def _contacted(cls, line1:LineType, line2:LineType) -> bool:
        d1, d2 = cls._direction_line(line1, line2)
        d3, d4 = cls._direction_line(line2, line1)

        return 0 in [d1,d2,d3,d4]

    @classmethod
    def _touched(cls, line1:LineType, line2:LineType) -> bool:
        return cls._straddled(line1, line2) or \
            cls._contacted(line1, line2)

    def direction(self, line:LineType) -> Tuple[int,int]:
        return self._direction_line(
            line1=self,
            line2=line
            )

    def contacted_point(self, line:LineType) -> PointType:
        return self._contacted_point(
            line1=self,
            line2=line
            )

    def contacted_degree(self, line:LineType) -> float:
        return self._contacted_degree(
            line1=self,
            line2=line
            )

    def straddled(self, line:LineType) -> bool:
        return self._straddled(
            line1=self,
            line2=line
            )

    def contacted(self, line:LineType) -> bool:
        return self._contacted(
            line1=self,
            line2=line
            )
    
    def touched(self, line:LineType) -> bool:
        return self._touched(
            line1=self,
            line2=line
            )

# === class unknown box definition ===

def order_not_straddled_eulerian_circuit(
        point1:PointType, 
        point2:PointType, 
        point3:PointType, 
        point4:PointType
        ) \
        -> Iterable[PointType]:
    '''
    this method returns a 4-length permutation of points 
    which is able to be ordered using eulerian circuit,
    but of which connected lines should not be straddled (across) each other.
    '''

    points = (
        point1 if isinstance(point1, Point) \
            else Point(*point1),
        point2 if isinstance(point2, Point) \
            else Point(*point2),
        point3 if isinstance(point3, Point) \
            else Point(*point3),
        point4 if isinstance(point4, Point) \
            else Point(*point4),
        )

    # set length of points
    length = len(points)

    # raise unavailable point
    if len(set(points)) != 4:
        raise ValueError(
            'should be consisted of 4 independent points.'
            )
    
    # raise unavailable degree
    if Point._has_aligned(*points):
        raise ValueError(
            'should be consisted of 4 degrees.'
            )
            
    # 4-length permutation of points 
    for permutation in permutations(points, 4):

        # set connected lines
        lines = []
        
        # on circuit
        for index in range(length):

            # set the line
            line = Line(
                permutation[index], 
                # eulerian circuit shoud be end with start point
                permutation[index+1 if index+1 < length else 0]
                )

            # does the line straddle other lines ?
            if any([line.straddled(l) for l in lines]):
                break 

            # the line is connected
            lines.append(line)

        # return this permutation
        if len(lines) == 4:
            return list(permutation)

    # does not match any permutation
    raise ValueError(
        'cannot be ordered in not straddled eulerian circuit.'
        )

UnknownBoxType = NewType(
    'UnknownBox',
    Tuple[PointType,PointType,PointType,PointType]
    )

class UnknownBox(Figure):
    '''
    
    '''

    _description = None
    _points = None
    _lines = None

    def __init__(
            self, 
            description:str=None, 
            point1:PointType=None, 
            point2:PointType=None, 
            point3:PointType=None, 
            point4:PointType=None
            ):

        # set description
        self._description = description

        # set ordered points by using not straddeled eulerian circuit 
        # the base method for organizing the unknown box
        self._points = order_not_straddled_eulerian_circuit(
            point1=point1,
            point2=point2,
            point3=point3,
            point4=point4,
            )

        # the uncertain assumptive definition of the lines
        # notice! it should be re-defined for its purpose by external access
        lines = []

        # set lines (point 1 > point 2 > point 3 > point 4)
        for index in range(4):
            next_index = index+1 if index < 3 else 0
            lines.append(Line(self._points[index],self._points[next_index]))

        # set lines temporarily
        self._lines = lines

        # the line 1 should be the line which of distance is the longest
        # a typical word or paragraph is longer horizontally than vertically
        # thus, it is based on assumption that the line 1 would be the horizontal line   
        line1 = max(lines, key=lambda x:x.distance)

        # the line 2 should be the line which is not contacted with the line 1
        line2 = self.not_contacted_lines(line1)[0]

        # the line 3 & line 4 are the rest of the lines
        # these would be the vertical lines which
        # can appear the direction of a typical word or paragraph 
        self._lines = [line1,line2] + self.contacted_lines(line1)

    @classmethod
    def to_dict(cls, obj:UnknownBoxType) -> dict:
        return {
            'cls' : obj.__class__.__name__,
            'description' : obj._description,
            'points' : [Point.to_dict(x) for x in obj._points],
            'lines' : [Line.to_dict(x) for x in obj._lines],
            }

    @classmethod
    def to_instance(cls, dict_:dict) -> UnknownBoxType:
        points = [Point.to_instance(x) for x in dict_['points']]
        lines = [Line.to_instance(x) for x in dict_['lines']]
        instance = cls(dict_['description'], *points)
        instance.lines = lines
        return instance

    def __str__(self) -> str:
        return '{}<points:{},lines:{}> "{}"'.format(
            self.__class__.__name__,
            self._points,
            self._lines,
            self._description,
            )

    def __repr__(self) -> str:
        return '{}<points:{},lines:{}> "{}"'.format(
            self.__class__.__name__,
            self._points,
            self._lines,
            self._description,
            )

    def __getitem__(self, index:int) -> PointType:
        if index == 0:
            return self._points[0]
        
        elif index == 1:
            return self._points[1]
        
        elif index == 2:
            return self._points[2]
        
        elif index == 3:
            return self._points[3]

        raise IndexError(
            'only index 0,1,2,3 stands for point1,2,3,4.'
            )

    def __hash__(self) -> int:
        return hash((self._points[0], self._points[1], self._points[2], self._points[3],))

    def __eq__(self, box:UnknownBoxType) -> bool:
        if not isinstance(box, self.__class__):
            return False
        else:
            return (self._description == box.description) and \
                (self._points[0] == box.point1) and \
                (self._points[1] == box.point2) and \
                (self._points[2] == box.point3) and \
                (self._points[3] == box.point4) and \
                (self._lines[0] == box.line1) and \
                (self._lines[1] == box.line2) and \
                (self._lines[2] == box.line3) and \
                (self._lines[3] == box.line4)
                
    def __iter__(self) -> Iterable[PointType]:
        return iter((self._points[0], self._points[1], self._points[2], self._points[3],))

    @property
    def description(self) -> str:
        return self._description

    @property
    def points(self) -> Tuple[PointType]:
        return self._points

    @property
    def lines(self) -> Iterable[LineType]:
        return self._lines
    
    @lines.setter
    def lines(self, lines_) -> None:
        set_ = set(self._lines).difference(set(lines_))
        if len(set_) != 0:
            raise ValueError(
                'should be the same lines.'
                )

        self._lines = lines_

    # === do not store properties [start] ===
    # below values should be retrieved from lines dynamically.

    @property
    def point1(self) -> PointType:
        return self._points[0]

    @property
    def point2(self) -> PointType:
        return self._points[1]
        
    @property
    def point3(self) -> PointType:
        return self._points[2]

    @property
    def point4(self) -> PointType:
        return self._points[3]

    @property
    def line1(self) -> LineType:
        return self._lines[0]

    @property
    def line2(self) -> LineType:
        return self._lines[1]
    
    @property
    def line3(self) -> LineType:
        return self._lines[2]
    
    @property
    def line4(self) -> LineType:
        return self._lines[3]

    @property
    def center_line1(self) -> LineType:
        return Line(self.line1.center, self.line2.center)

    @property
    def center_line2(self) -> LineType:
        return Line(self.line3.center, self.line4.center)

    @property
    def center(self) -> PointType:
        return self.center_line1.contacted_point(self.center_line2)

    # === do not store properties [end] ===

    @classmethod
    def _contacted_lines(cls, box:UnknownBoxType, line:LineType) -> Iterable[LineType]:
        return [l for l in box.lines if line.contacted(l) and l != line]

    @classmethod
    def _not_contacted_lines(cls, box:UnknownBoxType, line:LineType) -> Iterable[LineType]:
        return [l for l in box.lines if not line.contacted(l) and l != line]

    def contacted_lines(self, line:LineType) -> Iterable[LineType]:
        return self._contacted_lines(
            box=self,
            line=line
            )

    def not_contacted_lines(self, line:LineType) -> Iterable[LineType]:
        return self._not_contacted_lines(
            box=self,
            line=line
            )