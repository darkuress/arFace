#create LidCurve
# UI = controller size, offset   
'''
select two top joints and run the script  
premise : L/R eyeBall position is symetrical
upLowLR = "l_up", "r_up", "l_lo", "r_lo"
'''
import maya.cmds as cmds
import fnmatch

def createLidCtrls ( upLowLR, RotateScale, ctlSize ): 
    
    if not ('lEyePos'):
        print "create the face locators" 
        
    else: 
        eyeRotY = cmds.getAttr ('lEyePos.ry' ) 
        eyeCenterPos = cmds.xform( 'lEyePos', t = True, q = True, ws = True) 
        
    if "_up" in upLowLR:  
        miUpLowLR = upLowLR.replace( 'l_up', 'r_up' ) 
    if "_lo" in upLowLR:  
        miUpLowLR = upLowLR.replace( 'l_lo', 'r_lo' ) 
     
    jntList =cmds.ls ( sl = True, fl = True, type ='joint' ) 
    lTempJnts = cmds.listRelatives ( jntList[0], ad =True )
    rTempJnts = cmds.listRelatives ( jntList[1], ad =True ) 
    lChildJnts = fnmatch.filter ( lTempJnts, "*Blink*" ) 
    rChildJnts = fnmatch.filter ( rTempJnts, "*Blink*" ) 
    lWideJnts = fnmatch.filter ( lTempJnts, "*Wide*" )
    rWideJnts = fnmatch.filter ( rTempJnts, "*Wide*" )
    jntNum = len(lChildJnts)
    
    lidCrvGrp = cmds.group ( n = upLowLR +'LidCrv_grp', em =True ) 
    RlidCrvGrp = cmds.group ( n = miUpLowLR +'LidCrv_grp', em =True ) 

    lidsGrp = cmds.group (em=True, w =True, n = upLowLR + "LidCtl_grp" ) 
    cmds.xform (lidsGrp, ws = True, t = eyeCenterPos ) 
    cmds.setAttr ( lidsGrp + ".ry", eyeRotY )
    
    RlidsGrp = cmds.group (em=True, w =True, n = miUpLowLR + "LidCtl_grp" )
    cmds.xform (RlidsGrp, ws = True, t = (-eyeCenterPos[0], eyeCenterPos[1], eyeCenterPos[2]) )
    cmds.setAttr ( RlidsGrp + ".ry", -eyeRotY )
    
    # final lid shape curve
    lidCrv = cmds.curve ( d = 3, p =([0,0,0],[0.33,0,0],[0.66,0,0],[1,0,0])) 
    cmds.rebuildCurve ( rt = 0, d = 1, kr = 0, s = jntNum-1 )    
    tempCrv = cmds.rename (lidCrv, upLowLR +'Lid_crv')
    cmds.parent (tempCrv, lidCrvGrp)
    lidCrvShape = cmds.listRelatives ( tempCrv, c = True ) 
    
    RlidCrv = cmds.duplicate ( tempCrv, n = miUpLowLR +'Lid_crv' ) 
    cmds.parent ( RlidCrv[0], RlidCrvGrp)
    RlidCrvShape = cmds.listRelatives ( RlidCrv[0], c = True ) 
    
    wideJntCrv = cmds.duplicate ( tempCrv, n= upLowLR +'WideJnt_crv') 
    wideJntCrvShape = cmds.listRelatives ( wideJntCrv, c = True ) 
    
    RwideJntCrv = cmds.duplicate ( RlidCrv[0], n= miUpLowLR +'WideJnt_crv') 
    RwideJntCrvShape = cmds.listRelatives ( RwideJntCrv[0], c = True ) 
    
    # eyelids controller curve shape ( different number of points, so can not be target of the blendShape)      
    lidCtlCrv = cmds.curve ( d = 3, p =([0,0,0],[0.33,0,0],[0.66,0,0],[1,0,0])) 
    cmds.rebuildCurve ( rt = 0, d = 3, kr = 0, s = 2 )   
    tempCtlCrv = cmds.rename (lidCtlCrv, upLowLR +'Ctl_crv')
    lidCtlCrvShape = cmds.listRelatives ( tempCtlCrv, c = True ) 
    cmds.parent (tempCtlCrv, lidCrvGrp) 
    
    RlidCtlCrv = cmds.duplicate ( tempCtlCrv, n= miUpLowLR +'Ctl_crv') 
    RlidCtlCrvShape = cmds.listRelatives ( RlidCtlCrv[0], c = True )
    cmds.parent ( RlidCtlCrv[0], RlidCrvGrp)
    
    # eyeClose(blink) lid shape        
    blinkCrv = cmds.duplicate ( tempCrv, n= upLowLR +'Blink_crv')
    RblinkCrv = cmds.duplicate ( blinkCrv[0], instanceLeaf =True, n= miUpLowLR +'Blink_crv') 
    cmds.parent ( RblinkCrv[0], RlidCrvGrp)
    cmds.hide (RblinkCrv)
    
    # eyeOpen lid shape 
    eyeOpenCrv = cmds.duplicate ( tempCrv, n= upLowLR +'EyeOpen_crv')
    REyeOpenCrv = cmds.duplicate ( eyeOpenCrv[0], instanceLeaf =True, n= miUpLowLR +'EyeOpen_crv') 
    cmds.parent ( REyeOpenCrv[0], RlidCrvGrp)
    cmds.hide (RblinkCrv)
    
    # eyeWide(suprise) lid shape        
    wideCrv = cmds.duplicate ( tempCrv, n= upLowLR +'Wide_crv')
    RwideCrv = cmds.duplicate ( wideCrv[0], instanceLeaf =True, n= miUpLowLR +'Wide_crv') 
    cmds.parent ( RwideCrv[0], RlidCrvGrp)
    cmds.hide (RwideCrv)
    
    # eyeSquint lid shape        
    squintCrv = cmds.duplicate ( tempCrv, n= upLowLR +'Squint_crv') 
    RsquintCrv = cmds.duplicate ( squintCrv[0], instanceLeaf =True, n= miUpLowLR +'Squint_crv') 
    cmds.parent ( RsquintCrv[0], RlidCrvGrp)
    cmds.hide (RsquintCrv)
    
    # eyeDirection lid shape        
    lookUp = cmds.duplicate ( tempCrv, n= upLowLR +'LookUp_crv') 
    RlookUp = cmds.duplicate ( lookUp[0], instanceLeaf =True, n= miUpLowLR +'LookUp_crv')
    cmds.parent ( RlookUp[0], RlidCrvGrp)
    cmds.hide (RlookUp)
        
    lookDn = cmds.duplicate ( tempCrv, n= upLowLR +'LookDn_crv') 
    RlookDn = cmds.duplicate ( lookDn[0], instanceLeaf =True, n= miUpLowLR +'LookDn_crv')
    cmds.parent ( RlookDn[0], RlidCrvGrp)
    cmds.hide (RlookDn)
       
    lookLeft = cmds.duplicate ( tempCrv, n= upLowLR +'LookLeft_crv') 
    RlookLeft = cmds.duplicate ( RlidCrv[0], n= miUpLowLR +'LookLeft_crv')
        
    lookRight = cmds.duplicate ( tempCrv, n= upLowLR +'LookRight_crv') 
    RlookRight = cmds.duplicate ( RlidCrv[0], n= miUpLowLR +'LookRight_crv')
    
    crvBS = cmds.blendShape ( blinkCrv[0], eyeOpenCrv[0], lookUp[0], lookDn[0], lookLeft[0], lookRight[0], tempCrv, n =upLowLR + 'EyeCrvBS' )
    cmds.blendShape( crvBS[0], edit=True, w=[(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1)] )
    
    RcrvBS = cmds.blendShape ( RblinkCrv[0],REyeOpenCrv[0], RlookUp[0], RlookDn[0], RlookLeft[0], RlookRight[0], RlidCrv[0], n = miUpLowLR + 'EyeCrvBS' )
    cmds.blendShape( RcrvBS[0], edit=True, w=[(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1)])
      
    wideBS = cmds.blendShape ( wideCrv[0], squintCrv[0], wideJntCrv, n = upLowLR + 'WideJntBS')
    cmds.blendShape( wideBS[0], edit=True, w=[(0, 1), (1, 1)] )
    
    RwideBS = cmds.blendShape ( RwideCrv[0], RsquintCrv[0], RwideJntCrv[0], n = miUpLowLR + 'WideJntBS')
    cmds.blendShape( RwideBS[0], edit=True, w=[(0, 1), (1, 1)] )
       
    index = 0 
    indices = 0
        
    for jnt in lChildJnts:

        miValue = 1
        wideJnt = lWideJnts[index]
        childJnt = cmds.listRelatives (jnt, c =True)
        childPos = cmds.xform ( childJnt[0], t = True, q = True, ws = True)     
        #POC on the final lid curve 
        POC = cmds.shadingNode ( 'pointOnCurveInfo', asUtility=True, n = upLowLR + 'Poc' + str(index+1).zfill(2) )
        cmds.connectAttr ( lidCrvShape[0] + ".worldSpace",  POC + '.inputCurve')   
        cmds.setAttr ( POC + '.turnOnPercentage', 1 )        
        increment = 1.0/(jntNum-1)
        cmds.setAttr ( POC + '.parameter', increment *index )     
        initialX = cmds.getAttr (POC + '.positionX')
        
        #POC on the wideJnt curve
        wideJntPOC = cmds.shadingNode ( 'pointOnCurveInfo', asUtility=True, n = upLowLR + 'wideJntPoc' + str(index+1).zfill(2)) 
        cmds.connectAttr ( wideJntCrvShape[0] + ".worldSpace",  wideJntPOC + '.inputCurve')   
        cmds.setAttr ( wideJntPOC + '.turnOnPercentage', 1 )        
        cmds.setAttr ( wideJntPOC + '.parameter', increment *index )   
        
        #POC on the eyelids ctls curve
        ctlPOC = cmds.shadingNode ( 'pointOnCurveInfo', asUtility=True, n = upLowLR + 'CtlPoc' + str(index+1).zfill(2) ) 
        cmds.connectAttr ( lidCtlCrvShape[0] + ".worldSpace", ctlPOC + '.inputCurve')   
        cmds.setAttr ( ctlPOC + '.turnOnPercentage', 1 )        
        cmds.setAttr ( ctlPOC + '.parameter', increment *index ) 
        
        lidCtl = cmds.circle ( n = upLowLR + "Lid" + str(index+1).zfill(2), ch=False, o =True, nr = ( 0, 0, 1), r = ctlSize*0.1 ) 
        cmds.xform ( lidCtl[0], ws = True, t = ( childPos[0], childPos[1], childPos[2]+ ctlSize*0.1)) 
        cmds.parent ( lidCtl[0], lidsGrp )
        lidCtlP = cmds.duplicate ( lidCtl[0], po = True, n=  upLowLR +'P'+ str(index+1).zfill(2) ) 
        cmds.parent ( lidCtl[0], lidCtlP[0] )
        cmds.parentConstraint ( childJnt[0], lidCtlP[0], mo = True)
        index = index + 1
        
        crvCtrlToJnt ( lidCtl, jnt, wideJnt, POC, wideJntPOC, ctlPOC, initialX, RotateScale , miValue, index )
            
      
    for jnt in rChildJnts:         
    
        miValue = -1
        wideJnt = rWideJnts[indices]
        childJnt = cmds.listRelatives (jnt, c =True)
        childPos = cmds.xform ( childJnt[0], t = True, q = True, ws = True)     
        #POC on the final lid curve 
        POC = cmds.shadingNode ( 'pointOnCurveInfo', asUtility=True, n = miUpLowLR + 'Poc' + str(indices+1).zfill(2) )
        cmds.connectAttr ( RlidCrvShape[0]  + ".worldSpace",  POC + '.inputCurve')   
        cmds.setAttr ( POC + '.turnOnPercentage', 1 )        
        increment = 1.0/(jntNum-1)
        cmds.setAttr ( POC + '.parameter', increment *indices )     
        initialX = cmds.getAttr (POC + '.positionX')
        
        #POC on the wideJnt curve
        wideJntPOC = cmds.shadingNode ( 'pointOnCurveInfo', asUtility=True, n = miUpLowLR + 'wideJntPoc' + str(indices+1).zfill(2))
        cmds.connectAttr ( RwideJntCrvShape[0] + ".worldSpace",  wideJntPOC + '.inputCurve')   
        cmds.setAttr ( wideJntPOC + '.turnOnPercentage', 1 )        
        cmds.setAttr ( wideJntPOC + '.parameter', increment *indices )  
        
        #POC on the eyelids ctls curve
        ctlPOC = cmds.shadingNode ( 'pointOnCurveInfo', asUtility=True, n = miUpLowLR + 'CtlPoc' + str(indices+1).zfill(2)) 
        cmds.connectAttr ( RlidCtlCrvShape[0] + ".worldSpace",  ctlPOC + '.inputCurve')   
        cmds.setAttr ( ctlPOC + '.turnOnPercentage', 1 )        
        cmds.setAttr ( ctlPOC + '.parameter', increment *indices )   
        
        RlidCtl = cmds.circle ( n = miUpLowLR + "Lid" + str(indices+1).zfill(2), ch=False, o =True, nr = ( 0, 0, 1), r = ctlSize*0.1 )
        cmds.xform ( RlidCtl[0], ws = True, t = ( childPos[0], childPos[1], childPos[2]+ ctlSize*0.1)) 
        cmds.parent ( RlidCtl[0], RlidsGrp )
        RlidCtlP = cmds.duplicate ( RlidCtl[0], po = True, n=  miUpLowLR +'P'+ str(indices+1).zfill(2) ) 
        cmds.parent ( RlidCtl[0], RlidCtlP[0] )
        cmds.parentConstraint ( childJnt[0], RlidCtlP[0], mo = True) 
        indices = indices + 1
        
        crvCtrlToJnt ( RlidCtl, jnt, wideJnt, POC, wideJntPOC, ctlPOC, initialX, RotateScale , miValue, indices ) 