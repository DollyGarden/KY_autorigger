# ********************************************************************
#  content = create all controllers
#  version = 0.1.4
#  date = 2022-03-18
#  dependencies = Maya
#  TODO: For the class controller
#        1) A function to add 3 group layer on controllers.
#        2) A function to generate json file which stores the controller shape. The generated controller
#           shape will adapt to the size of the joints, because the unit of the scene and the size of 
#           the model may be different.
#        3) Put all the other controllers under this class.
#
#  license = MIT
#  author = Kelly Yang <kelly.yang1116@hotmail.com>
# ********************************************************************

import os
import json

import maya.cmds as cmds

CONTROLLER_SHAPE_PATH = os.path.dirname(__file__) + "/KY_ControllerShape.json"

def create_master():
    # master
    master_ctrl = cmds.circle(normal=(0, 1, 0), c=(0, 0, 0), radius=1, degree=1, sections=16, name="MASTER_CONTROLLER")
    selection = cmds.select("MASTER_CONTROLLER.cv[1]", "MASTER_CONTROLLER.cv[3]","MASTER_CONTROLLER.cv[5]", 
                            "MASTER_CONTROLLER.cv[7]", "MASTER_CONTROLLER.cv[9]","MASTER_CONTROLLER.cv[11]",
                            "MASTER_CONTROLLER.cv[13]","MASTER_CONTROLLER.cv[15]")
    cmds.scale(0.7, 0.7, 0.7, selection)
    cmds.makeIdentity(master_ctrl, apply=True, translate=1, rotate=1, scale=1)

def create_pelvis():    
    # pelvis
    pelvis_ctrl = cmds.circle(normal=(0, 1, 0), c=(0, 0, 0), radius=1, degree=1, sections=8, name="CTRL_PELVIS")
    root_pos    = cmds.xform(cmds.ls("RIG_ROOT", type='joint'), query=True, translation=True, worldSpace=True)
    cmds.move(root_pos[0], root_pos[1], root_pos[2], pelvis_ctrl)
    cmds.scale(0.5, 0.5, 0.5, pelvis_ctrl)
    cmds.makeIdentity(pelvis_ctrl, apply=True, translate=1, rotate=1, scale=1)
    cmds.parent("CTRL_PELVIS", "MASTER_CONTROLLER")

# spine
def create_spines(spine_count):
    for spine_index in range(0, spine_count):
        spine_pos  = cmds.xform(cmds.ls("RIG_SPINE_"+str(spine_index)), query=True, translation=True, worldSpace=True)
        spine_ctrl = cmds.circle(normal=(0,1,0), c=(0,0,0), radius=1, sections=8, name="CTRL_SPINE_"+str(spine_index))[0]
        cmds.move(spine_pos[0], spine_pos[1], spine_pos[2], spine_ctrl)
        cmds.scale(0.3, 0.3, 0.3, spine_ctrl)
        if spine_index == 0:
            cmds.parent(spine_ctrl, "CTRL_PELVIS")
        else:
            cmds.parent(spine_ctrl, "CTRL_SPINE_"+str(spine_index-1))
            
        cmds.makeIdentity(spine_ctrl, apply=True, translate=1, rotate=1, scale=1)
# neck
def create_neck(spine_count):
    neck_ctrl = cmds.circle(normal=(0,1,0),c=(0,0,0), radius=1, sections=8, name="CTRL_NECK")
    neck_pos  = cmds.xform(cmds.ls("RIG_Neck_Start"), query=True, translation=True, worldSpace=True)
    cmds.scale (0.2, 0.2, 0.2, neck_ctrl)
    cmds.move(neck_pos[0], neck_pos[1], neck_pos[2], neck_ctrl)
    cmds.parent("CTRL_NECK", "CTRL_SPINE_"+str(spine_count-1))
    
    cmds.makeIdentity(neck_ctrl, apply=True, translate=1, rotate=1, scale=1)
    
#  Head
def create_head():
    head_ctrl = cmds.circle(normal=(1,0,0), c=(0,0,0), radius=1, sections=8, name="CTRL_HEAD")
    head_pos  = cmds.xform(cmds.ls("RIG_Neck_End"), query=True, translation=True, worldSpace=True)
    head_rot  = cmds.xform(cmds.ls("RIG_Neck_End"), query=True, rotation=True, worldSpace=True)
    cmds.scale(0.25, 0.25, 0.25, head_ctrl)
    cmds.move(head_pos[0], head_pos[1], head_pos[2], head_ctrl)
    cmds.rotate(head_rot[0], head_rot[1], head_rot[2], head_ctrl)
    cmds.parent("CTRL_HEAD", "CTRL_NECK")
    
    cmds.makeIdentity(head_ctrl, apply=True, translate=1, rotate=1, scale=1)
    # jaw
    jaw = cmds.circle(normal=(0,1,0), c=(0,0,0), radius=0.2, sections=8, name="CTRL_JAW")
    jaw_start = cmds.xform(cmds.ls("RIG_Jaw_Start"), query=True, translation=True, worldSpace=True)
    jaw_end   = cmds.xform(cmds.ls("RIG_Jaw_End"), query=True, translation=True, worldSpace=True)
    jaw_rot   = cmds.xform(cmds.ls("RIG_Jaw_Start"), query=True, rotation=True, worldSpace=True)
    cmds.rotate(jaw_rot[0], jaw_rot[1], jaw_rot[2], jaw)
    cmds.move(jaw_end[0], jaw_end[1], jaw_end[2], jaw)
    cmds.move(jaw_start[0], jaw_start[1], jaw_start[2], "CTRL_JAW.scalePivot", "CTRL_JAW.rotatePivot")
    cmds.parent("CTRL_JAW", "CTRL_HEAD")
    
    cmds.makeIdentity(jaw, apply=True, translate=1, rotate=1, scale=1)

class Controller(object):
    """Top parent of all Controllers. It has a variable "side" and a function "get_controller_shape" to
        get the controller curve shape data from the json file 'KY_ControllerShape.json'.
    """
    def __init__(self, side):
        self.side = side

    def get_controller_shape(self, shape):
        """get controller shape point data from json file 'KY_ControllerShape.json'.
        Args:
            shape (string): Choose the controller shape in the json file
        Returns:
            list: A list of all the point position on the controller curve.
        """
        with open(CONTROLLER_SHAPE_PATH, 'r') as json_file:
            json_data = json_file.read()
            controller_shape_dict = json.loads(json_data)
            ctrl_shape = controller_shape_dict.get(shape)
        return ctrl_shape
    
class ArmController(Controller):
    """Create all the arm controllers. Inherit the "side" variable and get_controller_shape function from the Controller class. 
       Benefit: Don't need to write left and right side codes separately.
    """
    def __init__(self, side):
        super(ArmController, self).__init__(side)

    def create_clavicles(self, spine_count):
        # create controller
        clavicle = cmds.circle(normal=(0, 1, 0), c=(0, 0, 0), radius=1, sections=12, name="CTRL_"+self.side+"_Clavicle")[0]
        selection_01 = cmds.select("CTRL_"+self.side+"_Clavicle.cv[4]", "CTRL_"+self.side+"_Clavicle.cv[10]")
        cmds.move(0, 0.3, 0, selection_01, relative=True)
        selection_02 = cmds.select("CTRL_"+self.side+"_Clavicle.cv[3]", "CTRL_"+self.side+"_Clavicle.cv[5]",
                                   "CTRL_"+self.side+"_Clavicle.cv[9]", "CTRL_"+self.side+"_Clavicle.cv[11]")
        cmds.move(0, 0.2, 0, selection_02, relative=True)
        cmds.makeIdentity(clavicle, apply=True, translate=1, rotate=1, scale=1)
        clavicle_grp = cmds.group(empty=True, name="CTRL_GRP_"+self.side+"_Clavicle")
        cmds.parent(clavicle, clavicle_grp)
        
        cmds.scale(0.1, 0.2, 0.2, clavicle_grp)
        arm_pos = cmds.xform(cmds.ls("RIG_"+self.side+"_UpperArm"), query=True, translation=True, worldSpace=True)
        clavicle_pos = cmds.xform(cmds.ls("RIG_"+self.side+"_Clavicle"), query=True, translation=True, worldSpace=True)
        clavicle_rot = cmds.xform(cmds.ls("RIG_"+self.side+"_Clavicle"), query=True, rotation=True, worldSpace=True)
        cmds.rotate(clavicle_rot[0], clavicle_rot[1], clavicle_rot[2], clavicle_grp)
        cmds.move(arm_pos[0]-0.1, arm_pos[1]+0.125, arm_pos[2], clavicle_grp)
        cmds.move(clavicle_pos[0], clavicle_pos[1], clavicle_pos[2], "CTRL_"+self.side+"_Clavicle.scalePivot", "CTRL_"+self.side+"_Clavicle.rotatePivot")
        cmds.parent(clavicle_grp, "CTRL_SPINE_"+str(spine_count-1))
        

    # elbow
    def create_elbow(self):
        elbow_ctrl_shape = self.get_controller_shape("elbow")
        # Create elbow controller
        elbow = cmds.curve(point=elbow_ctrl_shape, degree=1, name="CTRL_"+self.side+"_Elbow")  
        elbow_grp = cmds.group(empty=True, name="CTRL_GRP_"+self.side+"_Elbow")    
        cmds.parent(elbow, elbow_grp)
        
        cmds.scale(0.15, 0.15, 0.15, elbow_grp)
        upper_arm_pos = cmds.xform(cmds.ls("RIG_"+self.side+"_UpperArm"), query=True, translation=True, worldSpace=True)
        elbow_pos     = cmds.xform(cmds.ls("RIG_"+self.side+"_Elbow"), query=True, translation=True, worldSpace=True)
        wrist_pos     = cmds.xform(cmds.ls("RIG_"+self.side+"_Wrist"), query=True, translation=True, worldSpace=True)
        cmds.move(elbow_pos[0], elbow_pos[1], elbow_pos[2]-0.5, elbow_grp)

        # align the elbow controller to the correct direction
        # create a polygon for elbow controller align
        elbow_ref_plane = cmds.polyCreateFacet(point=[(upper_arm_pos[0], upper_arm_pos[1], upper_arm_pos[2]),
                                                    (elbow_pos[0], elbow_pos[1], elbow_pos[2]),
                                                    (wrist_pos[0], wrist_pos[1], wrist_pos[2])], name=self.side+'_elbow_ref_plane')
        # align the controller grp to the polygon and delete the polygon
        cmds.normalConstraint(elbow_ref_plane, elbow_grp, aimVector=[0, -1, 0], upVector=[1, 0, 0], worldUpType='scene')
        # delete the normal constraint and ref plane
        cmds.delete(elbow_ref_plane)
        cmds.parent(elbow_grp, "MASTER_CONTROLLER")
        

    # wrist
    def create_wrists(self):
        wrist_ctrl     = cmds.circle(normal=(1, 0, 0), c=(0, 0, 0), radius=1, sections=16, name="CTRL_"+self.side+"_Wrist")[0]
        wrist_ctrl_grp = cmds.group(empty=True, name="CTRL_GRP_"+self.side+"_Wrist")
        cmds.parent(wrist_ctrl, wrist_ctrl_grp)
        cmds.scale(0.1, 0.1, 0.1, wrist_ctrl)

        wrist_pos = cmds.xform(cmds.ls("RIG_"+self.side+"_Wrist"), query=True, translation=True, worldSpace=True)
        wrist_rot = cmds.xform(cmds.ls("RIG_"+self.side+"_Wrist"), query=True, worldSpace=True, rotation=True)
        cmds.move(wrist_pos[0], wrist_pos[1], wrist_pos[2], wrist_ctrl_grp)
        cmds.rotate(wrist_rot[0], wrist_rot[1], wrist_rot[2], wrist_ctrl_grp)
        cmds.parent(wrist_ctrl_grp, "MASTER_CONTROLLER")

        
    # finger
    def create_fingers(self, finger_count):
        finger_ctrl_shape = self.get_controller_shape("finger")
        for finger_index in range(0, finger_count):
            for finger_joint in range(0, 3):
                finger_rot = cmds.xform(cmds.ls("RIG_"+self.side+"_Finger_"+str(finger_index)+"_"+str(finger_joint)), query=True, worldSpace=True, rotation=True)
                finger_pos = cmds.xform(cmds.ls("RIG_"+self.side+"_Finger_"+str(finger_index)+"_"+str(finger_joint)), query=True, worldSpace=True, translation=True)
                finger     = cmds.curve(point=finger_ctrl_shape, degree=1, name="CTRL_"+self.side+"_Finger_"+str(finger_index)+"_"+str(finger_joint))
                if self.side == 'R':
                    cmds.rotate(90, 0, 0, finger)
                else:
                    cmds.rotate(-90, 0, 0, finger)
                cmds.scale(0.1, 0.1, 0.1, finger)  
                
                finger_grp = cmds.group(empty=True, n="CTRL_GRP_"+self.side+"_Finger_"+str(finger_index)+"_"+str(finger_joint))
                cmds.parent(finger, finger_grp)
                cmds.rotate(finger_rot[0], finger_rot[1], finger_rot[2], finger_grp)
                cmds.move(finger_pos[0], finger_pos[1], finger_pos[2], finger_grp)
                cmds.makeIdentity(finger, apply=True, translate=1, rotate=1, s=1)

                if finger_joint > 0:
                    cmds.parent(finger_grp, "CTRL_"+self.side+"_Finger_"+str(finger_index)+"_"+str(finger_joint-1))
                else:
                    cmds.parent(finger_grp, "CTRL_"+self.side+"_Wrist")

       
# leg
class LegController(Controller):
    """Create all the leg controllers. Inherit the "side" variable and get_controller_shape function from the Controller class. 
    """
    def __init__(self, side):
        super(LegController, self).__init__(side)

    def create_leg(self):
        # knee
        knee_ctrl_shape = self.get_controller_shape("knee")
        knee_ctrl = cmds.curve(point=knee_ctrl_shape, degree=1, name="CTRL_"+self.side+"_Knee")  
        knee_ctrl_grp = cmds.group(empty=True, name="CTRL_GRP_"+self.side+"_Knee")    
        cmds.parent(knee_ctrl, knee_ctrl_grp)
        cmds.scale(0.15, 0.15, 0.15, knee_ctrl_grp)
        upper_leg_pos = cmds.xform(cmds.ls("RIG_"+self.side+"_UpperLeg"), query=True, translation=True, worldSpace=True)
        knee_pos = cmds.xform(cmds.ls("RIG_"+self.side+"_LowerLeg"), query=True, translation=True, worldSpace=True)
        foot_pos = cmds.xform(cmds.ls("RIG_"+self.side+"_Foot"), query=True, translation=True, worldSpace=True)
        cmds.move(knee_pos[0], knee_pos[1], knee_pos[2]+1, knee_ctrl_grp)

        # align the knee controller to the correct direction
        # create a polygon for knee controller align
        knee_ref_plane = cmds.polyCreateFacet(point=[(upper_leg_pos[0], upper_leg_pos[1], upper_leg_pos[2]), 
                                                (knee_pos[0], knee_pos[1], knee_pos[2]),
                                                (foot_pos[0], foot_pos[1], foot_pos[2])], name=self.side+'_knee_ref_plane')
        # align the controller grp to the polygon and delete the polygon
        cmds.normalConstraint(knee_ref_plane, knee_ctrl_grp, aimVector=[0, 1, 0], upVector=[1, 0, 0], worldUpType='scene')
        # delete the normal constraint and ref plane
        cmds.delete(knee_ref_plane)
        cmds.parent(knee_ctrl_grp, "MASTER_CONTROLLER")

        # foot
        foot_ctrl_shape = self.get_controller_shape("foot")
        foot_ctrl = cmds.curve(point=foot_ctrl_shape, degree=1, name="CTRL_"+self.side+"_Foot")
        cmds.addAttr(shortName="KF", longName="Knee_Fix", attributeType='double', defaultValue=0, 
                    minValue=0, maxValue=1, keyable=True)
        cmds.addAttr(shortName="FR", longName="Foot_Roll", attributeType='double', defaultValue=0, 
                    minValue=0, maxValue=100, keyable=True)  
        cmds.addAttr(shortName="BR", longName="Ball_Roll", attributeType='double', defaultValue=0, 
                    minValue=0, maxValue=100, keyable=True)       
                                      
        cmds.scale(0.08, 0.08, 0.08, foot_ctrl)
        cmds.move(foot_pos[0], 0, foot_pos[2], foot_ctrl)
        cmds.makeIdentity(foot_ctrl, apply=True, translate=1, rotate=1, scale=1)
        cmds.parent(foot_ctrl, "MASTER_CONTROLLER")             
                 
                    
def set_colors():
    cmds.setAttr('MASTER_CONTROLLER.overrideEnabled', 1)
    cmds.setAttr('MASTER_CONTROLLER.overrideRGBColors', 1)
    cmds.setAttr('MASTER_CONTROLLER.overrideColorRGB', 1, 1, 1)                                                    
                
                
def create_controller(spine_count, finger_count):
    create_master()
    create_pelvis()
    create_spines(spine_count)
    create_neck(spine_count)
    create_head()

    l_arm = ArmController(side="L")
    l_arm.create_clavicles(spine_count)
    l_arm.create_elbow()
    l_arm.create_wrists()
    l_arm.create_fingers(finger_count)

    r_arm = ArmController(side="R")
    r_arm.create_clavicles(spine_count)
    r_arm.create_elbow()
    r_arm.create_wrists()
    r_arm.create_fingers(finger_count)

    l_leg = LegController(side="L")
    l_leg.create_leg()

    r_leg = LegController(side="R")
    r_leg.create_leg()
    set_colors()
                
               
    