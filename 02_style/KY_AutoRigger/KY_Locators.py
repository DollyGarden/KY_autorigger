import maya.cmds as cmds

#create the input fields for the amound of spines and fingers
# def createFields(spineValue, fingerValue):
#     global spineCount
#     global fingerCount
    
#return the value from the fingerCount int field
# def ReturnFingerAmount():
#     return fingerCount
    
#return the value from the spineCount int field
# def ReturnSpineAmount():
#     return spineCount
    
#???can't understand the spineCount and fingerCount???
def createLocators(spineValue, fingerValue):
    # global spineCount
    # global fingerCount

    # spineCount=spineValue
    # fingerCount=fingerValue
    
    if cmds.objExists('GRP_Loc_Master'):
        deleteLocators()
  
    cmds.group(em=True, name="GRP_Loc_Master")
    
    root = cmds.spaceLocator(n="Loc_ROOT")
    cmds.scale(0.1, 0.1, 0.1, root)
    cmds.move(0, 1.5, 0, root)
    cmds.parent(root, "GRP_Loc_Master")
    
    createSpine(spineValue)
    createHead(spineValue)
    createArms(spineValue, 1, fingerValue)
    createArms(spineValue, -1, fingerValue)
    createLegs(1)
    createLegs(-1)
    setColors()
    lockLocatorAttr()

    
    
#create the spine function   
def createSpine(spineValue):
    for i in range(0, spineValue):
        spine=cmds.spaceLocator(n='Loc_SPINE_'+str(i))
        cmds.scale(0.1, 0.1, 0.1, spine)
        if i == 0:
            cmds.parent(spine, 'Loc_ROOT')
        else:
            cmds.parent(spine, 'Loc_SPINE_'+str(i-1))
        cmds.move(0, 1.75+(0.25*i), 0, spine)
    
def createHead(spineValue):
    neck_start = cmds.spaceLocator(n='Loc_Neck_Start')
    cmds.parent(neck_start,'Loc_SPINE_'+str(spineValue-1))
    cmds.scale(1,1,1,neck_start)
    cmds.move(0,1.6+(0.25*spineValue),0, neck_start)
   
    neck_end = cmds.spaceLocator(n='Loc_Neck_End')
    cmds.parent(neck_end,'Loc_Neck_Start')
    cmds.scale(1,1,1,neck_end)
    cmds.move(0,1.75+(0.25*spineValue),0, neck_end)
     
    head = cmds.spaceLocator(n='Loc_Head')
    cmds.parent(head,'Loc_Neck_End')
    cmds.scale(1,1,1,head)
    cmds.move(0,2+(0.25*spineValue),0, head)

    jawEnd = cmds.spaceLocator(n='Loc_Jaw_End')
    jawStart = cmds.spaceLocator(n='Loc_Jaw_Start')
    cmds.parent(jawStart,head)
    cmds.parent(jawEnd,jawStart)
    cmds.scale(1,1,1,jawEnd)
    cmds.scale(0.5,0.5,0.5,jawStart)
    cmds.move(0,1.9+(0.25*spineValue),0.02, jawStart)
    cmds.move(0,1.9+(0.25*spineValue),0.15, jawEnd)
    
def createLegs(side):
    if side == 1: #left
        # if cmds.objExists('L_Leg_GRP'):
        #     print('I am not doing anything.')
        # else:
            # upperLegGRP=cmds.group(em=True,name='L_Leg_GRP')
            # cmds.parent(upperLegGRP, 'Loc_ROOT')
            # cmds.move(0.1,1,0,upperLegGRP)

        #upperLeg
        upperLeg = cmds.spaceLocator(n='Loc_L_UpperLeg')
        cmds.scale(0.1, 0.1, 0.1, upperLeg)
        cmds.move(0.15, 1.5, 0, upperLeg)
        cmds.parent(upperLeg, 'Loc_ROOT')
        
        #lowerLeg
        lowerLeg = cmds.spaceLocator(n='Loc_L_LowerLeg')
        cmds.scale(0.1, 0.1, 0.1, lowerLeg)
        cmds.move(0.15, 0.75, 0.05,lowerLeg)
        cmds.parent(lowerLeg, 'Loc_L_UpperLeg')
        
        #foot
        foot = cmds.spaceLocator(n='Loc_L_Foot')
        cmds.scale(0.1, 0.1, 0.1, foot)
        cmds.move(0.15, 0.2, 0,foot)
        cmds.parent(foot, 'Loc_L_LowerLeg')
        
        #football
        football = cmds.spaceLocator(n='Loc_L_FootBall')
        cmds.scale(0.1, 0.1, 0.1, football)
        cmds.move(0.15, 0, 0.15, football)
        cmds.parent(football, 'Loc_L_Foot')     
        
        #toes
        toes = cmds.spaceLocator(n='Loc_L_Toes')
        cmds.scale(0.1, 0.1, 0.1, toes)
        cmds.move(0.15, 0, 0.3, toes)
        cmds.parent(toes, 'Loc_L_FootBall')    

    else:#right
        # if cmds.objExists('R_Leg_GRP'):
        #     print('Im not doing anything.')
        # else:
        #     upperLegGRP = cmds.group(em=True,name='R_Leg_GRP')
        #     cmds.parent(upperLegGRP, 'Loc_ROOT')
        #     cmds.move(-0.1, 1, 0, upperLegGRP)

        #upperLeg
        upperLeg = cmds.spaceLocator(n='Loc_R_UpperLeg')
        cmds.scale(0.1, 0.1, 0.1, upperLeg)
        cmds.move(-0.15, 1.5, 0, upperLeg)
        cmds.parent(upperLeg, 'Loc_ROOT')
        
        #lowerLeg
        lowerLeg = cmds.spaceLocator(n='Loc_R_LowerLeg')
        cmds.scale(0.1, 0.1, 0.1, lowerLeg)
        cmds.move(-0.15, 0.75, 0.05,lowerLeg)
        cmds.parent(lowerLeg, 'Loc_R_UpperLeg')
        
        #foot
        foot = cmds.spaceLocator(n='Loc_R_Foot')
        cmds.scale(0.1, 0.1, 0.1, foot)
        cmds.move(-0.15, 0.2, 0,foot)
        cmds.parent(foot, 'Loc_R_LowerLeg')
        
        #football
        football = cmds.spaceLocator(n='Loc_R_FootBall')
        cmds.scale(0.1, 0.1, 0.1, football)
        cmds.move(-0.15, 0, 0.15,football)
        cmds.parent(football, 'Loc_R_Foot')     
        
        #toes
        toes = cmds.spaceLocator(n='Loc_R_Toes')
        cmds.scale(0.1, 0.1, 0.1, toes)
        cmds.move(-0.15, 0, 0.3, toes)
        cmds.parent(toes, 'Loc_R_FootBall') 
                       
    
def createArms(spineValue, side, fingerValue):
    # global editMode
    if side == 1: #left
        # if cmds.objExists('L_Arm_GRP'):
        #     print('Im not doing anything.')
        # else:
            #clavicle start
        clavicle=cmds.spaceLocator(n='Loc_L_Clavicle')
        cmds.scale(0.1, 0.1,0.1, clavicle)
        cmds.parent(clavicle, 'Loc_SPINE_'+str(spineValue-1))
        cmds.move(0.1*side, 1.5+(0.25*spineValue), 0.1, clavicle)
        
        #upperArm
        upperArm=cmds.spaceLocator(n='Loc_L_UpperArm')#arm
        cmds.scale(0.1, 0.1,0.1, upperArm)
        cmds.parent(upperArm, clavicle)
        cmds.move(0.35*side, 1.5+(0.25*spineValue), 0, upperArm)
        
        #elbow
        elbow=cmds.spaceLocator(n='Loc_L_Elbow')#elbow
        cmds.scale(0.1, 0.1,0.1, elbow)
        cmds.parent(elbow, upperArm)
        cmds.move(0.8*side, 1.5+(0.25*spineValue), -0.2, elbow)
        
        #wrist
        wrist=cmds.spaceLocator(n='Loc_L_Wrist')#wrist
        cmds.scale(0.1, 0.1,0.1, wrist)
        cmds.parent(wrist, elbow)
        cmds.move(1.2*side, 1.5+(0.25*spineValue), 0, wrist)
        
        #palm
        palm=cmds.spaceLocator(n='Loc_L_Palm')
        cmds.scale(0.1, 0.1,0.1, palm)
        cmds.parent(palm, wrist)
        cmds.move(1.25*side, 1.5+(0.25*spineValue), 0, palm )
        
        createFingers(side, wrist, fingerValue)
            
    # else:#right
    #     if cmds.objExists('R_Arm_GRP'):
    #         print('Im not doing anything.')
    else:
        R_arm=cmds.group(em=True,name='R_Arm_GRP')
        cmds.parent(R_arm, 'Loc_SPINE_'+str(spineValue-1))
        
        #clavicle start
        clavicle=cmds.spaceLocator(n='Loc_R_Clavicle')
        cmds.scale(0.1, 0.1,0.1, clavicle)
        cmds.parent(clavicle, 'Loc_SPINE_'+str(spineValue-1))
        cmds.move(0.1*side, 1.5+(0.25*spineValue), 0.1, clavicle)
        
        #upperArm
        upperArm=cmds.spaceLocator(n='Loc_R_UpperArm')
        cmds.scale(0.1, 0.1,0.1, upperArm)
        cmds.parent(upperArm, clavicle)
        cmds.move(0.35*side, 1.5+(0.25*spineValue), 0, upperArm)
        
        #elbow
        elbow=cmds.spaceLocator(n='Loc_R_Elbow')#elbow
        cmds.scale(0.1, 0.1,0.1, elbow)
        cmds.parent(elbow, upperArm)
        cmds.move(0.8*side, 1.5+(0.25*spineValue), -0.2, elbow)
        
        #wrist
        wrist=cmds.spaceLocator(n='Loc_R_Wrist')#wrist
        cmds.scale(0.1, 0.1,0.1, wrist)
        cmds.parent(wrist, elbow)
        cmds.move(1.2*side, 1.5+(0.25*spineValue), 0, wrist)
        
        #palm
        palm=cmds.spaceLocator(n='Loc_R_Palm')
        cmds.scale(0.1, 0.1,0.1, palm)
        cmds.parent(palm, wrist)
        cmds.move(1.25*side, 1.5+(0.25*spineValue), 0, palm )

        createFingers(side, wrist, fingerValue)
    
# def createHands(side, wrist, fingerValue):
#     if side==1:
#         # if cmds.objExists('L_Hand_GRP'):
#         #     print('Im not doing anything.')
#         # else:
#         # hand=cmds.group(em=True,name='L_Hand_GRP')
#         # cmds.move(pos[0], pos[1], pos[2], hand)
#         # cmds.parent(hand, 'Loc_L_Wrist')
        
#         for i in range(0, fingerValue):
#             createFingers(1,pos,i)
#     else:
#         # if cmds.objExists('R_Hand_GRP'):
#         #     print('Im not doing anything.')
#         # else:
#         #     hand=cmds.group(em=True,name='R_Hand_GRP')
#         #     pos=cmds.xform(wrist, q=True, t=True, ws=True)
#         #     cmds.move(pos[0], pos[1], pos[2], hand)
#         #     cmds.parent(hand, 'Loc_R_Wrist')
            
#         for i in range(0, fingerValue):
#             createFingers(-1,pos,i)
                
def createFingers(side, wrist, fingerValue):
    handPos=cmds.xform(wrist, q=True, t=True, ws=True)
    for i in range(0, fingerValue):
        for x in range(0,4):
            if side ==1:
                finger = cmds. spaceLocator(n='Loc_L_Finger_'+str(i)+'_'+str(x))
                cmds.scale(0.05,0.05,0.05,finger)
                if x==0:
                    cmds.parent(finger, wrist)
                else:
                    cmds.parent(finger, 'Loc_L_Finger_'+str(i)+'_'+str(x-1))
                cmds.move(handPos[0]+(0.1+(0.1*x))*side,handPos[1], handPos[2]+-(0.05*i), finger)
            else:
                finger = cmds. spaceLocator(n='Loc_R_Finger_'+str(i)+'_'+str(x))
                cmds.scale(0.05,0.05,0.05,finger)
                if x==0:
                    cmds.parent(finger, wrist)
                else:
                    cmds.parent(finger, 'Loc_R_Finger_'+str(i)+'_'+str(x-1))
                cmds.move(handPos[0]+(0.1+(0.1*x))*side,handPos[1], handPos[2]+-(0.05*i), finger)

def setColors():
    cmds.setAttr('GRP_Loc_Master.overrideEnabled', 1)
    cmds.setAttr('GRP_Loc_Master.overrideRGBColors', 1)
    cmds.setAttr('GRP_Loc_Master.overrideColorRGB', 1, 1, 0)   

def mirrorLocators():
    l_locators = cmds.ls('Loc_L_*',type='transform')
    # r_locators=cmds.ls('Loc_R_*',type='transform')
    for l_locator in l_locators:
        last_name = l_locator. replace('Loc_L_', '')
        neg_attrs = ['.translateX', '.rotateY', '.rotateZ']
        pos_attrs = ['.translateY', '.translateZ', '.rotateX']
        for neg_attr in neg_attrs:
            if not cmds.getAttr(l_locator + neg_attr, lock=True):
                l_locator_attribute = cmds.getAttr(l_locator + neg_attr)
                cmds.setAttr('Loc_R_' + last_name + neg_attr, -1 * l_locator_attribute)
        for pos_attr in pos_attrs:
            if not cmds.getAttr(l_locator + pos_attr, lock=True):
                l_locator_attribute = cmds.getAttr(l_locator + pos_attr)
                cmds.setAttr('Loc_R_' + last_name + pos_attr, l_locator_attribute)        

                    
def lockLocatorAttr():
    axis=['X', 'Y', 'Z']
    for axe in axis:
        cmds.setAttr('GRP_Loc_Master.rotate'+axe, lock=True, k=False)
        cmds.setAttr('Loc_*_Wrist.scale'+axe, lock=True, k=False)
        l_fingerLocators=cmds.ls('Loc_L_Finger_*_0', type='transform')
        r_fingerLocators=cmds.ls('Loc_R_Finger_*_0', type='transform')
        allLocators=cmds.ls('Loc_*',type='transform')
        for l in (allLocators):
            if "Finger" in l:
                None
            else:
                if 'Wrist' in l:
                    cmds.setAttr(l+'.scale'+axe, lock=True, k=False)
                else:
                    cmds.setAttr(l+'.scale'+axe, lock=True, k=False)
                    cmds.setAttr(l+'.rotate'+axe, lock=True, k=False)
        
        for j in range(0,len(l_fingerLocators)):
            for k in range(0,3):
                cmds.setAttr('Loc_L_Finger_'+str(j)+"_"+str(k)+'.scale'+axe, lock=True, k=False)
                
                if k>0:
                    cmds.setAttr('Loc_L_Finger_'+str(j)+"_"+str(k)+'.translate'+axe, lock=True, k=False)
                    cmds.setAttr('Loc_L_Finger_'+str(j)+"_"+str(k)+'.rotateX', lock=True, k=False)
                    cmds.setAttr('Loc_L_Finger_'+str(j)+"_"+str(k)+'.rotateY', lock=True, k=False)

        for j in range(0,len(r_fingerLocators)):
            for k in range(0,3):
                cmds.setAttr('Loc_R_Finger_'+str(j)+"_"+str(k)+'.scale'+axe, lock=True, k=False)
                
                if k>0:
                    cmds.setAttr('Loc_R_Finger_'+str(j)+"_"+str(k)+'.translate'+axe, lock=True, k=False) 
                    cmds.setAttr('Loc_R_Finger_'+str(j)+"_"+str(k)+'.rotateX', lock=True, k=False)
                    cmds.setAttr('Loc_R_Finger_'+str(j)+"_"+str(k)+'.rotateY', lock=True, k=False)
    
def deleteLocators():
    nodes=cmds.ls('Loc_*')
    nodes.append('GRP_Loc_Master')
    if cmds.objExists('GRP_Loc_Secondary'):
        nodes.append('GRP_Loc_Secondary')
    
    result = cmds.confirmDialog(title='Delete Locators',
                                message='Do you want to delete all the locators?',
                                button=['Yes', 'No'],
                                defaultButton='Yes',
                                cancelButton='No')

    # EXECUTE button
    if result == 'Yes':
        cmds.delete(nodes)     

 