# -*- coding: iso-8859-1 -*-
#Function for connecting brow Curve and controller to the brow Joints
import maya.cmds as cmds
def browCrvCtlToJnt (browCtrl, browDetail, jnt, ctrlP, POC, initialX, RotateScale, index ):        
    #connect browCtrlCurve and controller to the brow joints
    ctrlMult = cmds.shadingNode ( 'multiplyDivide', asUtility=True, n = jnt.split('Base', 1)[0] +'CtrlMult'+ str(index) )
    crvMult = cmds.shadingNode ( 'multiplyDivide', asUtility=True, n = jnt.split('Base', 1)[0] +'CrvMult'+ str(index) )
    browSumY = cmds.shadingNode ( 'plusMinusAverage', asUtility=True, n = jnt.split('Base', 1)[0] +'YSum'+ str(index))
    browSumX = cmds.shadingNode ( 'plusMinusAverage', asUtility=True, n = jnt.split('Base', 1)[0] +'XSum'+ str(index))
    minusAvgX = cmds.shadingNode ( 'plusMinusAverage', asUtility=True, n = jnt.split('Base', 1)[0] +'Xminus'+ str(index))
    xyTotal = cmds.shadingNode ( 'plusMinusAverage', asUtility=True, n = jnt.split('Base', 1)[0] +'XYtotal'+ str(index))
     
    cmds.connectAttr ( browCtrl + '.tx', browSumX + '.input1D[0]')
    cmds.connectAttr ( browCtrl + '.ty', browSumY + '.input1D[0]')
    cmds.connectAttr ( browDetail + '.tx', browSumX + '.input1D[1]')
    cmds.connectAttr ( browDetail + '.ty', browSumY + '.input1D[1]')

    #browCrv's POC.tx zero out 
    cmds.connectAttr ( POC + '.positionX', minusAvgX + '.input1D[1]')
    cmds.setAttr ( minusAvgX + '.input1D[2]', -initialX )
    cmds.connectAttr ( minusAvgX + '.output1D', crvMult + '.input1X')
    cmds.connectAttr ( POC + '.positionY', crvMult + '.input1Y')
    cmds.setAttr ( crvMult + '.input2X', RotateScale )
    cmds.setAttr ( crvMult + '.input2Y', -RotateScale )
    cmds.connectAttr ( crvMult + ".outputX", ctrlP + '.ry')
    cmds.connectAttr ( crvMult + ".outputY", ctrlP + '.rx')
    #X total
    cmds.connectAttr ( browSumX + '.output1D', xyTotal + '.input2D[0].input2Dx')
    cmds.connectAttr ( minusAvgX + '.output1D', xyTotal + '.input2D[1].input2Dx')
    #Y total
    cmds.connectAttr ( browSumY + '.output1D', xyTotal + '.input2D[0].input2Dy')   
    cmds.connectAttr ( POC + '.positionY', xyTotal + '.input2D[1].input2Dy')  
    
    cmds.connectAttr ( xyTotal + '.output2Dx', ctrlMult + '.input1X')
    cmds.connectAttr ( xyTotal + '.output2Dy', ctrlMult + '.input1Y')
    cmds.setAttr ( ctrlMult + '.input2X', RotateScale )
    cmds.setAttr ( ctrlMult + '.input2Y', -RotateScale )
        
    cmds.connectAttr ( ctrlMult + '.outputX', jnt + '.ry')
    cmds.connectAttr ( ctrlMult + '.outputY', jnt + '.rx')
