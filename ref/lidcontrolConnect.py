import maya.cmds as cmds 
def lidcontrolConnect (): 
    '''??? ???? lid Ctrl box ? x  ??-1~1? ??? 0~1?? lidCtl_crv? ???? ????. 
    Blink, Squint, Wide ?????'''
    LRUpLow = ["l_up", "r_up", "l_lo", "r_lo" ]
    for pos in LRUpLow:
                
        ctlCrvCv = cmds.ls ( pos + 'Ctl_crv.cv[*]', fl =True )
        print ctlCrvCv
        cvNum = len ( ctlCrvCv )
    
        # lidCtl drive the center controlPoints on ctlCrv
        if not (pos + "Center") and (pos +"InCorner") and (pos + "OutCorner"):
            print "create lid main controllers"
        else :
            
            cntAddD = cmds.shadingNode ( 'addDoubleLinear', asUtility=True, n= pos + "Cnt_AddD" )            
            cmds.connectAttr ( pos + "InCorner.ty" , ctlCrvCv[0] + ".yValue" )
            cmds.connectAttr ( pos + "InCorner.ty" , ctlCrvCv[1] + ".yValue" )
            cmds.setAttr ( ctlCrvCv[0] + ".xValue" , lock = True )     
            cmds.setAttr ( ctlCrvCv[1] + ".xValue" , lock = True ) 
            cmds.connectAttr ( pos + "Center.ty" , ctlCrvCv[2] + ".yValue" )  
            # center control X match to center point (lidCtl_crv)
            
            if "l_" in pos :
                cmds.connectAttr ( pos + "Center.tx", cntAddD + ".input1" )
                cmds.setAttr (cntAddD + ".input2", 0.5 ) 
                cmds.connectAttr ( cntAddD + ".output" , ctlCrvCv[2] + ".xValue" )
                
            if "r_" in pos :
                cntMult = cmds.shadingNode ( 'multiplyDivide', asUtility=True, n = pos +'Cnt_mult' )
                cmds.connectAttr ( pos + "Center.tx" , cntMult + ".input1X" ) 
                cmds.setAttr ( cntMult + ".input2X", -1 )
                cmds.connectAttr ( cntMult + ".outputX", cntAddD + ".input1" )
                cmds.setAttr (cntAddD + ".input2", 0.5 ) 
                cmds.connectAttr ( cntAddD + ".output" , ctlCrvCv[2] + ".xValue" )            
             
            cmds.connectAttr ( pos + "OutCorner.ty" , ctlCrvCv[3] + ".yValue" )
            cmds.connectAttr ( pos + "OutCorner.ty" , ctlCrvCv[4] + ".yValue" )
            cmds.setAttr ( ctlCrvCv[3] + ".xValue", lock = True  )  
            cmds.setAttr ( ctlCrvCv[4] + ".xValue", lock = True  )   
    
        detailPCtls = cmds.ls ( pos + "Detail*P", type = 'transform')
        print detailPCtls 
        details = []
        for mom in detailPCtls :
            kid= cmds.listRelatives ( mom, c = True, type = 'transform' )
            details.append(kid[0])
                    
        ctlNum = len (details) 
            
        for i in range (0, ctlNum):
            # POC on ctlCrv drive detail control parent  
            cntRemoveX = cmds.shadingNode ( 'addDoubleLinear', asUtility=True, n= pos +"Cnt"+ str(i+1)+"RemoveX" )
            momMult = cmds.shadingNode ( 'multiplyDivide', asUtility=True, n = pos +'Mom'+ str(i+1)+'_mult' )
            cmds.connectAttr ( pos + "CtlPoc0" +str(i+1) +".positionY", detailPCtls[i] + ".ty" )
            #Xvalue match between POC and CtrlP
            cmds.connectAttr ( pos + "CtlPoc0" +str(i+1) +".positionX", momMult + ".input1X" )        
            cmds.connectAttr ( momMult + ".outputX", cntRemoveX + ".input1" )
            if "l_" in pos :
                cmds.setAttr ( momMult + ".input2X", 2)
                cmds.setAttr (  cntRemoveX  + ".input2", -1) 
                cmds.connectAttr ( cntRemoveX +".output", detailPCtls[i] + ".tx" )
            if "r_" in pos :
                cmds.setAttr ( momMult + ".input2X", -2)
                cmds.setAttr (  cntRemoveX  + ".input2", 1)              
                cmds.connectAttr ( cntRemoveX +".output", detailPCtls[ctlNum-i-1] + ".tx" )
                
            # detail control drive the joint ( add to the +-Average node)
            cmds.connectAttr ( details[i] + ".tx", pos +"Lid"+ str(i+1)+'_plusX'+".input1D[6]" ) 
            cmds.connectAttr ( details[i] + ".ty", pos +"Lid"+ str(i+1)+'_plusY'+".input1D[4]" )