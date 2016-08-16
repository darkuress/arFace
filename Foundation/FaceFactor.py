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

class FaceFactor(Core.Core, Util.Util):
    def __init__(self):
        """
        initializing variables
        """
        Core.Core.__init__(self)
        Util.Util.__init__(self)

    def create(self):
        """
        run
        """
        if not cmds.objExists(self.faceFactors['main']):
            self.node = cmds.group( n = self.faceFactors['main'], em = 1, p = 'faceMain' )
        
        self.__browFactor()
        return self.node
        
    def __browFactor(self):
        """
        create browFactor
        """
        self.browFactor = cmds.createNode('transform', n = self.faceFactors['eyebrow'])
        cmds.parent(self.browFactor, self.node)
        
        level_sub = cmds.shadingNode( 'plusMinusAverage', asUtility =1, n ='blinkLevel_sub ')
        cmds.addAttr(self.browFactor, longName= 'lidRotateX_scale', attributeType='float', dv = 20) 
        cmds.addAttr(self.browFactor, longName= 'lidRotateY_scale', attributeType='float', dv = 20) 
        cmds.addAttr(self.browFactor, longName= 'browRotateX_scale', attributeType='float', dv = 20) 
        cmds.addAttr(self.browFactor, longName= 'browRotateY_scale', attributeType='float', dv = 20) 
        prefix = self.prefix
        for LR in prefix:
            if self.prefix[0] in LR:
                XYZ = 'y'
            else: XYZ = 'x' 
        
            #temporary ranges to jumperPaner 
            cmds.addAttr(self.browFactor, longName= 'range_'+LR + "eyeU", attributeType='float', dv = 1)                      
            cmds.addAttr(self.browFactor, longName= 'range_'+LR + "eyeD", attributeType='float', dv = 1) 
            cmds.addAttr(self.browFactor, longName= 'range_'+LR + "eyeL", attributeType='float', dv = 1)                      
            cmds.addAttr(self.browFactor, longName= 'range_'+LR + "eyeR", attributeType='float', dv = 1) 
            #'''
            cmds.addAttr(self.browFactor, longName= LR + "loBlinkLevel", attributeType='float', dv = 0.05)
            cmds.addAttr(self.browFactor, longName= LR + "upBlinkLevel", attributeType='float', dv = .95)
            
            cmds.setAttr (level_sub + '.operation', 2 )
            cmds.setAttr (level_sub + '.input2D[0].input2Dx', 1 )
            cmds.setAttr (level_sub + '.input2D[0].input2Dy', 1 )
    
            cmds.connectAttr ( self.browFactor + '.' +LR +"loBlinkLevel", level_sub + '.input2D[1].input2D'+XYZ )
            cmds.connectAttr ( level_sub + '.output2D.output2D'+XYZ, self.browFactor + '.'+LR +"upBlinkLevel" )
        
        return self.browFactor