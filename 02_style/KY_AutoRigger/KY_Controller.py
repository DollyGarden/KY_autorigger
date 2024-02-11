import maya.cmds as cmds
import maya.OpenMaya as om

def createController(spine_count,finger_count):
    #arrow=cmds.curve(p=[(1,0,0), (1,0,2), (2,0,2), (0,0,6), (-2,0,2),(-1,0,2), (-1,0,0), (1,0,0)], degree=1)
    createMaster()
    createPelvis()
    createSpines(spine_count)
    createNeck(spine_count)
    createHead()
    createClavicles(spine_count)
    createElbow()
    createWrists()
    createFingers(finger_count)
    createLeg()
    setColors()
    
def createMaster():    
    #master
    master_ctrl=cmds.circle(nr=(0,1,0),c=(0,0,0), radius=1, degree=1, s=16, name="MASTER_CONTROLLER")
    selection=cmds.select("MASTER_CONTROLLER.cv[1]", "MASTER_CONTROLLER.cv[3]","MASTER_CONTROLLER.cv[5]", 
                          "MASTER_CONTROLLER.cv[7]", "MASTER_CONTROLLER.cv[9]","MASTER_CONTROLLER.cv[11]",
                          "MASTER_CONTROLLER.cv[13]","MASTER_CONTROLLER.cv[15]")
    cmds.scale(0.7,0.7,0.7, selection)
    cmds.makeIdentity(master_ctrl, apply=True, t=1, r=1, s=1)

def createPelvis():    
    #pelvis
    pelvis_ctrl=cmds.circle(nr=(0,1,0),c=(0,0,0), radius=1, degree=1, s=8, name="CTRL_PELVIS")
    rootPos=cmds.xform(cmds.ls("RIG_ROOT", type='joint'), q=True, t=True, ws=True)
    cmds.move(rootPos[0],rootPos[1],rootPos[2],pelvis_ctrl)
    cmds.scale(0.5,0.5,0.5,pelvis_ctrl)
    cmds.makeIdentity(pelvis_ctrl, apply=True, t=1, r=1, s=1)
    cmds.parent(pelvis_ctrl, "MASTER_CONTROLLER")

#spine
def createSpines(spine_count):
    for i in range(0,spine_count):
        spinePos=cmds.xform(cmds.ls("RIG_SPINE_"+str(i)),q=True, t=True,ws=True)
        spine_ctrl=cmds.circle(nr=(0,1,0),c=(0,0,0), radius=1,s=8, name="CTRL_SPINE_"+str(i))
        cmds.move(spinePos[0], spinePos[1], spinePos[2], spine_ctrl)
        cmds.scale (0.3,0.3,0.3,spine_ctrl)
        if (i==0):
            cmds.parent(spine_ctrl, "CTRL_PELVIS")
        else:
            cmds.parent(spine_ctrl, "CTRL_SPINE_"+str(i-1))
        cmds.makeIdentity(spine_ctrl, apply=True, t=1, r=1, s=1)
#neck
def createNeck(spine_count):
    neck_ctrl=cmds.circle(nr=(0,1,0),c=(0,0,0), radius=1,s=8, name="CTRL_NECK")
    neckPos=cmds.xform(cmds.ls("RIG_Neck_Start"), q=True, t=True, ws=True)
    cmds.scale (0.2,0.2,0.2,neck_ctrl)
    cmds.move(neckPos[0], neckPos[1], neckPos[2], neck_ctrl)
    cmds.parent(neck_ctrl,"CTRL_SPINE_"+str(spine_count-1))
    cmds.makeIdentity(neck_ctrl, apply=True, t=1, r=1, s=1)
    
# Head
def createHead():
    head_ctrl=cmds.circle(nr=(1,0,0),c=(0,0,0), radius=1,s=8, name="CTRL_HEAD")
    headPos=cmds.xform(cmds.ls("RIG_Neck_End"), q=True, t=True, ws=True)
    headRot=cmds.xform(cmds.ls("RIG_Neck_End"), q=True, ro=True, ws=True)
    cmds.scale (0.25,0.25,0.25,head_ctrl)
    cmds.move(headPos[0], headPos[1], headPos[2], head_ctrl)
    cmds.rotate(headRot[0], headRot[1], headRot[2], head_ctrl)
    cmds.parent(head_ctrl,"CTRL_NECK")
    cmds.makeIdentity(head_ctrl, apply=True, t=1, r=1, s=1)
    #jaw
    jaw = cmds.circle(nr=(0,1,0),c=(0,0,0), radius=0.2,s=8, name = "CTRL_JAW")
    jawStart=cmds.xform(cmds.ls("RIG_Jaw_Start"),q=True, t=True, ws=True)
    jawEnd=cmds.xform(cmds.ls("RIG_Jaw_End"),q=True, t=True, ws=True)
    jawRot=cmds.xform(cmds.ls("RIG_Jaw_Start"),q=True, ro=True, ws=True)
    cmds.rotate(jawRot[0],jawRot[1],jawRot[2],jaw)
    cmds.move(jawEnd[0], jawEnd[1], jawEnd[2], jaw)
    cmds.move(jawStart[0], jawStart[1], jawStart[2], "CTRL_JAW.scalePivot", "CTRL_JAW.rotatePivot")
    cmds.parent(jaw, "CTRL_HEAD")
    cmds.makeIdentity(jaw, apply=True, t=1, r=1, s=1)

# clavicle
def createClavicles(spine_count):
    #left clavicle
    #create controller
    l_clavicle=cmds.circle(nr=(0,1,0),c=(0,0,0), radius=1, s=12, name = "CTRL_L_Clavicle")
    selection_01=cmds.select("CTRL_L_Clavicle.cv[4]", "CTRL_L_Clavicle.cv[10]")
    cmds.move(0, 0.3, 0, selection_01, r=True)
    selection_02=cmds.select("CTRL_L_Clavicle.cv[3]", "CTRL_L_Clavicle.cv[5]","CTRL_L_Clavicle.cv[9]", "CTRL_L_Clavicle.cv[11]")
    cmds.move(0, 0.2, 0, selection_02, r=True)
    cmds.makeIdentity(l_clavicle, apply=True, t=1, r=1,s=1)
    l_clavicleGrp=cmds.group(em=True, name='CTRL_GRP_L_Clavicle')
    cmds.parent(l_clavicle, l_clavicleGrp)
    #move the controller group
    cmds.scale(0.1, 0.2, 0.2, l_clavicleGrp)
    l_ArmPos=cmds.xform(cmds.ls("RIG_L_UpperArm"), q=True, t=True, ws=True)
    l_claviclePos=cmds.xform(cmds.ls("RIG_L_Clavicle"), q=True, t=True, ws=True)
    l_clavicleRot=cmds.xform(cmds.ls("RIG_L_Clavicle"),q=True, ro=True, ws=True)
    cmds.rotate(l_clavicleRot[0],l_clavicleRot[1],l_clavicleRot[2], l_clavicleGrp)
    cmds.move(l_ArmPos[0]-0.1,l_ArmPos[1]+0.125,l_ArmPos[2], l_clavicleGrp)
    cmds.move(l_claviclePos[0],l_claviclePos[1],l_claviclePos[2], "CTRL_L_Clavicle.scalePivot",
              "CTRL_L_Clavicle.rotatePivot")
    cmds.parent(l_clavicleGrp, "CTRL_SPINE_"+str(spine_count-1))
    
    #right clavicle
    #create controller
    r_clavicle=cmds.circle(nr=(0,-1,0),c=(0,0,0), radius=1, s=12, name = "CTRL_R_Clavicle")
    selection_01=cmds.select("CTRL_R_Clavicle.cv[4]", "CTRL_R_Clavicle.cv[10]")
    cmds.move(0, -0.3, 0, selection_01,r=True)
    selection_02=cmds.select("CTRL_R_Clavicle.cv[3]", "CTRL_R_Clavicle.cv[5]","CTRL_R_Clavicle.cv[9]", "CTRL_R_Clavicle.cv[11]")
    cmds.move(0, -0.2, 0, selection_02,r=True)
    cmds.makeIdentity(r_clavicle, apply=True, t=1, r=1,s=1)
    r_clavicleGrp=cmds.group(em=True, name='CTRL_GRP_R_Clavicle') 
    cmds.parent(r_clavicle, r_clavicleGrp)
    #move the controller
    cmds.scale(0.1, 0.2, 0.2, r_clavicleGrp)
    r_ArmPos=cmds.xform(cmds.ls("RIG_R_UpperArm"), q=True, t=True, ws=True)
    r_claviclePos=cmds.xform(cmds.ls("RIG_R_Clavicle"), q=True, t=True, ws=True)
    r_clavicleRot=cmds.xform(cmds.ls("RIG_R_Clavicle"),q=True, ro=True, ws=True)
    cmds.rotate(r_clavicleRot[0],r_clavicleRot[1],r_clavicleRot[2], r_clavicleGrp)
    cmds.move(r_ArmPos[0]+0.1,r_ArmPos[1]+0.125,r_ArmPos[2], r_clavicleGrp)
    cmds.move(r_claviclePos[0],r_claviclePos[1],r_claviclePos[2], "CTRL_R_Clavicle.scalePivot",
              "CTRL_R_Clavicle.rotatePivot")
    cmds.parent(r_clavicleGrp, "CTRL_SPINE_"+str(spine_count-1))

#elbow
def createElbow():
    #left elbow
    l_elbow=cmds.curve(p=[[0.0,1.0,0.0], [0.0,-1.0,0.0], [0.0,0.0,0.0], 
                          [-1.0,0.0,0.0], [1.0,0.0,0.0], [0.0,0.0,0.0], 
                          [0.0,0.0,-1.0],[0.0,0.0,1.0]],degree=1,name="CTRL_L_Elbow")  
    l_elbowGrp=cmds.group(em=True, name='CTRL_GRP_L_Elbow')    
    cmds.parent(l_elbow, l_elbowGrp)
    cmds.scale(0.15, 0.15, 0.15, l_elbowGrp)
    l_upperArmPos=cmds.xform(cmds.ls("RIG_L_UpperArm"), q=True, t=True, ws=True)
    l_elbowPos=cmds.xform(cmds.ls("RIG_L_Elbow"), q=True, t=True, ws=True)
    l_wristPos=cmds.xform(cmds.ls("RIG_L_Wrist"), q=True, t=True, ws=True)
    cmds.move(l_elbowPos[0],l_elbowPos[1],l_elbowPos[2]-0.5, l_elbowGrp)

    #align the elbow controller to the correct direction
    #create a polygon for elbow controller align
    l_elbowRefPlane=cmds.polyCreateFacet(p=[(l_upperArmPos[0], l_upperArmPos[1], l_upperArmPos[2]), 
                                            (l_elbowPos[0], l_elbowPos[1], l_elbowPos[2]),
                                            (l_wristPos[0], l_wristPos[1], l_wristPos[2])], name='L_elbowRefPlane')
    #align the controller grp to the polygon and delet the polygon
    cmds.normalConstraint(l_elbowRefPlane, l_elbowGrp, aimVector=[0, -1, 0],upVector=[1, 0, 0], worldUpType='scene')
    #delete the normal constraint and ref plane
    cmds.delete(l_elbowRefPlane)
    cmds.parent(l_elbowGrp, "MASTER_CONTROLLER")

     #right elbow
    r_elbow=cmds.curve(p=[[0.0,1.0,0.0], [0.0,-1.0,0.0], [0.0,0.0,0.0], 
                          [-1.0,0.0,0.0], [1.0,0.0,0.0], [0.0,0.0,0.0], 
                          [0.0,0.0,-1.0],[0.0,0.0,1.0]],degree=1,name="CTRL_R_Elbow")  
    r_elbowGrp=cmds.group(em=True, name='CTRL_GRP_R_Elbow')    
    cmds.parent(r_elbow, r_elbowGrp)
    cmds.scale(0.15, 0.15, 0.15, r_elbowGrp)
    r_upperArmPos=cmds.xform(cmds.ls("RIG_R_UpperArm"), q=True, t=True, ws=True)
    r_elbowPos=cmds.xform(cmds.ls("RIG_R_Elbow"), q=True, t=True, ws=True)
    r_wristPos=cmds.xform(cmds.ls("RIG_R_Wrist"), q=True, t=True, ws=True)
    cmds.move(r_elbowPos[0],r_elbowPos[1],r_elbowPos[2]-0.5, r_elbowGrp)

    #align the elbow controller to the correct direction
    #create a polygon for elbow controller align
    r_elbowRefPlane=cmds.polyCreateFacet(p=[(r_upperArmPos[0], r_upperArmPos[1], r_upperArmPos[2]), 
                                            (r_elbowPos[0], r_elbowPos[1], r_elbowPos[2]),
                                            (r_wristPos[0], r_wristPos[1], r_wristPos[2])], name='R_elbowRefPlane')
    #align the controller grp to the polygon and delet the polygon
    cmds.normalConstraint(r_elbowRefPlane, r_elbowGrp, aimVector=[0, 1, 0],upVector=[1, 0, 0], worldUpType='scene')
    #delete the normal constraint and ref plane
    cmds.delete(r_elbowRefPlane)
    cmds.parent(r_elbowGrp, "MASTER_CONTROLLER")
          
#wrist
def createWrists():
    sides=['L','R']
    for side in sides:
        wrist_ctrl=cmds.circle(nr=(1,0,0),c=(0,0,0), radius=1, s=16, name="CTRL_"+side+"_Wrist")
        wrist_ctrl_grp=cmds.group(em=True, name="CTRL_GRP_"+side+"_Wrist")
        cmds.parent(wrist_ctrl, wrist_ctrl_grp)
        cmds.scale(0.1,0.1,0.1, wrist_ctrl)

        wristPos=cmds.xform(cmds.ls("RIG_"+side+"_Wrist"), q=True, t=True, ws=True)
        wristRot=cmds.xform(cmds.ls("RIG_"+side+"_Wrist"), q=True, ws=True, ro=True)
        cmds.move(wristPos[0],wristPos[1],wristPos[2],wrist_ctrl_grp)
        cmds.rotate(wristRot[0],wristRot[1],wristRot[2], wrist_ctrl_grp)
        cmds.parent(wrist_ctrl_grp, "MASTER_CONTROLLER")
        # if (side=='R'):
        #     cmds.scale(1,-1,1, wristGrp)
    
#finger
def createFingers(finger_count):
    sides=['L', 'R']
    
    for side in sides:
        for i in range(0, finger_count):
            for j in range(0,3):
                fingerRotation=cmds.xform(cmds.ls("RIG_"+side+"_Finger_"+str(i)+"_"+str(j)), q=True, ws=True, ro=True)
                fingerPosition=cmds.xform(cmds.ls("RIG_"+side+"_Finger_"+str(i)+"_"+str(j)), q=True, ws=True, t=True)
                finger = cmds.curve(p =[(0,0,0), (0,0,0.5), (0.2, 0, 0.7),(0,0,0.9), (-0.2, 0, 0.7), (0,0,0.5)], 
                                        degree = 1, name = "CTRL_"+side+"_Finger_"+str(i)+"_"+str(j))
                if(side=='R'):
                    cmds.rotate(90, 0,0, finger)
                else:
                    cmds.rotate(-90, 0,0, finger)
                cmds.scale(0.1,0.1,0.1,finger)  
                
                fingerGrp=cmds.group(em=True, n="CTRL_GRP_"+side+"_Finger_"+str(i)+"_"+str(j))
                cmds.parent(finger,fingerGrp)
                cmds.rotate(fingerRotation[0],fingerRotation[1], fingerRotation[2], fingerGrp)
                cmds.move(fingerPosition[0], fingerPosition[1],fingerPosition[2], fingerGrp)
                cmds.makeIdentity(finger, apply=True, t=1, r=1, s=1)

                if(j>0):
                    cmds.parent(fingerGrp, "CTRL_"+side+"_Finger_"+str(i)+"_"+str(j-1))
                else:
                    cmds.parent(fingerGrp, "CTRL_"+side+"_Wrist")
       
#leg
def createLeg():
    #knee
    l_knee= cmds. curve(p=[[0.0,1.0,0.0], [0.0,-1.0,0.0], [0.0,0.0,0.0], 
                           [-1.0,0.0,0.0], [1.0,0.0,0.0], [0.0,0.0,0.0], 
                           [0.0,0.0,-1.0],[0.0,0.0,1.0]], degree=1, name="CTRL_L_Knee")  
    l_kneeGrp= cmds. group(em=True, name= 'CTRL_GRP_L_Knee')    
    cmds.parent(l_knee, l_kneeGrp)
    cmds.scale(0.15, 0.15, 0.15, l_kneeGrp)
    l_upperLegPos=cmds.xform(cmds.ls("RIG_L_UpperLeg"), q=True, t=True, ws=True)
    l_kneePos=cmds.xform(cmds.ls("RIG_L_LowerLeg"), q=True, t=True, ws=True)
    l_footPos=cmds.xform(cmds.ls("RIG_L_Foot"), q=True, t=True, ws=True)
    cmds.move(l_kneePos[0],l_kneePos[1],l_kneePos[2]+1, l_kneeGrp)

    #align the knee controller to the correct direction
    #create a polygon for knee controller align
    l_kneeRefPlane= cmds.polyCreateFacet(p=[(l_upperLegPos[0], l_upperLegPos[1], l_upperLegPos[2]), 
                                            (l_kneePos[0], l_kneePos[1], l_kneePos[2]),
                                            (l_footPos[0], l_footPos[1], l_footPos[2])], name='L_kneeRefPlane')
    #align the controller grp to the polygon and delet the polygon
    cmds.normalConstraint(l_kneeRefPlane, l_kneeGrp, aimVector=[0, 1, 0],upVector=[1, 0, 0], worldUpType='scene')
    #delete the normal constraint and ref plane
    cmds.delete(l_kneeRefPlane)
    cmds.parent(l_kneeGrp, "MASTER_CONTROLLER")

    r_knee= cmds. curve(p=[[0.0,1.0,0.0], [0.0,-1.0,0.0], [0.0,0.0,0.0], 
                           [-1.0,0.0,0.0], [1.0,0.0,0.0], [0.0,0.0,0.0], 
                           [0.0,0.0,-1.0],[0.0,0.0,1.0]], degree=1, name="CTRL_R_Knee")  
    r_kneeGrp= cmds. group(em=True, name= 'CTRL_GRP_R_Knee')    
    cmds.parent(r_knee, r_kneeGrp)
    cmds.scale(0.15, 0.15, 0.15, r_kneeGrp)
    r_upperLegPos=cmds.xform(cmds.ls("RIG_R_UpperLeg"), q=True, t=True, ws=True)
    r_kneePos=cmds.xform(cmds.ls("RIG_R_LowerLeg"), q=True, t=True, ws=True)
    r_footPos=cmds.xform(cmds.ls("RIG_R_Foot"), q=True, t=True, ws=True)
    cmds.move(r_kneePos[0],r_kneePos[1],r_kneePos[2]+1, r_kneeGrp)

    #align the knee controller to the correct direction
    #create a polygon for knee controller align
    r_kneeRefPlane= cmds.polyCreateFacet(p=[(r_upperLegPos[0], r_upperLegPos[1], r_upperLegPos[2]), 
                                            (r_kneePos[0], r_kneePos[1], r_kneePos[2]),
                                            (r_footPos[0], r_footPos[1], r_footPos[2])], name='R_kneeRefPlane')
    #align the controller grp to the polygon and delet the polygon
    cmds.normalConstraint(r_kneeRefPlane, r_kneeGrp, aimVector=[0, -1, 0],upVector=[1, 0, 0], worldUpType='scene')
    #delete the normal constraint and ref plane
    cmds.delete(r_kneeRefPlane)
    cmds.parent(r_kneeGrp, "MASTER_CONTROLLER")

    #feet
    l_arrow = cmds.curve(p = [(1,0,0),(1,0,2), (2,0,2),(0,0,6), (-2,0,2), (-1,0,2), 
                              (-1,0,0), (1,0,0)], degree = 1, name = "CTRL_L_Foot")
    cmds.addAttr(shortName="KF", longName="Knee_Fix", attributeType='double', defaultValue=0, 
                 minValue=0, maxValue=1, keyable=True)
    cmds.addAttr(shortName="FR", longName="Foot_Roll", attributeType='double', defaultValue=0, 
                 minValue=0, maxValue=100, keyable=True)  
    cmds.addAttr(shortName="BR", longName="Ball_Roll", attributeType='double', defaultValue=0, 
                 minValue=0, maxValue=100, keyable=True)       
                 
    r_arrow = cmds.curve(p = [(1,0,0),(1,0,2), (2,0,2),(0,0,6), (-2,0,2), (-1,0,2), 
                              (-1,0,0), (1,0,0)], degree = 1, name = "CTRL_R_Foot")
    cmds.addAttr(shortName="KF", longName="Knee_Fix", attributeType='double', defaultValue=0, 
                 minValue=0, maxValue=1, keyable=True)
    cmds.addAttr(shortName="FR", longName="Foot_Roll", attributeType='double', defaultValue=0, 
                 minValue=0, maxValue=100, keyable=True)  
    cmds.addAttr(shortName="BR", longName="Ball_Roll", attributeType='double', defaultValue=0, 
                 minValue=0, maxValue=100, keyable=True)      
                 
    cmds.scale(0.08,0.08,0.08, l_arrow)
    cmds.scale(0.08,0.08,0.08, r_arrow)
    
    l_footPos=cmds.xform(cmds.ls("RIG_L_Foot"), q=True, t=True, ws=True)
    r_footPos=cmds.xform(cmds.ls("RIG_R_Foot"), q=True, t=True, ws=True)
    
    cmds.move(l_footPos[0], 0, l_footPos[2], l_arrow)
    cmds.move(r_footPos[0], 0, r_footPos[2], r_arrow)
    
    cmds.makeIdentity(l_arrow, apply=True, t=1, r=1, s=1)
    cmds.makeIdentity(r_arrow, apply=True, t=1, r=1, s=1)
                 
    cmds.parent(l_arrow, "MASTER_CONTROLLER")             
    cmds.parent(r_arrow, "MASTER_CONTROLLER")  
                 
                    
def setColors():
    cmds.setAttr('MASTER_CONTROLLER.overrideEnabled', 1)
    cmds.setAttr('MASTER_CONTROLLER.overrideRGBColors', 1)
    cmds.setAttr('MASTER_CONTROLLER.overrideColorRGB', 1,1,1)                                                    
                
                
                
               
    