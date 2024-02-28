# ********************************************************************
#  content = create IK on arms, legs and feet
#  version = 0.1.2
#  date = 2022-02-15
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
    # arm IK
    if cmds.objExists("RIG_L_sec_armTwist_*"):
        cmds.ikHandle(name="IK_L_Arm", sj=cmds.ls("RIG_L_UpperArm")[0], ee=cmds.ls("RIG_L_sec_armTwist_0")[0], sol='ikRPsolver')
        cmds.ikHandle(name="IK_R_Arm", sj=cmds.ls("RIG_R_UpperArm")[0], ee=cmds.ls("RIG_R_sec_armTwist_0")[0], sol='ikRPsolver')
        # move the end of ik pivot to the wrist
        l_wrist_pos  = cmds.xform(cmds.ls("RIG_L_Wrist"), q = True, t = True, ws = True)
        l_arm_ik_end = cmds.ikHandle("IK_L_Arm", q=True, ee=True)
        cmds.move(l_wrist_pos[0], l_wrist_pos[1], l_wrist_pos[2], l_arm_ik_end+".scalePivot", l_arm_ik_end+".rotatePivot") 
        r_wrist_pos  = cmds.xform(cmds.ls("RIG_R_Wrist"), q=True, t=True, ws=True)
        r_arm_ik_end = cmds.ikHandle("IK_R_Arm", q=True, ee=True)
        cmds.move(r_wrist_pos[0], r_wrist_pos[1], r_wrist_pos[2], r_arm_ik_end+".scalePivot", r_arm_ik_end+".rotatePivot")    
    else:
        cmds.ikHandle(name="IK_L_Arm", sj=cmds.ls("RIG_L_UpperArm")[0], ee=cmds.ls("RIG_L_Wrist")[0], sol='ikRPsolver')
        cmds.ikHandle(name="IK_R_Arm", sj=cmds.ls("RIG_R_UpperArm")[0], ee=cmds.ls("RIG_R_Wrist")[0], sol='ikRPsolver')
        
    # leg IK
    cmds.ikHandle(name="IK_L_Leg", sj=cmds.ls("RIG_L_UpperLeg")[0], ee=cmds.ls("RIG_L_Foot")[0], sol='ikRPsolver')
    cmds.ikHandle(name="IK_R_Leg", sj=cmds.ls("RIG_R_UpperLeg")[0], ee=cmds.ls("RIG_R_Foot")[0], sol='ikRPsolver')
    
    # foot IK
    cmds.ikHandle(name="IK_L_FootBall", sj=cmds.ls("RIG_L_Foot")[0], ee=cmds.ls("RIG_L_FootBall")[0], sol='ikSCsolver')
    cmds.ikHandle(name="IK_L_Toes", sj=cmds.ls("RIG_L_FootBall")[0], ee=cmds.ls("RIG_L_Toes")[0], sol='ikSCsolver')
    cmds.ikHandle(name="IK_R_FootBall", sj=cmds.ls("RIG_R_Foot")[0], ee=cmds.ls("RIG_R_FootBall")[0], sol='ikSCsolver')
    cmds.ikHandle(name="IK_R_Toes", sj=cmds.ls("RIG_R_FootBall")[0], ee=cmds.ls("RIG_R_Toes")[0], sol='ikSCsolver')
    
    root_pos = cmds.xform(cmds.ls("RIG_ROOT", type='joint'), q=True, t=True, ws=True)
    spines   = cmds.ls("RIG_SPINE_*", type='joint')
    
    spine_pos_list = []
    for spine in spines:
        spine_pos_list.append(cmds.xform(spine, q=True, t=True, ws=True))

    if cmds.objExists('SpineCurve'):
        cmds.delete('SpineCurve')

    cmds.curve(p=[(root_pos[0], root_pos[1], root_pos[2])], n="SpineCurve", degree=1)
    
    for spine_pos in spine_pos_list:
        cmds.curve('SpineCurve', a=True, p=[(spine_pos[0], spine_pos[1], spine_pos[2])])
        
    curve_cv = cmds.ls('SpineCurve.cv[0:]', fl=True)
        
    for k, cv in enumerate(curve_cv):
        c = cmds.cluster(cv, cv, n="Cluster_"+str(k)+"_")
        
        if k > 0:
            cmds.parent(c, "Cluster_"+str(k-1)+"_Handle")    
            
    spine_amount = cmds.ls("RIG_SPINE_*")       
    cmds.ikHandle(n="Ik_Spine", sj="RIG_ROOT", ee="RIG_SPINE_"+ str(len(spine_amount) - 1), 
                  sol='ikSplineSolver', c='SpineCurve', ccv=False)