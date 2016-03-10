# -*- coding: iso-8859-1 -*-
def bridgeJoints():    
    
    if cmds.objExists ('jawRig'):
        
        jawSemi = cmds.group ( n = 'jawSemi', em =True, parent = 'jaw' ) 
        cmds.setAttr ( jawSemi + ".translate", 0,0,0 )
        jawClose = cmds.joint(n = 'jawClose_jnt', relative = True, p = [ 0, 0, 0] )        
        jotStable = cmds.group ( n = 'lipJotStable', em =True, parent = 'jaw' ) 
        lipJotP = cmds.group( n = 'lipJotP', em =True, parent = jotStable )             
    else :
        print "create faceRig first!!!" 
    # create cheek joint - check the cheek/squintPush group and angle
    lEarP = cmds.group ( n = 'l_earP', em =True, p = "l_ear_grp" )
    cmds.xform (lEarP, relative = True, t = [ 0, 0, 0] )
    lEarJnt = cmds.joint(n = 'l_ear_jnt', relative = True, p = [ 0, 0, 0] ) 
    rEarP = cmds.group ( n = 'r_earP', em =True, p = "r_ear_grp" )
    cmds.xform (rEarP, relative = True, t = [ 0, 0, 0]  )
    rEarJnt = cmds.joint(n = 'r_ear_jnt', relative = True, p = [ 0, 0, 0] ) 
    
    noseP = cmds.group ( n = 'noseP', em =True, p = "noseRig" )
    cmds.xform (noseP, relative = True, t = [ 0, 0, 0] )
    noseJnt = cmds.joint(n = 'nose_jnt', relative = True, p = [ 0, 0, 0] ) 
    
    lCheekP = cmds.group ( n = 'l_cheekP', em =True, p = "l_cheek_grp" )
    cmds.xform (lCheekP, relative = True, t = [ 0, 0, 0] )
    lCheekJnt = cmds.joint(n = 'l_cheek_jnt', relative = True, p = [ 0, 0, 0] )     
    rCheekP = cmds.group ( n = 'r_cheekP', em =True, p = "r_cheek_grp" )
    cmds.xform (rCheekP, relative = True, t = [ 0, 0, 0] )
    rCheekJnt = cmds.joint(n = 'r_cheek_jnt', relative = True, p = [ 0, 0, 0] )
    
    lSqiuntPuff = cmds.group ( n = 'l_squintPuffP', em =True, p = "l_squintPuff_grp" )
    cmds.xform (lSqiuntPuff, relative = True, t = [ 0, 0, 0] )
    lSqiuntPuffJnt = cmds.joint(n = 'l_squintPuff_jnt', relative = True, p = [ 0, 0, 0] ) 
    rSquintPuff = cmds.group ( n = 'r_squintPuffP', em =True, p = "r_squintPuff_grp" )
    cmds.xform (rSquintPuff, relative = True, t = [ 0, 0, 0])
    rSqiuntPuffJnt = cmds.joint(n = 'r_squintPuff_jnt', relative = True, p = [ 0, 0, 0] ) 
    
    lLowCheek = cmds.group ( n = 'l_lowCheekP', em =True, p = "l_lowCheek_grp" )
    cmds.xform (lLowCheek, relative = True, t = [ 0, 0, 0] )
    lLowCheekJnt = cmds.joint(n = 'l_lowCheek_jnt', relative = True, p = [ 0, 0, 0] ) 
    rLowCheek = cmds.group ( n = 'r_lowCheekP', em =True, p = "r_lowCheek_grp" )
    cmds.xform (rLowCheek,  relative = True, t = [ 0, 0, 0]  )
    rLowCheekJnt = cmds.joint(n = 'r_lowCheek_jnt', relative = True, p = [ 0, 0, 0] ) 
    
    if cmds.objExists ( 'jawClose_jnt' ):
        cmds.parentConstraint ('jawClose_jnt', 'l_lowCheek_grp', maintainOffset = 1 )
        cmds.parentConstraint ('jawClose_jnt', 'r_lowCheek_grp', maintainOffset = 1 )