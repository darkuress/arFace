import maya.cmds as cmds
def crvCtrlToJnt ( lidCtl, jnt, wideJnt, POC, wideJntPOC, ctlPOC, initialX, RotateScale ,miValue, index ):   
    
    #connect browCtrlCurve and controller to the brow joints
    ctlMult = cmds.shadingNode ( 'multiplyDivide', asUtility=True, n = jnt.split('Blink', 1)[0] +'Ctl'+ str(index)+'_mult' )
    wideJntMult = cmds.shadingNode ( 'multiplyDivide', asUtility=True, n = jnt.split('Blink', 1)[0] + 'wideJnt'+ str(index)+'_mult' )
    plusXAvg = cmds.shadingNode ( 'plusMinusAverage', asUtility=True, n = jnt.split('Blink', 1)[0] + str(index) +'_plusX')
    wideJntAddX = cmds.shadingNode ( 'addDoubleLinear', asUtility=True, n = jnt.split('Blink', 1)[0] + 'wideJnt'+str(index)+'_addX' )
    plusYAvg = cmds.shadingNode ( 'plusMinusAverage', asUtility=True, n = jnt.split('Blink', 1)[0] + str(index)+'_plusY' )
    totalY = cmds.shadingNode ( 'addDoubleLinear', asUtility=True, n = jnt.split('Blink', 1)[0] + str(index)+'_yAdd' )
    blinkRemap = cmds.shadingNode ( 'remapValue', asUtility=True, n = jnt.split('Blink', 1)[0] + str(index)+'_remap' )
    blinkGap = cmds.shadingNode ( 'addDoubleLinear', asUtility=True, n = jnt.split('LidBlink', 1)[0] + 'BlinkGap'+str(index)+'_yAdd' )
    
    #TranslateX add up
    #1. curve translateX add up 
    cmds.setAttr ( plusXAvg + '.operation', 1 ) 
    cmds.connectAttr ( POC + '.positionX', plusXAvg + '.input1D[0]') 
    cmds.setAttr ( plusXAvg + '.input1D[1]', -initialX )
    cmds.connectAttr ( ctlPOC + '.positionX', plusXAvg + '.input1D[2]') 
    cmds.setAttr ( plusXAvg + '.input1D[3]', -initialX ) 
    cmds.connectAttr ( wideJntPOC + '.positionX', wideJntAddX + '.input1') 
    cmds.setAttr ( wideJntAddX + '.input2', -initialX ) 
    cmds.connectAttr ( wideJntAddX + '.output', plusXAvg + '.input1D[4]')
    #2. add miro control translateX 
    cmds.connectAttr ( lidCtl[0] + '.tx', plusXAvg + '.input1D[5]')
    #3. multiply XRotateScale
    cmds.connectAttr ( plusXAvg + '.output1D', ctlMult + '.input1X')
    cmds.setAttr ( ctlMult + '.input2X', miValue * RotateScale )
    cmds.connectAttr ( wideJntAddX + '.output', wideJntMult + '.input1X')
    cmds.setAttr ( wideJntMult + '.input2X', miValue * RotateScale )
    
    #4. connect jnt rotateY
    cmds.connectAttr ( ctlMult + '.outputX', jnt + '.ry' ) 
    cmds.connectAttr ( wideJntMult + '.outputX', wideJnt + '.ry')   
        
    # translateY add up
    #1. curve translateY add up 
    cmds.setAttr ( plusXAvg + '.operation', 1 )
    cmds.connectAttr ( POC + '.positionY', plusYAvg + '.input1D[0]')
    cmds.connectAttr ( ctlPOC + '.positionY', plusYAvg + '.input1D[1]')
    cmds.connectAttr ( wideJntPOC + '.positionY', plusYAvg + '.input1D[2]') 
    #2. add miro control translateY 
    cmds.connectAttr ( lidCtl[0] + '.ty', plusYAvg + '.input1D[3]')
    
    #3. multiply YRotateScale
    cmds.connectAttr ( plusYAvg + '.output1D', ctlMult + '.input1Y')
    cmds.setAttr ( ctlMult + '.input2Y', -RotateScale )
    cmds.connectAttr ( wideJntPOC + '.positionY', wideJntMult + '.input1Y')
    cmds.setAttr ( wideJntMult + '.input2Y', -RotateScale )   
    
    #4. connect jnt rotateX
    if "_up" in jnt: 
        blinkRemap = cmds.shadingNode ( 'remapValue', asUtility=True, n = jnt.split('Blink', 1)[0] + str(index+1).zfill(2)+'_remap' )
        cmds.connectAttr ( ctlMult + ".outputY", blinkRemap + '.outputMin' ) 
        cmds.connectAttr ( blinkRemap + '.outValue',  jnt + '.rx')
        cmds.connectAttr ( wideJntMult + '.outputY', wideJnt + '.rx') 
    
    elif "_lo" in jnt: 
        #get the remap from upJoint
        upJnt = jnt.replace("_lo","_up")
        cmds.connectAttr ( ctlMult + ".outputY", blinkGap + ".input1" ) 
        cmds.connectAttr ( blinkGap + ".output", ( upJnt.split('Blink',1)[0] + str(index+1).zfill(2)+'_remap'+'.outputMax'))  
        cmds.connectAttr ( ctlMult + ".outputY",  jnt + '.rx' ) 
        cmds.connectAttr ( wideJntMult + '.outputY', wideJnt + '.rx' ) 