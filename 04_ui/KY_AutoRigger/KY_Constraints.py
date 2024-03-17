# ********************************************************************
#  content = create ui functions
#  version = 0.1.4
#  date = 2022-03-18
#  dependencies = Maya
# 
#  license = MIT
#  author = Kelly Yang <kelly.yang1116@hotmail.com>
# ********************************************************************


import importlib

import maya.cmds as cmds

from KY_AutoRigger import KY_SetAttributes

importlib.reload(KY_SetAttributes)

def create_constrains(spine_count, finger_count):
    """Create constrains for arms, legs, head, finger and feet.

    Args:
        spine_count (int): number of spines
        finger_count (int): number of fingers

    """
    # spine constraints
    clusters   = cmds.ls("Cluster_*", type='transform')
    spine_ctrl = cmds.ls("CTRL_SPINE_*", type='transform')
    for spine_ctrl_index, cluster in enumerate(clusters):
        if spine_ctrl_index > 0:
            cmds.parent(cluster, spine_ctrl[spine_ctrl_index-1])
        else:
            cmds.parent(cluster, "CTRL_PELVIS")

    # head
    cmds.orientConstraint("CTRL_NECK", "RIG_Neck_Start", maintainOffset=True)
    cmds.orientConstraint("CTRL_HEAD", "RIG_Neck_End", maintainOffset=True)
    cmds.orientConstraint("CTRL_JAW", "RIG_Jaw_Start", maintainOffset=True)

    sides = ['L', 'R']
    for side in sides:

        # arm constraints
        cmds.orientConstraint("CTRL_"+side+"_Clavicle", "RIG_"+side+"_Clavicle", maintainOffset=True)
        wrist_ctrl  = cmds.ls("CTRL_"+side+"_Wrist", type='transform')
        wrist_ik    = cmds.ls("IK_"+side+"_Arm")
        wrist_joint = cmds.ls("RIG_"+side+"_Wrist")
        cmds.pointConstraint(wrist_ctrl, wrist_ik, maintainOffset=True)
        cmds.orientConstraint(wrist_ctrl, wrist_joint, maintainOffset=True)
        cmds.poleVectorConstraint("CTRL_"+side+"_Elbow", "IK_"+side+"_Arm")
        
        if cmds.objExists("RIG_"+side+"_sec_armTwist_0"):
            twist_joints = cmds.ls("RIG_"+side+"_sec_armTwist_*")
            if cmds.objExists(side+'_sec_armTwist_Node_*'):
                cmds.delete(side+'_sec_armTwist_Node_*')

            for index, twist_joint in enumerate(twist_joints):
                wrist_multiply = cmds.shadingNode("multiplyDivide", asUtility=True, n=side+"_sec_armTwist_Node_"+str(index))
                cmds.setAttr(wrist_multiply+".operation", 1)
                cmds.setAttr(wrist_multiply+".input2X", (1.0-(1.0/len(twist_joints)*(index+1)))*-1)
                # input
                cmds.connectAttr("CTRL_"+side+"_Wrist. rotateX", side+"_sec_armTwist_Node_"+str(index)+".input1X")
                # output
                cmds.connectAttr(side+"_sec_armTwist_Node_"+str(index)+".outputX", "RIG_"+side+"_sec_armTwist_"+str(index)+".rotateX")

        # finger constraints       
        for finger_index in range(0, finger_count):
            l_all_fingers = cmds.ls("RIG_"+side+"_Finger_"+str(finger_index)+"_*")        
            for finger_joints in range(0, 3):
                cmds.connectAttr("CTRL_"+side+"_Finger_"+str(finger_index)+"_"+str(finger_joints)+".rotateZ", l_all_fingers[finger_joints]+".rotateZ")
                if finger_joints == 0:
                    cmds.connectAttr("CTRL_"+side+"_Finger_"+str(finger_index)+"_"+str(finger_joints)+".rotateY", l_all_fingers[finger_joints]+".rotateY")
                    cmds.connectAttr("CTRL_"+side+"_Finger_"+str(finger_index)+"_"+str(finger_joints)+".rotateY", l_all_fingers[finger_joints]+".rotateX")

        # feet constraints
        if cmds.objExists("RIG_"+side+"_sec_INV_Heel"):
            cmds.pointConstraint("RIG_"+side+"_sec_INV_Toes", "IK_"+side+"_Toes", maintainOffset=True)
            cmds.pointConstraint("RIG_"+side+"_sec_INV_Ball", "IK_"+side+"_FootBall", maintainOffset=True)
            cmds.pointConstraint("RIG_"+side+"_sec_INV_Ankle", "IK_"+side+"_Leg", maintainOffset=True)
            cmds.pointConstraint("CTRL_"+side+"_Foot", "RIG_"+side+"_sec_INV_Heel", maintainOffset=True)
            cmds.orientConstraint("CTRL_"+side+"_Foot", "RIG_"+side+"_sec_INV_Heel", maintainOffset=True)
            cmds.connectAttr("CTRL_"+side+"_Foot.Foot_Roll", "RIG_"+side+"_sec_INV_Ball.rotateZ")
            cmds.connectAttr("CTRL_"+side+"_Foot.Ball_Roll", "RIG_"+side+"_sec_INV_Toes.rotateZ")
            
        else:
            cmds.parent("IK_"+side+"_Toes", "IK_"+side+"_FootBall")
            cmds.parent("IK_"+side+"_FootBall", "IK_"+side+"_Leg")
            cmds.pointConstraint("CTRL_"+side+"_Foot", "IK_"+side+"_Leg", maintainOffset=True)
            cmds.orientConstraint("CTRL_"+side+"_Foot", "IK_"+side+"_Leg", maintainOffset=True)
            
            
        # knee constraints
        cmds.poleVectorConstraint("CTRL_"+side+"_Knee", "IK_"+side+"_Leg")
        cmds.parentConstraint("CTRL_"+side+"_Foot", "CTRL_GRP_"+side+"_Knee", name="CTRL_GRP_"+side+"_Knee_parentConstraint", maintainOffset=True)
        cmds.connectAttr("CTRL_"+side+"_Foot.Knee_Fix", "CTRL_GRP_"+side+"_Knee_parentConstraint.CTRL_"+side+"_FootW0")
        
        
    KY_SetAttributes.lock_attributes()
    
    # set display layer
    if cmds.objExists("RIG_LAYER"):
        cmds.select("GRP_RIG")
        cmds.editDisplayLayerMembers("RIG_LAYER", "GRP_RIG")      
    else:
        cmds.select("GRP_RIG")
        cmds.createDisplayLayer(noRecurse=True, name="RIG_LAYER")     
        
    iks = cmds.ls("IK_*")
    cmds.editDisplayLayerMembers("RIG_LAYER", iks)
    
    if cmds.objExists("CONTROLLERS_LAYER"):
        cmds.select("MASTER_CONTROLLER")
        cmds.editDisplayLayerMembers("CONTROLLERS_LAYER", "MASTER_CONTROLLER")
    else:
        cmds.select("MASTER_CONTROLLER")
        cmds.createDisplayLayer(noRecurse=True, name="CONTROLLERS_LAYER")
