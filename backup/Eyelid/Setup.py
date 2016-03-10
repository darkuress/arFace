#!/bin/env python
# -*- coding: iso-8859-1 -*-
###############################################################################
#
# Copyright (c) 2015 Sukwon Shin, Jonghwan Hwang
# $Author: jhwang $
#
###############################################################################

'''
select base joints and run the script  
premise : L/R eyeBall position is symetrical
upLoEyeLid : should be either one of "upLf" or "loLf"
'''

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