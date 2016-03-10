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
import Func
reload(Func)

class Ctrls(Func.Func):
    def __init__(self, size, offset, rotateScale, **kw):
        """
        initializing variables
        """
        self.initialX         = 0
        self.size             = size
        self.offset           = offset
        self.rotateScale      = rotateScale
        
        #- initializing Func
        Func.Func.__init__(self, self.rotateScale, **kw)
                
    def createBrowCtrls (self, jnts):
        """
        select base joints and run the script
        """
        #jnts = cmds.ls(os = True, fl = True, type ='joint') 
        jntNum = len(jnts)
        jnts.sort()
        cJnt = [x for x in jnts if x.startswith(self.cPrefix)]
        lJnt = [x for x in jnts if x.startswith(self.prefix[0])]
        rJnt = [x for x in jnts if x.startswith(self.prefix[1])]
        rJnt.reverse()
        orderJnts = rJnt + cJnt + lJnt 
        
        basePos = cmds.xform( cJnt, t = True, q = True, ws = True)  
        
        browCrv = cmds.curve(d = 3, p =([-1,0,0],[-0.5,0,0],[0,0,0],[0.5,0,0],[1,0,0]), n='browCtrlCrv') 
        browCrvShape = cmds.listRelatives(browCrv, c = True) 
        
        index = 0 
        for jnt in orderJnts: 
            childJnt = cmds.listRelatives(jnt, c=True) 
            jntPos = cmds.xform(childJnt[0], t = True, q = True, ws = True) 
            self.pocNode = cmds.shadingNode('pointOnCurveInfo', asUtility=True, n = 'eyeBrowself.pocNode'+ str(index))
            cmds.connectAttr(browCrvShape[0] + ".worldSpace",  self.pocNode + '.inputCurve')
            cmds.setAttr(self.pocNode + '.turnOnPercentage', 1)
            increment = 1.0/(jntNum-1)
            cmds.setAttr(self.pocNode + '.parameter', increment *index)
            index = index + 1
            initialX = cmds.getAttr (self.pocNode + '.positionX')
            
            ctlName = jnt.split(self.jntSuffix)[0] + self.ctlSuffix
            
            if jnt in rJnt:
                rBrowCtrl, null = self.circleController(ctlName,
                                                        'xy',
                                                        self.size*0.2,
                                                        color = 17,
                                                        lockAttr = [])
                cmds.xform(null, ws = True, t = basePos)
                cmds.xform(rBrowCtrl, ws = True, t =(jntPos[0], jntPos[1], jntPos[2]+ self.offset))
                
                cmds.makeIdentity (null, apply=True, t=True, r=True, s=True, n =False) 
                self.crvCtrlToJnt (rBrowCtrl, jnt, null, self.pocNode, initialX, index)
                
            elif jnt in lJnt :
                lBrowCtrl, null = self.circleController(ctlName,
                                                        'xy',
                                                        self.size*0.2,
                                                        color = 6,
                                                        lockAttr = [])
                cmds.xform(null, ws = True, t = basePos)
                cmds.xform(lBrowCtrl, ws = True, t =(jntPos[0], jntPos[1], jntPos[2]+ self.offset))
                
                cmds.makeIdentity (null, apply=True, t=True, r=True, s=True, n =False) 
                self.crvCtrlToJnt (lBrowCtrl, jnt, null, self.pocNode, initialX, index)
                
            else :
                centerBrowCtrl = cmds.spaceLocator(n = ctlName, p =(0,0,0)) 
                cmds.setAttr(centerBrowCtrl[0]+'Shape.localScaleX', self.size * 0.3)
                cmds.setAttr(centerBrowCtrl[0]+'Shape.localScaleY', self.size * 0.3)
                cmds.setAttr(centerBrowCtrl[0]+'Shape.localScaleZ', self.size * 0.3)
                null = cmds.group (em=True, w =True, n = centerBrowCtrl[0] + "P")
                cmds.xform(null, ws = True, t = basePos)
                cmds.xform(centerBrowCtrl[0], ws = True, t =(jntPos[0], jntPos[1], jntPos[2]+ self.offset))
                cmds.parent(centerBrowCtrl[0], null) 
                cmds.makeIdentity (null, apply=True, t=True, r=True, s=True, n =False) 
                self.crvCtrlToJnt(centerBrowCtrl[0], jnt, null, self.pocNode, initialX, index)