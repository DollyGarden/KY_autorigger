import os
import json

controller_shape_path = os.path.dirname(__file__) + "/KY_ControllerShape.json"
#  write json file
controller_shapes = {
                    'elbow' : [[0.0, 1.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, 0.0], 
                                [-1.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0], 
                                [0.0, 0.0, -1.0], [0.0, 0.0, 1.0]],
                    'finger' : [[0, 0, 0], [0, 0, 0.5], [0.2, 0, 0.7],[0, 0, 0.9], 
                                [-0.2, 0, 0.7], [0, 0, 0.5]],
                    'knee' : [[0.0, 1.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, 0.0], 
                                [-1.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0], 
                                [0.0, 0.0, -1.0], [0.0, 0.0, 1.0]],
                    'foot' : [[1, 0, 0], [1, 0, 2], [2, 0, 2], [0, 0, 6], [-2, 0, 2], 
                                [-1, 0, 2], [-1, 0, 0], [1, 0, 0]],
                    }
with open(controller_shape_path, 'w') as outfile:
    json.dump(controller_shapes, outfile, indent=4)
