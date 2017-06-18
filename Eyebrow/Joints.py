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

class Joints(Base.Base):
    def __init__(self, **kw):
        """
        initializing variables
        """
        #local variables
        Base.Base.__init__(self, **kw)
        
        self.allBaseJnts = list()
        
        self.browRotXCrvPos = cmds.xform(self.browRotXCrv, t = True, q = True, ws = True)
        self.browRotYCrvPos = cmds.xform(self.browRotYCrv, t = True, q = True, ws = True)
        
        if kw.get('locData'):
            self.eyeBrowVtxs = kw.get('locData')['eyebrowVtxs']
            
    def createJnts(self, eyeBrowVtxs):
        """
        creating joints on selected vertaxes
        """
        self.eyeBrowVtxs = eyeBrowVtxs
        sel = eval(self.eyeBrowVtxs)
        tempVerts = sel
        verts = self.sortSelected(tempVerts)
        cmds.select(cl = True)
        index = 1
        
        for x in verts:
            vertPos = cmds.xform(x, t = True, q = True, ws = True)
            if vertPos[0] <= 0.05:

                baseCntJnt = cmds.joint(n = self.baseCntJntName + str(index).zfill(2) + self.jntSuffix,
                                        p = [ 0, self.browRotXCrvPos[1], self.browRotXCrvPos[2]])
                ryCntJnt   = cmds.joint(n = self.browRotYJntName.replace(self.prefix[0], self.cPrefix) + self.jntSuffix,
                                        p = [ 0, self.browRotYCrvPos[1], self.browRotYCrvPos[2]])
                parentCntJnt = cmds.joint(n = self.parentCntJntName + str(index).zfill(2) + self.jntSuffix,
                                          p = vertPos)
                cmds.setAttr(baseCntJnt+'.rotateOrder', 2)
                cmds.joint(n = self.cPrefix + self.jntName + str(index), p = vertPos)
                cmds.joint(ryCntJnt, e=1, oj= 'zyx', secondaryAxisOrient = 'yup', ch=1,  zso=1)
                cmds.select(cl = True)
                
                #- save base joints
                self.allBaseJnts.append(baseCntJnt)
                
            else:
                baseJnt = cmds.joint(n = self.baseJntName + str(index).zfill(2) + self.jntSuffix,
                                     p = self.browRotXCrvPos)
                ryJnt = cmds.joint(n = self.browRotYJntName + str(index).zfill(2)+ self.jntSuffix, p = self.browRotYCrvPos )
                parentJnt = cmds.joint(n = self.parentJntName + str(index).zfill(2) + self.jntSuffix,
                                       p = vertPos)
                cmds.setAttr(baseJnt+'.rotateOrder', 2)
                cmds.joint(n = self.ljntName + str(index) + self.jntSuffix, p = vertPos)
                cmds.select(cl = True)
                cmds.joint(ryJnt, e=1, oj= 'zyx', secondaryAxisOrient = 'yup', ch=1,  zso=1)
                
                #- miorroring joints
                #- so far mirroring in Util module does not work with this code
                #- self.mirrorJoints(baseJnt, prefix = self.prefix)
                mirrJnt = cmds.mirrorJoint(baseJnt, mirrorYZ= True, searchReplace=(self.prefix[0], self.prefix[1]), mirrorBehavior = 1)
                cmds.joint(mirrJnt, e=1, oj= 'zyx', secondaryAxisOrient = 'yup', ch=1,  zso=1)
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