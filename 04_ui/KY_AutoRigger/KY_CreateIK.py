# ********************************************************************
#  content = create IK on arms, legs and fendEffectort
#  version = 0.1.4
#  date = 2022-03-18
#  dependencies = Maya
# 
#  license = MIT
#  author = Kelly Yang <kelly.yang1116@hotmail.com>
# ********************************************************************


import importlib

import maya.cmds as cmds

from KY_AutoRigger import KY_Locators

importlib.reload(KY_Locators)

def ik_handles():

    # spine IK
    root_pos = cmds.xform(cmds.ls("RIG_ROOT", type='joint'), query=True, translation=True, worldSpace=True)
    spines   = cmds.ls("RIG_SPINE_*", type='joint')
    
    spine_pos_list = []
    for spine in spines:
        spine_pos_list.append(cmds.xform(spine, query=True, translation=True, worldSpace=True))

    if cmds.objExists('SpineCurve'):
        cmds.delete('SpineCurve')

    cmds.curve(name="SpineCurve", point=[(root_pos[0], root_pos[1], root_pos[2])], degree=1)
    
    for spine_pos in spine_pos_list:
        cmds.curve("SpineCurve", append=True, point=[(spine_pos[0], spine_pos[1], spine_pos[2])])
        
    curve_cv_list = cmds.ls('SpineCurve.cv[0:]', fl=True)
        
    for cv_index, cv in enumerate(curve_cv_list):
        cmds.cluster(cv, cv, name="Cluster_"+str(cv_index)+"_")

        if cv_index > 0:
            cmds.parent("Cluster_"+str(cv_index)+"_Handle", "Cluster_"+str(cv_index-1)+"_Handle")    
            
    spine_amount = cmds.ls("RIG_SPINE_*")       
    cmds.ikHandle(name="Ik_Spine", startJoint="RIG_ROOT", endEffector="RIG_SPINE_"+str(len(spine_amount)-1), 
                  solver='ikSplineSolver', curve='SpineCurve', createCurve=False)

    sides = ["L", "R"]
    for side in sides:
        # arm IK
        if cmds.objExists("RIG_"+side+"_sec_armTwist_*"):
            cmds.ikHandle(name="IK_"+side+"_Arm", startJoint=cmds.ls("RIG_"+side+"_UpperArm")[0], endEffector=cmds.ls("RIG_"+side+"_sec_armTwist_0")[0], solver='ikRPsolver')
            # move the end of ik pivot to the wrist
            wrist_pos  = cmds.xform(cmds.ls("RIG_"+side+"_Wrist"), query=True, translation=True, worldSpace=True)
            arm_ik_end = cmds.ikHandle("IK_"+side+"_Arm", query=True, endEffector=True)
            cmds.move(wrist_pos[0], wrist_pos[1], wrist_pos[2], arm_ik_end+".scalePivot", arm_ik_end+".rotatePivot") 
        else:
            cmds.ikHandle(name="IK_"+side+"_Arm", startJoint=cmds.ls("RIG_"+side+"_UpperArm")[0], endEffector=cmds.ls("RIG_"+side+"_Wrist")[0], solver='ikRPsolver')
            
        # leg IK
        cmds.ikHandle(name="IK_"+side+"_Leg", startJoint=cmds.ls("RIG_"+side+"_UpperLeg")[0], endEffector=cmds.ls("RIG_"+side+"_Foot")[0], solver='ikRPsolver')
        
        # foot IK
        cmds.ikHandle(name="IK_"+side+"_FootBall", startJoint=cmds.ls("RIG_"+side+"_Foot")[0], endEffector=cmds.ls("RIG_"+side+"_FootBall")[0], solver='ikSCsolver')
        cmds.ikHandle(name="IK_"+side+"_Toes", startJoint=cmds.ls("RIG_"+side+"_FootBall")[0], endEffector=cmds.ls("RIG_"+side+"_Toes")[0], solver='ikSCsolver')
    
    