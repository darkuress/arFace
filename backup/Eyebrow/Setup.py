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
        self.createJnts()
        return None
    
    def createCtrls(self, jnts):
        """
        select base joints and run the script
        """
        cmds.select(cl = True)
        self.createBrowCtrls(jnts)
    
    def saveVertaxPos(self):
        pass