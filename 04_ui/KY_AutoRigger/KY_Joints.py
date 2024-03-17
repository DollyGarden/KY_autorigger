#  ********************************************************************
#  content = Generate full body joints
#  version = 0.1.4
#  date = 2022-02-13
#  dependencies = Maya
# 
#  license = MIT
#  author = Kelly Yang <kelly.yang1116@hotmail.com>
#  ********************************************************************


import maya.cmds as cmds


def create_joints():
    if cmds.objExists('GRP_RIG'):
        cmds.delete('GRP_RIG')

    joints_grp = cmds.group(empty=True, name='GRP_RIG')
    locators   = cmds.ls('Loc_*', type='transform')

    #  create all joints with the same name and transform as locators, but don't parent to each other
    for loc in locators:
        pos = cmds.xform(loc, q=True, ws=True, t=True)
        joint_name = loc.replace('Loc', 'RIG')
        new_joint = cmds.joint(name=joint_name, position=pos)
        cmds.select(deselect=True)

    #  Put all joints in to a list, except 'RIG_ROOT'
    joints = cmds.ls('RIG_*', type='transform')
    joints.remove('RIG_ROOT')
    sec_joints_list = []
    #  get the parent-child relationship of locators, then parent the joints to it's parent joint.
    for new_joint in joints:
        #  for the body skeleton's parent-child relationship
        if 'sec' not in new_joint:
            joint_locator_name = new_joint.replace('RIG', 'Loc')
            parent_loc = cmds.listRelatives(joint_locator_name, parent=True, type='transform')[0]
            parent_joint = parent_loc. replace('Loc', 'RIG')
            cmds.parent(new_joint, parent_joint)
        #  do the reverse foot and armtwist parent-child relationship one by one
        else:
            sec_joints_list.append(new_joint)

    if sec_joints_list:
        sides = ['L', 'R']
        for side in sides:
            #  reverse foot
            cmds.parent('RIG_'+side+'_sec_INV_Toes', 'RIG_'+side+'_sec_INV_Heel')
            cmds.parent('RIG_'+side+'_sec_INV_Ball', 'RIG_'+side+'_sec_INV_Toes')
            cmds.parent('RIG_'+side+'_sec_INV_Ankle', 'RIG_'+side+'_sec_INV_Ball')
            cmds.parent('RIG_'+side+'_sec_INV_Heel', joints_grp)
            #  armtwist
            arm_twist_list = cmds.ls('RIG_'+side+'_sec_armTwist_*', type='transform')
            cmds.parent('RIG_'+side+'_sec_armTwist_0', 'RIG_'+side+'_Elbow')
            for x in range(1, len(arm_twist_list)):
                cmds.parent('RIG_'+side+'_sec_armTwist_'+str(x), 'RIG_'+side+'_sec_armTwist_'+str(x-1))
            cmds.parent('RIG_'+side+'_Wrist', 'RIG_'+side+'_sec_armTwist_'+str(len(arm_twist_list)-1))

    #  set the orientation of all the joints
    set_joint_orientation()

    #  put all joints into a group
    cmds.parent('RIG_ROOT', joints_grp)


def set_joint_orientation():

    cmds.joint('RIG_ROOT', edit=True, ch=True, orientJoint='xyz', secondaryAxisOrient='yup')
    if cmds.objExists('RIG_L_sec_INV_Heel'):
        cmds.joint('RIG_L_sec_INV_Heel', edit=True, ch=True, orientJoint='xyz', secondaryAxisOrient='yup')
    if cmds.objExists('RIG_R_sec_INV_Heel'):
        cmds.joint('RIG_R_sec_INV_Heel', edit=True, ch=True, orientJoint='xyz', secondaryAxisOrient='yup')

    #  change the right arm and leg axis orient to make it mirror with the left
    r_joints_list = cmds.ls("RIG_R_*", type='transform')
    for r_joint in r_joints_list:
        cmds.xform(r_joint, preserve=True, rotateAxis=[180, 180, 0])


def delete_joints():
    cmds.select(deselect=True)
    cmds.delete(cmds.ls('GRP_RIG'))