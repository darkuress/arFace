# -*- coding: iso-8859-1 -*-
#create brow controllers and browCurve
'''
select base joints and run the script 
not working : check if the brow ctl crv exists / number of detail ctls
number of brow crv CVs = 7  /  main controller (arc ABC...) = 5   
'''
import maya.cmds as cmds
def connectBrowCtrls ( size, offset, RotateScale ):
    
    jnts = cmds.ls ( os = True, fl = True, type ='joint') 
    jntNum = len(jnts)
    jnts.sort()
    z = [ jnts[0] ]
    y = jnts[1:jntNum/2+1]
    jnts.reverse()
    x = jnts[:jntNum/2]
    orderJnts = x + z + y 
    
    basePos = cmds.xform( z, t = True, q = True, ws = True)  
    
    browCrv = cmds.curve ( d = 2, p =([-1,0,0],[-0.5,0,0],[0,0,0],[0.5,0,0],[1,0,0]) )
    tempCrv = cmds.rename (browCrv, 'browCtrlCrv' ) 
    cmds.rebuildCurve (tempCrv, rebuildType = 0, spans = 4, keepRange = 0, degree = 3 ) 
    browCrvShape = cmds.listRelatives ( tempCrv, c = True ) 
    sumX = cmds.shadingNode ( 'plusMinusAverage', asUtility =True, n = 'browTX_sum' )
    cmds.setAttr ( sumX + '.operation', 1 )
    
    #connect browMain Ctrls to browCrv
    sequence =['A', 'B', 'C', 'D', 'E']
    cvs= cmds.ls("browCtrlCrv.cv[*]", fl=True )
    cvBX = cmds.getAttr ( cvs[2] + '.xValue' )
    cvDX = cmds.getAttr ( cvs[4] + '.xValue' )
    cmds.connectAttr ( 'brow_arcB.tx', sumX + '.input2D[0].input2Dx' )
    cmds.setAttr ( sumX + '.input2D[1].input2Dx', cvBX )
    cmds.connectAttr ( sumX + '.output2D.output2Dx', cvs[2] + '.xValue' )
    cmds.connectAttr ( 'brow_arcD.tx', sumX + '.input2D[0].input2Dy' )
    cmds.setAttr ( sumX + '.input2D[1].input2Dy', cvDX )
    cmds.connectAttr ( sumX + '.output2D.output2Dy', cvs[4] + '.xValue' )
    cmds.connectAttr ('brow_arcA.ty',  cvs[0] + '.yValue' )
    cmds.connectAttr ('brow_arcE.ty',  cvs[6] + '.yValue' )
    
    for num in range (1, 6):
        
        cmds.connectAttr ('brow_arc' + sequence[num-1] + '.ty',  cvs[num] + '.yValue' )
    
    
    browDMom = cmds.ls ( 'browDetail*P', fl =True, type = "transform")
    browDetails = cmds.listRelatives ( browDMom, c=True, type = "transform") 
    index = 0 
    for jnt in orderJnts: 
        childJnt = cmds.listRelatives ( jnt, c=True) 
        jntPos = cmds.xform(childJnt[0], t = True, q = True, ws = True) 
        POC = cmds.shadingNode ( 'pointOnCurveInfo', asUtility=True, n = 'eyeBrowPOC'+ str(index))
        cmds.connectAttr ( browCrvShape[0] + ".worldSpace",  POC + '.inputCurve')
        cmds.setAttr ( POC + '.turnOnPercentage', 1 )
        increment = 1.0/(jntNum-1)        
        cmds.setAttr ( POC + '.parameter', increment *index )
        #browCrv controls browDetail parent 
        #cmds.connectAttr ( POC + ".positionX", browDMom[index] + ".tx"  )
        cmds.connectAttr ( POC + ".positionY", browDMom[index] + ".ty"  )
        
        initialX = cmds.getAttr (POC + '.positionX')
    
        if jnt in x :
            browDetail = browDetails[index]
            rBrowCtrl = cmds.nurbsPlane (n = 'R_BrowCtrl'+ jnt.split('BrowBase', 1)[1], ch=False, p = (0,0,0), w = size *0.3, lr= 1, polygon = 0 )
            cmds.setAttr (rBrowCtrl[0] +".overrideEnabled", 1)
            cmds.setAttr (rBrowCtrl[0] +".overrideShading", 0)
            cmds.setAttr (rBrowCtrl[0] + ".rotateAxisY", -90)
            null = cmds.group (em=True, w =True, n = rBrowCtrl[0] + "P" )
            cmds.xform (null, ws = True, t = basePos )
            cmds.xform (rBrowCtrl[0], ws = True, t = ( jntPos[0], jntPos[1], jntPos[2]+ offset))
            cmds.parent ( rBrowCtrl[0], null ) 
            cmds.makeIdentity (null, apply=True, t=True, r=True, s=True, n =False) 
            browCrvCtlToJnt  (rBrowCtrl[0], browDetail, jnt, null, POC, initialX, RotateScale, index )
            
        elif jnt in y :
            browDetail = browDetails[index]
            lBrowCtrl = cmds.circle ( n = 'L_BrowCtrl'+ jnt.split('BrowBase', 1)[1], ch=False, o =True, nr = ( 0, 0, 1), r = size*0.2 )
            null = cmds.group (em=True, w =True, n = lBrowCtrl[0] + "P" )
            cmds.xform ( null, ws = True, t = basePos )
            cmds.xform ( lBrowCtrl[0], ws = True, t = ( jntPos[0], jntPos[1], jntPos[2]+ offset))
            cmds.parent ( lBrowCtrl[0], null ) 
            cmds.makeIdentity (null, apply=True, t=True, r=True, s=True, n =False) 
            browCrvCtlToJnt (lBrowCtrl[0], browDetail, jnt, null, POC, initialX, RotateScale, index  )
            
        elif jnt == z[0] :
            browDetail = browDetails[index]
            centerBrowCtrl = cmds.spaceLocator ( n = 'C_BrowCtrl'+ jnt.split('BrowBase', 1)[1], p =(0,0,0) ) 
            cmds.setAttr ( centerBrowCtrl[0]+'Shape.localScaleX', size * 0.3 )
            cmds.setAttr ( centerBrowCtrl[0]+'Shape.localScaleY', size * 0.3 )
            cmds.setAttr ( centerBrowCtrl[0]+'Shape.localScaleZ', size * 0.3 )
            null = cmds.group (em=True, w =True, n = centerBrowCtrl[0] + "P" )
            cmds.xform ( null, ws = True, t = basePos )
            cmds.xform ( centerBrowCtrl[0], ws = True, t = ( jntPos[0], jntPos[1], jntPos[2]+ offset))
            cmds.parent ( centerBrowCtrl[0], null ) 
            cmds.makeIdentity (null, apply=True, t=True, r=True, s=True, n =False) 
            browCrvCtlToJnt ( centerBrowCtrl[0], browDetail, jnt, null, POC, initialX, RotateScale, index )
        index = index + 1
