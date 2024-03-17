#  ********************************************************************
#  content = create locators for the reference of the position of the joint
#  version = 0.1.4
#  date = 2022-03-18
#  dependencies = Maya
# 
#  license = MIT
#  author = Kelly Yang <kelly.yang1116@hotmail.com>
#  ********************************************************************


import maya.cmds as cmds

def create_spine(spine_count):
    for spine_index in range(0, spine_count):
        spine = cmds.spaceLocator(name='Loc_SPINE_'+str(spine_index))
        cmds.scale(0.1, 0.1, 0.1, spine)
        if spine_index == 0:
            cmds.parent(spine, 'Loc_ROOT')
        else:
            cmds.parent(spine, 'Loc_SPINE_'+str(spine_index-1))
        cmds.move(0, 1.75+(0.25*spine_index), 0, spine)


def create_head(spine_count):
    neck_start = cmds.spaceLocator(name='Loc_Neck_Start')
    cmds.parent(neck_start, 'Loc_SPINE_'+str(spine_count-1))
    cmds.scale(1, 1, 1, neck_start)
    cmds.move(0, 1.6+(0.25*spine_count), 0, neck_start)

    neck_end = cmds.spaceLocator(name='Loc_Neck_End')
    cmds.parent(neck_end, 'Loc_Neck_Start')
    cmds.scale(1, 1, 1, neck_end)
    cmds.move(0, 1.75+(0.25*spine_count), 0, neck_end)

    head = cmds.spaceLocator(name='Loc_Head')
    cmds.parent(head, 'Loc_Neck_End')
    cmds.scale(1, 1, 1, head)
    cmds.move(0, 2+(0.25*spine_count), 0, head)

    jaw_end = cmds.spaceLocator(name='Loc_Jaw_End')
    jaw_start = cmds.spaceLocator(name='Loc_Jaw_Start')
    cmds.parent(jaw_start, head)
    cmds.parent(jaw_end, jaw_start)
    cmds.scale(1, 1, 1, jaw_end)
    cmds.scale(0.5, 0.5, 0.5, jaw_start)
    cmds.move(0, 1.9+(0.25*spine_count), 0.02, jaw_start)
    cmds.move(0, 1.9+(0.25*spine_count), 0.15, jaw_end)


def create_legs(side):
    if side == 1:  
        prefix = "L"
    else:
        prefix = "R"

    # upper_leg
    upper_leg = cmds.spaceLocator(name='Loc_'+prefix+'_UpperLeg')
    cmds.scale(0.1, 0.1, 0.1, upper_leg)
    cmds.move(0.15*side, 1.5, 0, upper_leg)
    cmds.parent(upper_leg, 'Loc_ROOT')

    # lower_leg
    lower_leg = cmds.spaceLocator(name='Loc_'+prefix+'_LowerLeg')
    cmds.scale(0.1, 0.1, 0.1, lower_leg)
    cmds.move(0.15*side, 0.75, 0.05, lower_leg)
    cmds.parent(lower_leg, 'Loc_'+prefix+'_UpperLeg')

    # foot
    foot = cmds.spaceLocator(name='Loc_'+prefix+'_Foot')
    cmds.scale(0.1, 0.1, 0.1, foot)
    cmds.move(0.15*side, 0.2, 0, foot)
    cmds.parent(foot, 'Loc_'+prefix+'_LowerLeg')

    # football
    football = cmds.spaceLocator(name='Loc_'+prefix+'_FootBall')
    cmds.scale(0.1, 0.1, 0.1, football)
    cmds.move(0.15*side, 0, 0.15, football)
    cmds.parent(football, 'Loc_'+prefix+'_Foot')

    # toes
    toes = cmds.spaceLocator(name='Loc_'+prefix+'_Toes')
    cmds.scale(0.1, 0.1, 0.1, toes)
    cmds.move(0.15*side, 0, 0.3, toes)
    cmds.parent(toes, 'Loc_'+prefix+'_FootBall')


def create_arms(spine_count, side, finger_count):

    if side == 1:  
        prefix = "L"
    else:
        prefix = "R"

    # clavicle
    clavicle = cmds.spaceLocator(name='Loc_'+prefix+'_Clavicle')
    cmds.scale(0.1, 0.1, 0.1, clavicle)
    cmds.parent(clavicle, 'Loc_SPINE_'+str(spine_count-1))
    cmds.move(0.1*side, 1.5+(0.25*spine_count), 0.1, clavicle)

    # upper_arm
    upper_arm = cmds.spaceLocator(name='Loc_'+prefix+'_UpperArm')
    cmds.scale(0.1, 0.1, 0.1, upper_arm)
    cmds.parent(upper_arm, clavicle)
    cmds.move(0.35*side, 1.5+(0.25*spine_count), 0, upper_arm)

    # elbow
    elbow = cmds.spaceLocator(name='Loc_'+prefix+'_Elbow')
    cmds.scale(0.1, 0.1, 0.1, elbow)
    cmds.parent(elbow, upper_arm)
    cmds.move(0.8*side, 1.5+(0.25*spine_count), -0.2, elbow)

    # wrist
    wrist = cmds.spaceLocator(name='Loc_'+prefix+'_Wrist')  #  wrist
    cmds.scale(0.1, 0.1, 0.1, wrist)
    cmds.parent(wrist, elbow)
    cmds.move(1.2*side, 1.5+(0.25*spine_count), 0, wrist)

    # palm
    palm = cmds.spaceLocator(name='Loc_'+prefix+'_Palm')
    cmds.scale(0.1, 0.1, 0.1, palm)
    cmds.parent(palm, wrist)
    cmds.move(1.25*side, 1.5+(0.25*spine_count), 0, palm)

    create_fingers(side, wrist, finger_count)


def create_fingers(side, wrist, finger_count):
    hand_pos = cmds.xform(wrist, query=True, translation=True, worldSpace=True)
    for finger_index in range(0, finger_count):
        for finger_joint in range(0, 4):
            if side == 1:  
                prefix = "L"
            else:
                prefix = "R"

            finger = cmds.spaceLocator(name='Loc_'+prefix+'_Finger_'+str(finger_index)+'_'+str(finger_joint))
            cmds.scale(0.05, 0.05, 0.05, finger)
            if finger_joint == 0:
                cmds.parent(finger, wrist)
            else:
                cmds.parent(finger, 'Loc_'+prefix+'_Finger_'+str(finger_index)+'_'+str(finger_joint-1))
            cmds.move(hand_pos[0]+(0.1+(0.1*finger_joint))*side, hand_pos[1], hand_pos[2]+-(0.05*finger_index), finger)


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
    """Lock unnecessary attributes of the locators.
    """
    axis = ['X', 'Y', 'Z']
    for axe in axis:
        cmds.setAttr('GRP_Loc_Master.rotate'+axe, lock=True, keyable=False)
        cmds.setAttr('Loc_*_Wrist.scale'+axe, lock=True, keyable=False)
        finger_locators = cmds.ls('Loc_*_Finger_*_0', type='transform')
        all_locators      = cmds.ls('Loc_*', type='transform')
        for l in all_locators:
            if "Finger" in l:
                None
            else:
                if 'Wrist' in l:
                    cmds.setAttr(l+'.scale'+axe, lock=True, keyable=False)
                else:
                    cmds.setAttr(l+'.scale'+axe, lock=True, keyable=False)
                    cmds.setAttr(l+'.rotate'+axe, lock=True, keyable=False)

        for finger_index in range(0, int(len(finger_locators)/2)):
            for finger_joint in range(0, 4):
                cmds.setAttr('Loc_*_Finger_'+str(finger_index)+"_"+str(finger_joint)+'.scale'+axe, lock=True, keyable=False)

                if finger_joint > 0:
                    cmds.setAttr('Loc_*_Finger_'+str(finger_index)+"_"+str(finger_joint) +'.translate'+axe, lock=True, keyable=False)
                    cmds.setAttr('Loc_*_Finger_'+str(finger_index)+"_" +str(finger_joint)+'.rotateX', lock=True, keyable=False)
                    cmds.setAttr('Loc_*_Finger_'+str(finger_index)+"_" +str(finger_joint)+'.rotateY', lock=True, keyable=False)


def delete_locators():
    """Delete all locators.
    """
    nodes = cmds.ls('Loc_*')
    nodes.append('GRP_Loc_Master')
    if cmds.objExists('GRP_Loc_Secondary'):
        nodes.append('GRP_Loc_Secondary')

    delete_locators_ui = cmds.confirmDialog(title='Delete Locators',
                                message='Do you want to delete all the locators?',
                                button=['Yes', 'No'],
                                defaultButton='Yes',
                                cancelButton='No')

    #  EXECUTE button
    if delete_locators_ui == 'Yes':
        cmds.delete(nodes)


def create_locators(spine_count, finger_count):
    """Create locators for reference of the joint position.

    Args:
        spine_count (int): numbers of spines
        finger_count (int): numbers of fingers
    """
    if cmds.objExists('GRP_Loc_Master'):
        delete_locators()

    cmds.group(empty=True, name="GRP_Loc_Master")

    root = cmds.spaceLocator(name="Loc_ROOT")
    cmds.scale(0.1, 0.1, 0.1, root)
    cmds.move(0, 1.5, 0, root)
    cmds.parent(root, "GRP_Loc_Master")

    create_spine(spine_count)
    create_head(spine_count)
    create_arms(spine_count, 1, finger_count)
    create_arms(spine_count, -1, finger_count)
    create_legs(1)
    create_legs(-1)
    set_colors()
    lock_locator_attr()