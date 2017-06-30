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
    def __init__(self, **kw):
        """
        initializing variables
        """
        Core.Core.__init__(self, **kw)
        Util.Util.__init__(self)

    def create(self):
        """
        run
        """
        if not cmds.objExists(self.faceFactors['main']):
            self.node = cmds.group( n = self.faceFactors['main'], em = 1, p = self.faceMainNode )
        
        self.__browFactor()
        self.__lidFactor()
        self.__lipFactor()
        
        return self.node
        
    def __browFactor(self):
        """
        create browFactor
        """
        self.browFactor = cmds.createNode('transform', n = self.faceFactors['eyebrow'])
        cmds.parent(self.browFactor, self.node)
        
        #cmds.addAttr(self.browFactor, longName= 'lidRotateX_scale',  attributeType='float', dv = 20) 
        #cmds.addAttr(self.browFactor, longName= 'lidRotateY_scale',  attributeType='float', dv = 20) 
        cmds.addAttr(self.browFactor, longName= 'browUp_scale',      attributeType='float', dv = 20)
        cmds.addAttr(self.browFactor, longName= 'browDown_scale',    attributeType='float', dv = 10) 
        cmds.addAttr(self.browFactor, longName= 'browRotateY_scale', attributeType='float', dv = 20) 
        
        return self.browFactor

    def __lidFactor(self):
        """
        create browFactor
        """        
        self.lidFactor = cmds.createNode('transform', n = self.faceFactors['eyelid'])
        cmds.parent(self.lidFactor, self.node)
            
        level_sub = cmds.shadingNode( 'plusMinusAverage', asUtility =1, n ='blinkLevel_sub ')
        cmds.addAttr(self.lidFactor, longName= 'lidRotateX_scale', attributeType='float', dv = 20) 
        cmds.addAttr(self.lidFactor, longName= 'lidRotateY_scale', attributeType='float', dv = 20) 
        cmds.addAttr(self.lidFactor, longName= 'eyeBallRotY_scale', attributeType='float', dv = 20)
        cmds.addAttr(self.lidFactor, longName= 'eyeBallRotX_scale', attributeType='float', dv = 20)
        
        for LR in self.prefix:
            if 'l_' in LR:
                XYZ = 'y'
            else: XYZ = 'x' 
        
            #temporary ranges to jumperPaner 
            cmds.addAttr(self.lidFactor, longName= 'range_' + LR + "eyeU", attributeType='float', dv = 1)                      
            cmds.addAttr(self.lidFactor, longName= 'range_' + LR + "eyeD", attributeType='float', dv = 1) 
            cmds.addAttr(self.lidFactor, longName= 'range_' + LR + "eyeL", attributeType='float', dv = 1)                      
            cmds.addAttr(self.lidFactor, longName= 'range_' + LR + "eyeR", attributeType='float', dv = 1) 
            #'''
            cmds.addAttr(self.lidFactor, longName= LR + "loBlinkLevel", attributeType='float', dv = 0.05)
            cmds.addAttr(self.lidFactor, longName= LR + "upBlinkLevel", attributeType='float', dv = .95)
            
            cmds.setAttr(level_sub + '.operation', 2)
            cmds.setAttr(level_sub + '.input2D[0].input2Dx', 1)
            cmds.setAttr(level_sub + '.input2D[0].input2Dy', 1)
    
            cmds.connectAttr(self.lidFactor + '.' + LR + "loBlinkLevel", level_sub + '.input2D[1].input2D' + XYZ)
            cmds.connectAttr(level_sub + '.output2D.output2D' + XYZ, self.lidFactor + '.' + LR + "upBlinkLevel")
            
    def __lipFactor(self):
        """
        create lipFactor
        """
        self.lipFactor = cmds.createNode('transform', n = self.faceFactors['lip'])
        cmds.parent(self.lipFactor, self.node)
    
        #swivel factors
        cmds.addAttr(self.lipFactor, longName= 'swivel_lipJntP_tx', attributeType='float', dv = 1.5 )
        cmds.addAttr(self.lipFactor, longName= 'swivel_lipJntP_ty', attributeType='float', dv = 2 )
        cmds.addAttr(self.lipFactor, longName= 'swivel_lipJntX_ry', attributeType='float', dv =6)
        cmds.addAttr(self.lipFactor, longName= 'swivel_lipJntX_rz', attributeType='float', dv =15)
        cmds.addAttr(self.lipFactor, longName= 'swivel_lipJntP_sx', attributeType='float', dv =0.05 )
        cmds.addAttr(self.lipFactor, longName= 'swivel_lipJntP_sz', attributeType='float', dv =0.02 )
        cmds.addAttr(self.lipFactor, longName= 'swivel_jawSemi_sx', attributeType='float', dv =0.05 )
        cmds.addAttr(self.lipFactor, longName= 'swivel_jawSemi_sz', attributeType='float', dv =0.02 )
        
        #UDLR   
        cmds.addAttr(self.lipFactor, longName= 'UDLR_TX_scale', attributeType='float', dv =1 )
        cmds.addAttr(self.lipFactor, longName= 'UDLR_TY_scale', attributeType='float', dv =1.5 )
        #UDLR drive lip joint and jawClose
        cmds.addAttr(self.lipFactor, longName= 'txSum_lipJntX_tx', attributeType='float', dv =2 )
        cmds.addAttr(self.lipFactor, longName= 'tySum_lipJntX_ty', attributeType='float', dv =2 )
        cmds.addAttr(self.lipFactor, longName= 'UDLR_jawCloseTY', attributeType='float', dv =3 )
        cmds.addAttr(self.lipFactor, longName= 'UDLR_jawCloseTZ', attributeType='float', dv =2 )
        
        cmds.addAttr(self.lipFactor, longName= 'tzSum_lipJntX_tz', attributeType='float', dv =1.5 )
        cmds.addAttr(self.lipFactor, longName= 'tySum_lipJntX_rx', attributeType='float', dv =-20 )
        cmds.addAttr(self.lipFactor, longName= 'txSum_lipJntX_ry', attributeType='float', dv =6 )

        #jawOpen
        cmds.addAttr(self.lipFactor, longName= 'jawOpenTX_scale', attributeType='float', dv =1.5 ) 
        cmds.addAttr(self.lipFactor, longName= 'jawOpenTY_scale', attributeType='float', dv =2 )  
        cmds.addAttr(self.lipFactor, longName= 'jawOpen_jawCloseRX', attributeType='float', dv = -36 )
        cmds.addAttr(self.lipFactor, longName= 'jawOpen_jawCloseRY', attributeType='float', dv = 8 )
        
        #mouth_move : lipJotY* only driven by lipCtrl(freeform) / mouth_move
        cmds.addAttr(self.lipFactor, longName= 'mouth_lipJntX_rx', attributeType='float', dv =-20 )
        cmds.addAttr(self.lipFactor, longName= 'mouth_lipJntY_ry', attributeType='float', dv = 14 ) 
        cmds.addAttr(self.lipFactor, longName= 'mouth_lipJntY_rz', attributeType='float', dv = 7 )
            
        #cmds.addAttr(self.lipFactor, longName= 'move_RZscale', attributeType='float', dv =1 )
        cmds.addAttr(self.lipFactor, longName= 'txSum_lipJntY_ry', attributeType='float', dv =14 )
        cmds.addAttr(self.lipFactor, longName= 'txSum_lipJntY_rz', attributeType='float', dv =7 )
        cmds.addAttr(self.lipFactor, longName= 'mouth_midCheekRY', attributeType='float', dv = 6 ) 
        cmds.addAttr(self.lipFactor, longName= 'mouth_midCheekRZ', attributeType='float', dv = 4 ) 
        cmds.addAttr(self.lipFactor, longName= 'mouth_midCheekRX', attributeType='float', dv = -8 )
        cmds.addAttr(self.lipFactor, longName= 'mouth_loCheekRY', attributeType='float', dv =10 )
        cmds.addAttr(self.lipFactor, longName= 'mouth_loCheekRZ', attributeType='float', dv =5 )
        cmds.addAttr(self.lipFactor, longName= 'mouth_loCheekRX', attributeType='float', dv =-15 )
        #lipRoll 
        cmds.addAttr(self.lipFactor, longName= 'YZPoc_rollJntT_ty', attributeType='float', dv =1.5 )
        cmds.addAttr(self.lipFactor, longName= 'YZPoc_rollJntT_tz', attributeType='float', dv =2 )
        