#********************************************************************
# content = create all controllers
# version = 0.1.2
# date = 2022-02-15
# dependencies = Maya
#
# license = MIT
# author = Kelly Yang <kelly.yang1116@hotmail.com>
#********************************************************************

import maya.cmds as cmds

def create_master():
    #master
    master_ctrl = cmds.circle(nr=(0, 1, 0),c=(0, 0, 0), radius=1, degree=1, s=16, name="MASTER_CONTROLLER")
    selection = cmds.select("MASTER_CONTROLLER.cv[1]", "MASTER_CONTROLLER.cv[3]","MASTER_CONTROLLER.cv[5]", 
                            "MASTER_CONTROLLER.cv[7]", "MASTER_CONTROLLER.cv[9]","MASTER_CONTROLLER.cv[11]",
                            "MASTER_CONTROLLER.cv[13]","MASTER_CONTROLLER.cv[15]")
    cmds.scale(0.7, 0.7, 0.7, selection)
    cmds.makeIdentity(master_ctrl, apply=True, t=1, r=1, s=1)

def create_pelvis():    
    #pelvis
    pelvis_ctrl = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), radius=1, degree=1, s=8, name="CTRL_PELVIS")
    root_pos    = cmds.xform(cmds.ls("RIG_ROOT", type='joint'), q=True, t=True, ws=True)
    cmds.move(root_pos[0], root_pos[1], root_pos[2], pelvis_ctrl)
    cmds.scale(0.5, 0.5, 0.5, pelvis_ctrl)
    cmds.makeIdentity(pelvis_ctrl, apply=True, t=1, r=1, s=1)
    cmds.parent(pelvis_ctrl, "MASTER_CONTROLLER")

#spine
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
#neck
def create_neck(spine_count):
    neck_ctrl = cmds.circle(nr=(0,1,0),c=(0,0,0), radius=1,s=8, name="CTRL_NECK")
    neck_pos  = cmds.xform(cmds.ls("RIG_Neck_Start"), q=True, t=True, ws=True)
    cmds.scale (0.2,0.2,0.2,neck_ctrl)
    cmds.move(neck_pos[0], neck_pos[1], neck_pos[2], neck_ctrl)
    cmds.parent(neck_ctrl, "CTRL_SPINE_"+str(spine_count-1))
    cmds.makeIdentity(neck_ctrl, apply=True, t=1, r=1, s=1)
    
# Head
def create_head():
    head_ctrl = cmds.circle(nr=(1,0,0),c=(0,0,0), radius=1,s=8, name="CTRL_HEAD")
    head_pos  = cmds.xform(cmds.ls("RIG_Neck_End"), q=True, t=True, ws=True)
    head_rot  = cmds.xform(cmds.ls("RIG_Neck_End"), q=True, ro=True, ws=True)
    cmds.scale(0.25, 0.25, 0.25, head_ctrl)
    cmds.move(head_pos[0], head_pos[1], head_pos[2], head_ctrl)
    cmds.rotate(head_rot[0], head_rot[1], head_rot[2], head_ctrl)
    cmds.parent(head_ctrl, "CTRL_NECK")
    cmds.makeIdentity(head_ctrl, apply=True, t=1, r=1, s=1)
    #jaw
    jaw = cmds.circle(nr=(0,1,0), c=(0,0,0), radius=0.2,s=8, name = "CTRL_JAW")
    jaw_start = cmds.xform(cmds.ls("RIG_Jaw_Start"), q=True, t=True, ws=True)
    jaw_end   = cmds.xform(cmds.ls("RIG_Jaw_End"), q=True, t=True, ws=True)
    jaw_rot   = cmds.xform(cmds.ls("RIG_Jaw_Start"), q=True, ro=True, ws=True)
    cmds.rotate(jaw_rot[0], jaw_rot[1], jaw_rot[2], jaw)
    cmds.move(jaw_end[0], jaw_end[1], jaw_end[2], jaw)
    cmds.move(jaw_start[0], jaw_start[1], jaw_start[2], "CTRL_JAW.scalePivot", "CTRL_JAW.rotatePivot")
    cmds.parent(jaw, "CTRL_HEAD")
    cmds.makeIdentity(jaw, apply=True, t=1, r=1, s=1)


def create_clavicles(spine_count):
    #left clavicle
    #create controller
    l_clavicle = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), radius=1, s=12, name = "CTRL_L_Clavicle")
    selection_01 = cmds.select("CTRL_L_Clavicle.cv[4]", "CTRL_L_Clavicle.cv[10]")
    cmds.move(0, 0.3, 0, selection_01, r=True)
    selection_02 = cmds.select("CTRL_L_Clavicle.cv[3]", "CTRL_L_Clavicle.cv[5]", "CTRL_L_Clavicle.cv[9]", "CTRL_L_Clavicle.cv[11]")
    cmds.move(0, 0.2, 0, selection_02, r=True)
    cmds.makeIdentity(l_clavicle, apply=True, t=1, r=1, s=1)
    l_clavicle_grp = cmds.group(em=True, name='CTRL_GRP_L_Clavicle')
    cmds.parent(l_clavicle, l_clavicle_grp)
    #move the controller group
    cmds.scale(0.1, 0.2, 0.2, l_clavicle_grp)
    l_arm_pos = cmds.xform(cmds.ls("RIG_L_UpperArm"), q=True, t=True, ws=True)
    l_clavicle_pos = cmds.xform(cmds.ls("RIG_L_Clavicle"), q=True, t=True, ws=True)
    l_clavicle_rot = cmds.xform(cmds.ls("RIG_L_Clavicle"), q=True, ro=True, ws=True)
    cmds.rotate(l_clavicle_rot[0], l_clavicle_rot[1], l_clavicle_rot[2], l_clavicle_grp)
    cmds.move(l_arm_pos[0]-0.1, l_arm_pos[1]+0.125, l_arm_pos[2], l_clavicle_grp)
    cmds.move(l_clavicle_pos[0], l_clavicle_pos[1], l_clavicle_pos[2], "CTRL_L_Clavicle.scalePivot", "CTRL_L_Clavicle.rotatePivot")
    cmds.parent(l_clavicle_grp, "CTRL_SPINE_"+str(spine_count-1))
    
    #right clavicle
    #create controller
    r_clavicle = cmds.circle(nr=(0, -1, 0), c=(0, 0, 0), radius=1, s=12, name="CTRL_R_Clavicle")
    selection_01 = cmds.select("CTRL_R_Clavicle.cv[4]", "CTRL_R_Clavicle.cv[10]")
    cmds.move(0, -0.3, 0, selection_01, r=True)
    selection_02 = cmds.select("CTRL_R_Clavicle.cv[3]", "CTRL_R_Clavicle.cv[5]", "CTRL_R_Clavicle.cv[9]", "CTRL_R_Clavicle.cv[11]")
    cmds.move(0, -0.2, 0, selection_02, r=True)
    cmds.makeIdentity(r_clavicle, apply=True, t=1, r=1, s=1)
    r_clavicle_grp = cmds.group(em=True, name='CTRL_GRP_R_Clavicle') 
    cmds.parent(r_clavicle, r_clavicle_grp)
    #move the controller
    cmds.scale(0.1, 0.2, 0.2, r_clavicle_grp)
    r_arm_pos = cmds.xform(cmds.ls("RIG_R_UpperArm"), q=True, t=True, ws=True)
    r_clavicle_pos = cmds.xform(cmds.ls("RIG_R_Clavicle"), q=True, t=True, ws=True)
    r_clavicle_rot = cmds.xform(cmds.ls("RIG_R_Clavicle"), q=True, ro=True, ws=True)
    cmds.rotate(r_clavicle_rot[0], r_clavicle_rot[1], r_clavicle_rot[2], r_clavicle_grp)
    cmds.move(r_arm_pos[0]+0.1, r_arm_pos[1]+0.125, r_arm_pos[2], r_clavicle_grp)
    cmds.move(r_clavicle_pos[0], r_clavicle_pos[1], r_clavicle_pos[2], "CTRL_R_Clavicle.scalePivot", "CTRL_R_Clavicle.rotatePivot")
    cmds.parent(r_clavicle_grp, "CTRL_SPINE_"+str(spine_count-1))

#elbow
def create_elbow():
    #left elbow
    l_elbow = cmds.curve(p=[[0.0, 1.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, 0.0], 
                            [-1.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0], 
                            [0.0, 0.0, -1.0], [0.0, 0.0, 1.0]], degree=1, name="CTRL_L_Elbow")  
    l_elbow_grp = cmds.group(em=True, name='CTRL_GRP_L_Elbow')    
    cmds.parent(l_elbow, l_elbow_grp)
    cmds.scale(0.15, 0.15, 0.15, l_elbow_grp)
    l_upper_arm_pos = cmds.xform(cmds.ls("RIG_L_UpperArm"), q=True, t=True, ws=True)
    l_elbow_pos     = cmds.xform(cmds.ls("RIG_L_Elbow"), q=True, t=True, ws=True)
    l_wrist_pos     = cmds.xform(cmds.ls("RIG_L_Wrist"), q=True, t=True, ws=True)
    cmds.move(l_elbow_pos[0], l_elbow_pos[1], l_elbow_pos[2]-0.5, l_elbow_grp)

    #align the elbow controller to the correct direction
    #create a polygon for elbow controller align
    l_elbow_ref_plane = cmds.polyCreateFacet(p=[(l_upper_arm_pos[0], l_upper_arm_pos[1], l_upper_arm_pos[2]),
                                                (l_elbow_pos[0], l_elbow_pos[1], l_elbow_pos[2]),
                                                (l_wrist_pos[0], l_wrist_pos[1], l_wrist_pos[2])], name='L_elbow_ref_plane')
    #align the controller grp to the polygon and delete the polygon
    cmds.normalConstraint(l_elbow_ref_plane, l_elbow_grp, aimVector=[0, -1, 0], upVector=[1, 0, 0], worldUpType='scene')
    #delete the normal constraint and ref plane
    cmds.delete(l_elbow_ref_plane)
    cmds.parent(l_elbow_grp, "MASTER_CONTROLLER")

     #right elbow
    r_elbow = cmds.curve(p=[[0.0, 1.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, 0.0], 
                            [-1.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0], 
                            [0.0, 0.0, -1.0],[0.0, 0.0, 1.0]], degree=1, name="CTRL_R_Elbow")  
    r_elbow_grp = cmds.group(em=True, name='CTRL_GRP_R_Elbow')    
    cmds.parent(r_elbow, r_elbow_grp)
    cmds.scale(0.15, 0.15, 0.15, r_elbow_grp)
    r_upper_arm_pos = cmds.xform(cmds.ls("RIG_R_UpperArm"), q=True, t=True, ws=True)
    r_elbow_pos     = cmds.xform(cmds.ls("RIG_R_Elbow"), q=True, t=True, ws=True)
    r_wrist_pos     = cmds.xform(cmds.ls("RIG_R_Wrist"), q=True, t=True, ws=True)
    cmds.move(r_elbow_pos[0], r_elbow_pos[1], r_elbow_pos[2]-0.5, r_elbow_grp)

    #align the elbow controller to the correct direction
    #create a polygon for elbow controller align
    r_elbow_ref_plane = cmds.polyCreateFacet(p=[(r_upper_arm_pos[0], r_upper_arm_pos[1], r_upper_arm_pos[2]), 
                                                (r_elbow_pos[0], r_elbow_pos[1], r_elbow_pos[2]),
                                                (r_wrist_pos[0], r_wrist_pos[1], r_wrist_pos[2])], name='R_elbow_ref_plane')
    #align the controller grp to the polygon and delet the polygon
    cmds.normalConstraint(r_elbow_ref_plane, r_elbow_grp, aimVector=[0, 1, 0], upVector=[1, 0, 0], worldUpType='scene')
    #delete the normal constraint and ref plane
    cmds.delete(r_elbow_ref_plane)
    cmds.parent(r_elbow_grp, "MASTER_CONTROLLER")
          
#wrist
def create_wrists():
    sides = ['L','R']
    for side in sides:
        wrist_ctrl = cmds.circle(nr=(1, 0, 0), c=(0, 0, 0), radius=1, s=16, name="CTRL_"+side+"_Wrist")
        wrist_ctrl_grp = cmds.group(em=True, name="CTRL_GRP_"+side+"_Wrist")
        cmds.parent(wrist_ctrl, wrist_ctrl_grp)
        cmds.scale(0.1, 0.1, 0.1, wrist_ctrl)

        wrist_pos = cmds.xform(cmds.ls("RIG_"+side+"_Wrist"), q=True, t=True, ws=True)
        wrist_rot = cmds.xform(cmds.ls("RIG_"+side+"_Wrist"), q=True, ws=True, ro=True)
        cmds.move(wrist_pos[0], wrist_pos[1], wrist_pos[2], wrist_ctrl_grp)
        cmds.rotate(wrist_rot[0], wrist_rot[1], wrist_rot[2], wrist_ctrl_grp)
        cmds.parent(wrist_ctrl_grp, "MASTER_CONTROLLER")
    
#finger
def create_fingers(finger_count):
    sides = ['L', 'R']
    
    for side in sides:
        for i in range(0, finger_count):
            for j in range(0,3):
                finger_rot = cmds.xform(cmds.ls("RIG_"+side+"_Finger_"+str(i)+"_"+str(j)), q=True, ws=True, ro=True)
                finger_pos = cmds.xform(cmds.ls("RIG_"+side+"_Finger_"+str(i)+"_"+str(j)), q=True, ws=True, t=True)
                finger     = cmds.curve(p=[(0, 0, 0), (0, 0, 0.5), (0.2, 0, 0.7),(0, 0, 0.9), (-0.2, 0, 0.7), (0, 0, 0.5)], 
                                        degree=1, name="CTRL_"+side+"_Finger_"+str(i)+"_"+str(j))
                if side == 'R':
                    cmds.rotate(90, 0,0, finger)
                else:
                    cmds.rotate(-90, 0,0, finger)
                cmds.scale(0.1,0.1,0.1,finger)  
                
                finger_grp = cmds.group(em=True, n="CTRL_GRP_"+side+"_Finger_"+str(i)+"_"+str(j))
                cmds.parent(finger, finger_grp)
                cmds.rotate(finger_rot[0], finger_rot[1], finger_rot[2], finger_grp)
                cmds.move(finger_pos[0], finger_pos[1], finger_pos[2], finger_grp)
                cmds.makeIdentity(finger, apply=True, t=1, r=1, s=1)

                if j > 0:
                    cmds.parent(finger_grp, "CTRL_"+side+"_Finger_"+str(i)+"_"+str(j-1))
                else:
                    cmds.parent(finger_grp, "CTRL_"+side+"_Wrist")
       
#leg
def create_leg():
    #knee
    l_knee = cmds. curve(p=[[0.0, 1.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, 0.0], 
                            [-1.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0], 
                            [0.0, 0.0, -1.0], [0.0, 0.0, 1.0]], degree=1, name="CTRL_L_Knee")  
    l_knee_grp = cmds. group(em=True, name= 'CTRL_GRP_L_Knee')    
    cmds.parent(l_knee, l_knee_grp)
    cmds.scale(0.15, 0.15, 0.15, l_knee_grp)
    l_upper_leg_pos = cmds.xform(cmds.ls("RIG_L_UpperLeg"), q=True, t=True, ws=True)
    l_knee_pos = cmds.xform(cmds.ls("RIG_L_LowerLeg"), q=True, t=True, ws=True)
    l_foot_pos = cmds.xform(cmds.ls("RIG_L_Foot"), q=True, t=True, ws=True)
    cmds.move(l_knee_pos[0], l_knee_pos[1], l_knee_pos[2]+1, l_knee_grp)

    #align the knee controller to the correct direction
    #create a polygon for knee controller align
    l_knee_ref_plane = cmds.polyCreateFacet(p=[(l_upper_leg_pos[0], l_upper_leg_pos[1], l_upper_leg_pos[2]), 
                                             (l_knee_pos[0], l_knee_pos[1], l_knee_pos[2]),
                                             (l_foot_pos[0], l_foot_pos[1], l_foot_pos[2])], name='L_knee_ref_plane')
    #align the controller grp to the polygon and delete the polygon
    cmds.normalConstraint(l_knee_ref_plane, l_knee_grp, aimVector=[0, 1, 0],upVector=[1, 0, 0], worldUpType='scene')
    #delete the normal constraint and ref plane
    cmds.delete(l_knee_ref_plane)
    cmds.parent(l_knee_grp, "MASTER_CONTROLLER")

    r_knee = cmds. curve(p=[[0.0, 1.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, 0.0], 
                            [-1.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0], 
                            [0.0, 0.0, -1.0],[0.0, 0.0, 1.0]], degree=1, name="CTRL_R_Knee")  
    r_knee_grp = cmds. group(em=True, name= 'CTRL_GRP_R_Knee')    
    cmds.parent(r_knee, r_knee_grp)
    cmds.scale(0.15, 0.15, 0.15, r_knee_grp)
    r_upper_leg_pos = cmds.xform(cmds.ls("RIG_R_UpperLeg"), q=True, t=True, ws=True)
    r_knee_pos = cmds.xform(cmds.ls("RIG_R_LowerLeg"), q=True, t=True, ws=True)
    r_foot_pos = cmds.xform(cmds.ls("RIG_R_Foot"), q=True, t=True, ws=True)
    cmds.move(r_knee_pos[0], r_knee_pos[1], r_knee_pos[2]+1, r_knee_grp)

    #align the knee controller to the correct direction
    #create a polygon for knee controller align
    r_knee_ref_plane = cmds.polyCreateFacet(p=[(r_upper_leg_pos[0], r_upper_leg_pos[1], r_upper_leg_pos[2]), 
                                               (r_knee_pos[0], r_knee_pos[1], r_knee_pos[2]),
                                               (r_foot_pos[0], r_foot_pos[1], r_foot_pos[2])], name='R_knee_ref_plane')
    #align the controller grp to the polygon and delete the polygon
    cmds.normalConstraint(r_knee_ref_plane, r_knee_grp, aimVector=[0, -1, 0],upVector=[1, 0, 0], worldUpType='scene')
    #delete the normal constraint and ref plane
    cmds.delete(r_knee_ref_plane)
    cmds.parent(r_knee_grp, "MASTER_CONTROLLER")

    #feet
    l_arrow = cmds.curve(p = [(1, 0, 0),(1, 0, 2), (2, 0, 2),(0, 0, 6), (-2, 0, 2), (-1, 0, 2), 
                              (-1, 0, 0), (1, 0, 0)], degree=1, name="CTRL_L_Foot")
    cmds.addAttr(shortName="KF", longName="Knee_Fix", attributeType='double', defaultValue=0, 
                 minValue=0, maxValue=1, keyable=True)
    cmds.addAttr(shortName="FR", longName="Foot_Roll", attributeType='double', defaultValue=0, 
                 minValue=0, maxValue=100, keyable=True)  
    cmds.addAttr(shortName="BR", longName="Ball_Roll", attributeType='double', defaultValue=0, 
                 minValue=0, maxValue=100, keyable=True)       
                 
    r_arrow = cmds.curve(p = [(1, 0, 0),(1, 0, 2), (2, 0, 2),(0, 0, 6), (-2, 0, 2), (-1, 0, 2), 
                              (-1, 0, 0), (1, 0, 0)], degree=1, name="CTRL_R_Foot")
    cmds.addAttr(shortName="KF", longName="Knee_Fix", attributeType='double', defaultValue=0, 
                 minValue=0, maxValue=1, keyable=True)
    cmds.addAttr(shortName="FR", longName="Foot_Roll", attributeType='double', defaultValue=0, 
                 minValue=0, maxValue=100, keyable=True)  
    cmds.addAttr(shortName="BR", longName="Ball_Roll", attributeType='double', defaultValue=0, 
                 minValue=0, maxValue=100, keyable=True)      
                 
    cmds.scale(0.08, 0.08, 0.08, l_arrow)
    cmds.scale(0.08, 0.08, 0.08, r_arrow)
    
    l_foot_pos = cmds.xform(cmds.ls("RIG_L_Foot"), q=True, t=True, ws=True)
    r_foot_pos = cmds.xform(cmds.ls("RIG_R_Foot"), q=True, t=True, ws=True)
    
    cmds.move(l_foot_pos[0], 0, l_foot_pos[2], l_arrow)
    cmds.move(r_foot_pos[0], 0, r_foot_pos[2], r_arrow)
    
    cmds.makeIdentity(l_arrow, apply=True, t=1, r=1, s=1)
    cmds.makeIdentity(r_arrow, apply=True, t=1, r=1, s=1)
                 
    cmds.parent(l_arrow, "MASTER_CONTROLLER")             
    cmds.parent(r_arrow, "MASTER_CONTROLLER")  
                 
                    
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
    create_clavicles(spine_count)
    create_elbow()
    create_wrists()
    create_fingers(finger_count)
    create_leg()
    set_colors()
                
               
    