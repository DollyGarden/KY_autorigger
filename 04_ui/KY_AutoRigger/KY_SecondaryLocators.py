#  ********************************************************************
#  content = create secondary locators
#  version = 0.1.2
#  date = 2022-02-15
#  dependencies = Maya
# 
#  license = MIT
#  author = Kelly Yang <kelly.yang1116@hotmail.com>
#  ********************************************************************


import maya.cmds as cmds

from math import pow, sqrt, cos, acos, radians


def check_group():
    if cmds.objExists('GRP_Loc_Secondary'):
        print('Secondary locators are exists already!')
    else:
        cmds.group(em=True, n="GRP_Loc_Secondary")

    set_colors()


def create_reverse_footroll():
    check_group()

    cmds.select(deselect=True)
    #  heels
    l_rev_heel = cmds.spaceLocator(n="Loc_L_sec_INV_Heel")
    cmds.scale(0.05, 0.05, 0.05, l_rev_heel)
    l_heel_loc = cmds.xform(cmds.ls("Loc_L_Foot"), q=True, t=True, ws=True)
    cmds.move(l_heel_loc[0], 0, l_heel_loc[2], l_rev_heel)
    cmds.parent(l_rev_heel, 'GRP_Loc_Secondary')

    r_rev_heel = cmds.spaceLocator(n="Loc_R_sec_INV_Heel")
    cmds.scale(0.05, 0.05, 0.05, r_rev_heel)
    r_heel_loc = cmds.xform(cmds.ls("Loc_R_Foot"), q=True, t=True, ws=True)
    cmds.move(r_heel_loc[0], 0, r_heel_loc[2], r_rev_heel)
    cmds.parent(r_rev_heel, 'GRP_Loc_Secondary')

    #  toes
    l_toe_loc = cmds.xform(cmds.ls("Loc_L_Toes"), q=True, t=True, ws=True)
    l_rev_toes = cmds.spaceLocator(n="Loc_L_sec_INV_Toes")
    cmds. scale(0.05, 0.05, 0.05, l_rev_toes)
    cmds.move(l_toe_loc[0], l_toe_loc[1], l_toe_loc[2], l_rev_toes)
    cmds.parent(l_rev_toes, 'Loc_L_sec_INV_Heel')

    r_toe_loc = cmds.xform(cmds.ls("Loc_R_Toes"), q=True, t=True, ws=True)
    r_rev_toes = cmds.spaceLocator(n="Loc_R_sec_INV_Toes")
    cmds. scale(0.05, 0.05, 0.05, r_rev_toes)
    cmds.move(r_toe_loc[0], r_toe_loc[1], r_toe_loc[2], r_rev_toes)
    cmds.parent(r_rev_toes, 'Loc_R_sec_INV_Heel')

    #  toe ball
    l_ball_loc = cmds.xform(cmds.ls("Loc_L_FootBall"), q=True, t=True, ws=True)
    l_rev_ball = cmds.spaceLocator(n="Loc_L_sec_INV_Ball")
    cmds. scale(0.05, 0.05, 0.05, l_rev_ball)
    cmds.move(l_ball_loc[0], l_ball_loc[1], l_ball_loc[2], l_rev_ball)
    cmds.parent(l_rev_ball, 'Loc_L_sec_INV_Toes')

    r_ball_loc = cmds.xform(cmds.ls("Loc_R_FootBall"), q=True, t=True, ws=True)
    r_rev_ball = cmds.spaceLocator(n="Loc_R_sec_INV_Ball")
    cmds. scale(0.05, 0.05, 0.05, r_rev_ball)
    cmds.move(r_ball_loc[0], r_ball_loc[1], r_ball_loc[2], r_rev_ball)
    cmds.parent(r_rev_ball, 'Loc_R_sec_INV_Toes')

    #  ankle
    l_ankle_loc = cmds.xform(cmds.ls("Loc_L_Foot"), q=True, t=True, ws=True)
    l_rev_ankle = cmds.spaceLocator(n="Loc_L_sec_INV_Ankle")
    cmds. scale(0.05, 0.05, 0.05, l_rev_ankle)
    cmds.move(l_ankle_loc[0], l_ankle_loc[1], l_ankle_loc[2], l_rev_ankle)
    cmds.parent(l_rev_ankle, 'Loc_L_sec_INV_Ball')

    r_ankle_loc = cmds.xform(cmds.ls("Loc_R_Foot"), q=True, t=True, ws=True)
    r_rev_ankle = cmds.spaceLocator(n="Loc_R_sec_INV_Ankle")
    cmds. scale(0.05, 0.05, 0.05, r_rev_ankle)
    cmds.move(r_ankle_loc[0], r_ankle_loc[1], r_ankle_loc[2], r_rev_ankle)
    cmds.parent(r_rev_ankle, 'Loc_R_sec_INV_Ball')


def create_forearm_twist(amount):
    check_group()
    cmds.select(deselect=True)
    global arm_twist
    #  left arm twist locatorR
    l_elbow_pos = cmds.xform(cmds.ls('Loc_L_Elbow'), q=True, t=True, ws=True)
    l_wrist_pos = cmds.xform(cmds.ls('Loc_L_Wrist'), q=True, t=True, ws=True)

    l_vectorX = l_wrist_pos[0]-l_elbow_pos[0]
    l_vectorY = l_wrist_pos[1]-l_elbow_pos[1]
    l_vectorZ = l_wrist_pos[2]-l_elbow_pos[2]

    for i in range(amount-1):
        l_twist_loc = cmds.spaceLocator(n='Loc_L_sec_armTwist_'+str(i))
        cmds.move(l_elbow_pos[0]+(l_vectorX/amount)+((l_vectorX/amount)*i),
                  l_elbow_pos[1]+(l_vectorY/amount)+((l_vectorY/amount)*i),
                  l_elbow_pos[2]+(l_vectorZ/amount)+((l_vectorZ/amount)*i),
                  l_twist_loc)
        cmds.scale(0.05, 0.05, 0.05, l_twist_loc)
        cmds.parent(l_twist_loc, 'GRP_Loc_Secondary')

    #  right arm twist locator
    r_elbow_pos = cmds.xform(cmds.ls('Loc_R_Elbow'), q=True, t=True, ws=True)
    r_wrist_pos = cmds.xform(cmds.ls('Loc_R_Wrist'), q=True, t=True, ws=True)

    r_vectorX = r_wrist_pos[0] - r_elbow_pos[0]
    r_vectorY = r_wrist_pos[1] - r_elbow_pos[1]
    r_vectorZ = r_wrist_pos[2] - r_elbow_pos[2]

    for j in range(amount-1):
        r_twist_loc = cmds.spaceLocator(n='Loc_R_sec_armTwist_'+str(j))
        cmds.move(r_elbow_pos[0]+(r_vectorX/amount)+((r_vectorX/amount)*j),
                  r_elbow_pos[1]+(r_vectorY/amount)+((r_vectorY/amount)*j),
                  r_elbow_pos[2]+(r_vectorZ/amount)+((r_vectorZ/amount)*j),
                  r_twist_loc)
        cmds.scale(0.05, 0.05, 0.05, r_twist_loc)
        cmds.parent(r_twist_loc, 'GRP_Loc_Secondary')


def set_colors():
    cmds.setAttr('GRP_Loc_Secondary.overrideEnabled', 1)
    cmds.setAttr('GRP_Loc_Secondary.overrideRGBColors', 1)
    cmds.setAttr('GRP_Loc_Secondary.overrideColorRGB', 1, 1, 1)


def DeleteSecondary():
    cmds.delete(cmds.ls('GRP_Loc_Secondary'))


def create_seclocator_windows():
    cmds.window("Secondary Controllers")
    cmds.rowColumnLayout(nc=1)
    cmds.button(l="Create Reverse Footroll", w=200, c="KY_SecondaryLocators.create_reverse_footroll()")
    cmds.separator(h=10)
    cmds.text("Twist Amount", l="Amount of twist joints")
    arm_twist = cmds.intField(minValue=2, maxValue=10, value=3)
    cmds.button(l="Create Forearm Twist", w=200,
                c="KY_SecondaryLocators.create_forearm_twist("+str(cmds.intField(arm_twist, query=True, value=True))+")")
    cmds.separator(h=10)
    cmds.button(l="Delete Locators", w=200, c="KY_SecondaryLocators.DeleteSecondary()")
    cmds.showWindow()
