#!/bin/env python
# -*- coding: iso-8859-1 -*-
###############################################################################
#
# Copyright (c) 2015 Sukwon Shin, Jonghwan Hwang
# $Author: jhwang $
#
###############################################################################

import maya.cmds as cmds
import Base
reload(Base)

class Func(Base.Base):
    def __init__(self, **kw):
        """
        initializing variables
        """
        #local variables
        Base.Base.__init__(self, **kw)

    def crvCtrlToJnt (self, uploPrefix, lidCtl, jnt, wideJnt, pocNode, wideJntPocNode, ctlPocNode, initialX, RotateScale ,miValue, index ):
        #connect browCtrlCurve and controller to the brow joints
        ctlMult = cmds.shadingNode ( 'multiplyDivide', asUtility=True, n = uploPrefix + 'CtlMult' + str(index) )
        wideJntMult = cmds.shadingNode ( 'multiplyDivide', asUtility=True, n = uploPrefix + 'wideJntMult' + str(index) )
        plusXAvg = cmds.shadingNode ( 'plusMinusAverage', asUtility=True, n = uploPrefix + 'PlusX' + str(index))
        wideJntAddX = cmds.shadingNode ( 'addDoubleLinear', asUtility=True, n = uploPrefix + 'wideJntAddX' + str(index) )
        plusYAvg = cmds.shadingNode ( 'plusMinusAverage', asUtility=True, n = uploPrefix + 'PlusY' + str(index))
        totalY = cmds.shadingNode ( 'addDoubleLinear', asUtility=True, n = uploPrefix + 'YAdd' + str(index))
        blinkRemap = cmds.shadingNode ( 'remapValue', asUtility=True, n = uploPrefix + 'Remap' + str(index))
        blinkGap = cmds.shadingNode ( 'addDoubleLinear', asUtility=True, n = uploPrefix + 'BlinkGap_yAdd' + str(index))
        
        #TranslateX add up
        #1. curve translateX add up 
        cmds.setAttr ( plusXAvg + '.operation', 1 ) 
        cmds.connectAttr ( pocNode + '.positionX', plusXAvg + '.input1D[0]') 
        cmds.setAttr ( plusXAvg + '.input1D[1]', -initialX )
        cmds.connectAttr ( ctlPocNode + '.positionX', plusXAvg + '.input1D[2]') 
        cmds.setAttr ( plusXAvg + '.input1D[3]', -initialX ) 
        cmds.connectAttr ( wideJntPocNode + '.positionX', wideJntAddX + '.input1') 
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
        cmds.connectAttr ( pocNode + '.positionY', plusYAvg + '.input1D[0]')
        cmds.connectAttr ( ctlPocNode + '.positionY', plusYAvg + '.input1D[1]')
        cmds.connectAttr ( wideJntPocNode + '.positionY', plusYAvg + '.input1D[2]') 
        #2. add miro control translateY 
        cmds.connectAttr ( lidCtl[0] + '.ty', plusYAvg + '.input1D[3]')
        
        #3. multiply YRotateScale
        cmds.connectAttr ( plusYAvg + '.output1D', ctlMult + '.input1Y')
        cmds.setAttr ( ctlMult + '.input2Y', -RotateScale )
        cmds.connectAttr ( wideJntPocNode + '.positionY', wideJntMult + '.input1Y')
        cmds.setAttr ( wideJntMult + '.input2Y', -RotateScale )   
        
        #4. connect jnt rotateX
        if self.uplo[0] in jnt: 
            blinkRemap = cmds.shadingNode ( 'remapValue', asUtility=True, n = jnt.split('Blink', 1)[0] + str(index+1).zfill(2)+'_remap' )
            cmds.connectAttr ( ctlMult + ".outputY", blinkRemap + '.outputMin' ) 
            cmds.connectAttr ( blinkRemap + '.outValue',  jnt + '.rx')
            cmds.connectAttr ( wideJntMult + '.outputY', wideJnt + '.rx') 
        
        elif self.uplo[1] in jnt: 
            #get the remap from upJoint
            upJnt = jnt.replace("_lo","_up")
            cmds.connectAttr ( ctlMult + ".outputY", blinkGap + ".input1" ) 
            cmds.connectAttr ( blinkGap + ".output", ( upJnt.split('Blink',1)[0] + str(index+1).zfill(2)+'_remap'+'.outputMax'))  
            cmds.connectAttr ( ctlMult + ".outputY",  jnt + '.rx' ) 
            cmds.connectAttr ( wideJntMult + '.outputY', wideJnt + '.rx' ) 