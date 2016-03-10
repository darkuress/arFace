import maya.cmds as cmds

import fnmatch

#lipJotP input
cmds.setAttr (swivelTranYMult + '.input2', 2, 0 ,1)
swivel ty * input2 X = lipJotP ty
swivel ty * input2 Z = loLipJotX* rx

cmds.setAttr (swivelTranXMult + '.input2', 1, .3, 20)
swivel tx * 1 = lipJotP tx
swivel tx * 0.3 = loLipJotX* ry
swivel tx * 20 = lipJotP rz


#lipJotP input
cmds.setAttr(jawScaleDownMult+'.input2', .2,.5,.3)
swivel ty * 0.5 = jawSemi.sx 

upLO_crv upLHappy_crv upLSad_crv upLM_crv uplERollYZ_crv / upURoll_crv
# for E, happy, U, M...start with Capial Letter / ?? ??
import fnmatch
import maya.cmds as cmds 
def indiShapeCrvRig(name, posX, posY):
    #select upLip curves that need joints control ('upJawOpen_crv', 'upUDLR_crv'...)  
    upLCrv = 'upL'+ name + '_crv'
    loLCrv = upLCrv.replace('up', 'lo', 1)

    crvShape = cmds.listRelatives(upLCrv, c= 1, type = 'nurbsCurve')
    crvCVs = cmds.ls(upLCrv + '.cv[*]', fl = 1)
    cvNum = len(crvCVs) 
       
    lipCrvStartPos = cmds.xform (crvCVs[0], q= 1, ws = 1, t = 1)
    lipCrvEndPos = cmds.xform (crvCVs[cvNum-1], q= 1, ws = 1, t = 1)   
    nCrvPoc = cmds.shadingNode('pointOnCurveInfo', asUtility =True, n = 'cnt' + name + '_poc')
    cmds.connectAttr(crvShape[0]+'.worldSpace',  nCrvPoc + '.inputCurve')   
    cmds.setAttr(nCrvPoc + '.turnOnPercentage', 1)    
    cmds.setAttr(nCrvPoc + '.parameter', .5)    
    lipCrvMidPos = cmds.getAttr(nCrvPoc + '.position')    
    
    lipCrvStart = cmds.group (em = 1, n = name + 'Start_grp')
    cmds.xform(lipCrvStart, ws = 1, t = lipCrvStartPos)
    upRCorner = cmds.joint(n= 'upRCorner'+ name+'_jnt', p= lipCrvStartPos)
    cmds.select(lipCrvStart, r= 1)
    loRCorner = cmds.joint(n= 'loRCorner'+ name+'_jnt', p= lipCrvStartPos)  
    
    lipCrvMid = cmds.group (em = 1, n = name + 'Mid_grp') 
    cmds.xform(lipCrvMid, ws = 1, t = list(lipCrvMidPos[0])) 
    midUpJnt = cmds.joint(n = 'cntUp' + name + '_jnt', relative = True, p = [ 0, 0, 0]) 
    cmds.select(lipCrvMid, r= 1) 
    midLoJnt = cmds.joint(n = 'cntLo' + name + '_jnt', relative = True, p = [ 0, 0, 0])

    lipCrvEnd = cmds.group (em = 1, n = name + 'End_grp') 
    cmds.xform(lipCrvEnd, ws = 1, t = lipCrvEndPos) 
    upLCorner = cmds.joint(n= 'upLCorner' + name + '_jnt', relative = True, p = [ 0, 0, 0])
    cmds.select (lipCrvEnd, r = 1)
    loLCorner = cmds.joint(n= 'loLCorner' + name + '_jnt', relative = True, p = [ 0, 0, 0])  
    
    cmds.parent(lipCrvStart, lipCrvMid, lipCrvEnd, name+'Crv_indiGrp') 
    cmds.parent (indiGrp, 'lipCrv_grp')
    cmds.setAttr(indiGrp + '.tx', posX)
    cmds.setAttr(indiGrp + '.ty', posY)
    #skinning (cv skin weight input)
    cmds.skinCluster(upRCorner, midUpJnt, upLCorner, upLCrv, toSelectedBones = 1)  
    cmds.skinCluster(loRCorner, midLoJnt, loLCorner, loLCrv, toSelectedBones = 1)
        
        # skin weight number / blendShape mirror weight!!!!!!!!!!!!!!!!
    
indiShapeCrvRig('O', 0, 4) 







import maya.cmds as cmds 
def indiShapeCrvRig(name, posX, posY, typeAB):
    #select upLip curves that need joints control ('upJawOpen_crv', 'upUDLR_crv'...)  
    upLCrv = 'upL'+ name + '_crv'
    loLCrv = upLCrv.replace('up', 'lo', 1)
    upRCrv = 'upR'+ name + '_crv'
    loRCrv = upLCrv.replace('up', 'lo', 1)
    crvShape = cmds.listRelatives(upLCrv, c= 1, type = 'nurbsCurve')
    crvCVs = cmds.ls(upLCrv + '.cv[*]', fl = 1)
    cvNum = len(crvCVs) 
       
    lipCrvStartPos = cmds.xform (crvCVs[0], q= 1, ws = 1, t = 1)
    lipCrvEndPos = cmds.xform (crvCVs[cvNum-1], q= 1, ws = 1, t = 1)
    nCrvPoc = cmds.shadingNode('pointOnCurveInfo', asUtility =True, n = 'cnt' + name + '_poc')
    cmds.connectAttr(crvShape[0]+'.worldSpace',  nCrvPoc + '.inputCurve')   
    cmds.setAttr(nCrvPoc + '.turnOnPercentage', 1)    
    cmds.setAttr(nCrvPoc + '.parameter', .5)
    lipCrvMidPos = cmds.getAttr(nCrvPoc + '.position')
    
    lipCrvStart = cmds.group (em = 1, n = name + 'Start_grp')
    cmds.xform(lipCrvStart, ws = 1, t = lipCrvStartPos)
    rCorner = cmds.joint(n= 'rCorner'+ name+'_jnt', p= lipCrvStartPos) 
    
    uplipCrvMid = cmds.group (em = 1, n = 'up' + name + 'Mid_grp') 
    cmds.xform(uplipCrvMid, ws = 1, t = list(lipCrvMidPos[0])) 
    midUpJnt = cmds.joint(n = 'cntUp' + name + '_jnt', relative = True, p = [ 0, 0, 0])  

    lolipCrvMid = cmds.group (em = 1, n = 'lo' + name + 'Mid_grp') 
    cmds.xform(lolipCrvMid, ws = 1, t = list(lipCrvMidPos[0])) 
    midLoJnt = cmds.joint(n = 'cntLo' + name + '_jnt', relative = True, p = [ 0, 0, 0])

    lipCrvEnd = cmds.group (em = 1, n = name + 'End_grp') 
    cmds.xform(lipCrvEnd, ws = 1, t = lipCrvEndPos) 
    lCorner = cmds.joint(n= 'lCorner' + name + '_jnt', relative = True, p = [ 0, 0, 0])  
    
    crvList = cmds.listRelatives('crv_grp', allDescendents = 1, type = 'transform')
    if fnmatch.filter(crvList, '*%s*'% name):
        indiCrvs = fnmatch.filter(crvList, '*%s*'% name)
        indiGrp = cmds.group(lipCrvStart, uplipCrvMid, lolipCrvMid, lipCrvEnd, indiCrvs, n = name + '_indiGrp') 
        cmds.parent (indiGrp, 'lipCrv_grp')
        cmds.setAttr(indiGrp + '.tx', posX)
        cmds.setAttr(indiGrp + '.ty', posY)
        #skinning (cv skin weight input)
        cmds.skinCluster(rCorner, midUpJnt, lCorner, upLCrv, toSelectedBones = 1)  
        cmds.skinCluster(rCorner, midUpJnt, lCorner, upRCrv, toSelectedBones = 1)   
        cmds.skinCluster(rCorner, midLoJnt, lCorner, loLCrv, toSelectedBones = 1)
        cmds.skinCluster(rCorner, midLoJnt, lCorner, loRCrv, toSelectedBones = 1)
        
    # skin weight number / blendShape mirror weight!!!!!!!!!!!!!!!!

    if type == 'B':
                
        cornerMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = name +'_mult')
        dampMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = name + 'damp_mult')
        txAvg = cmds.shadingNode('plusMinusAverage', asUtility=True, n = name + 'TX_plus')  
        
        #?ty? ? ?? ????? inputX,Y?  ??? tx ? tz?  inputZ ? ??.
        txzPick = ['.' + myAttr ]
        cmds.connectAttr(midLoJnt+ '.ty', cornerMult+ '.input1X')  
        cmds.connectAttr(midLoJnt+ '.ty', cornerMult+ '.input1Y')  
        cmds.connectAttr(midLoJnt + txzPick, cornerMult+ '.input1Z') 
        cmds.setAttr(cornerMult + '.input2X', .1) #= lCorner jnts move inside(tx) as jaw open
        cmds.setAttr(cornerMult + '.input2Y', .1) #= rCorner jnts move inside(tx) as jaw open 
        cmds.setAttr(cornerMult + '.input2Z', -.3) #= corner jnts (tx or tz) go along as jaw moving tx

        cmds.connectAttr(cornerMult + '.outputX', txAvg + '.input3D[0].input3Dx')
        cmds.connectAttr(cornerMult + '.outputY', txAvg + '.input3D[0].input3Dy')
        cmds.connectAttr(cornerMult + '.outputZ', txAvg + '.input3D[1].input3Dx')
        cmds.connectAttr(cornerMult + '.outputZ', txAvg + '.input3D[1].input3Dy')
        cmds.connectAttr(txAvg + '.output3Dx', lCorner +  txzPick)
        cmds.connectAttr(txAvg + '.output3Dy', rCorner + txzPick)

        # lip corners translateY go along with jaw open
        cmds.connectAttr(midLoJnt+ '.ty', dampMult + '.input1X')  
        cmds.connectAttr(midLoJnt+ '.ty', dampMult + '.input1Y')  
        cmds.connectAttr(midLoJnt + txzPick, dampMult + '.input1Z') 

        cmds.setAttr(dampMult+ '.input2X', .05) #= ??? ??? ??? ?ty?
        cmds.setAttr(dampMult+ '.input2Y', .35) #= corner jnts ?ty? go along with jaw open
        cmds.setAttr(dampMult+ '.input2Z', .05) #=  ??? ??? ??? ?tx? or ?tz?

       
        cmds.connectAttr(dampMult + '.outputX',  midUpJnt+'.ty')
        cmds.connectAttr(dampMult + '.outputY',  lCorner+'.ty')
        cmds.connectAttr(dampMult + '.outputY',  rCorner+'.ty')
        cmds.connectAttr(dampMult + '.outputZ',  midUpJnt + txzPick)
        
indiCrvSetup('JawOpen', -0, 2)














import maya.cmds as cmds 
def indiCrvSetup(name, posX, posY, typeAB):
    #select upLip curves that need joints control ('upJawOpen_crv', 'upUDLR_crv'...)  
    crv = 'up'+ name + '_crv'
    loCrv = crv.replace('up', 'lo', 1)
    crvShape = cmds.listRelatives(crv, c= 1, type = 'nurbsCurve')
    crvCVs = cmds.ls(crv + '.cv[*]', fl = 1)
    cvNum = len(crvCVs) 
       
    lipCrvStartPos = cmds.xform (crvCVs[0], q= 1, ws = 1, t = 1)
    lipCrvEndPos = cmds.xform (crvCVs[cvNum-1], q= 1, ws = 1, t = 1)
    nCrvPoc = cmds.shadingNode('pointOnCurveInfo', asUtility =True, n = 'cnt' + name + '_poc')
    cmds.connectAttr(crvShape[0]+'.worldSpace',  nCrvPoc + '.inputCurve')   
    cmds.setAttr(nCrvPoc + '.turnOnPercentage', 1)    
    cmds.setAttr(nCrvPoc + '.parameter', .5)
    lipCrvMidPos = cmds.getAttr(nCrvPoc + '.position')
    
    lipCrvStart = cmds.group (em = 1, n = name + 'Start_grp')
    cmds.xform(lipCrvStart, ws = 1, t = lipCrvStartPos)
    rCorner = cmds.joint(n= 'rCorner'+ name+'_jnt', p= lipCrvStartPos) 
    
    uplipCrvMid = cmds.group (em = 1, n = 'up' + name + 'Mid_grp') 
    cmds.xform(uplipCrvMid, ws = 1, t = list(lipCrvMidPos[0])) 
    midUpJnt = cmds.joint(n = 'cntUp' + name + '_jnt', relative = True, p = [ 0, 0, 0])  

    lolipCrvMid = cmds.group (em = 1, n = 'lo' + name + 'Mid_grp') 
    cmds.xform(lolipCrvMid, ws = 1, t = list(lipCrvMidPos[0])) 
    midLoJnt = cmds.joint(n = 'cntLo' + name + '_jnt', relative = True, p = [ 0, 0, 0])

    lipCrvEnd = cmds.group (em = 1, n = name + 'End_grp') 
    cmds.xform(lipCrvEnd, ws = 1, t = lipCrvEndPos) 
    lCorner = cmds.joint(n= 'lCorner' + name + '_jnt', relative = True, p = [ 0, 0, 0])  
    crvList = cmds.listRelatives('crv_grp', allDescendents = 1, type = 'transform')
    if objExists(name +) in crvList:
        indiCrvs = fnmatch.filter(crvList, '*%s*'% name)
        indiGrp = cmds.group(lipCrvStart, uplipCrvMid, lolipCrvMid, lipCrvEnd, indiCrvs, n = name + '_indiGrp') 
        cmds.parent (indiGrp, 'lipCrv_grp')
        cmds.setAttr(indiGrp + '.tx', posX)
        cmds.setAttr(indiGrp + '.ty', posY)
        #skinning (cv skin weight input)
        cmds.skinCluster(rCorner, midUpJnt, lCorner, crv, toSelectedBones = 1)    
        cmds.skinCluster(rCorner, midLoJnt, lCorner, loCrv, toSelectedBones = 1)

    if type == 'B':
                
        cornerMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = name +'_mult')
        dampMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = name + 'damp_mult')
        txAvg = cmds.shadingNode('plusMinusAverage', asUtility=True, n = name + 'TX_plus')  
        
        #?ty? ? ?? ????? inputX,Y?  ??? tx ? tz?  inputZ ? ??.
        txzPick = ['.' + myAttr ]
        cmds.connectAttr(midLoJnt+ '.ty', cornerMult+ '.input1X')  
        cmds.connectAttr(midLoJnt+ '.ty', cornerMult+ '.input1Y')  
        cmds.connectAttr(midLoJnt + txzPick, cornerMult+ '.input1Z') 
        cmds.setAttr(cornerMult + '.input2X', .1) #= lCorner jnts move inside(tx) as jaw open
        cmds.setAttr(cornerMult + '.input2Y', .1) #= rCorner jnts move inside(tx) as jaw open 
        cmds.setAttr(cornerMult + '.input2Z', -.3) #= corner jnts (tx or tz) go along as jaw moving tx

        cmds.connectAttr(cornerMult + '.outputX', txAvg + '.input3D[0].input3Dx')
        cmds.connectAttr(cornerMult + '.outputY', txAvg + '.input3D[0].input3Dy')
        cmds.connectAttr(cornerMult + '.outputZ', txAvg + '.input3D[1].input3Dx')
        cmds.connectAttr(cornerMult + '.outputZ', txAvg + '.input3D[1].input3Dy')
        cmds.connectAttr(txAvg + '.output3Dx', lCorner +  txzPick)
        cmds.connectAttr(txAvg + '.output3Dy', rCorner + txzPick)

        # lip corners translateY go along with jaw open
        cmds.connectAttr(midLoJnt+ '.ty', dampMult + '.input1X')  
        cmds.connectAttr(midLoJnt+ '.ty', dampMult + '.input1Y')  
        cmds.connectAttr(midLoJnt + txzPick, dampMult + '.input1Z') 

        cmds.setAttr(dampMult+ '.input2X', .05) #= ??? ??? ??? ?ty?
        cmds.setAttr(dampMult+ '.input2Y', .35) #= corner jnts ?ty? go along with jaw open
        cmds.setAttr(dampMult+ '.input2Z', .05) #=  ??? ??? ??? ?tx? or ?tz?

       
        cmds.connectAttr(dampMult + '.outputX',  midUpJnt+'.ty')
        cmds.connectAttr(dampMult + '.outputY',  lCorner+'.ty')
        cmds.connectAttr(dampMult + '.outputY',  rCorner+'.ty')
        cmds.connectAttr(dampMult + '.outputZ',  midUpJnt + txzPick)
        
indiCrvSetup('JawOpen', -0, 2)
