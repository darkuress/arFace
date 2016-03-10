 #눈꺼플 커브와 눈 컨트롤러 연결
#build help panel / connect Blink, Squint, Wide Curves  
cmds.ls ("l_loEyelidBlink*_yAdd*", fl=True, type="addDoubleLinear" )
cmds.ls ( "l_upLidBlink*_jnt", fl=True, type="joint" )
def helpPanelToEyeCrv ():
    '''
    ctlNames = ['eyeCtl', 'eyeBlink', 'eyeSquint', 'eyeSquach' ]'''
    cmds.group ( em=True, n = "helpPanels" )
    LfRt = ["l_", "r_"]
    for pfx in LfRt: 
        
        # set blink range 
        blinkJnts = cmds.ls ( pfx + "upLidBlink*_jnt", fl=True, type="joint" )
        blinkJnts.sort()    
        blinkGap = cmds.ls ( pfx + "loEyelidBlink*_yAdd*", fl=True, type="addDoubleLinear" )
        blinkGap.sort()
        numJnts = len (blinkJnts)
        for i in range (0, numJnts ):
            rotX = cmds.getAttr ( blinkJnts[i] +".rx" )
            cmds.setAttr ( blinkGap[i] + ".input2", rotX) 
       
        cmds.setAttr( pfx + "upLidCrvBS." + pfx + "upBlink_crv", 0 )   
        
        #Blink setup                     
        if not cmds.objExists ("eyeBlinkHelpPanel"):
            cmds.group ( em=True, p = 'helpPanels', n = "eyeBlinkHelpPanel" )
        
        attList = cmds.listAttr( "eyeBlinkHelpPanel", s=True, r=True, w=True, c=True, st = ["*Pos", "Neg"]) 
        if not ( attList ):
            createHelpPanel ( 'eyeBlink', "A" )
                
        #blinkCtrl connect to the eyeOpen curves ( lidCurve BlendShape )
        #cmds.connectAttr ( "eyeBlinkHelpPanel." + pfx + "VPos", pfx+"upLidCrvBS." + pfx + "upEyeOpen_crv" )
        #cmds.connectAttr ( "eyeBlinkHelpPanel." + pfx + "VPos", pfx+"loLidCrvBS." + pfx + "loEyeOpen_crv" )
        
        # blinkCtrl connect to all the remapValue.inputValue / loBlink curves
        remapList = cmds.ls ( pfx + "upLid*_remap", fl =True, type = "remapValue")
        for remap in remapList:
            cmds.connectAttr ( "eyeBlinkHelpPanel." + pfx + "VNeg", remap + ".inputValue" )
    
        cmds.connectAttr ( "eyeBlinkHelpPanel." + pfx + "VNeg", pfx + "loLidCrvBS." + pfx + "loBlink_crv" )
        
             
        #Squint Wide setup                     
        if not cmds.objExists ("eyeSquintHelpPanel"):
            cmds.group ( em=True, p = 'helpPanels', n = "eyeSquintHelpPanel" )
        
        attList = cmds.listAttr( "eyeSquintHelpPanel", s=True, r=True, w=True, c=True, st = ["*Pos", "Neg"]) 
        if not ( attList ):
            createHelpPanel ("eyeSquint", "A" )
                    
        #squint_wide ctrl connect to the eyeWideJnt curves ( WideJnt BlendShape )
        cmds.connectAttr ( "eyeSquintHelpPanel." + pfx + "VPos", pfx+"upWideJntBS." + pfx + "upWide_crv" )
        cmds.connectAttr ( "eyeSquintHelpPanel." + pfx + "VPos", pfx+"loWideJntBS." + pfx + "loWide_crv" )
        cmds.connectAttr ( "eyeSquintHelpPanel." + pfx + "VNeg", pfx+"upWideJntBS." + pfx + "upSquint_crv" )
        cmds.connectAttr ( "eyeSquintHelpPanel." + pfx + "VNeg", pfx+"loWideJntBS." + pfx + "loSquint_crv" )  
        
        if not cmds.objExists ("eyeCtlHelpPanel"):
            cmds.group ( em=True, p = 'helpPanels', n = "eyeCtlHelpPanel" )
        
        attList = cmds.listAttr( "eyeCtlHelpPanel", s=True, r=True, w=True, c=True, st = ["*Pos", "Neg"]) 
        if not ( attList ):
            createHelpPanel ( "eyeCtl", "A" )        
                                  
        #squint_wide ctrl connect to the eyeWideJnt curves ( WideJnt BlendShape )
        cmds.connectAttr ( "eyeSquintHelpPanel." + pfx + "VPos", pfx+"upLidCrvBS." + pfx + "upLookUp_crv" )
        cmds.connectAttr ( "eyeSquintHelpPanel." + pfx + "VPos", pfx+"loLidCrvBS." + pfx + "loLookUp_crv" )
        
        cmds.connectAttr ( "eyeSquintHelpPanel." + pfx + "VNeg", pfx+"upLidCrvBS." + pfx + "upLookDn_crv" )
        cmds.connectAttr ( "eyeSquintHelpPanel." + pfx + "VNeg", pfx+"loLidCrvBS." + pfx + "loLookDn_crv" )  
        
        cmds.connectAttr ( "eyeSquintHelpPanel." + pfx + "HPos", pfx+"upLidCrvBS." + pfx + "upLookLeft_crv" )
        cmds.connectAttr ( "eyeSquintHelpPanel." + pfx + "HPos", pfx+"loLidCrvBS." + pfx + "loLookLeft_crv" )
        
        cmds.connectAttr ( "eyeSquintHelpPanel." + pfx + "HNeg", pfx+"upLidCrvBS." + pfx + "upLookRight_crv" )
        cmds.connectAttr ( "eyeSquintHelpPanel." + pfx + "HNeg", pfx+"loLidCrvBS." + pfx + "loLookRight_crv" )
helpPanelToEyeCrv ()
