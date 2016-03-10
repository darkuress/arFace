#create eyeLidController (miNum = number of lidJoints )    
'''control parent name should be "l_upCtrl0"....'''
import maya.cmds as cmds
def createLidCtl ( miNum ):        
    LRUpLow = ['l_up','r_up', 'l_lo', 'r_lo' ]
    for updn in LRUpLow:
        
        ctlP = updn + "Ctrl0"
        kids = cmds.listRelatives (ctlP, ad=True, type ='transform')   
        if kids:
            cmds.delete (kids)
                
        cntCtlP = cmds.duplicate ( ctlP, po =True, n = updn + 'CntCtlP' )
        cmds.parent(cntCtlP[0],ctlP)
        cntCtl = cmds.circle ( n = updn + "Center", ch=False, o =True, nr = ( 0, 0, 1), r = 0.1  )
        cntCtl[0]
        cmds.parent(cntCtl[0], cntCtlP[0])
        cmds.setAttr (cntCtl[0]+".overrideEnabled", 1)
        cmds.setAttr (cntCtl[0]+"Shape.overrideEnabled", 1)
        cmds.setAttr( cntCtl[0]+"Shape.overrideColor", 9)
        cmds.setAttr (cntCtl[0]+'.translate', 0,0,0)
        cmds.transformLimits ( cntCtl, tx = ( -1, 1), etx=( True, True) )
        cmds.transformLimits ( cntCtl, ty = ( -1, 1), ety=( True, True) )
    
        inCornerP = cmds.duplicate ( cntCtlP , n = updn + 'InCornerP', rc =True )
        cmds.setAttr (inCornerP[0] +'.tx', -1 )
        inTemp = cmds.listRelatives ( inCornerP[0], c=True, type ='transform') 
        inCorner = cmds.rename ( inTemp[0], updn + 'InCorner' )
        cmds.setAttr (inCorner +'.scale', .8, .8, .8 )
        cmds.transformLimits ( inCorner, tx = ( -.25, .25), etx=( True, True) )
        cmds.transformLimits ( inCorner, ty = ( -1,  1), ety=( True, True) )
                
        outCornerP = cmds.duplicate ( cntCtlP , n = updn + 'OutCornerP', rc=True )
        cmds.setAttr (outCornerP[0] +'.tx', 1 )
        outTemp = cmds.listRelatives ( outCornerP[0], c=True, type ='transform') 
        outCorner = cmds.rename ( outTemp[0], updn + 'OutCorner' ) 
        cmds.setAttr (outCorner +'.scale', .8, .8, .8 ) 
        cmds.transformLimits ( outCorner, tx = ( -.25, .25), etx=( True, True) )
        cmds.transformLimits ( outCorner, ty = ( -1, 1), ety=( True, True) )
        
        attTemp = ['scaleX','scaleY','scaleZ', 'rotateX','rotateY','rotateZ', 'tz', 'visibility' ]  
        for x in attTemp:
            cmds.setAttr (cntCtl[0] +"."+ x, lock = True, keyable = False, channelBox =False)
            cmds.setAttr (inCorner +"."+ x, lock = True, keyable = False, channelBox =False ) 
            cmds.setAttr (outCorner+"."+ x, lock = True, keyable = False, channelBox =False ) 
    
        for i in range(0, miNum):
            detailCtl = cmds.spaceLocator ( n = updn  + 'Detail' + str(i+1).zfill(2))
            detailCtlP = cmds.group ( em =True, n = updn  + 'Detail'+ str(i+1).zfill(2) + 'P' )
            cmds.parent (detailCtl[0], detailCtlP )
            cmds.parent (detailCtlP, ctlP )
            cmds.setAttr (detailCtl[0] +".overrideEnabled", 1)
            cmds.setAttr (detailCtl[0] +"Shape.overrideEnabled", 1)
            cmds.setAttr( detailCtl[0]+"Shape.overrideColor", 20)
            increment = 2.0 /(miNum-1)
            cmds.setAttr (detailCtlP + ".tx", increment*i - 1.0 )
            cmds.setAttr (detailCtlP + ".ty", 0 )
            cmds.setAttr (detailCtlP + ".tz", 0 )
            cmds.xform ( detailCtl, r =True, s = (0.1, 0.1, 0.1))
            cmds.transformLimits ( detailCtl , tx = ( -.25, .25), etx=( True, True) )
            cmds.transformLimits ( detailCtl , ty = ( -.5, .5), ety=( True, True) )
            for y in attTemp:
                cmds.setAttr (detailCtl[0] +"."+ y, lock = True, keyable = False, channelBox =False)