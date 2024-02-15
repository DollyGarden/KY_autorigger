# ********************************************************************
# content = create locators for the reference of the position of the joint
# version = 0.1.2
# date = 2022-02-15
# dependencies = Maya
#
# license = MIT
# author = Kelly Yang <kelly.yang1116@hotmail.com>
# ********************************************************************


import maya.cmds as cmds

# create the spine function
def create_spine(spine_value):
    for i in range(0, spine_value):
        spine = cmds.spaceLocator(n='Loc_SPINE_'+str(i))
        cmds.scale(0.1, 0.1, 0.1, spine)
        if i == 0:
            cmds.parent(spine, 'Loc_ROOT')
        else:
            cmds.parent(spine, 'Loc_SPINE_'+str(i-1))
        cmds.move(0, 1.75+(0.25*i), 0, spine)


def create_head(spine_value):
    neck_start = cmds.spaceLocator(n='Loc_Neck_Start')
    cmds.parent(neck_start, 'Loc_SPINE_'+str(spine_value-1))
    cmds.scale(1, 1, 1, neck_start)
    cmds.move(0, 1.6+(0.25*spine_value), 0, neck_start)

    neck_end = cmds.spaceLocator(n='Loc_Neck_End')
    cmds.parent(neck_end, 'Loc_Neck_Start')
    cmds.scale(1, 1, 1, neck_end)
    cmds.move(0, 1.75+(0.25*spine_value), 0, neck_end)

    head = cmds.spaceLocator(n='Loc_Head')
    cmds.parent(head, 'Loc_Neck_End')
    cmds.scale(1, 1, 1, head)
    cmds.move(0, 2+(0.25*spine_value), 0, head)

    jaw_end = cmds.spaceLocator(n='Loc_Jaw_End')
    jaw_start = cmds.spaceLocator(n='Loc_Jaw_Start')
    cmds.parent(jaw_start, head)
    cmds.parent(jaw_end, jaw_start)
    cmds.scale(1, 1, 1, jaw_end)
    cmds.scale(0.5, 0.5, 0.5, jaw_start)
    cmds.move(0, 1.9+(0.25*spine_value), 0.02, jaw_start)
    cmds.move(0, 1.9+(0.25*spine_value), 0.15, jaw_end)


def create_legs(side):
    if side == 1:  # left
        # upper_leg
        upper_leg = cmds.spaceLocator(n='Loc_L_UpperLeg')
        cmds.scale(0.1, 0.1, 0.1, upper_leg)
        cmds.move(0.15, 1.5, 0, upper_leg)
        cmds.parent(upper_leg, 'Loc_ROOT')

        # lower_leg
        lower_leg = cmds.spaceLocator(n='Loc_L_LowerLeg')
        cmds.scale(0.1, 0.1, 0.1, lower_leg)
        cmds.move(0.15, 0.75, 0.05, lower_leg)
        cmds.parent(lower_leg, 'Loc_L_UpperLeg')

        # foot
        foot = cmds.spaceLocator(n='Loc_L_Foot')
        cmds.scale(0.1, 0.1, 0.1, foot)
        cmds.move(0.15, 0.2, 0, foot)
        cmds.parent(foot, 'Loc_L_LowerLeg')

        # football
        football = cmds.spaceLocator(n='Loc_L_FootBall')
        cmds.scale(0.1, 0.1, 0.1, football)
        cmds.move(0.15, 0, 0.15, football)
        cmds.parent(football, 'Loc_L_Foot')

        # toes
        toes = cmds.spaceLocator(n='Loc_L_Toes')
        cmds.scale(0.1, 0.1, 0.1, toes)
        cmds.move(0.15, 0, 0.3, toes)
        cmds.parent(toes, 'Loc_L_FootBall')

    else:  # right
        # upper_leg
        upper_leg = cmds.spaceLocator(n='Loc_R_UpperLeg')
        cmds.scale(0.1, 0.1, 0.1, upper_leg)
        cmds.move(-0.15, 1.5, 0, upper_leg)
        cmds.parent(upper_leg, 'Loc_ROOT')

        # lower_leg
        lower_leg = cmds.spaceLocator(n='Loc_R_LowerLeg')
        cmds.scale(0.1, 0.1, 0.1, lower_leg)
        cmds.move(-0.15, 0.75, 0.05, lower_leg)
        cmds.parent(lower_leg, 'Loc_R_UpperLeg')

        # foot
        foot = cmds.spaceLocator(n='Loc_R_Foot')
        cmds.scale(0.1, 0.1, 0.1, foot)
        cmds.move(-0.15, 0.2, 0, foot)
        cmds.parent(foot, 'Loc_R_LowerLeg')

        # football
        football = cmds.spaceLocator(n='Loc_R_FootBall')
        cmds.scale(0.1, 0.1, 0.1, football)
        cmds.move(-0.15, 0, 0.15, football)
        cmds.parent(football, 'Loc_R_Foot')

        # toes
        toes = cmds.spaceLocator(n='Loc_R_Toes')
        cmds.scale(0.1, 0.1, 0.1, toes)
        cmds.move(-0.15, 0, 0.3, toes)
        cmds.parent(toes, 'Loc_R_FootBall')


def create_arms(spine_value, side, finger_value):
    # global editMode
    if side == 1:  # left
        clavicle = cmds.spaceLocator(n='Loc_L_Clavicle')
        cmds.scale(0.1, 0.1, 0.1, clavicle)
        cmds.parent(clavicle, 'Loc_SPINE_'+str(spine_value-1))
        cmds.move(0.1*side, 1.5+(0.25*spine_value), 0.1, clavicle)

        # upper_arm
        upper_arm = cmds.spaceLocator(n='Loc_L_UpperArm')
        cmds.scale(0.1, 0.1, 0.1, upper_arm)
        cmds.parent(upper_arm, clavicle)
        cmds.move(0.35*side, 1.5+(0.25*spine_value), 0, upper_arm)

        # elbow
        elbow = cmds.spaceLocator(n='Loc_L_Elbow')
        cmds.scale(0.1, 0.1, 0.1, elbow)
        cmds.parent(elbow, upper_arm)
        cmds.move(0.8*side, 1.5+(0.25*spine_value), -0.2, elbow)

        # wrist
        wrist = cmds.spaceLocator(n='Loc_L_Wrist')  # wrist
        cmds.scale(0.1, 0.1, 0.1, wrist)
        cmds.parent(wrist, elbow)
        cmds.move(1.2*side, 1.5+(0.25*spine_value), 0, wrist)

        # palm
        palm = cmds.spaceLocator(n='Loc_L_Palm')
        cmds.scale(0.1, 0.1, 0.1, palm)
        cmds.parent(palm, wrist)
        cmds.move(1.25*side, 1.5+(0.25*spine_value), 0, palm)

        create_fingers(side, wrist, finger_value)

    else:
        r_arm = cmds.group(em=True, name='R_Arm_GRP')
        cmds.parent(r_arm, 'Loc_SPINE_'+str(spine_value-1))

        # clavicle start
        clavicle = cmds.spaceLocator(n='Loc_R_Clavicle')
        cmds.scale(0.1, 0.1, 0.1, clavicle)
        cmds.parent(clavicle, 'Loc_SPINE_'+str(spine_value-1))
        cmds.move(0.1*side, 1.5+(0.25*spine_value), 0.1, clavicle)

        # upper_arm
        upper_arm = cmds.spaceLocator(n='Loc_R_UpperArm')
        cmds.scale(0.1, 0.1, 0.1, upper_arm)
        cmds.parent(upper_arm, clavicle)
        cmds.move(0.35*side, 1.5+(0.25*spine_value), 0, upper_arm)

        # elbow
        elbow = cmds.spaceLocator(n='Loc_R_Elbow')
        cmds.scale(0.1, 0.1, 0.1, elbow)
        cmds.parent(elbow, upper_arm)
        cmds.move(0.8*side, 1.5+(0.25*spine_value), -0.2, elbow)

        # wrist
        wrist = cmds.spaceLocator(n='Loc_R_Wrist')
        cmds.scale(0.1, 0.1, 0.1, wrist)
        cmds.parent(wrist, elbow)
        cmds.move(1.2*side, 1.5+(0.25*spine_value), 0, wrist)

        # palm
        palm = cmds.spaceLocator(n='Loc_R_Palm')
        cmds.scale(0.1, 0.1, 0.1, palm)
        cmds.parent(palm, wrist)
        cmds.move(1.25*side, 1.5+(0.25*spine_value), 0, palm)

        create_fingers(side, wrist, finger_value)


def create_fingers(side, wrist, finger_value):
    hand_pos = cmds.xform(wrist, q=True, t=True, ws=True)
    for i in range(0, finger_value):
        for x in range(0, 4):
            if side == 1:
                finger = cmds.spaceLocator(n='Loc_L_Finger_'+str(i)+'_'+str(x))
                cmds.scale(0.05, 0.05, 0.05, finger)
                if x == 0:
                    cmds.parent(finger, wrist)
                else:
                    cmds.parent(finger, 'Loc_L_Finger_'+str(i)+'_'+str(x-1))
                cmds.move(hand_pos[0]+(0.1+(0.1*x))*side, hand_pos[1], hand_pos[2]+-(0.05*i), finger)
            else:
                finger = cmds.spaceLocator(n='Loc_R_Finger_'+str(i)+'_'+str(x))
                cmds.scale(0.05, 0.05, 0.05, finger)
                if x == 0:
                    cmds.parent(finger, wrist)
                else:
                    cmds.parent(finger, 'Loc_R_Finger_'+str(i)+'_'+str(x-1))
                cmds.move(hand_pos[0]+(0.1+(0.1*x))*side, hand_pos[1], hand_pos[2]+-(0.05*i), finger)


def set_colors():
    cmds.setAttr('GRP_Loc_Master.overrideEnabled', 1)
    cmds.setAttr('GRP_Loc_Master.overrideRGBColors', 1)
    cmds.setAttr('GRP_Loc_Master.overrideColorRGB', 1, 1, 0)


def mirror_locators():
    l_locators = cmds.ls('Loc_L_*', type='transform')
    for l_locator in l_locators:
        last_name = l_locator.replace('Loc_L_', '')
        neg_attrs = ['.translateX', '.rotateY', '.rotateZ']
        pos_attrs = ['.translateY', '.translateZ', '.rotateX']
        for neg_attr in neg_attrs:
            if not cmds.getAttr(l_locator+neg_attr, lock=True):
                l_locator_attribute = cmds.getAttr(l_locator+neg_attr)
                cmds.setAttr('Loc_R_'+last_name+neg_attr, -1*l_locator_attribute)
        for pos_attr in pos_attrs:
            if not cmds.getAttr(l_locator+pos_attr, lock=True):
                l_locator_attribute = cmds.getAttr(l_locator+pos_attr)
                cmds.setAttr('Loc_R_'+last_name+pos_attr, l_locator_attribute)


def lock_locator_attr():
    axis = ['X', 'Y', 'Z']
    for axe in axis:
        cmds.setAttr('GRP_Loc_Master.rotate'+axe, lock=True, k=False)
        cmds.setAttr('Loc_*_Wrist.scale'+axe, lock=True, k=False)
        l_finger_locators = cmds.ls('Loc_L_Finger_*_0', type='transform')
        r_finger_locators = cmds.ls('Loc_R_Finger_*_0', type='transform')
        all_locators      = cmds.ls('Loc_*', type='transform')
        for l in all_locators:
            if "Finger" in l:
                None
            else:
                if 'Wrist' in l:
                    cmds.setAttr(l+'.scale'+axe, lock=True, k=False)
                else:
                    cmds.setAttr(l+'.scale'+axe, lock=True, k=False)
                    cmds.setAttr(l+'.rotate'+axe, lock=True, k=False)

        for j in range(0, len(l_finger_locators)):
            for k in range(0, 3):
                cmds.setAttr('Loc_L_Finger_'+str(j)+"_"+str(k)+'.scale'+axe, lock=True, k=False)

                if k > 0:
                    cmds.setAttr('Loc_L_Finger_'+str(j)+"_"+str(k) +'.translate'+axe, lock=True, k=False)
                    cmds.setAttr('Loc_L_Finger_'+str(j)+"_" +str(k)+'.rotateX', lock=True, k=False)
                    cmds.setAttr('Loc_L_Finger_'+str(j)+"_" +str(k)+'.rotateY', lock=True, k=False)

        for j in range(0, len(r_finger_locators)):
            for k in range(0, 3):
                cmds.setAttr('Loc_R_Finger_'+str(j)+"_"+str(k)+'.scale'+axe, lock=True, k=False)

                if k > 0:
                    cmds.setAttr('Loc_R_Finger_'+str(j)+"_"+str(k)+'.translate'+axe, lock=True, k=False)
                    cmds.setAttr('Loc_R_Finger_'+str(j)+"_"+str(k)+'.rotateX', lock=True, k=False)
                    cmds.setAttr('Loc_R_Finger_'+str(j)+"_"+str(k)+'.rotateY', lock=True, k=False)


def delete_locators():
    nodes = cmds.ls('Loc_*')
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

def create_locators(spine_value, finger_value):
    """Create locators for reference of the joint position.

    Args:
        spine_value (int): How many spine in the rig?
        finger_value (int): How many fingers in the rig?
    """
    if cmds.objExists('GRP_Loc_Master'):
        delete_locators()

    cmds.group(em=True, name="GRP_Loc_Master")

    root = cmds.spaceLocator(n="Loc_ROOT")
    cmds.scale(0.1, 0.1, 0.1, root)
    cmds.move(0, 1.5, 0, root)
    cmds.parent(root, "GRP_Loc_Master")

    create_spine(spine_value)
    create_head(spine_value)
    create_arms(spine_value, 1, finger_value)
    create_arms(spine_value, -1, finger_value)
    create_legs(1)
    create_legs(-1)
    set_colors()
    lock_locator_attr()