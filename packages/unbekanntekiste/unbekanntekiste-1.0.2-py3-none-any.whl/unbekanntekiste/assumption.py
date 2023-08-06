
from math import tan
from math import radians
from statistics import mean

from .figure import Line

from typing import Union
from typing import Tuple 
from typing import Iterable
from typing import Callable
from io import TextIOWrapper
from .figure import LineType
from .figure import PointType
from .figure import UnknownBoxType

def assume_wordbreadth_bounging_box(boxes:Iterable[UnknownBoxType]) -> None:

    def cdm(line1:LineType, line2:LineType) -> float:
        degree = line1.contacted_degree(line2)
        return min([degree, 360-degree])
    
    # the assumptive definition of the lines (bounding box)
    # set average contacted degree of each the bounding box lines 
    average = {
        l : mean([cdm(b.line1, l) for b in boxes[1:]])
        for l in boxes[0].lines
        }

    # the line 1 should be the line which of average virtual degree is minimal
    # it means that this line is the most parallel to the line 1 of instance boxes
    line1 = min(boxes[0].lines, key=lambda x:average[x])

    # the line 2 should be the line which is not contacted with line 1
    line2 = boxes[0].not_contacted_lines(line1)[0]

    # the line 3 & line 4 are the rest of the lines
    lines = [line1,line2] + boxes[0].contacted_lines(line1)

    # switch the lines of the bounding box
    boxes[0].lines = lines

def assume_wordbreadth_instance_boxes(boxes:Iterable[UnknownBoxType]) -> None:

    def cdm(line1:LineType, line2:LineType) -> float:
        degree = line1.contacted_degree(line2)
        return min([degree, 360-degree])

    # the assumptive definition of the lines (instance box)
    for index in range(1,len(boxes)):

        # the line 1 should be the line which of average degree is minimal with the line 1 of the bounding box
        # now it is possible to define of the horizontal line even though there is an outlier
        # which of the longest line is vertical line 
        # e.g. an unknown box for a character might have the longest vertical line 
        line1 = min(boxes[index].lines, key=lambda x:cdm(x, boxes[0].line1))

        # line 2 should be the line which is not contacted with line 1
        line2 = boxes[index].not_contacted_lines(line1)[0]

        # line 3 & line 4 are the rest of the lines
        lines = [line1,line2] + boxes[index].contacted_lines(line1)

        # switch the lines of the unknown box
        boxes[index].lines = lines

def group_horizontally(
        boxes:Iterable[UnknownBoxType], 
        distance_tolerance:Union[float,None]=None,
        relative_ratio:Union[float,None]=0.6,
        box_sorting_key:Callable[[UnknownBoxType],Tuple]=lambda b:(b.center,),
        group_sorting_key:Callable[[UnknownBoxType],Tuple]=lambda b:(b.center,)
        ) \
        -> Iterable[Iterable[UnknownBoxType]]:

    def perpendicular_distance(box1:UnknownBoxType, box2:UnknownBoxType):
        # set the direction of a typical word or paragraph 
        closest_line = min(
            [box1.line3, box1.line4],
            key=lambda x:x.center.distance(box2.center)
            )

        # set the degree facing the perdenicular (distance)
        degree = box1.center.degree(
            closest_line.center,
            box2.center
            )
            
        # perdenicular (distance) = line*tan(theta)
        tan_ = tan(radians(degree))

        return abs(box1.center.distance(box2.center)*tan_)

    if (distance_tolerance is None and relative_ratio is None) or \
        (distance_tolerance is not None and relative_ratio is not None):
        raise ValueError(
            'should be provided only an argument between' + 
            'distance tolerance or relative ratio'
            )

    # sort unknown boxes by box sorting key 
    # except the bounding box
    boxes_ = sorted(boxes[1:], key=box_sorting_key)

    # set visited indices 
    visited = []

    # set groups
    groups = []

    # start to group with other boxes
    for index1 in range(0,len(boxes_)):

        # if the box index is in other group
        if index1 in visited:
            continue
        
        # the box index is visited
        visited.append(index1)

        # set group
        group = [boxes_[index1]]

        # start to group with other boxes [candidate]
        for index2 in range(0,len(boxes_)):

            # if the candidate box index is in other group
            if index2 in visited:
                continue
            
            # as persisting the continuous of horizontal characteristic,
            # it will compute the average perpendicular distance between
            # boxes of the group and the candidate box, not only the start of the group
            distance = mean(perpendicular_distance(box, boxes_[index2]) for box in group)
            
            # set the line between the box and the candidate box 
            connection = Line(boxes_[index1].center, boxes_[index2].center)
            
            # does the line toward to the proper direction ? 
            touched = group[-1].line1.touched(connection) or \
                group[-1].line2.touched(connection)

            # set tolerance (distance tolerance|relative ratio)
            tolerance = distance_tolerance if distance_tolerance is not None \
                else mean(box.center_line1.distance * relative_ratio for box in boxes_)

            # if computed perpendicular distance is under tolerance
            if distance <= tolerance and not touched:

                # notice that the candidate box index is in other group
                visited.append(index2)
                
                # append the candidate box to the group
                group.append(boxes_[index2])

                # sort by group sorting key
                group.sort(key=group_sorting_key)

        # append the group to groups
        groups.append(group)
    
    # sorting unaltered order of unknown boxes
    sorting_order = {
        group[0] : boxes.index(group[0])
        for group in groups
        }

    # sort by unaltered sorting order
    groups.sort(key=lambda x:sorting_order[x[0]])

    return groups
