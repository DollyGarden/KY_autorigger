import maya.cmds as cmds
from KY_AutoRigger import KY_Locators
import importlib

importlib.reload(KY_Locators)

def IKHandles():
    #arm IK
    if not (cmds.objExists("RIG_L_sec_armTwist_*")):
        cmds.ikHandle(name="IK_L_Arm", sj=cmds.ls("RIG_L_UpperArm")[0], ee=cmds.ls("RIG_L_Wrist")[0], sol='ikRPsolver')
        cmds.ikHandle(name="IK_R_Arm", sj=cmds.ls("RIG_R_UpperArm")[0], ee=cmds.ls("RIG_R_Wrist")[0], sol='ikRPsolver')
    else:
        cmds.ikHandle(name="IK_L_Arm", sj=cmds.ls("RIG_L_UpperArm")[0], ee=cmds.ls("RIG_L_sec_armTwist_0")[0], sol='ikRPsolver')
        cmds.ikHandle(name="IK_R_Arm", sj=cmds.ls("RIG_R_UpperArm")[0], ee=cmds.ls("RIG_R_sec_armTwist_0")[0], sol='ikRPsolver')
        #move the end of ik pivot to the wrist
        leftWristPos = cmds.xform(cmds.ls("RIG_L_Wrist"), q = True, t = True, ws = True)
        leftArmIKEnd = cmds.ikHandle("IK_L_Arm", q=True, ee=True)
        cmds.move(leftWristPos[0], leftWristPos[1], leftWristPos[2],leftArmIKEnd+".scalePivot", leftArmIKEnd+".rotatePivot") 
        rightWristPos=cmds.xform(cmds.ls("RIG_R_Wrist"), q=True, t=True, ws=True)
        rightArmIKEnd=cmds.ikHandle("IK_R_Arm", q=True, ee=True)
        cmds.move(rightWristPos[0], rightWristPos[1], rightWristPos[2],rightArmIKEnd+".scalePivot", rightArmIKEnd+".rotatePivot")
        
    #leg IK
    cmds.ikHandle(name="IK_L_Leg", sj=cmds.ls("RIG_L_UpperLeg")[0], ee=cmds.ls("RIG_L_Foot")[0], sol='ikRPsolver')
    cmds.ikHandle(name="IK_R_Leg", sj=cmds.ls("RIG_R_UpperLeg")[0], ee=cmds.ls("RIG_R_Foot")[0], sol='ikRPsolver')
    
    #foot IK
    cmds.ikHandle(name="IK_L_FootBall", sj=cmds.ls("RIG_L_Foot")[0], ee=cmds.ls("RIG_L_FootBall")[0], sol='ikSCsolver')
    cmds.ikHandle(name="IK_L_Toes", sj=cmds.ls("RIG_L_FootBall")[0], ee=cmds.ls("RIG_L_Toes")[0], sol='ikSCsolver')
    cmds.ikHandle(name="IK_R_FootBall", sj=cmds.ls("RIG_R_Foot")[0], ee=cmds.ls("RIG_R_FootBall")[0], sol='ikSCsolver')
    cmds.ikHandle(name="IK_R_Toes", sj=cmds.ls("RIG_R_FootBall")[0], ee=cmds.ls("RIG_R_Toes")[0], sol='ikSCsolver')
    
    rootPos=cmds.xform(cmds.ls("RIG_ROOT", type='joint'),q=True, t=True, ws=True)
    spines=cmds.ls("RIG_SPINE_*",type='joint')
    
    spinePos=[]
    for i,sp in enumerate(spines):
        spinePos.append(cmds.xform(spines[i], q=True, t=True, ws=True))

    if cmds.objExists('SpineCurve'):
        cmds.delete('SpineCurve')

    cmds.curve(p=[(rootPos[0], rootPos[1], rootPos[2])],n="SpineCurve",degree=1)
    
    for j,sp in enumerate(spinePos):
        cmds.curve('SpineCurve', a=True, p=[(spinePos[j][0], spinePos[j][1], spinePos[j][2])])
        
    curveCV=cmds.ls('SpineCurve.cv[0:]',fl=True) #????what does this mean?
        
    for k,cv in enumerate(curveCV):
        c=cmds.cluster(cv,cv,n="Cluster_"+str(k)+"_")
        
        if k>0:
            cmds.parent(c,"Cluster_"+str(k-1)+"_Handle")    
            
    spineAmount=cmds.ls("RIG_SPINE_*")       
    cmds.ikHandle(n="Ik_Spine", sj="RIG_ROOT", ee="RIG_SPINE_"+ str(len(spineAmount) - 1), 
                  sol='ikSplineSolver', c='SpineCurve',ccv=False)
    