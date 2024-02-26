# ********************************************************************
#  content = create ui functions
#  version = 0.1.2
#  date = 2022-02-15
#  dependencies = Maya
# 
#  license = MIT
#  author = Kelly Yang <kelly.yang1116@hotmail.com>
# ********************************************************************


import importlib

import maya.cmds as cmds

from KY_AutoRigger import KY_SetAttributes

importlib.reload(KY_SetAttributes)

def create_constrains(finger_count, spine_amount):
    """Create constrains for arms, legs, head, finger and feet.

    Args:
        finger_count (int): How many fingers in the rig?
        spine_amount (int): How many spines in the rig?
    """
    # left arm
    cmds.orientConstraint("CTRL_L_Clavicle", "RIG_L_Clavicle", mo=True)
    l_wrist_ctrl  = cmds.ls("CTRL_L_Wrist", type='transform')
    l_wrist_ik    = cmds.ls("IK_L_Arm")
    l_wrist_joint = cmds.ls("RIG_L_Wrist")
    cmds.pointConstraint(l_wrist_ctrl, l_wrist_ik, mo=True)
    cmds.orientConstraint(l_wrist_ctrl, l_wrist_joint, mo=True)
    cmds.poleVectorConstraint("CTRL_L_Elbow", "IK_L_Arm")
    
    if cmds.objExists("RIG_L_sec_armTwist_0"):
        l_twist_joints = cmds.ls("RIG_L_sec_armTwist_*")
        if cmds.objExists('L_sec_armTwist_Node_*'):
            cmds.delete('L_sec_armTwist_Node_*')
        for i in enumerate(l_twist_joints):
            l_wrist_multiply = cmds.shadingNode("multiplyDivide", asUtility=True, n="L_sec_armTwist_Node_"+str(i))
            cmds.setAttr(l_wrist_multiply+".operation", 1)
            cmds.setAttr(l_wrist_multiply+".input2X", (1.0-(1.0/len(l_twist_joints)*(i+1)))*-1)
            # input
            cmds.connectAttr("CTRL_L_Wrist. rotateX", "L_sec_armTwist_Node_"+str(i)+".input1X")
            # output
            cmds.connectAttr("L_sec_armTwist_Node_"+str(i)+".outputX", "RIG_L_sec_armTwist_"+str(i)+".rotateX")
    
    # right arm
    cmds.orientConstraint("CTRL_R_Clavicle", "RIG_R_Clavicle", mo=True)
    r_wrist_ctrl  = cmds.ls("CTRL_R_Wrist", type='transform')
    r_wrist_ik    = cmds.ls("IK_R_Arm")
    r_wrist_joint = cmds.ls("RIG_R_Wrist")
    cmds.pointConstraint(r_wrist_ctrl, r_wrist_ik, mo=True)
    cmds.orientConstraint(r_wrist_ctrl, r_wrist_joint, mo=True)
    cmds.poleVectorConstraint("CTRL_R_Elbow", "IK_R_Arm")
    
    if cmds.objExists("RIG_R_sec_armTwist_0"):
        r_twist_joints = cmds.ls("RIG_R_sec_armTwist_*")
        if cmds.objExists('R_sec_armTwist_Node_*'):
            cmds.delete('R_sec_armTwist_Node_*')
        for i in enumerate(r_twist_joints):
            r_wrist_multiply = cmds.shadingNode("multiplyDivide", asUtility=True, n="R_sec_armTwist_Node_"+str(i))
            cmds.setAttr(r_wrist_multiply+".operation", 1)
            cmds.setAttr(r_wrist_multiply+".input2X", (1.0-(1.0/len(r_twist_joints)*(i+1)))*-1)
            # input
            cmds.connectAttr("CTRL_R_Wrist.rotateX", "R_sec_armTwist_Node_"+str(i)+".input1X")
            # output
            cmds.connectAttr("R_sec_armTwist_Node_"+str(i)+".outputX", "RIG_R_sec_armTwist_"+str(i)+".rotateX")
    
    # spine
    clusters   = cmds.ls("Cluster_*", type='transform')
    spine_ctrl = cmds.ls("CTRL_SPINE_*", type='transform')
    for j, cl in enumerate(clusters):
        if j > 0:
            cmds.parent(cl, spine_ctrl[j-1])
        else:
            cmds.parent(cl, "CTRL_PELVIS")
            
    # finger        
    for k in range(0, finger_count):
        l_all_fingers = cmds.ls("RIG_L_Finger_"+str(k)+"_*")        
        r_all_fingers = cmds.ls("RIG_R_Finger_"+str(k)+"_*")  
        for l in range(0, 3):
            cmds.connectAttr("CTRL_L_Finger_"+str(k)+"_"+str(l)+".rotateZ", l_all_fingers[l]+".rotateZ")
            cmds.connectAttr("CTRL_R_Finger_"+str(k)+"_"+str(l)+".rotateZ", r_all_fingers[l]+".rotateZ")
            if l == 0:
                cmds.connectAttr("CTRL_L_Finger_"+str(k)+"_"+str(l)+".rotateY", l_all_fingers[l]+".rotateY")
                cmds.connectAttr("CTRL_R_Finger_"+str(k)+"_"+str(l)+".rotateY", r_all_fingers[l]+".rotateY")
                cmds.connectAttr("CTRL_L_Finger_"+str(k)+"_"+str(l)+".rotateY", l_all_fingers[l]+".rotateX")
                cmds.connectAttr("CTRL_R_Finger_"+str(k)+"_"+str(l)+".rotateY", r_all_fingers[l]+".rotateX")

    # head
    cmds.orientConstraint("CTRL_NECK", "RIG_Neck_Start", mo=True)
    cmds.orientConstraint("CTRL_HEAD", "RIG_Neck_End", mo=True)
    cmds.orientConstraint("CTRL_JAW", "RIG_Jaw_Start", mo=True)
    
    # feet
    if cmds.objExists("RIG_L_sec_INV_Heel"):
        cmds.pointConstraint("RIG_L_sec_INV_Toes", "IK_L_Toes", mo=True)
        cmds.pointConstraint("RIG_L_sec_INV_Ball", "IK_L_FootBall", mo=True)
        cmds.pointConstraint("RIG_L_sec_INV_Ankle", "IK_L_Leg", mo=True)
        cmds.pointConstraint("CTRL_L_Foot", "RIG_L_sec_INV_Heel", mo=True)
        cmds.orientConstraint("CTRL_L_Foot", "RIG_L_sec_INV_Heel", mo=True)
        cmds.connectAttr("CTRL_L_Foot.Foot_Roll", "RIG_L_sec_INV_Ball.rotateY")
        cmds.connectAttr("CTRL_L_Foot.Ball_Roll", "RIG_L_sec_INV_Toes.rotateY")
        
        cmds.pointConstraint("RIG_R_sec_INV_Toes", "IK_R_Toes", mo=True)
        cmds.pointConstraint("RIG_R_sec_INV_Ball", "IK_R_FootBall", mo=True)
        cmds.pointConstraint("RIG_R_sec_INV_Ankle", "IK_R_Leg", mo=True)
        cmds.pointConstraint("CTRL_R_Foot", "RIG_R_sec_INV_Heel", mo=True)
        cmds.orientConstraint("CTRL_R_Foot", "RIG_R_sec_INV_Heel", mo=True)
        cmds.connectAttr("CTRL_R_Foot.Foot_Roll", "RIG_R_sec_INV_Ball.rotateY")
        cmds.connectAttr("CTRL_R_Foot.Ball_Roll", "RIG_R_sec_INV_Toes.rotateY")
    else:
        cmds.parent("IK_L_Toes", "IK_L_FootBall")
        cmds.parent("IK_L_FootBall", "IK_L_Leg")
        cmds.pointConstraint("CTRL_L_Foot", "IK_L_Leg", mo=True)
        cmds.orientConstraint("CTRL_L_Foot", "IK_L_Leg", mo=True)
        
        cmds.parent("IK_R_Toes", "IK_R_FootBall")
        cmds.parent("IK_R_FootBall", "IK_R_Leg")
        cmds.pointConstraint("CTRL_R_Foot", "IK_R_Leg", mo=True)
        cmds.orientConstraint("CTRL_R_Foot", "IK_R_Leg", mo=True)
        
    # left knee attribute setting
    cmds.poleVectorConstraint("CTRL_L_Knee", "IK_L_Leg")
    cmds.parentConstraint('CTRL_L_Foot', 'CTRL_GRP_L_Knee', name='CTRL_GRP_L_Knee_parentConstraint', mo=True)
    cmds.connectAttr("CTRL_L_Foot.Knee_Fix", "CTRL_GRP_L_Knee_parentConstraint.CTRL_L_FootW0")
    
    # right knee attribute setting
    cmds.poleVectorConstraint("CTRL_R_Knee", "IK_R_Leg")
    cmds.parentConstraint('CTRL_R_Foot', 'CTRL_GRP_R_Knee', name='CTRL_GRP_R_Knee_parentConstraint', mo=True)
    cmds.connectAttr("CTRL_R_Foot.Knee_Fix", "CTRL_GRP_R_Knee_parentConstraint.CTRL_R_FootW0")
    
    KY_SetAttributes.lock_attributes()
    
    # set display layer
    if cmds.objExists("RIG_LAYER"):
        cmds.select("GRP_RIG")
        cmds.editDisplayLayerMembers("RIG_LAYER", "GRP_RIG")      
    else:
        cmds.select("GRP_RIG")
        cmds.createDisplayLayer(nr=True, name="RIG_LAYER")     
        
    iks = cmds.ls("IK_*")
    cmds.editDisplayLayerMembers("RIG_LAYER", iks)
    
    if cmds.objExists("CONTROLLERS_LAYER"):
        cmds.select("MASTER_CONTROLLER")
        cmds.editDisplayLayerMembers("CONTROLLERS_LAYER", "MASTER_CONTROLLER")
    else:
        cmds.select("MASTER_CONTROLLER")
        cmds.createDisplayLayer(nr=True, name="CONTROLLERS_LAYER")
