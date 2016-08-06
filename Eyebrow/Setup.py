#!/bin/env pyth
# -*- coding: iso-8859-1 -*-
###############################################################################
#
# Copyright (c) 2015 Sukwon Shin, Jonghwan Hwang
# $Author: jhwang $
#
###############################################################################

import maya.cmds as cmds
import Joints
reload(Joints)
import Ctrls
reload(Ctrls)

class Setup(Joints.Joints, Ctrls.Ctrls):
    def __init__(self,
                 size = 1,
                 offset = 1,
                 rotateScale = 10,
                 **kw):
        """
        initializing variables
        """
        
        Joints.Joints.__init__(self, **kw)
        Ctrls.Ctrls.__init__(self, size, offset, rotateScale, **kw)
         
    def createJoints(self):
        """
        creating joints on selected vertaxes
        """
        allJnts = self.createJnts()
        #- grouping joints
        self.group(allJnts, self.eyebrowJntGrpName)
        cmds.parent(self.eyebrowJntGrpName, self.jntGrp)
        
        return self.eyebrowJntGrpName
    
    def createCtrls(self, jnts):
        """
        select base joints and run the script
        """
        cmds.select(cl = True)
        self.ctrlInfo = self.createBrowCtrls(jnts)
        #self.group(self.ctrlInfo['browsCtlGrp'], self.eyebrowCtlGrpName)
        #self.group(self.ctrlInfo['browsCrvGrp'], self.eyebrowCrvGrpName)
        #cmds.parent(self.eyebrowCtlGrpName, self.ctlGrp)
        #cmds.parent(self.eyebrowCrvGrpName, self.crvGrp)
        
        return self.eyebrowCtlGrpName, self.eyebrowCrvGrpName

    def createSurfMapGeo(self, faceGeo):
        """
        create surface map geo
        """
        return self.createMapSurf(faceGeo)
    
    def browMapSkinning(self):
        """
        eyebrow map surface skinning 
        """
        self.skinBrowSurfaceMap()

    def connectToControlPanel(self):
        """
        connect brow control to panel
        """
        self.connectToPanel()
    
    def saveVertaxPos(self):
        pass