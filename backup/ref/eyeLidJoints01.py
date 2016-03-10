# eyeLid joints create (z forward joint (x rotation))
'''
UI  : controller size, mult.input 2 values
The locator "lEyePos" for eye center should exist.  
select left eyeLid vertex points and run the script 
upLowLR = "l_up", "r_up", "l_lo", "r_lo" '''

import maya.cmds as cmds
def eyelidJoints ( upLowLR ): 
    
    if not ('lEyePos'):
        print "create the face locators" 
        
    else:    
        eyeRotY = cmds.getAttr ('lEyePos.ry' ) 
        eyeCenterPos = cmds.xform( 'lEyePos', t = True, q = True, ws = True) 


    verts = cmds.ls( os = True, fl = True) 
    geoName = verts[0].split('.vtx', 1)[0] 

    # create parent group for eyelid joints
    null = cmds.group ( n = upLowLR+'EyeLidJnt_grp', em =True ) 
    cmds.xform (null, t = eyeCenterPos ) 
    cmds.setAttr ( null + '.ry', eyeRotY ) 
    cmds.select(cl = True) 

    #create eyeLids parent joint
    LidJntP = cmds.joint(n = upLowLR + 'LidP_jnt', p = eyeCenterPos) 
    cmds.setAttr ( LidJntP + '.ry', eyeRotY ) 
    cmds.parent ( LidJntP, null )
    
    index = 1
    posXs = []
    # sort out Vertices based on tx position
    for i in verts:
        vertPos = cmds.xform ( i, t = True, q = True, ws = True)
        posX = str(vertPos[0]) + i
        posXs.append(posX)
    
    posXs.sort()
    orderedVerts = []
    # list vertices by tx position order
    for x in posXs:
        
        y = x.split(geoName, 1)[1]
        orderedVerts.append(geoName + y)
        
    for v in orderedVerts:
     
        vertPos = cmds.xform ( v, t = True, q = True, ws = True)        
        lidJnt = cmds.joint(n = upLowLR + 'Lid' + str(index).zfill(2) + '_jnt', p = vertPos ) 
        lidJntTX = cmds.joint(n = upLowLR + 'LidTX' + str(index).zfill(2) + '_jnt', p = vertPos ) 
        cmds.parent ( lidJnt, null )
        blinkJnt = cmds.duplicate (lidJnt, po=True, n = upLowLR + 'LidBlink' + str(index).zfill(2)+'_jnt' )  
        cmds.setAttr ( blinkJnt[0] + '.ty' , 0 ) 
        cmds.setAttr ( blinkJnt[0] + '.tz' , 0 )
        cmds.parent ( lidJnt , blinkJnt[0] )
        cmds.joint ( blinkJnt[0], e =True, zso =True, oj = 'zyx', sao= 'yup')   
          
        wideJnt = cmds.duplicate ( blinkJnt[0], po=True, n = upLowLR + 'LidWide' + str(index).zfill(2) + '_jnt' )  
        scaleJnt = cmds.duplicate ( blinkJnt[0], po=True, n = upLowLR + 'LidScale' + str(index).zfill(2) + '_jnt' )
        cmds.parent ( blinkJnt[0], scaleJnt[0] )
        #cmds.joint ( scaleJnt[0], e =True, zso =True, oj = 'xyz', sao= 'yup')
        cmds.parent ( wideJnt[0], scaleJnt[0] )
        cmds.parent ( scaleJnt[0], LidJntP )

        index = index + 1
    
    mirrorLowLR = ''
    if 'l_up' in upLowLR:
        mirrorLowLR = 'r_up'
    elif 'l_lo' in upLowLR:
        mirrorLowLR = 'r_lo'
        
    RNull = cmds.group ( n = mirrorLowLR +'EyeLidJnt_grp', em =True ) 
    cmds.xform (RNull, t = (-eyeCenterPos[0], eyeCenterPos[1], eyeCenterPos[2]) ) 
    cmds.setAttr ( RNull + '.ry', -eyeRotY ) 
    RLidJntP = cmds.mirrorJoint ( LidJntP, mirrorBehavior=True, myz = True, searchReplace = ('l_', 'r_'))
    cmds.parent ( RLidJntP[0], RNull ) 
    zeroAtts = ['tx', 'ty', 'tz', 'rx','rz']
    for i in zeroAtts:
        cmds.setAttr ( RLidJntP[0] + '.' + i, 0)