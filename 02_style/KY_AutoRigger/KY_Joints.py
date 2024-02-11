import maya.cmds as cmds

# new script to generate full body joints
def create_joints():
    if cmds.objExists('GRP_RIG'):
        cmds.delete('GRP_RIG')

    joints_grp = cmds.group(em=True, name='GRP_RIG')
    locators = cmds.ls('Loc_*',type='transform')

    # create all joints with the same name and transform as locators, but don't parent to each other
    for loc in locators:
        pos = cmds.xform(loc, q=True, ws=True, t=True)
        # rot = cmds.xform(loc, q=True, ws=True, ro=True)
        joint_name = loc.replace('Loc', 'RIG')
        new_joint = cmds.joint(name=joint_name, position=pos)
        cmds.select(deselect=True)   

    # Put all joints in to a list, except 'RIG_ROOT'
    joints = cmds.ls('RIG_*', type='transform')
    joints.remove('RIG_ROOT')
    sec_joints_list = []
    # get the parent-child relationship of locators, then parent the joints to it's parent joint.
    for new_joint in joints:
        # for the body skeleton's parent-child relationship
        if 'sec' not in new_joint:
            # print(new_joint)
            joint_locator_name = new_joint.replace('RIG', 'Loc')
            parent_loc = cmds.listRelatives(joint_locator_name, parent=True, type='transform')[0]
            parent_joint = parent_loc. replace('Loc', 'RIG')
            cmds.parent(new_joint, parent_joint)
        # do the reverse foot and armtwist parent-child relationship one by one
        else:
            sec_joints_list.append(new_joint)

    if sec_joints_list!=[]:
        sides = ['L', 'R']
        for side in sides:
            # # reverse foot
            cmds.parent('RIG_'+side+'_sec_INV_Toes', 'RIG_'+side+'_sec_INV_Heel')
            cmds.parent('RIG_'+side+'_sec_INV_Ball', 'RIG_'+side+'_sec_INV_Toes')
            cmds.parent('RIG_'+side+'_sec_INV_Ankle', 'RIG_'+side+'_sec_INV_Ball')
            cmds.parent('RIG_'+side+'_sec_INV_Heel', joints_grp)
            # armtwist
            armTwist_list = cmds.ls('RIG_'+side+'_sec_armTwist_*', type='transform')
            cmds.parent('RIG_'+side+'_sec_armTwist_0', 'RIG_'+side+'_Elbow')
            for x in range(1, len(armTwist_list)):
                cmds.parent('RIG_'+side+'_sec_armTwist_' + str(x), 'RIG_'+side+'_sec_armTwist_' + str(x-1))
            cmds.parent('RIG_'+side+'_Wrist', 'RIG_'+side+'_sec_armTwist_'+str(len(armTwist_list)-1))

    # set the orientation of all the joints
    setJointOrientation()

    # put all joints into a group
    cmds.parent('RIG_ROOT', joints_grp)



def setJointOrientation():
    
    cmds.joint('RIG_ROOT', edit=True, ch=True, orientJoint='xyz',secondaryAxisOrient = 'yup')
    if cmds.objExists('RIG_L_sec_INV_Heel'):
        cmds.joint('RIG_L_sec_INV_Heel', edit=True, ch=True, orientJoint='xyz',secondaryAxisOrient = 'yup')
    if cmds.objExists('RIG_R_sec_INV_Heel'):
        cmds.joint('RIG_R_sec_INV_Heel', edit=True, ch=True, orientJoint='xyz',secondaryAxisOrient = 'yup')

    # change the right arm and leg axis orient to make it mirror with the left
    r_joints_list=cmds.ls("RIG_R_*", type='transform')
    for r_joint in r_joints_list:
        cmds.xform(r_joint, preserve=True, rotateAxis=[180, 180 ,0])


def deleteJoints():
    cmds.select(deselect=True)
    cmds.delete(cmds.ls('GRP_RIG'))





# old script
# def createJoints(spineAmount, fingerAmount):
#     cmds.select(deselect=True)    
#     if cmds.objExists('RIG'):
#         print('RIG already exists.')
#     else:
#         jointGRP=cmds.group(em=True, name="RIG")
          
#     ## create spine
#     root=cmds.ls("Loc_ROOT")
    
#     allSpines=cmds.ls("Loc_SPINE_*", type='locator')
#     spine=cmds.listRelatives(*allSpines, p=True, f=True)
    
#     rootPos= cmds.xform(root, q=True, t=True, ws=True)
#     rootJoint=cmds.joint(radius=3, p=rootPos, name="RIG_ROOT")
    
#     #cmds.parent(rootJoint, w=True, a=True)
#     #cmds.parent(rootJoint, 'RIG', a=True)
    
#     for i,s in enumerate(spine):
#         pos=cmds.xform(s, q=True, t=True,ws=True)
#         j=cmds.joint(radius=3, p=pos, name="RIG_SPINE_"+str(i))
    
#     createHead(spineAmount)    
#     createArmJoints(spineAmount)
#     createFingersJoints(fingerAmount)
    
#     if(cmds.objExists('Loc_L_INV_Heel*')):
#         createInverseFootRoll()
#     else:
#         print('')
#     createLegs()
#     setJointOrientation()

# def createHead(amount):
#     cmds.select(deselect=True)   
#     cmds.select("RIG_SPINE_"+str(amount-1))
    
#     neckJoint=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_Neck_Start'), q=True, t=True, ws=True), 
#                          name="RIG_Neck_Start")
#     cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_Neck_End'),q=True, t=True, ws=True), name="RIG_Neck_End")
#     cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_Head'),q=True, t=True, ws=True), name="RIG_Head")
#     cmds.select(deselect=True)
#     cmds.select("RIG_Neck_End")
#     jawJointStart=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_Jaw_Start'), q=True, t=True, ws=True), 
#                          name="RIG_Jaw_Start")
#     jawJointEnd=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_Jaw_End'), q=True, t=True, ws=True), 
#                          name="RIG_Jaw_End")
                         
# def createArmJoints(amount):
#     cmds.select(deselect=True) 
#     cmds.select("RIG_SPINE_"+str(amount-1))
#     L_ClavicleJoint=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_L_Clavicle'), q=True, t=True, ws=True), 
#                          name="RIG_L_Clavicle")
#     L_UpperArmJoint=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_L_UpperArm'), q=True, t=True, ws=True), 
#                          name="RIG_L_UpperArm")
#     L_ElbowJoint=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_L_Elbow'), q=True, t=True, ws=True), 
#                          name="RIG_L_Elbow")
#     if (cmds.objExists('Loc_L_ArmTwist_*')):
#         L_armTwists=cmds.ls('Loc_L_ArmTwist_*', type='transform')
#         for i,a in enumerate(L_armTwists):
#             L_armTwistJoint=cmds.joint(radius=3, p=cmds.xform(a, q=True, t=True, ws=True), 
#                          name="RIG_L_ArmTwist_"+str(i))
#         else:
#             print('Donnot create armTwist')
#     L_WristJoint=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_L_Wrist'), q=True, t=True, ws=True), 
#                          name="RIG_L_Wrist")
#     L_PalmJoint=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_L_Palm'), q=True, t=True, ws=True), 
#                          name="RIG_L_Palm")
                         
#     cmds.select(deselect=True) 
#     cmds.select("RIG_SPINE_"+str(amount-1))
#     R_ClavicleJoint=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_R_Clavicle'), q=True, t=True, ws=True), 
#                          name="RIG_R_Clavicle")
#     R_UpperArmJoint=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_R_UpperArm'), q=True, t=True, ws=True), 
#                          name="RIG_R_UpperArm")
#     R_ElbowJoint=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_R_Elbow'), q=True, t=True, ws=True), 
#                          name="RIG_R_Elbow")
#     if (cmds.objExists('Loc_R_ArmTwist_*')):
#         R_armTwists=cmds.ls('Loc_R_ArmTwist_*', type='transform')
#         for i,a in enumerate(R_armTwists):
#             R_armTwistJoint=cmds.joint(radius=3, p=cmds.xform(a, q=True, t=True, ws=True), 
#                          name="RIG_R_ArmTwist_"+str(i))
#         else:
#             print('Donnot create armTwist')
#     R_WristJoint=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_R_Wrist'), q=True, t=True, ws=True), 
#                          name="RIG_R_Wrist")    
#     R_PalmJoint=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_R_Palm'), q=True, t=True, ws=True), 
#                          name="RIG_R_Palm")                     

# def createFingersJoints(amount):
#     for x in range(0, amount):
#         createFingers(x)                 
        
# def createFingers(i): 
#     cmds.select(deselect=True) 
#     cmds.select("RIG_L_Wrist")
#     l_allFingers=cmds.ls("Loc_L_Finger_"+str(i)+'_*', type='transform')
    
#     for x,f in enumerate(l_allFingers):
#         l_pos=cmds.xform(f, q=True, t=True, ws=True)
#         l_j=cmds.joint(radius=3, p=l_pos, name="RIG_L_Finger_"+str(i)+"_"+str(x))   
        
#     cmds.select(deselect=True) 
#     cmds.select("RIG_R_Wrist")
#     r_allFingers=cmds.ls("Loc_R_Finger_"+str(i)+'_*', type='transform')
#     #r_fingers=cmds.listRelatives(r_allFingers, p=True, s=False) 
    
#     for y,g in enumerate(r_allFingers):
#         r_pos=cmds.xform(g, q=True, t=True, ws=True)
#         r_j=cmds.joint(radius=3, p=r_pos, name="RIG_R_Finger_"+str(i)+"_"+str(y))           
        
# def createLegs():
    
#     #left leg joint
#     cmds.select(deselect=True)
#     cmds.select('RIG_ROOT')        
#     L_UpperLegJoint=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_L_UpperLeg',type='transform'), 
#                                q=True, t=True, ws=True), name="RIG_L_UpperLeg")    
#     L_KneeJoint=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_L_LowerLeg',type='transform'), 
#                                q=True, t=True, ws=True), name="RIG_L_LowerLeg")
#     L_FootJoint=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_L_Foot',type='transform'), 
#                                q=True, t=True, ws=True), name="RIG_L_Foot")       
#     L_FootBallJoint=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_L_FootBall',type='transform'), 
#                                q=True, t=True, ws=True), name="RIG_L_FootBall")                                                
#     L_ToeJoint=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_L_Toes',type='transform'), 
#                                q=True, t=True, ws=True), name="RIG_L_Toes")   
                               
#     #right leg joint
#     cmds.select(deselect=True)
#     cmds.select('RIG_ROOT')        
#     R_UpperLegJoint=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_R_UpperLeg',type='transform'), 
#                                q=True, t=True, ws=True), name="RIG_R_UpperLeg")    
#     R_KneeJoint=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_R_LowerLeg',type='transform'), 
#                                q=True, t=True, ws=True), name="RIG_R_LowerLeg")
#     R_FootJoint=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_R_Foot',type='transform'), 
#                                q=True, t=True, ws=True), name="RIG_R_Foot")           
#     R_FootBallJoint=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_R_FootBall',type='transform'), 
#                                q=True, t=True, ws=True), name="RIG_R_FootBall")      
#     R_ToeJoint=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_R_Toes',type='transform'), 
#                                q=True, t=True, ws=True), name="RIG_R_Toes")                            
                               
# def createInverseFootRoll():
#     cmds.select(deselect=True)
#     L_invHeelJoint=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_L_INV_Heel',type='transform'), 
#                               q=True, t=True, ws=True), name="RIG_L_INV_Heel")                                 
#     L_invToeJoint=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_L_INV_Toes',type='transform'), 
#                              q=True, t=True, ws=True), name="RIG_L_INV_Toe")      
#     L_invBallJoint=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_L_INV_Ball',type='transform'), 
#                               q=True, t=True, ws=True), name="RIG_L_INV_Ball")      
#     L_invAnkleJoint=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_L_INV_Ankle',type='transform'), 
#                                q=True, t=True, ws=True), name="RIG_L_INV_Ankle") 
#     cmds.parent(L_invHeelJoint, 'RIG')
    
#     cmds.select(deselect=True)
#     R_invHeelJoint=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_R_INV_Heel',type='transform'), 
#                               q=True, t=True, ws=True), name="RIG_R_INV_Heel")                                 
#     R_invToeJoint=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_R_INV_Toes',type='transform'), 
#                              q=True, t=True, ws=True), name="RIG_R_INV_Toe")      
#     R_invBallJoint=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_R_INV_Ball',type='transform'), 
#                               q=True, t=True, ws=True), name="RIG_R_INV_Ball")      
#     R_invAnkleJoint=cmds.joint(radius=3, p=cmds.xform(cmds.ls('Loc_R_INV_Ankle',type='transform'), 
#                                q=True, t=True, ws=True), name="RIG_R_INV_Ankle") 
#     cmds.parent(R_invHeelJoint, 'RIG')  
    
    
                     
                      
                      
                                                       