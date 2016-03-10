def createHelpPanel ( ctlName, type):
    '''ctlNames = ['eyeCtl', 'eyeBlink', 'eyeSquint', 'eyeSquach' ]'''
    
    LfRt = ["l_", "r_"]
    for pfx in LfRt:
        attrs=[ pfx +'HCtl', pfx +'VCtl', pfx +'HPos', pfx +'HNeg', pfx +'VPos', pfx +'VNeg']
        if ( type == 'B' ):
            attrs=[ pfx +'HCtl', pfx +'VCtl', pfx +'HPos', pfx +'HNeg', pfx +'VPos', pfx +'VNeg', pfx +'HPosVPos', pfx +'HPosVNeg', pfx +'HNegVPos', pfx +'HNegVNeg']
            
        for att in attrs:
            cmds.addAttr ( ctlName + "HelpPanel", longName = att , at='double', defaultValue= 0 , minValue=0, maxValue=1 )
        
        negMult = cmds.shadingNode ( 'multiplyDivide', asUtility=True, n = pfx + ctlName + 'Neg_mult' )
        posClamp = cmds.shadingNode ( 'clamp', asUtility=True, n = pfx + ctlName + 'Pos_clamp' )
        negClamp = cmds.shadingNode ( 'clamp', asUtility=True, n = pfx + ctlName + 'Neg_clamp' )
        cmds.connectAttr ( pfx + ctlName +".tx", ctlName + "HelpPanel." + pfx + "HCtl")
        cmds.connectAttr ( pfx + ctlName +".ty", ctlName + "HelpPanel." + pfx + "VCtl")
        cmds.connectAttr ( pfx + ctlName +".tx", posClamp + ".inputR" )
        cmds.connectAttr ( pfx + ctlName +".ty", posClamp + ".inputG" )
        cmds.setAttr ( posClamp + ".maxR", 1 )
        cmds.setAttr ( posClamp + ".maxG", 1 )
        cmds.connectAttr ( posClamp + ".outputR", ctlName + "HelpPanel." + pfx + "HPos")
        cmds.connectAttr ( posClamp + ".outputG", ctlName + "HelpPanel." + pfx + "VPos")
        
        cmds.connectAttr (  pfx + ctlName +".tx", negMult + ".input1X" )
        cmds.connectAttr (  pfx + ctlName +".ty", negMult + ".input1Y" )
        cmds.setAttr ( negMult + ".input2X", -1 )
        cmds.setAttr ( negMult + ".input2Y", -1 )
        cmds.connectAttr ( negMult + ".outputX", negClamp + ".inputR" )
        cmds.connectAttr ( negMult + ".outputY", negClamp + ".inputG" )            
        cmds.setAttr ( negClamp  + ".maxR", 1 )
        cmds.setAttr ( negClamp  + ".maxG", 1 )
        cmds.connectAttr ( negClamp + ".outputR", ctlName + "HelpPanel." + pfx + "HNeg")
        cmds.connectAttr ( negClamp + ".outputG", ctlName + "HelpPanel." + pfx + "VNeg")
        
        if ( type =='B' ):
            plusOne = cmds.shadingNode ( 'plusMinusAverage', asUtility=True, n = pfx + ctlName + '_plusOne' )
            vNegMult = cmds.shadingNode ( 'multiplyDivide', asUtility=True, n = pfx + ctlName + 'VNeg_mult' )
            vPosMult = cmds.shadingNode ( 'multiplyDivide', asUtility=True, n = pfx + ctlName + 'VPos_mult' )
            plusOneClamp = cmds.shadingNode ( 'clamp', asUtility=True, n = pfx + ctlName + 'plusOne_clamp' )
            cmds.connectAttr ( pfx + ctlName +".tx", plusOne + '.input3D[0].input3Dx' ) 
            cmds.connectAttr ( negMult + '.outputX', plusOne + '.input3D[0].input3Dy' )
            cmds.setAttr ( plusOne + ".operation",  1 )
            cmds.setAttr ( plusOne + '.input3D[1].input3Dx', 1 )
            cmds.setAttr ( plusOne + '.input3D[1].input3Dy', 1 )
            cmds.connectAttr ( plusOne + '.output3Dx', plusOneClamp + ".inputR" )
            cmds.connectAttr ( plusOne + '.output3Dy', plusOneClamp + ".inputG" )
            cmds.setAttr ( plusOneClamp + '.maxR', 1 )
            cmds.setAttr ( plusOneClamp + '.maxG', 1 )
            cmds.connectAttr ( plusOneClamp + '.outputR', vPosMult + ".input1X" )
            cmds.connectAttr ( plusOneClamp + '.outputG', vPosMult + ".input1Y" )
            cmds.connectAttr ( ctlName + "HelpPanel." + pfx + "VPos", vPosMult + ".input2X" )
            cmds.connectAttr ( ctlName + "HelpPanel." + pfx + "VPos", vPosMult + ".input2Y" )
            cmds.connectAttr ( vPosMult + ".outputX", ctlName + "HelpPanel." + pfx + 'HPosVPos' )
            cmds.connectAttr ( vPosMult + ".outputY", ctlName + "HelpPanel." + pfx + 'HNegVPos' )
            
            cmds.connectAttr ( plusOneClamp + '.outputR', vNegMult + ".input1X" )
            cmds.connectAttr ( plusOneClamp + '.outputG', vNegMult + ".input1Y" )
            cmds.connectAttr ( ctlName + "HelpPanel." + pfx + "VNeg", vNegMult + ".input2X" )
            cmds.connectAttr ( ctlName + "HelpPanel." + pfx + "VNeg", vNegMult + ".input2Y" )
            cmds.connectAttr ( vNegMult + ".outputX", ctlName + "HelpPanel." + pfx + 'HPosVNeg' )
            cmds.connectAttr ( vNegMult + ".outputY", ctlName + "HelpPanel." + pfx + 'HNegVNeg' )