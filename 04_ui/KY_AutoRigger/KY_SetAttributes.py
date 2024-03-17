# ********************************************************************
#  content = Lock unnecessary attributes on controllers
#  version = 0.1.4
#  date = 2022-03-18
#  dependencies = Maya
# 
#  license = MIT
#  author = Kelly Yang <kelly.yang1116@hotmail.com>
# ********************************************************************


import maya.cmds as cmds

def lock_attributes():
    axis = ['X', 'Y', 'Z']
    all_spines    = cmds.ls('CTRL_SPINE_*', type='transform')
    all_fingers = cmds.ls('CTRL_*_Finger_*_0', type='transform')    

    for axe in axis:
        cmds.setAttr('CTRL_PELVIS.scale'+axe, lock=True, keyable=False)
        for i in range(0, len(all_spines)):
            cmds.setAttr('CTRL_SPINE_'+str(i)+'.translate'+axe, lock=True, keyable=False)
            cmds.setAttr('CTRL_SPINE_'+str(i)+'.scale'+axe, lock=True, keyable=False)
            
        cmds.setAttr('CTRL_NECK.scale'+axe, lock=True, keyable=False)    
        cmds.setAttr('CTRL_NECK.translate'+axe, lock=True, keyable=False)
        cmds.setAttr('CTRL_HEAD.scale'+axe, lock=True, keyable=False)    
        cmds.setAttr('CTRL_HEAD.translate'+axe, lock=True, keyable=False)
        cmds.setAttr('CTRL_JAW.scale'+axe, lock=True, keyable=False)    
        cmds.setAttr('CTRL_JAW.translate'+axe, lock=True, keyable=False)

        sides = ["L", "R"]
        for side in sides:
            cmds.setAttr('CTRL_'+side+'_Wrist.scale'+axe, lock=True, keyable=False)
            cmds.setAttr('CTRL_'+side+'_Foot.scale'+axe, lock=True, keyable=False)
            cmds.setAttr('CTRL_'+side+'_Clavicle.scale'+axe, lock=True, keyable=False)
            cmds.setAttr('CTRL_'+side+'_Clavicle.translate'+axe, lock=True, keyable=False)
            
            for finger_index in range(0, int(len(all_fingers)/4)):
                for finger_joint in range(0, 3):
                    cmds.setAttr('CTRL_'+side+'_Finger_'+str(finger_index)+"_"+str(finger_joint)+'.scale'+axe, lock=True, keyable=False)
                    cmds.setAttr('CTRL_'+side+'_Finger_'+str(finger_index)+"_"+str(finger_joint)+'.translate'+axe, lock=True, keyable=False) 
                    if finger_joint > 0:
                        cmds.setAttr('CTRL_'+side+'_Finger_'+str(finger_index)+"_"+str(finger_joint)+'.rotateX', lock=True, keyable=False)
                        cmds.setAttr('CTRL_'+side+'_Finger_'+str(finger_index)+"_"+str(finger_joint)+'.rotateY', lock=True, keyable=False)