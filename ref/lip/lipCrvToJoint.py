# panel name change : create lipCtrlRTipFloat, lipCtrlLTipFloat!!!
# see if 3 ctrls are enough for lip (delete lipUpCtrlLA... or not) 
import maya.cmds as cmds
def lipCrvToJoint(upLow):
    #main lipCtrls connect with LipCtl_crv    
    mainCtrlP = cmds.listRelatives(cmds.ls('lip*Ctr*Float', fl=True, type ='transform'), c =1, type = 'transform')
    lipCtrls = [x for x in mainCtrlP if upLow.title() in x]
    lipCtrls.reverse()
    lipCtrls.insert(0, mainCtrlP[1])
    lipCtrls.insert(len(lipCtrls), mainCtrlP[0])
    
    index = 0
    for n in lipCtrls:
        # curve cv xValue zero out
        zeroX = cmds.shadingNode('addDoubleLinear', asUtility=True, n = upLow + lipCtrls[index].split('Ctrl', 1)[1] + '_xAdd') 
        cvTx = cmds.getAttr(upLow + 'LipCtl_crv.controlPoints['+str(index)+'].xValue')
        cmds.connectAttr(n+'.tx', zeroX + '.input1')
        cmds.setAttr (zeroX + '.input2' , cvTx) 
        cmds.connectAttr(zeroX + '.output', upLow + 'LipCtl_crv.controlPoints['+str(index)+'].xValue')
        # main ctrl's TY drive the ctrl curve point yValue
        cmds.connectAttr(n+'.ty' , upLow + 'LipCtl_crv.controlPoints['+str(index)+'].yValue')
        index = index +1  
    
    # curve's Poc drive the joint
    lipJots= cmds.ls(upLow + 'LipJotX*', fl=True, type ='transform')
    jotNum = len (lipJots)
    
    if upLow == 'up':
        min = 0
        max = jotNum
    elif upLow == 'lo':  
        jotNum = len (lipJots) + 2 
        min = 1
        max = jotNum-1
    
    for i in range(min, max):  
    
        jotXMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = upLow + 'lipJotX' + str(i)+'_mult')
        jotYMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = upLow + 'lipJotY' + str(i)+'_mult')
        plusTXAvg = cmds.shadingNode('plusMinusAverage', asUtility=True, n = upLow + 'TX' + str(i) +'_plus')    
        plusTYAvg = cmds.shadingNode('plusMinusAverage', asUtility=True, n = upLow + 'TY' + str(i)+'_plus')
      
        #blinkRemap = cmds.shadingNode('remapValue', asUtility=True, n = jnt.split('Blink', 1)[0] + str(i)+'_remap')
        #blinkGap = cmds.shadingNode('addDoubleLinear', asUtility=True, n = jnt.split('LidBlink', 1)[0] + 'BlinkGap'+str(i)+'_yAdd')
                        
        poc = upLow +'LipCrv' + str(i) + '_poc'
        initialX = cmds.getAttr(poc + '.positionX')
        
        ctlPoc = upLow +'LipCtl' + str(i) + '_poc'
        initialCtlX = cmds.getAttr(ctlPoc + '.positionX')            
        
        #TranslateX add up for  
        #1. curve translateX add up for LipJotX
        cmds.setAttr(plusTXAvg + '.operation', 1) 
        cmds.connectAttr(poc + '.positionX', plusTXAvg + '.input3D[0].input3Dx') 
        cmds.setAttr (plusTXAvg + '.input3D[1].input3Dx', -initialX) 
        cmds.connectAttr(plusTXAvg + '.output3Dx', jotXMult + '.input1X') 
        cmds.setAttr(jotXMult + '.input2X', 30)   
        cmds.connectAttr(jotXMult + '.outputX', upLow + 'LipJotX'+str(i)+'.ry') 
        
        #2. LipCtlCrv Poc.positionX + LipDetail.tx for LipJotY 
        cmds.connectAttr(ctlPoc + '.positionX', plusTXAvg + '.input3D[0].input3Dy')  
        cmds.setAttr(plusTXAvg + '.input3D[1].input3Dy', -initialCtlX)  
        cmds.connectAttr(upLow + 'LipDetail'+ str(i)+'.tx', plusTXAvg + '.input3D[2].input3Dy')  
        cmds.connectAttr(plusTXAvg + '.output3Dy', jotYMult + '.input1Y')          
        cmds.setAttr(jotYMult + '.input2Y', 30)   
        cmds.connectAttr(jotYMult + '.outputY', upLow+'LipJotY'+str(i)+'.ry') 
        
        if i==0 or i==jotNum-1:
            zeroTip = cmds.shadingNode('addDoubleLinear', asUtility=True, n = 'zeroTip' + str(i) + '_plus')
            momTY = cmds.getAttr(upLow + 'LipDetailP' + str(i) +'.ty')
            cmds.connectAttr(ctlPoc + '.positionY', zeroTip + '.input1' )
            cmds.setAttr(zeroTip + '.input2', momTY)
            cmds.connectAttr(zeroTip + '.output', upLow + 'LipDetailP' +str(i) + '.ty')
            
        else:
            #3. LipCtl_crv connect with lipDetailP (lipDetailCtrl parents)
            cmds.connectAttr(ctlPoc + '.positionY', upLow + 'LipDetailP' +str(i) + '.ty')
        
        #TranslateY add up
        #1. curve translateY add up 
        cmds.setAttr(plusTYAvg + '.operation', 1)
        cmds.connectAttr(poc + '.positionY', plusTYAvg + '.input1D[0]')
        cmds.connectAttr(ctlPoc + '.positionY', plusTYAvg + '.input1D[1]') 
        cmds.connectAttr(upLow + 'LipDetail'+ str(i) + '.ty', plusTYAvg + '.input1D[2]')
    
        #connect translateY plusAvg to joint rotateX Mult
        
        cmds.connectAttr(plusTYAvg + '.output1D', jotXMult + '.input1Y')  
        cmds.setAttr(jotXMult + '.input2Y', -30) 
        cmds.connectAttr(jotXMult + '.outputY', upLow + 'LipJotX'+ str(i) + '.rx')  
        
        cmds.connectAttr(poc + '.positionZ', jotXMult + '.input1Z')  
        cmds.setAttr(jotXMult + '.input2Z', 10) 
        cmds.connectAttr(jotXMult + '.outputZ', upLow + 'LipJotX'+ str(i) + '.tz')   

