import maya.cmds as cmds

def LockAttributes():
    axis=['X', 'Y', 'Z']
    allSpines=cmds.ls('CTRL_SPINE_*', type='transform')
    l_allFingers=cmds.ls('CTRL_L_Finger_*_0', type='transform')
    r_allFingers=cmds.ls('CTRL_R_Finger_*_0', type='transform')
    
    
    for axe in axis:
        cmds.setAttr('CTRL_PELVIS.scale'+axe, lock=True, k=False)
        cmds.setAttr('CTRL_L_Wrist.scale'+axe, lock=True, k=False)
        cmds.setAttr('CTRL_R_Wrist.scale'+axe, lock=True, k=False)
        cmds.setAttr('CTRL_L_Foot.scale'+axe, lock=True, k=False)
        cmds.setAttr('CTRL_R_Foot.scale'+axe, lock=True, k=False)
        cmds.setAttr('CTRL_L_Clavicle.scale'+axe, lock=True, k=False)
        cmds.setAttr('CTRL_L_Clavicle.translate'+axe, lock=True, k=False)
        cmds.setAttr('CTRL_R_Clavicle.scale'+axe, lock=True, k=False)
        cmds.setAttr('CTRL_R_Clavicle.translate'+axe, lock=True, k=False)
   
        for i in range(0, len(allSpines)):
            cmds.setAttr('CTRL_SPINE_'+str(i)+'.translate'+axe, lock=True, k=False)
            cmds.setAttr('CTRL_SPINE_'+str(i)+'.scale'+axe, lock=True, k=False)
            
        cmds.setAttr('CTRL_NECK.scale'+axe, lock=True, k=False)    
        cmds.setAttr('CTRL_NECK.translate'+axe, lock=True, k=False)
        cmds.setAttr('CTRL_HEAD.scale'+axe, lock=True, k=False)    
        cmds.setAttr('CTRL_HEAD.translate'+axe, lock=True, k=False)
        cmds.setAttr('CTRL_JAW.scale'+axe, lock=True, k=False)    
        cmds.setAttr('CTRL_JAW.translate'+axe, lock=True, k=False)
        
        for j in range(0,len(l_allFingers)):
            for k in range(0,3):
                cmds.setAttr('CTRL_L_Finger_'+str(j)+"_"+str(k)+'.scale'+axe, lock=True, k=False)
                cmds.setAttr('CTRL_L_Finger_'+str(j)+"_"+str(k)+'.translate'+axe, lock=True, k=False) 
                if k>0:
                    cmds.setAttr('CTRL_L_Finger_'+str(j)+"_"+str(k)+'.rotateX', lock=True, k=False)
                    cmds.setAttr('CTRL_L_Finger_'+str(j)+"_"+str(k)+'.rotateY', lock=True, k=False)

        for j in range(0,len(r_allFingers)):
            for k in range(0,3):
                cmds.setAttr('CTRL_R_Finger_'+str(j)+"_"+str(k)+'.scale'+axe, lock=True, k=False)
                cmds.setAttr('CTRL_R_Finger_'+str(j)+"_"+str(k)+'.translate'+axe, lock=True, k=False) 
                if k>0:
                    cmds.setAttr('CTRL_R_Finger_'+str(j)+"_"+str(k)+'.rotateX', lock=True, k=False)
                    cmds.setAttr('CTRL_R_Finger_'+str(j)+"_"+str(k)+'.rotateY', lock=True, k=False)
