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

class Joints(Base.Base):
    def __init__(self, **kw):
        """
        initializing variables
        """
        #local variables
        Base.Base.__init__(self, **kw)
        
        self.allBaseJnts = list()

    def createJnts(self):
        """
        creating joints on selected vertaxes
        """
        #sel = cmds.ls( os= True, fl = True)
        sel = eval(self.eyeBrowVtxs) + eval(self.eyeBrowLoc)
        tempVerts = sel[:-1]
        verts = self.sortSelected(tempVerts)
        browBall = sel[-1]
        browBallPos = cmds.xform(browBall, t = True, q = True, ws = True)
        cmds.select(cl = True)
        index = 1
        
        for x in verts:
            vertPos = cmds.xform(x, t = True, q = True, ws = True)
            if vertPos[0] <= 0.05:
                baseCntJnt = cmds.joint(n = self.baseCntJntName + str(index).zfill(2) + self.jntSuffix,
                                        p = [ 0, browBallPos[1], browBallPos[2]])
                parentCntJnt = cmds.joint(n = self.parentCntJntName + str(index).zfill(2) + self.jntSuffix,
                                          p = vertPos)
                cmds.setAttr(baseCntJnt+'.rotateOrder', 2)
                cmds.joint(n = self.cPrefix + self.jntName + str(index), p = vertPos)
                cmds.select(cl = True)
                
                #- save base joints
                self.allBaseJnts.append(baseCntJnt)
                
            else:
                baseJnt = cmds.joint(n = self.baseJntName + str(index).zfill(2) + self.jntSuffix,
                                     p = [browBallPos[0], browBallPos[1], browBallPos[2]])
                parentJnt = cmds.joint(n = self.parentJntName + str(index).zfill(2) + self.jntSuffix,
                                       p = vertPos)
                cmds.setAttr(baseJnt+'.rotateOrder', 2)
                cmds.joint(n = self.ljntName + str(index) + self.jntSuffix, p = vertPos)
                cmds.select(cl = True)
                               
                #- miorroring joints
                #- so far mirroring in Util module does not work with this code
                #- self.mirrorJoints(baseJnt, prefix = self.prefix)
                cmds.mirrorJoint(baseJnt, mirrorYZ= True, searchReplace=(self.prefix[0], self.prefix[1]))
                cmds.select(cl = True)
                index = index + 1
                
                #- save base joints
                self.allBaseJnts.append(baseJnt)
                self.allBaseJnts.append(baseJnt.replace(self.prefix[0], self.prefix[1]))
                
        return self.allBaseJnts
    
    @property
    def baseJnts(self):
        """
        return all Base Jnts (left only)
        """
        return self.allBaseJnts