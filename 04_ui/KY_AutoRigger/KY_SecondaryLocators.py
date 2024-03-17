#  ********************************************************************
#  content = create secondary locators
#  version = 0.1.4
#  date = 2022-03-18
#  dependencies = Maya
# 
#  license = MIT
#  author = Kelly Yang <kelly.yang1116@hotmail.com>
#  ********************************************************************


import maya.cmds as cmds

def check_group():
    if cmds.objExists("GRP_Loc_Secondary"):
        print("Secondary locators are exists already!")
    else:
        cmds.group(empty=True, name="GRP_Loc_Secondary")

    set_colors()

def create_reverse_footroll():
    check_group()

    cmds.select(deselect=True)

    sides = ["L", "R"]
    for side in sides:
        #  heels
        rev_heel = cmds.spaceLocator(name="Loc_"+side+"_sec_INV_Heel")
        cmds.scale(0.05, 0.05, 0.05, rev_heel)
        heel_loc = cmds.xform(cmds.ls("Loc_"+side+"_Foot"), query=True, translation=True, worldSpace=True)
        cmds.move(heel_loc[0], 0, heel_loc[2], rev_heel)
        cmds.parent(rev_heel, "GRP_Loc_Secondary")

        #  toes
        toe_loc = cmds.xform(cmds.ls("Loc_"+side+"_Toes"), query=True, translation=True, worldSpace=True)
        rev_toes = cmds.spaceLocator(name="Loc_"+side+"_sec_INV_Toes")
        cmds. scale(0.05, 0.05, 0.05, rev_toes)
        cmds.move(toe_loc[0], toe_loc[1], toe_loc[2], rev_toes)
        cmds.parent(rev_toes, "Loc_"+side+"_sec_INV_Heel")

        #  toe ball
        ball_loc = cmds.xform(cmds.ls("Loc_"+side+"_FootBall"), query=True, translation=True, worldSpace=True)
        rev_ball = cmds.spaceLocator(name="Loc_"+side+"_sec_INV_Ball")
        cmds. scale(0.05, 0.05, 0.05, rev_ball)
        cmds.move(ball_loc[0], ball_loc[1], ball_loc[2], rev_ball)
        cmds.parent(rev_ball, "Loc_"+side+"_sec_INV_Toes")

        #  ankle
        ankle_loc = cmds.xform(cmds.ls("Loc_"+side+"_Foot"), query=True, translation=True, worldSpace=True)
        rev_ankle = cmds.spaceLocator(name="Loc_"+side+"_sec_INV_Ankle")
        cmds. scale(0.05, 0.05, 0.05, rev_ankle)
        cmds.move(ankle_loc[0], ankle_loc[1], ankle_loc[2], rev_ankle)
        cmds.parent(rev_ankle, "Loc_"+side+"_sec_INV_Ball")


def create_forearm_twist(amount):
    check_group()
    cmds.select(deselect=True)

    sides = ["L", "R"]
    for side in sides:
        elbow_pos = cmds.xform(cmds.ls("Loc_"+side+"_Elbow"), query=True, translation=True, worldSpace=True)
        wrist_pos = cmds.xform(cmds.ls("Loc_"+side+"_Wrist"), query=True, translation=True, worldSpace=True)

        vectorX = wrist_pos[0]-elbow_pos[0]
        vectorY = wrist_pos[1]-elbow_pos[1]
        vectorZ = wrist_pos[2]-elbow_pos[2]

        for index in range(amount-1):
            twist_loc = cmds.spaceLocator(name="Loc_"+side+"_sec_armTwist_"+str(index))
            cmds.move(elbow_pos[0]+(vectorX/amount)+((vectorX/amount)*index),
                      elbow_pos[1]+(vectorY/amount)+((vectorY/amount)*index),
                      elbow_pos[2]+(vectorZ/amount)+((vectorZ/amount)*index),
                      twist_loc)
            cmds.scale(0.05, 0.05, 0.05, twist_loc)
            cmds.parent(twist_loc, "GRP_Loc_Secondary")


def set_colors():
    cmds.setAttr("GRP_Loc_Secondary.overrideEnabled", 1)
    cmds.setAttr("GRP_Loc_Secondary.overrideRGBColors", 1)
    cmds.setAttr("GRP_Loc_Secondary.overrideColorRGB", 1, 1, 1)


def delete_secondary_locator():
    cmds.delete(cmds.ls("GRP_Loc_Secondary"))

