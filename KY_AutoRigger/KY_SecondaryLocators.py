import maya.cmds as cmds
from math import pow, sqrt, cos, acos, radians

def CreateSecLocatorWindows():
    cmds.window("Secondary Controllers")
    cmds.rowColumnLayout(nc=1)
    cmds.button(l="Create Reverse Footroll", w=200, c="KY_SecondaryLocators.CreateReverseFootroll()")
    cmds.separator(h=10)
    cmds.text("Twist Amount", l="Amount of twist joints")
    armTwist=cmds.intField(minValue=2, maxValue=10, value=3)
    cmds.button(l="Create Forearm Twist", w=200, 
                c="KY_SecondaryLocators.CreateForearmTwist("+str(cmds.intField(armTwist, query=True, value=True))+")") #??what does this mean?
    cmds.separator(h=10)
    cmds.button(l="Delete Locators", w=200, c="KY_SecondaryLocators.DeleteSecondary()")
    cmds.showWindow()
    
#???why always need to check?
def CheckGroup():
    if cmds.objExists('GRP_Loc_Secondary'):
        print('Secondary locators are exists already!')
    else:
        cmds.group(em=True, n="GRP_Loc_Secondary")
        
    setColors()
    
def CreateReverseFootroll():
    CheckGroup()
    
    cmds.select(deselect=True)
    #heels
    l_rev_heel=cmds.spaceLocator(n="Loc_L_sec_INV_Heel")
    cmds.scale(0.05, 0.05, 0.05, l_rev_heel)
    l_heelLoc=cmds.xform(cmds.ls("Loc_L_Foot"), q=True, t=True, ws=True)
    cmds.move(l_heelLoc[0], 0, l_heelLoc[2], l_rev_heel)
    cmds.parent(l_rev_heel, 'GRP_Loc_Secondary')
    
    r_rev_heel=cmds.spaceLocator(n="Loc_R_sec_INV_Heel")
    cmds.scale(0.05, 0.05, 0.05, r_rev_heel)
    r_heelLoc=cmds.xform(cmds.ls("Loc_R_Foot"), q=True, t=True, ws=True)
    cmds.move(r_heelLoc[0], 0, r_heelLoc[2], r_rev_heel)
    cmds.parent(r_rev_heel, 'GRP_Loc_Secondary')
       
    #toes
    l_toeLoc=cmds.xform(cmds.ls("Loc_L_Toes"), q=True, t=True, ws=True)
    l_rev_toes=cmds.spaceLocator(n="Loc_L_sec_INV_Toes")
    cmds. scale(0.05, 0.05, 0.05, l_rev_toes)
    cmds.move(l_toeLoc[0], l_toeLoc[1], l_toeLoc[2], l_rev_toes)
    cmds.parent(l_rev_toes, 'Loc_L_sec_INV_Heel')   
    
    r_toeLoc=cmds.xform(cmds.ls("Loc_R_Toes"), q=True, t=True, ws=True)
    r_rev_toes=cmds.spaceLocator(n="Loc_R_sec_INV_Toes")
    cmds. scale(0.05, 0.05, 0.05, r_rev_toes)
    cmds.move(r_toeLoc[0], r_toeLoc[1], r_toeLoc[2], r_rev_toes)
    cmds.parent(r_rev_toes, 'Loc_R_sec_INV_Heel') 
    
    #toe ball
    l_ballLoc=cmds.xform(cmds.ls("Loc_L_FootBall"), q=True, t=True, ws=True)
    l_rev_ball=cmds.spaceLocator(n="Loc_L_sec_INV_Ball")
    cmds. scale(0.05, 0.05, 0.05, l_rev_ball)
    cmds.move(l_ballLoc[0], l_ballLoc[1],l_ballLoc[2], l_rev_ball)
    cmds.parent(l_rev_ball, 'Loc_L_sec_INV_Toes')   
    
    r_ballLoc=cmds.xform(cmds.ls("Loc_R_FootBall"), q=True, t=True, ws=True)
    r_rev_ball=cmds.spaceLocator(n="Loc_R_sec_INV_Ball")
    cmds. scale(0.05, 0.05, 0.05, r_rev_ball)
    cmds.move(r_ballLoc[0], r_ballLoc[1], r_ballLoc[2], r_rev_ball)
    cmds.parent(r_rev_ball, 'Loc_R_sec_INV_Toes')         
    
    #ankle
    l_ankleLoc=cmds.xform(cmds.ls("Loc_L_Foot"), q=True, t=True, ws=True)
    l_rev_ankle=cmds.spaceLocator(n="Loc_L_sec_INV_Ankle")
    cmds. scale(0.05, 0.05, 0.05, l_rev_ankle)
    cmds.move(l_ankleLoc[0], l_ankleLoc[1], l_ankleLoc[2], l_rev_ankle)
    cmds.parent(l_rev_ankle, 'Loc_L_sec_INV_Ball')   
    
    r_ankleLoc=cmds.xform(cmds.ls("Loc_R_Foot"), q=True, t=True, ws=True)
    r_rev_ankle=cmds.spaceLocator(n="Loc_R_sec_INV_Ankle")
    cmds. scale(0.05, 0.05, 0.05, r_rev_ankle)
    cmds.move(r_ankleLoc[0], r_ankleLoc[1], r_ankleLoc[2], r_rev_ankle)
    cmds.parent(r_rev_ankle, 'Loc_R_sec_INV_Ball')   
    
def CreateForearmTwist(amount):
    CheckGroup()
    cmds.select(deselect=True)
    global armTwist
    #left arm twist locator
    L_elbowPos=cmds.xform(cmds.ls('Loc_L_Elbow'), q=True, t=True, ws=True)    
    L_wristPos=cmds.xform(cmds.ls('Loc_L_Wrist'), q=True, t=True, ws=True)    
    
    L_vectorX=L_wristPos[0]-L_elbowPos[0]
    L_vectorY=L_wristPos[1]-L_elbowPos[1]
    L_vectorZ=L_wristPos[2]-L_elbowPos[2]  
    
    for i in range(amount-1):
        l_twistLoc=cmds.spaceLocator(n='Loc_L_sec_armTwist_'+str(i))
        cmds.move(L_elbowPos[0]+(L_vectorX/amount)+((L_vectorX/amount)*i),
                  L_elbowPos[1]+(L_vectorY/amount)+((L_vectorY/amount)*i),
                  L_elbowPos[2]+(L_vectorZ/amount)+((L_vectorZ/amount)*i),
                  l_twistLoc)
        cmds.scale(0.05,0.05,0.05, l_twistLoc)
        cmds.parent(l_twistLoc, 'GRP_Loc_Secondary')

    #right arm twist locator
    R_elbowPos=cmds.xform(cmds.ls('Loc_R_Elbow'), q=True, t=True, ws=True)    
    R_wristPos=cmds.xform(cmds.ls('Loc_R_Wrist'), q=True, t=True, ws=True)    
    
    R_vectorX=R_wristPos[0]-R_elbowPos[0]
    R_vectorY=R_wristPos[1]-R_elbowPos[1]
    R_vectorZ=R_wristPos[2]-R_elbowPos[2]  
    
    for j in range(amount-1):
        r_twistLoc=cmds.spaceLocator(n='Loc_R_sec_armTwist_'+str(j))
        cmds.move(R_elbowPos[0]+(R_vectorX/amount)+((R_vectorX/amount)*j),
                  R_elbowPos[1]+(R_vectorY/amount)+((R_vectorY/amount)*j),
                  R_elbowPos[2]+(R_vectorZ/amount)+((R_vectorZ/amount)*j),
                  r_twistLoc)
        cmds.scale(0.05,0.05,0.05, r_twistLoc)
        cmds.parent(r_twistLoc, 'GRP_Loc_Secondary')    
        
def setColors():
    cmds.setAttr('GRP_Loc_Secondary.overrideEnabled',1) 
    cmds.setAttr('GRP_Loc_Secondary.overrideRGBColors',1)
    cmds.setAttr('GRP_Loc_Secondary.overrideColorRGB',1,1,1)   
    
def DeleteSecondary():
    cmds.delete(cmds.ls('GRP_Loc_Secondary'))                 
                