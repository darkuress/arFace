#!/bin/env python
# -*- coding: iso-8859-1 -*-
###############################################################################
#
# Copyright (c) 2015 Sukwon Shin, Jonghwan Hwang
# $Author: jhwang $
#
###############################################################################

# brow joints create
'''select left brow vertex points and pivot point. run the script
  name = centerBrowBase0l, EyeBrowBase01... '''

import maya.cmds as cmds
import Base
reload(Base)

class Func(Base.Base):
    def __init__(self, rotateScale, **kw):
        """
        initializing variables
        """
        #local variables
        Base.Base.__init__(self, **kw)

    def crvCtrlToJnt(self, browCtrl, jnt, ctrlP, pocNode, initialX, index):
        #connect browCtrlCurve and Controller to the brow joints
        ctrlMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = jnt.split('Base', 1)[0] +'CtrlMult'+ str(index))
        crvMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = jnt.split('Base', 1)[0] +'CrvMult'+ str(index))
        browAddDY = cmds.shadingNode('addDoubleLinear', asUtility=True, n = jnt.split('Base', 1)[0] +'YAdd'+ str(index))
        browAddDX = cmds.shadingNode('addDoubleLinear', asUtility=True, n = jnt.split('Base', 1)[0] +'XAdd'+ str(index))
        minusAvgX = cmds.shadingNode('plusMinusAverage', asUtility=True, n = jnt.split('Base', 1)[0] +'Xminus'+ str(index))
         
        cmds.connectAttr(browCtrl + '.tx', ctrlMult + '.input1X')
        cmds.connectAttr(browCtrl + '.ty', ctrlMult + '.input1Y')
        cmds.setAttr(ctrlMult + '.input2X', self.rotateScale)
        cmds.setAttr(ctrlMult + '.input2Y', -self.rotateScale)
        
        cmds.setAttr(minusAvgX + '.operation', 2)
        cmds.connectAttr(pocNode + '.positionX', minusAvgX + '.input1D[0]')
        cmds.setAttr(minusAvgX + '.input1D[1]', initialX)
    
        cmds.connectAttr(minusAvgX + '.output1D', crvMult + '.input1X')
        cmds.connectAttr(pocNode + '.positionY', crvMult + '.input1Y')
        cmds.setAttr(crvMult + '.input2X', self.rotateScale)
        cmds.setAttr(crvMult + '.input2Y', -self.rotateScale)
        cmds.connectAttr(crvMult + ".outputX", ctrlP + '.ry')
        cmds.connectAttr(crvMult + ".outputY", ctrlP + '.rx')
            
        cmds.connectAttr(ctrlMult + '.outputX', browAddDX + '.input1')
        cmds.connectAttr(crvMult + '.outputX', browAddDX + '.input2')
        cmds.connectAttr(ctrlMult + '.outputY', browAddDY + '.input1')
        cmds.connectAttr(crvMult + '.outputY', browAddDY + '.input2')
        
        cmds.connectAttr(browAddDY + ".output", jnt + '.rx')
        cmds.connectAttr(browAddDX + ".output", jnt + '.ry')