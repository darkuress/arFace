#!/bin/env python
# -*- coding: iso-8859-1 -*-
###############################################################################
#
# Copyright(c) 2015 Sukwon Shin, Jonghwan Hwang
# $Author: jhwang $
#
###############################################################################

import maya.cmds as cmds

from ..Misc import Core
reload(Core)
from ..Misc import Util
reload(Util)

class Container(Core.Core, Util.Util):
    def __init__(self):
        """
        initializing variables
        """
        Core.Core.__init__(self)
        Util.Util.__init__(self)

    def faceFactors(self):
        if not cmds.objExists('faceFactors'):
            cmds.group( n = "faceFactors", em = 1, p = "faceMainRig" ) 
        
        level_sub = cmds.shadingNode( 'plusMinusAverage', asUtility =1, n ='blinkLevel_sub ')
        cmds.addAttr('faceFactors', longName= 'lidRotateX_scale', attributeType='float', dv = 20) 
        cmds.addAttr('faceFactors', longName= 'lidRotateY_scale', attributeType='float', dv = 20) 
        cmds.addAttr('faceFactors', longName= 'browRotateX_scale', attributeType='float', dv = 20) 
        cmds.addAttr('faceFactors', longName= 'browRotateY_scale', attributeType='float', dv = 20) 
        prefix = self.prefix
        for LR in prefix:
            if self.prefix[0] in LR:
                XYZ = 'y'
            else: XYZ = 'x' 
        
            #temporary ranges to jumperPaner 
            cmds.addAttr('faceFactors', longName= 'range_'+LR + "eyeU", attributeType='float', dv = 1)                      
            cmds.addAttr('faceFactors', longName= 'range_'+LR + "eyeD", attributeType='float', dv = 1) 
            cmds.addAttr('faceFactors', longName= 'range_'+LR + "eyeL", attributeType='float', dv = 1)                      
            cmds.addAttr('faceFactors', longName= 'range_'+LR + "eyeR", attributeType='float', dv = 1) 
            #'''
            cmds.addAttr('faceFactors', longName= LR + "loBlinkLevel", attributeType='float', dv = 0.05)
            cmds.addAttr('faceFactors', longName= LR + "upBlinkLevel", attributeType='float', dv = .95)
            
            cmds.setAttr (level_sub + '.operation', 2 )
            cmds.setAttr (level_sub + '.input2D[0].input2Dx', 1 )
            cmds.setAttr (level_sub + '.input2D[0].input2Dy', 1 )
    
            cmds.connectAttr ( 'faceFactors.'+LR +"loBlinkLevel", level_sub + '.input2D[1].input2D'+XYZ )
            cmds.connectAttr ( level_sub + '.output2D.output2D'+XYZ, 'faceFactors.'+LR +"upBlinkLevel" ) 