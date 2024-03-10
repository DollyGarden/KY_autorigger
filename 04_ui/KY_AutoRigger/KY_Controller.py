# ********************************************************************
#  content = create all controllers
#  version = 0.1.2
#  date = 2022-02-15
#  dependencies = Maya
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
    master_ctrl = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), radius=1, degree=1, s=16, name="MASTER_CONTROLLER")
    selection = cmds.select("MASTER_CONTROLLER.cv[1]", "MASTER_CONTROLLER.cv[3]","MASTER_CONTROLLER.cv[5]", 
                            "MASTER_CONTROLLER.cv[7]", "MASTER_CONTROLLER.cv[9]","MASTER_CONTROLLER.cv[11]",
                            "MASTER_CONTROLLER.cv[13]","MASTER_CONTROLLER.cv[15]")
    cmds.scale(0.7, 0.7, 0.7, selection)
    cmds.makeIdentity(master_ctrl, apply=True, t=1, r=1, s=1)

def create_pelvis():    
    # pelvis
    pelvis_ctrl = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), radius=1, degree=1, s=8, name="CTRL_PELVIS")
    root_pos    = cmds.xform(cmds.ls("RIG_ROOT", type='joint'), q=True, t=True, ws=True)
    cmds.move(root_pos[0], root_pos[1], root_pos[2], pelvis_ctrl)
    cmds.scale(0.5, 0.5, 0.5, pelvis_ctrl)
    cmds.makeIdentity(pelvis_ctrl, apply=True, t=1, r=1, s=1)
    cmds.parent(pelvis_ctrl, "MASTER_CONTROLLER")

# spine
def create_spines(spine_count):
    for i in range(0, spine_count):
        spine_pos  = cmds.xform(cmds.ls("RIG_SPINE_"+str(i)), q=True, t=True, ws=True)
        spine_ctrl = cmds.circle(nr=(0,1,0), c=(0,0,0), radius=1, s=8, name="CTRL_SPINE_"+str(i))
        cmds.move(spine_pos[0], spine_pos[1], spine_pos[2], spine_ctrl)
        cmds.scale (0.3, 0.3, 0.3, spine_ctrl)
        if i == 0:
            cmds.parent(spine_ctrl, "CTRL_PELVIS")
        else:
            cmds.parent(spine_ctrl, "CTRL_SPINE_"+str(i-1))
        cmds.makeIdentity(spine_ctrl, apply=True, t=1, r=1, s=1)
# neck
def create_neck(spine_count):
    neck_ctrl = cmds.circle(nr=(0,1,0),c=(0,0,0), radius=1, s=8, name="CTRL_NECK")
    neck_pos  = cmds.xform(cmds.ls("RIG_Neck_Start"), q=True, t=True, ws=True)
    cmds.scale (0.2,0.2,0.2,neck_ctrl)
    cmds.move(neck_pos[0], neck_pos[1], neck_pos[2], neck_ctrl)
    cmds.parent(neck_ctrl, "CTRL_SPINE_"+str(spine_count-1))
    cmds.makeIdentity(neck_ctrl, apply=True, t=1, r=1, s=1)
    
#  Head
def create_head():
    head_ctrl = cmds.circle(nr=(1,0,0),c=(0,0,0), radius=1,s=8, name="CTRL_HEAD")
    head_pos  = cmds.xform(cmds.ls("RIG_Neck_End"), q=True, t=True, ws=True)
    head_rot  = cmds.xform(cmds.ls("RIG_Neck_End"), q=True, ro=True, ws=True)
    cmds.scale(0.25, 0.25, 0.25, head_ctrl)
    cmds.move(head_pos[0], head_pos[1], head_pos[2], head_ctrl)
    cmds.rotate(head_rot[0], head_rot[1], head_rot[2], head_ctrl)
    cmds.parent(head_ctrl, "CTRL_NECK")
    cmds.makeIdentity(head_ctrl, apply=True, t=1, r=1, s=1)
    # jaw
    jaw = cmds.circle(nr=(0,1,0), c=(0,0,0), radius=0.2,s=8, name = "CTRL_JAW")
    jaw_start = cmds.xform(cmds.ls("RIG_Jaw_Start"), q=True, t=True, ws=True)
    jaw_end   = cmds.xform(cmds.ls("RIG_Jaw_End"), q=True, t=True, ws=True)
    jaw_rot   = cmds.xform(cmds.ls("RIG_Jaw_Start"), q=True, ro=True, ws=True)
    cmds.rotate(jaw_rot[0], jaw_rot[1], jaw_rot[2], jaw)
    cmds.move(jaw_end[0], jaw_end[1], jaw_end[2], jaw)
    cmds.move(jaw_start[0], jaw_start[1], jaw_start[2], "CTRL_JAW.scalePivot", "CTRL_JAW.rotatePivot")
    cmds.parent(jaw, "CTRL_HEAD")
    cmds.makeIdentity(jaw, apply=True, t=1, r=1, s=1)

class Controller(object):
    """Top parent of all Controllers. It has a variable "side" and a function "get_controller_shape" to
        get the controller curve shape data from the json file 'KY_ControllerShape.json'.

        Benefit: Don't need to get the controller shape from json in every controller creating function.

        TODO: 1) A function to add 3 group layer on controllers.
              2) Put all the other controller under this class.
    """
    def __init__(self, side):
        self.side = side

    def get_controller_shape(self, shape):
        """get controller shape point data from json file 'KY_ControllerShape.json'.
        Args:
            shape (string): Choose the controller shape in the json file
        Returns:
            list: A list of all the point position on the controller curve.
        Benefits:
            Putting all the curve point data in the json file can make the file more readable and better 
            for data organization.
        """
        # 
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
        clavicle = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), radius=1, s=12, name = "CTRL_"+self.side+"_Clavicle")
        selection_01 = cmds.select("CTRL_"+self.side+"_Clavicle.cv[4]", "CTRL_"+self.side+"_Clavicle.cv[10]")
        cmds.move(0, 0.3, 0, selection_01, r=True)
        selection_02 = cmds.select("CTRL_"+self.side+"_Clavicle.cv[3]", "CTRL_"+self.side+"_Clavicle.cv[5]",
                                   "CTRL_"+self.side+"_Clavicle.cv[9]", "CTRL_"+self.side+"_Clavicle.cv[11]")
        cmds.move(0, 0.2, 0, selection_02, r=True)
        cmds.makeIdentity(clavicle, apply=True, t=1, r=1, s=1)
        clavicle_grp = cmds.group(em=True, name="CTRL_GRP_"+self.side+"_Clavicle")
        cmds.parent(clavicle, clavicle_grp)
        # move the controller group
        cmds.scale(0.1, 0.2, 0.2, clavicle_grp)
        arm_pos = cmds.xform(cmds.ls("RIG_"+self.side+"_UpperArm"), q=True, t=True, ws=True)
        clavicle_pos = cmds.xform(cmds.ls("RIG_"+self.side+"_Clavicle"), q=True, t=True, ws=True)
        clavicle_rot = cmds.xform(cmds.ls("RIG_"+self.side+"_Clavicle"), q=True, ro=True, ws=True)
        cmds.rotate(clavicle_rot[0], clavicle_rot[1], clavicle_rot[2], clavicle_grp)
        cmds.move(arm_pos[0]-0.1, arm_pos[1]+0.125, arm_pos[2], clavicle_grp)
        cmds.move(clavicle_pos[0], clavicle_pos[1], clavicle_pos[2], "CTRL_"+self.side+"_Clavicle.scalePivot", "CTRL_"+self.side+"_Clavicle.rotatePivot")
        cmds.parent(clavicle_grp, "CTRL_SPINE_"+str(spine_count-1))

    # elbow
    def create_elbow(self):
        elbow_ctrl_shape = self.get_controller_shape("elbow")
        # Create elbow controller
        elbow = cmds.curve(p=elbow_ctrl_shape, degree=1, name="CTRL_"+self.side+"_Elbow")  
        elbow_grp = cmds.group(em=True, name="CTRL_GRP_"+self.side+"_Elbow")    
        cmds.parent(elbow, elbow_grp)
        cmds.scale(0.15, 0.15, 0.15, elbow_grp)
        upper_arm_pos = cmds.xform(cmds.ls("RIG_"+self.side+"_UpperArm"), q=True, t=True, ws=True)
        elbow_pos     = cmds.xform(cmds.ls("RIG_"+self.side+"_Elbow"), q=True, t=True, ws=True)
        wrist_pos     = cmds.xform(cmds.ls("RIG_"+self.side+"_Wrist"), q=True, t=True, ws=True)
        cmds.move(elbow_pos[0], elbow_pos[1], elbow_pos[2]-0.5, elbow_grp)

        # align the elbow controller to the correct direction
        # create a polygon for elbow controller align
        elbow_ref_plane = cmds.polyCreateFacet(p=[(upper_arm_pos[0], upper_arm_pos[1], upper_arm_pos[2]),
                                                    (elbow_pos[0], elbow_pos[1], elbow_pos[2]),
                                                    (wrist_pos[0], wrist_pos[1], wrist_pos[2])], name=self.side+'_elbow_ref_plane')
        # align the controller grp to the polygon and delete the polygon
        cmds.normalConstraint(elbow_ref_plane, elbow_grp, aimVector=[0, -1, 0], upVector=[1, 0, 0], worldUpType='scene')
        # delete the normal constraint and ref plane
        cmds.delete(elbow_ref_plane)
        cmds.parent(elbow_grp, "MASTER_CONTROLLER")

    # wrist
    def create_wrists(self):
        wrist_ctrl     = cmds.circle(nr=(1, 0, 0), c=(0, 0, 0), radius=1, s=16, name="CTRL_"+self.side+"_Wrist")
        wrist_ctrl_grp = cmds.group(em=True, name="CTRL_GRP_"+self.side+"_Wrist")
        cmds.parent(wrist_ctrl, wrist_ctrl_grp)
        cmds.scale(0.1, 0.1, 0.1, wrist_ctrl)

        wrist_pos = cmds.xform(cmds.ls("RIG_"+self.side+"_Wrist"), q=True, t=True, ws=True)
        wrist_rot = cmds.xform(cmds.ls("RIG_"+self.side+"_Wrist"), q=True, ws=True, ro=True)
        cmds.move(wrist_pos[0], wrist_pos[1], wrist_pos[2], wrist_ctrl_grp)
        cmds.rotate(wrist_rot[0], wrist_rot[1], wrist_rot[2], wrist_ctrl_grp)
        cmds.parent(wrist_ctrl_grp, "MASTER_CONTROLLER")
        
    # finger
    def create_fingers(self, finger_count):
        finger_ctrl_shape = self.get_controller_shape("finger")
        for finger_index in range(0, finger_count):
            for finger_joint in range(0, 3):
                finger_rot = cmds.xform(cmds.ls("RIG_"+self.side+"_Finger_"+str(finger_index)+"_"+str(finger_joint)), q=True, ws=True, ro=True)
                finger_pos = cmds.xform(cmds.ls("RIG_"+self.side+"_Finger_"+str(finger_index)+"_"+str(finger_joint)), q=True, ws=True, t=True)
                finger     = cmds.curve(p=finger_ctrl_shape, degree=1, name="CTRL_"+self.side+"_Finger_"+str(finger_index)+"_"+str(finger_joint))
                if self.side == 'R':
                    cmds.rotate(90, 0, 0, finger)
                else:
                    cmds.rotate(-90, 0, 0, finger)
                cmds.scale(0.1, 0.1, 0.1, finger)  
                
                finger_grp = cmds.group(em=True, n="CTRL_GRP_"+self.side+"_Finger_"+str(finger_index)+"_"+str(finger_joint))
                cmds.parent(finger, finger_grp)
                cmds.rotate(finger_rot[0], finger_rot[1], finger_rot[2], finger_grp)
                cmds.move(finger_pos[0], finger_pos[1], finger_pos[2], finger_grp)
                cmds.makeIdentity(finger, apply=True, t=1, r=1, s=1)

                if finger_joint > 0:
                    cmds.parent(finger_grp, "CTRL_"+self.side+"_Finger_"+str(finger_index)+"_"+str(finger_joint-1))
                else:
                    cmds.parent(finger_grp, "CTRL_"+self.side+"_Wrist")

       
# leg
class LegController(Controller):
    """Create all the leg controllers. Inherit the "side" variable and get_controller_shape function from the Controller class. 
       Benefit: Don't need to write left and right side codes separately.
    """
    def __init__(self, side):
        super(LegController, self).__init__(side)

    def create_leg(self):
        # knee
        knee_ctrl_shape = self.get_controller_shape("knee")
        knee_ctrl = cmds.curve(p=knee_ctrl_shape, degree=1, name="CTRL_"+self.side+"_Knee")  
        knee_ctrl_grp = cmds.group(em=True, name="CTRL_GRP_"+self.side+"_Knee")    
        cmds.parent(knee_ctrl, knee_ctrl_grp)
        cmds.scale(0.15, 0.15, 0.15, knee_ctrl_grp)
        upper_leg_pos = cmds.xform(cmds.ls("RIG_"+self.side+"_UpperLeg"), q=True, t=True, ws=True)
        knee_pos = cmds.xform(cmds.ls("RIG_"+self.side+"_LowerLeg"), q=True, t=True, ws=True)
        foot_pos = cmds.xform(cmds.ls("RIG_"+self.side+"_Foot"), q=True, t=True, ws=True)
        cmds.move(knee_pos[0], knee_pos[1], knee_pos[2]+1, knee_ctrl_grp)

        # align the knee controller to the correct direction
        # create a polygon for knee controller align
        knee_ref_plane = cmds.polyCreateFacet(p=[(upper_leg_pos[0], upper_leg_pos[1], upper_leg_pos[2]), 
                                                (knee_pos[0], knee_pos[1], knee_pos[2]),
                                                (foot_pos[0], foot_pos[1], foot_pos[2])], name=self.side+'_knee_ref_plane')
        # align the controller grp to the polygon and delete the polygon
        cmds.normalConstraint(knee_ref_plane, knee_ctrl_grp, aimVector=[0, 1, 0], upVector=[1, 0, 0], worldUpType='scene')
        # delete the normal constraint and ref plane
        cmds.delete(knee_ref_plane)
        cmds.parent(knee_ctrl_grp, "MASTER_CONTROLLER")

        # foot
        foot_ctrl_shape = self.get_controller_shape("foot")
        foot_ctrl = cmds.curve(p=foot_ctrl_shape, degree=1, name="CTRL_"+self.side+"_Foot")
        cmds.addAttr(shortName="KF", longName="Knee_Fix", attributeType='double', defaultValue=0, 
                    minValue=0, maxValue=1, keyable=True)
        cmds.addAttr(shortName="FR", longName="Foot_Roll", attributeType='double', defaultValue=0, 
                    minValue=0, maxValue=100, keyable=True)  
        cmds.addAttr(shortName="BR", longName="Ball_Roll", attributeType='double', defaultValue=0, 
                    minValue=0, maxValue=100, keyable=True)       
                                      
        cmds.scale(0.08, 0.08, 0.08, foot_ctrl)
        cmds.move(foot_pos[0], 0, foot_pos[2], foot_ctrl)
        cmds.makeIdentity(foot_ctrl, apply=True, t=1, r=1, s=1)
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
                
               
    