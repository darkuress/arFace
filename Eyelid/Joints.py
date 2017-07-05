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

        try:
            self.eyeRotY      = cmds.getAttr(self.lEyeLoc + '.ry')
            self.eyeRotZ      = cmds.getAttr(self.lEyeLoc + '.rz')
            self.eyeCenterPos = cmds.xform(self.lEyeLoc, t = True, q = True, ws = True) 
        except ValueError:
            print "create the eye locators"
            raise 

    def createJnts(self,
                   updown        = 'up',
                   upEyelidVtxs  = '',
                   loEyelidVtxs  = '',
                   cnrEyelidVtxs = ''):
        """
        creatint Joints
        """       
        #Eyelid Vertexes        
        #verts = cmds.ls( os = True, fl = True)
        if updown == self.uploPrefix[0]:
            verts = eval(upEyelidVtxs)
        elif updown == self.uploPrefix[1]:
            verts = eval(loEyelidVtxs)
        elif updown == self.cnrPrefix:
            verts = eval(cnrEyelidVtxs)
        geoName = self.headGeo
        
        #- list vertices by tx position order
        orderedVerts = self.sortSelected(verts)
        cmds.select(cl = True)
        
        # create parent group for eyelid joints
        lidJntP = cmds.joint(n = self.prefix[0] + updown + self.lidJntPName)
        null = self.group(children = [lidJntP], parent = self.prefix[0] + updown+'EyeLid'+ self.jntSuffix + self.grpSuffix)
        cmds.xform(null, t = self.eyeCenterPos) 
        cmds.setAttr(null + '.ry', self.eyeRotY)
        if not updown == self.cnrPrefix:
            cmds.setAttr(null + '.rz', self.eyeRotZ)
            
        cmds.select(cl = True)
            
        self.allBaseJnts = []
        #create Joints on selected vertex
        index = 1
        for vert in orderedVerts:       
            vertPos = cmds.xform(vert, t = True, q = True, ws = True)
            if updown == self.cnrPrefix:
                lidJnt = cmds.joint(n = self.prefix[0] + self.innerOuter[index-1] + self.lidJntName + self.jntSuffix, p = vertPos ) 
                lidJntTX = cmds.joint(n = self.prefix[0] + self.innerOuter[index-1] + self.lidJntTXName + 'TX' + self.jntSuffix, p = vertPos )
            else:
                lidJnt = cmds.joint(n = self.prefix[0] + updown +  self.lidJntName + str(index).zfill(2) + self.jntSuffix, p = vertPos) 
                lidJntTX = cmds.joint(n = self.prefix[0] + updown + self.lidJntTXName + str(index).zfill(2) + self.jntSuffix, p = vertPos) 
            cmds.joint(lidJnt, e =True, zso =True, oj = 'zyx', sao= 'yup')
            
            cmds.parent(lidJnt, null)
            
            blinkJnt = cmds.duplicate (lidJnt, po=True, n = self.prefix[0] + updown + self.blinkJntName + str(index).zfill(2) + self.jntSuffix)
            cmds.setAttr(blinkJnt[0] + '.tx' , 0) 
            cmds.setAttr(blinkJnt[0] + '.ty' , 0) 
            cmds.setAttr(blinkJnt[0] + '.tz' , 0)
            wideJnt = cmds.duplicate(blinkJnt, n = self.prefix[0] + updown + self.wideJntName + str(index).zfill(2) + self.jntSuffix)  
            scaleJnt = cmds.duplicate(blinkJnt, n = self.prefix[0] + updown + self.scaleJntName + str(index).zfill(2) + self.jntSuffix)
            cmds.parent(lidJnt , blinkJnt[0])
            cmds.parent(blinkJnt[0], scaleJnt[0])
            cmds.parent(wideJnt[0], scaleJnt[0])
            cmds.parent(scaleJnt[0], lidJntP)
            index = index + 1
            
        #- mirror joints
        rLidJntP = self.mirrorJoints(topJoint = lidJntP, prefix = [self.prefix[0], self.prefix[1]])
        #rLidJntP = cmds.mirrorJoint(lidJntP, mirrorBehavior=True, myz = True, searchReplace = (self.prefix[0], self.prefix[1]))
        rNull = cmds.group(n = self.prefix[1] + updown + 'EyeLid'+ self.jntSuffix + self.grpSuffix, em =True)
        self.match(dest = rNull, source = rLidJntP)
        cmds.parent(lidJntP, null)
        cmds.parent(rLidJntP, rNull)
        
        self.allBaseJnts.append(null)
        self.allBaseJnts.append(rNull)
        
        self.__eyeWideJntLabel()
        
        return self.allBaseJnts

    def __eyeWideJntLabel(self):    
        """
        labeling wide joint label after creating joints
        """
        lWideLid = cmds.ls(self.prefix[0] + "*Wide*" + self.jntSuffix, fl=1, type = "transform")
        rWideLid = cmds.ls(self.prefix[1] + "*Wide*" + self.jntSuffix, fl=1, type = "transform")
        for i, j in enumerate(lWideLid):
            #print i, j
            cmds.setAttr(j + ".side", 1)
            cmds.setAttr(j + ".type", 18)
            cmds.setAttr(j + ".otherType", str(i).zfill(2), type = "string")        
        
        for id, k in enumerate(rWideLid):
            #print id, k
            cmds.setAttr(k + ".side", 2)
            cmds.setAttr(k + ".type", 18)
            cmds.setAttr(k + ".otherType", str(id).zfill(2), type = "string")
        
        
    def createCnrJoints(self):
        pass

    @property
    def baseJnts(self):
        """
        return all Base Jnts (left only)
        """
        return self.allBaseJnts
