def createLipJoint( upLow, JawRigPos, lipYPos, poc, lipJotGrp, i):
    

    lipJotX  = cmds.group( n = upLow + 'LipJotX' + str(i), em =True, parent = lipJotGrp ) 
    lipJotZ  = cmds.group( n = upLow +' LipJotZ' + str(i), em =True, parent = lipJotX ) 
   
    lipJotY  = cmds.group( n = upLow +'LipJotY' + str(i), em =True, parent = lipJotZ )     
    lipJot = cmds.group( n = upLow +'LipJot' + str(i), em =True, parent = lipJotY )
    lipRollJotT = cmds.group( n = upLow +'LipRollJotT' + str(i), em =True, parent = lipJot )
    cmds.setAttr ( lipJotY + ".tz", lipYPos[2] )
     
    #lip joint placement on the curve with verts tx        
    lipRollJotP = cmds.group( n =upLow + 'LipRollJotP' + str(i), em =True, p = lipRollJotT ) 
    pocPosX = cmds.getAttr ( poc + '.positionX')
    pocPosY = cmds.getAttr ( poc + '.positionY')
    pocPosZ = cmds.getAttr ( poc + '.positionZ')
    
    cmds.xform ( lipRollJotP, ws = True, t = [ pocPosX, pocPosY, pocPosZ] ) 

    lipRollJot = cmds.joint(n = upLow + 'LipRollJot' + str(i) + '_jnt', relative = True, p = [ 0, 0, 0] ) 


    
    
def createDetailCtl( updn, i ):

    detailCtlP = cmds.group ( em =True, n = updn  + 'LipDetailP'+ str(i) )
    detailCtl = cmds.circle ( n = updn  + 'LipDetail' + str(i), ch=False, o =True, nr = ( 0, 0, 1), r = 0.05  )
    cmds.parent(detailCtl[0], detailCtlP)
    cmds.setAttr (detailCtl[0]+"Shape.overrideEnabled", 1 )
    cmds.setAttr( detailCtl[0]+"Shape.overrideColor", 20 )
    cmds.setAttr (detailCtl[0]+'.translate', 0,0,0 )
    cmds.transformLimits ( detailCtl[0], tx = ( -.5, .5), etx=( True, True) )
    cmds.transformLimits ( detailCtl[0], ty = ( -.5, .5), ety=( True, True) )
    attTemp = ['scaleX','scaleY','scaleZ', 'rotateX','rotateY','rotateZ', 'tz', 'visibility' ]  
    for y in attTemp:
        cmds.setAttr (detailCtl[0] +"."+ y, lock = True, keyable = False, channelBox =False) 







placefaceRig()


def placefaceRig():
    ''' after place the face locators'''

    headSkelPos = cmds.xform( 'headSkelPos', t = True, q = True, ws = True)
    JawRigPos = cmds.xform( 'JawRigPos', t = True, q = True, ws = True)
    lEyePos = cmds.xform( 'lEyePos', t = True, q = True, ws = True)
    cheekPos = cmds.xform( 'cheekPos', t = True, q = True, ws = True)
    cheekRot = cmds.xform( 'cheekPos', ro = True, q = True, ws = True)
    squintPuffPos = cmds.xform( 'squintPuffPos', t = True, q = True, ws = True)
    squintPuffRot = cmds.xform( 'squintPuffPos', ro = True, q = True, ws = True)
    lowCheekPos = cmds.xform( 'lowCheekPos', t = True, q = True, ws = True)
    LEarPos = cmds.xform( 'lEarPos', t = True, q = True, ws = True)
    nosePos = cmds.xform( 'nosePos', t = True, q = True, ws = True)
    
    faceMain = cmds.group (em =1, n = 'faceMain' )    
    clsGroup = cmds.group (em =1, n = 'cls_grp', p = faceMain )
    crvGroup = cmds.group (em =1, n = 'crv_grp', p = faceMain )
    faceGeoGroup = cmds.group (em =1, n = 'faceGeo_grp', p = faceMain )
    helpPanel = cmds.group (em =1, n = 'helpPanel_grp', p = faceMain )
    spn = cmds.group (em =1, n = 'spn', p = faceMain )
    headSkel = cmds.group (em =1, n = 'headSkel', p = spn )
    cmds.xform ( headSkel, ws = 1, t = headSkelPos )
    #jawRig hierarchy
    jawRig = cmds.group (em =1, n = 'jawRig', p = headSkel )
    cmds.xform ( jawRig, ws = 1, t = JawRigPos )
    jaw = cmds.group (em =1, n = 'jaw', p = jawRig )
    jawSemiAdd = cmds.group ( n = 'jawSemiAdd', em =True, parent = 'jaw' )     
    jawSemi = cmds.group ( n = 'jawSemi', em =True, parent = 'jaw' ) 
    cmds.setAttr ( jawSemi + ".translate", 0,0,0 )
    jawClose = cmds.joint(n = 'jawClose_jnt', relative = True, p = [ 0, 0, 0] )        
    jotStable = cmds.group ( n = 'lipJotStable', em =True, parent = 'jaw' ) 
    lipJotP = cmds.group( n = 'lipJotP', em =True, parent = jotStable )    
    #eyeRig hierarchy
    eyeRig = cmds.group (em =1, n = 'eyeRig', p = headSkel )
    cmds.xform ( eyeRig, ws = 1, t =( 0, lEyePos[1],lEyePos[2] ) )
    eyeRigP = cmds.group (em =1, n = 'eyeRigP', p = eyeRig )
    eyeTR = cmds.group (em =1, n = 'eyeTR', p = eyeRigP )
    ffdSquachLattice = cmds.group (em =1, n = 'ffdSquachLattice', p = eyeRigP )
    browRig = cmds.group (em =1, n = 'browRig', p = headSkel )
    bodyHeadP = cmds.group (em =1, n = 'bodyHeadTRSP', p = headSkel )
    cmds.xform ( bodyHeadP, ws = 1, t = headSkelPos )    
    bodyHead = cmds.group (em =1, n = 'bodyHeadTRS', p = bodyHeadP )
    cmds.xform ( bodyHead, ws = 1, t = headSkelPos )    
    
    supportRig = cmds.group (em =1, n = 'supportRig', p = faceMain )
    
    lEarP = cmds.group (em =1, n = 'l_ear_grp', p = supportRig )
    cmds.xform ( lEarP, ws = 1, t = LEarPos )
    rEarP = cmds.group (em =1, n = 'r_ear_grp', p = supportRig )
    cmds.xform ( rEarP, ws = 1, t = (-LEarPos[0], LEarPos[1], LEarPos[2]) )
    noseRig = cmds.group (em =1, n = 'noseRig', p = supportRig )
    cmds.xform ( noseRig, ws = 1, t = nosePos )
    lCheekGrp = cmds.group (em =1, n = 'l_cheek_grp', p = supportRig )
    cmds.xform ( lCheekGrp, ws = 1, t = cheekPos, ro = cheekRot )
    rCheekGrp = cmds.group (em =1, n = 'r_cheek_grp', p = supportRig )
    cmds.xform ( rCheekGrp, ws = 1, t = (-cheekPos[0], cheekPos[1], cheekPos[2]), ro = (cheekRot[0],cheekRot[1],-cheekRot[2]) )
    lSquintPuffGrp = cmds.group (em =1, n = 'l_squintPuff_grp', p = supportRig )
    cmds.xform ( lSquintPuffGrp, ws = 1, t = squintPuffPos, ro = squintPuffRot )
    rSquintPuffGrp = cmds.group (em =1, n = 'r_squintPuff_grp', p = supportRig )
    cmds.xform ( rSquintPuffGrp, ws = 1, t = (-squintPuffPos[0], squintPuffPos[1], squintPuffPos[2]), ro = (squintPuffRot[0],squintPuffRot[1],-squintPuffRot[2]))
    lLowCheek = cmds.group (em =1, n = 'l_lowCheek_grp', p = supportRig ) 
    cmds.xform ( lLowCheek, ws = 1, t = lowCheekPos )
    rLowCheek = cmds.group (em =1, n = 'r_lowCheek_grp', p = supportRig ) 
    cmds.xform ( rLowCheek, ws = 1, t = (-lowCheekPos[0], lowCheekPos[1], lowCheekPos[2]) ) 




bridgeJoints()

def bridgeJoints():    
    JawRigPos = cmds.xform( 'JawRigPos', t = True, q = True, ws = True)
    # create cheek joint - check the cheek/squintPush group and angle
    lEarP = cmds.group ( n = 'l_earP', em =True, p = "l_ear_grp" )
    cmds.xform (lEarP, relative = True, t = [ 0, 0, 0] )
    lEarJnt = cmds.joint(n = 'l_ear_jnt', relative = True, p = [ 0, 0, 0] ) 
    rEarP = cmds.group ( n = 'r_earP', em =True, p = "r_ear_grp" )
    cmds.xform (rEarP, relative = True, t = [ 0, 0, 0]  )
    rEarJnt = cmds.joint(n = 'r_ear_jnt', relative = True, p = [ 0, 0, 0] ) 
    
    noseP = cmds.group ( n = 'noseP', em =True, p = "noseRig" )
    cmds.xform (noseP, relative = True, t = [ 0, 0, 0] )
    noseJnt = cmds.joint(n = 'nose_jnt', relative = True, p = [ 0, 0, 0] ) 
    
    lCheekP = cmds.group ( n = 'l_cheekP', em =True, p = "l_cheek_grp" )
    cmds.xform (lCheekP, relative = True, t = [ 0, 0, 0] )
    lCheekJnt = cmds.joint(n = 'l_cheek_jnt', relative = True, p = [ 0, 0, 0] ) 
    cmds.xform ( lCheekP ws = 1, rp = JawRigPos  )    
    rCheekP = cmds.group ( n = 'r_cheekP', em =True, p = "r_cheek_grp" )
    cmds.xform (rCheekP, relative = True, t = [ 0, 0, 0] )
    rCheekJnt = cmds.joint(n = 'r_cheek_jnt', relative = True, p = [ 0, 0, 0] )
    cmds.xform ( rCheekP, ws = 1, rp = JawRigPos  )
    
    lSqiuntPuff = cmds.group ( n = 'l_squintPuffP', em =True, p = "l_squintPuff_grp" )
    cmds.xform (lSqiuntPuff, relative = True, t = [ 0, 0, 0] )
    lSqiuntPuffJnt = cmds.joint(n = 'l_squintPuff_jnt', relative = True, p = [ 0, 0, 0] ) 
    rSquintPuff = cmds.group ( n = 'r_squintPuffP', em =True, p = "r_squintPuff_grp" )
    cmds.xform (rSquintPuff, relative = True, t = [ 0, 0, 0])
    rSqiuntPuffJnt = cmds.joint(n = 'r_squintPuff_jnt', relative = True, p = [ 0, 0, 0] ) 
    
    lLowCheek = cmds.group ( n = 'l_lowCheekP', em =True, p = "l_lowCheek_grp" )
    cmds.xform (lLowCheek, relative = True, t = [ 0, 0, 0] )
    lLowCheekJnt = cmds.joint(n = 'l_lowCheek_jnt', relative = True, p = [ 0, 0, 0] )
    cmds.xform ( lLowCheek, ws = 1, rp = JawRigPos  )
    
    rLowCheek = cmds.group ( n = 'r_lowCheekP', em =True, p = "r_lowCheek_grp" )
    cmds.xform (rLowCheek,  relative = True, t = [ 0, 0, 0]  )
    rLowCheekJnt = cmds.joint(n = 'r_lowCheek_jnt', relative = True, p = [ 0, 0, 0] ) 
    cmds.xform ( rLowCheek, ws = 1, rp = JawRigPos  )
















import maya.cmds as cmds
def mouthJoint( upLow ): 
    verts = cmds.ls( os = True, fl = True)  
    vNum = len (verts) + 2       
    lipEPos = cmds.xform( 'lipEPos', t = True, q = True, ws = True) 
    lipNPos = cmds.xform( 'lipNPos', t = True, q = True, ws = True) 
    lipSPos = cmds.xform( 'lipSPos', t = True, q = True, ws = True) 
    lipYPos = cmds.xform( 'lipYPos', t = True, q = True, r = True) 
    JawRigPos = cmds.xform( 'JawRigPos', t = True, q = True, ws = True) 
    cheekPos = cmds.xform( 'cheekPos', t = True, q = True, ws = True)
    squintPuffPos = cmds.xform( 'squintPuffPos', t = True, q = True, ws = True)
    lowCheekPos = cmds.xform( 'lowCheekPos', t = True, q = True, ws = True)
    
    if upLow == "up":
        lipCntPos = lipNPos 
            
    elif upLow == "lo":
        lipCntPos = lipSPos
            
    increment = 1.0/(vNum-1) 
    # create lip joint guide curve
    tempCrv = cmds.curve ( d= 3, ep= [(-lipEPos[0], lipEPos[1], lipEPos[2]), ( lipCntPos ), (lipEPos)] ) 
    guideCrv = cmds.rename ( tempCrv, upLow + "Guide_crv" )
    guideCrvShape = cmds.listRelatives ( guideCrv, c = True ) 
    cmds.rebuildCurve ( guideCrv, d = 3, rebuildType = 0, keepRange = 0) 
    
    # final lip shape ctrl curve
    if not cmds.objExists('lipCrv_grp'):
        lipCrvGrp = cmds.group ( n = 'lipCrv_grp', em =True, p = 'faceMain|crv_grp' )    
    lipCrvP = cmds.group ( n = upLow +'LipCrvP', em =True, p = 'faceMain|crv_grp|lipCrv_grp') 
    templipCrv = cmds.curve ( d = 3, p =([0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0])) 
    cmds.rebuildCurve ( rt = 0, d = 3, kr = 0, s = 4)    
    lipCrv = cmds.rename (templipCrv, upLow +'Lip_crv')
    lipCrvShape = cmds.listRelatives ( lipCrv, c = True )
    cmds.parent ( lipCrv, lipCrvP )
    # lipTarget curve shape
    jawOpenCrv = cmds.duplicate ( lipCrv, n= upLow +'JawOpen_crv')
    lWideCrv = cmds.duplicate ( lipCrv, n= upLow +'LWide_crv')
    rWideCrv = cmds.duplicate ( lWideCrv, n= upLow +'RWide_crv')
    rCrvTolCrv( lWideCrv[0], rWideCrv[0], 'Wide')
    cmds.hide(rWideCrv[0])
    lECrv = cmds.duplicate ( lipCrv, n= upLow +'LE_crv')
    rECrv = cmds.duplicate ( lECrv, n= upLow +'RE_crv')  
    rCrvTolCrv( lECrv, rECrv, 'E')
    cmds.hide(rECrv[0])
    lOCrv = cmds.duplicate ( lipCrv, n= upLow +'LO_crv') 
    rOCrv = cmds.duplicate ( lOCrv, n= upLow +'RO_crv')
    rCrvTolCrv( lOCrv[0], rOCrv[0], 'O')
    cmds.hide(rOCrv[0])
    lUCrv = cmds.duplicate ( lipCrv, n= upLow +'LU_crv')
    rUCrv = cmds.duplicate ( lUCrv, n= upLow +'RU_crv') 
    rCrvTolCrv( lUCrv[0], rUCrv[0], 'U') 
    cmds.hide(rUCrv[0])
    lHappyCrv = cmds.duplicate ( lipCrv, n= upLow +'LHappy_crv') 
    rHappyCrv = cmds.duplicate ( lHappyCrv, n= upLow +'RHappy_crv')
    rCrvTolCrv( lHappyCrv[0], rHappyCrv[0], 'Happy')
    cmds.hide(rHappyCrv[0])
    lSadCrv = cmds.duplicate ( lipCrv, n= upLow +'LSad_crv') 
    rSadCrv = cmds.duplicate ( lSadCrv, n= upLow +'RSad_crv') 
    rCrvTolCrv( lSadCrv[0], rSadCrv[0], 'Sad')
    cmds.hide(rSadCrv[0])
    lMCrv = cmds.duplicate ( lipCrv, n= upLow +'LM_crv') 
    rMCrv = cmds.duplicate ( lMCrv, n= upLow +'RM_crv')
    rCrvTolCrv( lMCrv[0], rMCrv[0], 'M')
    cmds.hide(rMCrv[0])
    lipCrvBS = cmds.blendShape ( jawOpenCrv[0], lWideCrv[0],rWideCrv[0],lECrv[0],rECrv[0],lOCrv[0],rOCrv[0],lUCrv[0],rUCrv[0],lHappyCrv[0],rHappyCrv[0],lSadCrv[0],rSadCrv[0],lMCrv[0],rMCrv[0], lipCrv, n =upLow + 'LipCrvBS')
    cmds.blendShape( lipCrvBS[0], edit=True, w=[(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1), (14, 1)])   
    

    # lip curve for LipJotX translateYZ
    tempTylipCrv = cmds.curve ( d = 3, p =([0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0])) 
    cmds.rebuildCurve ( rt = 0, d = 3, kr = 0, s = 4 )    
    tyLipCrv = cmds.rename (tempTylipCrv, upLow +'LipTY_crv' )  
    tylipCrvShape = cmds.listRelatives ( tyLipCrv, c = True )  
    cmds.parent ( tyLipCrv, lipCrvP )
    # lip Swivel crv Target for LipJotX tx,ty
    UDLRCrv = cmds.duplicate ( tyLipCrv, n= upLow +'UDLR_crv') 
    jawOpenTyCrv = cmds.duplicate ( tyLipCrv, n= upLow +'JawOpenTY_crv') #lipJotX translateY when jawOpen 
    lipTYBS = cmds.blendShape ( UDLRCrv[0], jawOpenTyCrv[0], tyLipCrv, n =upLow + 'LipTYBS')
    cmds.blendShape( lipTYBS[0], edit=True, w=[(0, 1), (1, 1)]) 
        
    # lip controller curve shape ( different number of points (4), so can not be target of the blendShape)      
    templipCtlCrv = cmds.curve ( d = 3, p =([0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0])) 
    cmds.rebuildCurve ( rt = 0, d = 3, kr = 0, s = 2)   
    lipCtlCrv = cmds.rename ( templipCtlCrv, upLow +'LipCtl_crv')
    lipCtlCrvShape = cmds.listRelatives ( lipCtlCrv, c = True ) 
    cmds.parent (lipCtlCrv, lipCrvP)   

    # lip Roll control curve shape ( different number of points (4), so can not be target of the blendShape)      
    tempRollCrv = cmds.curve ( d = 3, p =([0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0])) 
    cmds.rebuildCurve ( rt = 0, d = 3, kr = 0, s = 2)   
    lipRollCrv = cmds.rename ( tempRollCrv, upLow +'LipRoll_crv') 
    lipRollCrvShape = cmds.listRelatives ( lipRollCrv, c = True ) 
    cmds.parent ( lipRollCrv, lipCrvP )
    #targets for lip Roll crv
    rollCtlCrv = cmds.duplicate ( lipRollCrv, n= upLow +'RollCtl_crv') 
    lURollCrv = cmds.duplicate ( lipRollCrv, n= upLow +'LURoll_crv')
    rURollCrv = cmds.duplicate ( lURollCrv, n= upLow +'RURoll_crv') 
    rCrvTolCrv( lURollCrv[0], rURollCrv[0], 'U')
    cmds.hide(rURollCrv[0])
    lORollCrv = cmds.duplicate ( lipRollCrv, n= upLow +'LORoll_crv')
    rORollCrv = cmds.duplicate ( lORollCrv, n= upLow +'RORoll_crv') 
    rCrvTolCrv( lORollCrv[0], rORollCrv[0], 'O')
    cmds.hide(rORollCrv[0])
    lShRollCrv = cmds.duplicate ( lipRollCrv, n= upLow +'LShRoll_crv')
    rShRollCrv = cmds.duplicate ( lShRollCrv, n= upLow +'RShRoll_crv')
    rCrvTolCrv( lShRollCrv[0], rShRollCrv[0], 'Sh')
    cmds.hide(rShRollCrv[0])
    lMRollCrv = cmds.duplicate ( lipRollCrv, n= upLow +'LMRoll_crv')
    rMRollCrv = cmds.duplicate ( lipRollCrv, n= upLow +'RMRoll_crv')
    rCrvTolCrv( lMRollCrv[0], rMRollCrv[0], 'M')
    cmds.hide(rMRollCrv[0])
    lipRollBS = cmds.blendShape ( rollCtlCrv[0], lURollCrv[0],rURollCrv[0], rORollCrv[0],rORollCrv[0], lShRollCrv[0],lShRollCrv[0], lMRollCrv[0],rMRollCrv[0], lipRollCrv, n =upLow + 'LipRollBS')
    cmds.blendShape( lipRollBS[0], edit=True, w=[(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1), (7,1), (8,1)]) 
    
    # lip RollYZ control curve shape
    lipRollYZCrv = cmds.duplicate ( lipRollCrv, n= upLow +'RollYZ_crv')
    lipRollYZCrvShape = cmds.listRelatives ( lipRollYZCrv, c = True )
    #targets for lip RollYZ crv
    RollYZCtrlCrv = cmds.duplicate ( lipRollYZCrv, n= upLow +'RollYZCtl_crv')
    lURollYZCrv = cmds.duplicate ( lipRollYZCrv, n= upLow +'LURollYZ_crv') 
    rURollYZCrv = cmds.duplicate ( lURollYZCrv, n= upLow +'RURollYZ_crv')
    rCrvTolCrv( lURollYZCrv[0], rURollYZCrv[0], 'U')
    cmds.hide(rURollYZCrv[0])
    lORollYZCrv = cmds.duplicate ( lipRollYZCrv, n= upLow +'LORollYZ_crv') 
    rORollYZCrv = cmds.duplicate ( lORollYZCrv, n= upLow +'RORollYZ_crv')
    rCrvTolCrv( lORollYZCrv[0], rORollYZCrv[0], 'O')
    cmds.hide(rORollYZCrv[0])  
    lShRollYZCrv = cmds.duplicate ( lipRollYZCrv, n= upLow +'LShRollYZ_crv')
    rShRollYZCrv = cmds.duplicate ( lShRollYZCrv, n= upLow +'RShRollYZ_crv')
    rCrvTolCrv( lShRollYZCrv[0], rShRollYZCrv[0], 'Sh')
    cmds.hide(rShRollYZCrv[0])
    lHappyRollYZCrv = cmds.duplicate ( lipRollYZCrv, n= upLow +'LHappyRollYZ_crv')
    rHappyRollYZCrv = cmds.duplicate ( lHappyRollYZCrv, n= upLow +'RHappyRollYZ_crv')
    rCrvTolCrv( lHappyRollYZCrv[0], rHappyRollYZCrv[0], 'Happy')
    cmds.hide(rHappyRollYZCrv[0])    
    lWideRollYZCrv = cmds.duplicate ( lipRollYZCrv, n= upLow +'lWideRollYZ_crv')
    rWideRollYZCrv = cmds.duplicate ( lWideRollYZCrv, n= upLow +'rWideRollYZ_crv')
    rCrvTolCrv( lWideRollYZCrv[0], rWideRollYZCrv[0], 'Wide')
    cmds.hide(rWideRollYZCrv[0])
    lERollYZCrv = cmds.duplicate ( lipRollYZCrv, n= upLow +'LERollYZ_crv')
    rERollYZCrv = cmds.duplicate ( lERollYZCrv, n= upLow +'RERollYZ_crv')
    rCrvTolCrv( lERollYZCrv[0], rERollYZCrv[0], 'E' )
    cmds.hide(rERollYZCrv[0])
    lMRollYZCrv = cmds.duplicate ( lipRollYZCrv, n= upLow +'LMRollYZ_crv')
    rMRollYZCrv = cmds.duplicate ( lMRollYZCrv, n= upLow +'RMRollYZ_crv')
    rCrvTolCrv( lMRollYZCrv[0], rMRollYZCrv[0], 'M')
    cmds.hide(rMRollYZCrv[0])
    RollYZBS = cmds.blendShape ( RollYZCtrlCrv[0], lURollYZCrv[0],rURollYZCrv[0], rORollYZCrv[0],rORollYZCrv[0], lShRollYZCrv[0],rShRollYZCrv[0], lHappyRollYZCrv[0],lHappyRollYZCrv[0], lERollYZCrv[0],rERollYZCrv[0], lMRollYZCrv[0],rMRollYZCrv[0], lipRollYZCrv[0], n =upLow + 'RollYZBS')
    cmds.blendShape( RollYZBS[0], edit=True, w=[(0, 1), (1, 1), (2, 1), (3,1), (4,1),(5,1),(6,1),(7,1),(8,1),(9,1),(10,1),(11,1),(12,1)])     

    # lip RollYZ control curve shape!!!!!!!!!!!! center pivot / place the group in world to mirror 
    if not cmds.objExists('cheekCrv_grp'):
        cheekCrvGrp = cmds.group ( n = 'cheekCrv_grp', em =True, p = 'faceMain|crv_grp' )  
        cheekTempCrv = cmds.curve ( d=1, p = [(lowCheekPos), (lipEPos), (cheekPos), (squintPuffPos)] )  
        lCheekCrv = cmds.rename ( cheekTempCrv, "l_cheek_crv" ) 
        rCheekCrv = cmds.duplicate ( lCheekCrv, n= 'r_cheek_crv')
        cmds.setAttr ( rCheekCrv[0] + '.scaleX', -1)
        cmds.parent(lCheekCrv,rCheekCrv, 'faceMain|crv_grp|cheekCrv_grp')
        cmds.xform (lCheekCrv,rCheekCrv, centerPivots = 1) 
        lJawSwivelCheek = cmds.duplicate ( lCheekCrv, n= 'lCheekJawSwivel_crv')#cheek inward movement ( downward movement by jawSemi) 
        rJawSwivelCheek = cmds.instance ( lJawSwivelCheek, n= 'rCheekJawSwivel_crv') # left right control seperately using blendShape
        lJawOpenCheek = cmds.duplicate ( lCheekCrv, n= 'lCheekJawOpen_crv')#cheek inward movement ( downward movement by jawSemi) 
        rJawOpenCheek = cmds.instance ( lJawOpenCheek, n= 'rCheekJawOpen_crv')
        lJawUDLRCheek = cmds.duplicate ( lCheekCrv, n= 'lCheekJawUDLR_crv')#cheek inward movement ( downward movement by jawSemi) 
        rJawUDLRCheek = cmds.instance ( lJawUDLRCheek, n= 'rCheekJawUDLR_crv')
        lHappyCheekCrv = cmds.duplicate ( lCheekCrv, n= 'lHappyCheek_crv') 
        rHappyCheekCrv = cmds.instance ( lHappyCheekCrv, n= 'rHappyCheek_crv')
        cmds.parent ( lHappyCheekCrv, rHappyCheekCrv, 'HappyCrv_grp')
        lWideCheekCrv = cmds.duplicate ( lCheekCrv, n= 'lWideCheek_crv') 
        rWideCheekCrv = cmds.instance ( lWideCheekCrv, n= 'rWideCheek_crv')
        cmds.parent ( lWideCheekCrv, rWideCheekCrv, 'WideCrv_grp')
        lSadCheekCrv = cmds.duplicate ( lCheekCrv, n= 'lSadCheek_crv') 
        rSadCheekCrv = cmds.instance ( lSadCheekCrv, n= 'rSadCheek_crv')
        cmds.parent ( lSadCheekCrv, rSadCheekCrv, 'SadCrv_grp')
        lECheekCrv = cmds.duplicate ( lCheekCrv, n= 'lECheek_crv') 
        rECheekCrv = cmds.instance ( lECheekCrv, n= 'rECheek_crv') 
        cmds.parent ( lECheekCrv, rECheekCrv, 'ECrv_grp')
        lUCheekCrv = cmds.duplicate ( lCheekCrv, n= 'lUCheek_crv') 
        rUCheekCrv = cmds.instance ( lUCheekCrv, n= 'rUCheek_crv') 
        cmds.parent ( lUCheekCrv, rUCheekCrv, 'UCrv_grp')
        lOCheekCrv = cmds.duplicate ( lCheekCrv, n= 'lOCheek_crv') 
        rOCheekCrv = cmds.instance ( lOCheekCrv, n= 'rOCheek_crv') 
        cmds.parent ( lOCheekCrv, rOCheekCrv, 'OCrv_grp')
        lShCheekCrv = cmds.duplicate ( lCheekCrv, n= 'lShCheek_crv') 
        rShCheekCrv = cmds.instance ( lShCheekCrv, n= 'rShCheek_crv') 
        cmds.parent ( lShCheekCrv, rShCheekCrv, 'ShCrv_grp')
        lCheekBS = cmds.blendShape ( lJawSwivelCheek[0], lJawOpenCheek[0], lJawUDLRCheek[0],lHappyCheekCrv[0],lWideCheekCrv[0],lSadCheekCrv[0],lECheekCrv[0],lUCheekCrv[0],lOCheekCrv[0], lShCheekCrv[0], lCheekCrv, n ='lCheekBS')
        cmds.blendShape( lCheekBS[0], edit=True, w=[(0, 1), (1, 1), (2, 1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1)])   
        rCheekBS = cmds.blendShape ( rJawSwivelCheek[0], rJawOpenCheek[0], rJawUDLRCheek[0],rHappyCheekCrv[0],rWideCheekCrv[0],rSadCheekCrv[0],rECheekCrv[0],rUCheekCrv[0],rOCheekCrv[0], rShCheekCrv[0], rCheekCrv, n ='rCheekBS')
        cmds.blendShape( rCheekBS[0], edit=True, w=[(0, 1), (1, 1), (2, 1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1)])    
        cmds.move ( 2,0,0, lJawSwivelCheek, lJawOpenCheek, lJawUDLRCheek, lHappyCheekCrv, lWideCheekCrv, lSadCheekCrv, lECheekCrv, lOCheekCrv, lShCheekCrv, rotatePivotRelative = 1  )
        cmds.move (-2,0,0, rJawSwivelCheek, rJawOpenCheek, rJawUDLRCheek, rHappyCheekCrv, rWideCheekCrv, rSadCheekCrv, rECheekCrv, rOCheekCrv, rShCheekCrv, rotatePivotRelative = 1  )
        
        #attach ctrls to main cheek curves
        for LR in ['l','r']:
            cvLs = cmds.ls( LR + '_cheek_crv.cv[*]', fl = 1 )
            cvLen = len(cvLs)
            lipCorner = cmds.group (em =1, n= LR+'_lipCorner', p ='supportRig') 
            cheekList = [LR + '_lowCheek_grp', str(lipCorner), LR + '_cheek_grp', LR + '_squintPuff_grp'] 
         
            for v in range(0, cvLen):
                cheekPoc = cmds.shadingNode ( 'pointOnCurveInfo', asUtility =True, n = 'cheek' + str(v) + '_poc' )
                cmds.connectAttr ( LR+'_cheek_crvShape.worldSpace', cheekPoc + '.inputCurve')   
                cmds.setAttr (cheekPoc + '.parameter', v )            
                cmds.connectAttr (cheekPoc + '.positionX', cheekList[v] + '.tx')
                cmds.connectAttr (cheekPoc + '.positionY', cheekList[v] + '.ty')
                cmds.connectAttr (cheekPoc + '.positionZ', cheekList[v] + '.tz')
     
    #create lip joints parent group
    lipJotGrp = cmds.group ( n = upLow + 'Lip_grp', em =True )  
    cmds.parent ( lipJotGrp, 'lipJotP' )
    cmds.xform (lipJotGrp, ws = 1, t = JawRigPos ) 
    # delete detail lip ctrls 
    lipDetailP = upLow + 'LipDetailGrp'
    kids = cmds.listRelatives (lipDetailP, ad=True, type ='transform')   
    if kids:
        cmds.delete (kids)     
        
    if upLow == 'up':
        min = 0
        max = vNum
    elif upLow == 'lo':    
        min = 1
        max = vNum-1           
          
    for i in range (min, max ):                
        poc = cmds.shadingNode ( 'pointOnCurveInfo', asUtility =True, n = upLow + 'Lip' + str(i) + '_poc' )
        cmds.connectAttr ( guideCrvShape[0]+'.worldSpace',  poc + '.inputCurve')   
        cmds.setAttr ( poc + '.turnOnPercentage', 1 )    
        cmds.setAttr ( poc + '.parameter', increment*i)
        createLipJoint( upLow, JawRigPos, lipYPos, poc, lipJotGrp, i)
        #create detail lip ctrl        
        if i==0 or i== vNum-1:
            createDetailCtl( upLow, i )
            cmds.parent ( upLow +'LipDetailP'+ str(i), lipDetailP )
            cmds.setAttr (upLow +'LipDetailP'+ str(i)+'.tx', increment*i )
            cmds.setAttr (upLow +'LipDetailP'+ str(i)+'.ty', -1.5 )
            cmds.setAttr (upLow +'LipDetailP'+ str(i)+'.tz', 0 )
            cmds.setAttr (upLow +'LipDetailP'+ str(i)+'.sx', 0.25 )
        else: 
            createDetailCtl( upLow, i )           
            cmds.parent ( upLow +'LipDetailP'+ str(i), lipDetailP )
            cmds.setAttr (upLow +'LipDetailP'+ str(i) + '.tx', increment*i) 
            cmds.setAttr (upLow +'LipDetailP'+ str(i) + '.ty', 0 ) 
            cmds.setAttr (upLow +'LipDetailP'+ str(i) + '.tz', 0 ) 
        # create lip curve POC
        lipCrvPoc = cmds.shadingNode ( 'pointOnCurveInfo', asUtility =True, n = upLow +'LipCrv' + str(i) + '_poc'  )
        cmds.connectAttr ( lipCrvShape[0] + ".worldSpace",  lipCrvPoc + '.inputCurve')   
        cmds.setAttr ( lipCrvPoc  + '.turnOnPercentage', 1 )    
        cmds.setAttr ( lipCrvPoc  + '.parameter', increment*i )  
        # create lip Ty curve POC
        lipTYPoc = cmds.shadingNode ( 'pointOnCurveInfo', asUtility =True, n = upLow +'LipTY' + str(i) + '_poc'  )
        cmds.connectAttr ( tylipCrvShape[0] + ".worldSpace",  lipTYPoc + '.inputCurve')   
        cmds.setAttr ( lipTYPoc  + '.turnOnPercentage', 1 )    
        cmds.setAttr ( lipTYPoc  + '.parameter', increment*i )        
        # create lipCtrl curve POC
        ctlPoc = cmds.shadingNode ( 'pointOnCurveInfo', asUtility =True, n = upLow +'LipCtl' + str(i) + '_poc' )
        cmds.connectAttr ( lipCtlCrvShape[0] + ".worldSpace",  ctlPoc + '.inputCurve')   
        cmds.setAttr ( ctlPoc  + '.turnOnPercentage', 1 )    
        cmds.setAttr ( ctlPoc  + '.parameter', increment*i )               
        # create lipRoll curve POC  lipRollCrv, lipRollYZCrv,
        lipRollPoc = cmds.shadingNode ( 'pointOnCurveInfo', asUtility =True, n = upLow +'LipRoll' + str(i) + '_poc'  )
        cmds.connectAttr ( lipRollCrvShape[0] + ".worldSpace",  lipRollPoc + '.inputCurve')   
        cmds.setAttr ( lipRollPoc + '.turnOnPercentage', 1 )    
        cmds.setAttr ( lipRollPoc + '.parameter', increment*i )  
        
        lipRollYZPoc = cmds.shadingNode ( 'pointOnCurveInfo', asUtility =True, n = upLow +'LipRollYZ' + str(i) + '_poc'  )
        cmds.connectAttr ( lipRollYZCrvShape[0] + ".worldSpace",  lipRollYZPoc + '.inputCurve')   
        cmds.setAttr ( lipRollYZPoc  + '.turnOnPercentage', 1 )    
        cmds.setAttr ( lipRollYZPoc  + '.parameter', increment*i ) 

mouthJoint( 'lo' ) 

#rCrvTolCrv( 'upLWide_crv', 'upRWide_crv', 'Wide' )
def rCrvTolCrv( lCrv, rCrv, name ):
    if not cmds.objExists( name+'Crv_grp'): 
        crvGrp = cmds.group ( n =  name+'Crv_grp', em =True, p = 'faceMain|crv_grp|lipCrv_grp' ) 
    cmds.parent (lCrv, rCrv, name+'Crv_grp' ) 
    cvLs = cmds.ls( lCrv + '.cv[*]', fl = 1 )
    print cvLs
    cvLen = len(cvLs)
    print cvLen
    for x in range ( 0, cvLen):  
        cmds.connectAttr ( lCrv + 'Shape.controlPoints[' + str(x) + ']', rCrv + 'Shape.controlPoints[' + str(x) + ']', f=1 )

























import maya.cmds as cmds
import fnmatch
def lipCrvToJoint(): 
    swivelTranXMult = cmds.shadingNode ('multiplyDivide', asUtility = 1, n = 'swivelTranX_mult')
    cmds.connectAttr ( 'Swivel_ctrl.tx', swivelTranXMult + '.input1X' )
    cmds.connectAttr ( 'Swivel_ctrl.tx', swivelTranXMult + '.input1Y' )
    cmds.connectAttr ( 'Swivel_ctrl.tx', swivelTranXMult + '.input1Z' )
    # x:2 = lipJotP.tx / y*0.5 = LipJotX*.ry / z*20 = 'jawSemi.rz'
    cmds.setAttr (swivelTranXMult + '.input2', 2, .5, 20)
    cmds.connectAttr ( swivelTranXMult + '.outputX', 'lipJotP.tx' )
    cmds.connectAttr ( swivelTranXMult + '.outputZ', 'lipJotP.rz' )
    
    swivelTranYMult = cmds.shadingNode ('multiplyDivide', asUtility = 1, n = 'swivelTranY_mult')
    cmds.connectAttr ( 'Swivel_ctrl.ty', swivelTranYMult + '.input1X' )
    cmds.connectAttr ( 'Swivel_ctrl.ty', swivelTranYMult + '.input1Z' )
    cmds.setAttr (swivelTranYMult + '.input2', 2, 0 ,1)
    cmds.connectAttr ( swivelTranYMult + '.outputX', 'lipJotP.ty' )
    
    # connect the 'jawSemiAdd'
    jawSemiAddMult = cmds.shadingNode ('multiplyDivide', asUtility = 1, n = 'jawSemiAdd_mult')
    cmds.connectAttr ( 'jawSemi.translate', jawSemiAddMult + '.input1')
    cmds.setAttr ( jawSemiAddMult + '.input2', .5,.5,.5 )
    cmds.connectAttr ( jawSemiAddMult + '.output', 'jawSemiAdd.translate' )
    cmds.connectAttr ( 'jawSemi.rotate', 'jawSemiAdd.rotate')

    prefix = ['up','lo']
    for upLow in prefix:        
        #main lipCtrls connect with LipCtl_crv    
        mainCtrlP = cmds.listRelatives ( cmds.ls ( 'lip*Ctr*Float', fl=True, type ='transform'), c =1, type = 'transform' )
        lipCtrls = fnmatch.filter( mainCtrlP, 'lip%s*'% upLow.title()) 
        lipCtrls.reverse()
        lipCtrls.insert(0, mainCtrlP[1])
        lipCtrls.insert(len(lipCtrls), mainCtrlP[0])
        
        index = 0
        for n in lipCtrls:
            # curve cv xValue zero out
            zeroX = cmds.shadingNode ( 'addDoubleLinear', asUtility=True, n = upLow + lipCtrls[index].split('Ctrl', 1)[1] + '_xAdd' ) 
            cvTx = cmds.getAttr(upLow + 'LipCtl_crv.controlPoints['+str(index)+'].xValue' ) 
            cmds.connectAttr ( n+'.tx', zeroX + '.input1' )
            cmds.setAttr (zeroX + '.input2' , cvTx )  
            cmds.connectAttr ( zeroX + '.output', upLow + 'LipCtl_crv.controlPoints['+str(index)+'].xValue' )
            # main ctrl's TY drive the ctrl curve point yValue
            cmds.connectAttr ( n+'.ty' , upLow + 'LipCtl_crv.controlPoints['+str(index)+'].yValue' )
            index = index +1      
    
        #main lipRoll Ctrls connect with 'LipRollCtl_crv' /'RollYZCtl_crv' 
        mainRollCtrlP = cmds.listRelatives ( 'Lip'+ upLow.title() + 'RollCtrl', ad =1, type = 'transform' )
        lipRollCtls = fnmatch.filter( mainRollCtrlP, '*Roll_ctl') 
        # lipRollCtrl  to 'RollCtl_crv' 
        cmds.connectAttr ( lipRollCtls[0]+ '.rz', upLow + 'RollCtl_crv.controlPoints[2].yValue' )
        cmds.connectAttr ( lipRollCtls[1]+ '.rz', upLow + 'RollCtl_crv.controlPoints[3].yValue' ) 
        cmds.connectAttr ( lipRollCtls[2]+ '.rz', upLow + 'RollCtl_crv.controlPoints[1].yValue' )
        # lipRollCtrl  to 'RollYZCtl_crv' 
        cmds.connectAttr ( lipRollCtls[0]+ '.ty', upLow + 'RollYZCtl_crv.controlPoints[2].yValue' )
        cmds.connectAttr ( lipRollCtls[1]+ '.ty', upLow + 'RollYZCtl_crv.controlPoints[3].yValue' )
        cmds.connectAttr ( lipRollCtls[2]+ '.ty', upLow + 'RollYZCtl_crv.controlPoints[1].yValue' )
        cmds.connectAttr ( lipRollCtls[0]+ '.tx', upLow + 'RollYZCtl_crv.controlPoints[2].zValue' )
        cmds.connectAttr ( lipRollCtls[1]+ '.tx', upLow + 'RollYZCtl_crv.controlPoints[3].zValue' )
        cmds.connectAttr ( lipRollCtls[2]+ '.tx', upLow + 'RollYZCtl_crv.controlPoints[1].zValue' ) 
 
        # curve's Poc drive the joint
        lipJots= cmds.ls ( upLow + 'LipJotX*', fl=True, type ='transform' )
        jotNum = len (lipJots)    
        
        if upLow == 'up':
            min = 0
            max = jotNum
        elif upLow == 'lo':  
            jotNum = len (lipJots) + 2 
            min = 1
            max = jotNum-1
        
        for i in range ( min, max ):  
        
            jotXMult = cmds.shadingNode ( 'multiplyDivide', asUtility=True, n = upLow + 'JotXRot' + str(i)+'_mult' )
            jotYMult = cmds.shadingNode ( 'multiplyDivide', asUtility=True, n = upLow + 'JotYRot' + str(i)+'_mult' )
            jotXPosMult = cmds.shadingNode ( 'multiplyDivide', asUtility=True, n = upLow + 'LipJotXPos' + str(i)+'_mult' )
            plusTXAvg = cmds.shadingNode ( 'plusMinusAverage', asUtility=True, n = upLow + 'TX' + str(i) +'_plus')   
            plusTYAvg = cmds.shadingNode ( 'plusMinusAverage', asUtility=True, n = upLow + 'TY' + str(i) +'_plus')  
            jotXPosAvg = cmds.shadingNode ( 'plusMinusAverage', asUtility=True, n = upLow + 'LipJotXPos' + str(i)+'_plus' )        
            jotXTYaddD = cmds.shadingNode ( 'addDoubleLinear', asUtility=True, n = upLow + 'TY' + str(i) + '_add' )
            lipRollMult = cmds.shadingNode ( 'multiplyDivide', asUtility=True, n = upLow + 'LipRoll' + str(i)+'_mult' )
            lipRollAvg = cmds.shadingNode ( 'plusMinusAverage', asUtility=True, n = upLow + 'LipRoll' + str(i) +'_plus')   
            
            #blinkRemap = cmds.shadingNode ( 'remapValue', asUtility=True, n = jnt.split('Blink', 1)[0] + str(i)+'_remap' )
            #blinkGap = cmds.shadingNode ( 'addDoubleLinear', asUtility=True, n = jnt.split('LidBlink', 1)[0] + 'BlinkGap'+str(i)+'_yAdd' )
                            
            poc = upLow +'LipCrv' + str(i) + '_poc'
            initialX = cmds.getAttr ( poc + '.positionX' )
            
            TYpoc = upLow +'LipTY' + str(i) + '_poc'
            initialTYX = cmds.getAttr ( TYpoc + '.positionX' )
            
            ctlPoc = upLow +'LipCtl' + str(i) + '_poc'
            initialCtlX = cmds.getAttr ( ctlPoc + '.positionX' )            
            
            rollPoc = upLow +'LipRoll' + str(i) + '_poc'
            rollYZPoc = upLow +'LipRollYZ' + str(i) + '_poc'
            #ty tz = Ucrv.tz + happyCrv.tz + 'LipRoll_poc.positionZ' / rx = Ucrv + 'LipRoll_poc.positionY'
            #lipRoll_crv to lipRoll_joint !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            cmds.setAttr ( lipRollAvg + '.operation', 1 ) 
            cmds.setAttr ( lipRollMult + '.input2', 2,2,2)
            cmds.connectAttr ( rollPoc + '.positionY', lipRollMult+'.input1X')
            cmds.connectAttr ( lipRollMult+'.outputX', upLow + 'LipRollJot'+str(i)+'_jnt.rx') 
            
            cmds.connectAttr ( rollYZPoc + '.positionY', lipRollMult+'.input1Y')
            cmds.connectAttr ( lipRollMult+'.outputY', upLow + 'LipRollJot'+str(i)+'_jnt.ty' )
            
            cmds.connectAttr ( rollYZPoc + '.positionZ', lipRollMult+'.input1Z')            
            cmds.connectAttr ( lipRollMult+'.outputZ', upLow + 'LipRollJot'+str(i)+'_jnt.tz' )
            
            #TranslateX add up for  
            #1. curve translateX add up for LipJotX
            cmds.setAttr ( plusTXAvg + '.operation', 1 ) 
            cmds.connectAttr ( poc + '.positionX', plusTXAvg + '.input3D[0].input3Dx') 
            cmds.setAttr (plusTXAvg + '.input3D[1].input3Dx', -initialX ) 
            cmds.connectAttr ( swivelTranXMult + '.outputY',  plusTXAvg + '.input3D[2].input3Dx' )
            cmds.connectAttr ( plusTXAvg + '.output3Dx', jotXMult + '.input1X' ) 
            cmds.setAttr ( jotXMult + '.input2X', 30 )   
            cmds.connectAttr ( jotXMult + '.outputX', upLow + 'LipJotX'+str(i)+'.ry') 
            
            #2. poc positionY,Z sum drive joint("lipJotX") translateY,Z
            cmds.connectAttr ( TYpoc + '.positionY',  jotXPosAvg + '.input3D[0].input3Dy' )
            cmds.connectAttr ( jotXPosAvg + '.output3Dy', jotXPosMult + '.input1Y' )
            cmds.setAttr ( jotXPosMult + '.input2Y', 5 )   
            cmds.connectAttr ( jotXPosMult + '.outputY', upLow + 'LipJotX'+str(i)+'.ty')        
            cmds.connectAttr ( TYpoc + '.positionZ', jotXPosAvg + '.input3D[0].input3Dz' )  
            
            #3. LipCtlCrv Poc.positionX + LipDetail.tx for LipJotY 
            cmds.connectAttr ( ctlPoc + '.positionX', plusTXAvg + '.input3D[0].input3Dy' )  
            cmds.setAttr ( plusTXAvg + '.input3D[1].input3Dy', -initialCtlX )  
            cmds.connectAttr ( upLow + 'LipDetail'+ str(i)+'.tx', plusTXAvg + '.input3D[2].input3Dy' )             
            cmds.connectAttr (  plusTXAvg + '.output3Dy', jotYMult + '.input1Y' )          
            cmds.setAttr ( jotYMult + '.input2', -30, 30, 30 )   
            cmds.connectAttr ( jotYMult + '.outputY', upLow+'LipJotY'+str(i)+'.ry' ) 
            #mouth ctrl to LipJotY rx, ry
            cmds.connectAttr ( 'mouth_move.tx', plusTXAvg + '.input3D[3].input3Dy' ) 
            cmds.connectAttr ( 'mouth_move.ty', jotYMult + '.input1X' )            
            cmds.connectAttr ( jotYMult + '.outputX', upLow+'LipJotY'+str(i)+'.rx' )             
            
            if i==0 or i==jotNum-1:
                zeroTip = cmds.shadingNode ( 'addDoubleLinear', asUtility=True, n = 'zeroTip' + str(i) + '_plus' )
                momTY = cmds.getAttr ( upLow + 'LipDetailP' + str(i) +'.ty' )
                cmds.connectAttr ( ctlPoc + '.positionY', zeroTip + '.input1' )
                cmds.setAttr ( zeroTip + '.input2', momTY )
                cmds.connectAttr ( zeroTip + '.output', upLow + 'LipDetailP' +str(i) + '.ty')
                
            else:
                #3. LipCtl_crv connect with lipDetailP (lipDetailCtrl parents)
                cmds.connectAttr ( ctlPoc + '.positionY', upLow + 'LipDetailP' +str(i) + '.ty')
            
            # curve translateY add up ( joint(LipJotX)"rx" driven by both curves(lipCrv, lipCtlCrv))
            # ty(input3Dy) / extra ty(input3Dx) seperate out for jawSemi
            cmds.setAttr ( plusTYAvg + '.operation', 1 )
            cmds.connectAttr ( poc + '.positionY', plusTYAvg + '.input3D[0].input3Dy')
            cmds.connectAttr ( swivelTranYMult + '.outputZ', plusTYAvg + '.input3D[1].input3Dy' )
            
            cmds.connectAttr ( ctlPoc + '.positionY', plusTYAvg + '.input3D[0].input3Dx') 
            cmds.connectAttr ( upLow + 'LipDetail'+ str(i) + '.ty', plusTYAvg + '.input3D[1].input3Dx' )
            cmds.connectAttr ( plusTYAvg + '.output3Dx', jotXTYaddD+'.input1')
            cmds.connectAttr ( plusTYAvg + '.output3Dy', jotXTYaddD+'.input2')
        
            #connect translateY plusAvg to joint rotateX Mult        
            cmds.connectAttr ( jotXTYaddD + '.output', jotXMult + '.input1Y' )  
            cmds.setAttr ( jotXMult + '.input2Y', -20 ) 
            cmds.connectAttr ( jotXMult + '.outputY', upLow + 'LipJotX'+ str(i) + '.rx' ) 
            
            # joint(LipJotX) translateX driven by poc positionX sum
            cmds.connectAttr ( TYpoc + '.positionX', jotXPosAvg + '.input3D[0].input3Dx' ) 
            cmds.setAttr ( jotXPosAvg + '.input3D[1].input3Dx', -initialTYX )
            cmds.connectAttr ( jotXPosAvg + '.output3Dx', jotXPosMult + '.input1X' )  
            cmds.setAttr ( jotXPosMult + '.input2X', 5 ) 
            cmds.connectAttr ( jotXPosMult + '.outputX', upLow + 'LipJotX'+ str(i) + '.tx' )
             
            # joint(LipJotX) translateZ driven by poc positionZ sum
            cmds.connectAttr ( poc + '.positionZ', jotXPosAvg + '.input3D[1].input3Dz' ) 
            cmds.connectAttr ( jotXPosAvg + '.output3Dz', jotXPosMult + '.input1Z')  
            cmds.setAttr ( jotXPosMult + '.input2Z', 2 ) 
            cmds.connectAttr ( jotXPosMult + '.outputZ', upLow + 'LipJotX'+ str(i) + '.tz' )  
            
    #jawSemi movement define
    if not upLow == 'up':
        cntTXAvg = 'loTX' + str(jotNum/2) + '_plus' 
        cntTYAvg = 'loTY' + str(jotNum/2) + '_plus'
        jawSemiRotMult = cmds.shadingNode ('multiplyDivide', asUtility = 1, n = 'jawSemiRot_mult')        
        cmds.connectAttr ( cntTXAvg + '.output3Dx',  jawSemiRotMult + '.input1X' )  
        cmds.connectAttr ( cntTYAvg + '.output3Dy',  jawSemiRotMult + '.input1Y' )
        # jawSemi rotateX move as same as the joint7. rotateX 
        rotXScale = cmds.getAttr ( jotXMult + '.input2Y' ) 
        cmds.setAttr ( jawSemiRotMult + '.input2', 10, rotXScale, 0 )
        cmds.connectAttr ( jawSemiRotMult + '.outputX', 'jawSemi.ry' ) 
        cmds.connectAttr ( jawSemiRotMult + '.outputY', 'jawSemi.rx' )           
        # jawSemi rotateZ driven by swivel     
        cmds.connectAttr ( swivelTranXMult + '.outputZ', 'jawSemi.rz' )
        # jawSemi translate driven by TYcrv / Swivel
        cntPosAvg = 'loLipJotXPos' + str(jotNum/2) + '_plus' 
        jawSemiPosPlus = cmds.shadingNode ('plusMinusAverage', asUtility = 1, n = 'jawSemiPos_plus')        
        jawSemiPosMult = cmds.shadingNode ('multiplyDivide', asUtility = True, n = 'jawSemiPos_mult')            
        cmds.connectAttr ( cntPosAvg + '.output3Dx', jawSemiPosPlus + '.input3D[0].input3Dx')           
        cmds.connectAttr ( swivelTranXMult + '.outputX', jawSemiPosPlus + '.input3D[1].input3Dx')
        cmds.connectAttr ( cntPosAvg + '.output3Dy', jawSemiPosPlus + '.input3D[0].input3Dy')

        #swivel ty   * 1 (swivelTranY_mult.outputZ)  jawSemi. ty 
        #, swivel ty   * 1( swivelTranY_mult.outputX)   lipJotP. ty                      
        cmds.connectAttr ( swivelTranYMult + '.outputZ', jawSemiPosPlus + '.input3D[1].input3Dy')            
        cmds.connectAttr ( jawSemiPosPlus + '.output3Dx',  jawSemiPosMult + '.input1X' )     
        cmds.connectAttr ( jawSemiPosPlus + '.output3Dy',  jawSemiPosMult + '.input1Y' )
        cmds.connectAttr ( cntPosAvg + '.output3Dz',  jawSemiPosMult + '.input1Z' )
        # jawSemi follow rate = tx: 1.5/2 , ty: move as same as the joint7. translateY
        tranYScale=cmds.getAttr ( swivelTranYMult + '.input2X' )
        cmds.setAttr ( jawSemiPosMult + '.input2', 1.2, tranYScale, 1 ) 
        cmds.connectAttr ( jawSemiPosMult + '.outputX', 'jawSemi.tx' ) 
        cmds.connectAttr ( jawSemiPosMult + '.outputY', 'jawSemi.ty' )  
        cmds.connectAttr ( jawSemiPosMult + '.outputZ', 'jawSemi.tz' ) 
        #jawSemi ScaleX driven by jawOpen/ jawSwivel / jawUDLR / E / Happy / Sad
        jawSemiScaleXRemap = cmds.shadingNode ('remapValue', asUtility = True, n = 'jawSemiScale_remap')
        jawSemiScalePlus = cmds.shadingNode ('plusMinusAverage', asUtility = 1, n = 'jawSemiScale_plus')
        jawScaleDownMult = cmds.shadingNode ('multiplyDivide', asUtility = True, n = 'jawScaleDown_mult')  

        cmds.setAttr( jawSemiScaleXRemap + ".outputMin", 0.8 )
        cmds.setAttr( jawSemiScaleXRemap + ".outputMax", 1.2 )
        cmds.setAttr( jawSemiScaleXRemap + ".inputMin", -1 )
        cmds.connectAttr ( jawSemiScaleXRemap + '.outValue', 'jawSemi.sx' ) 
        
        cmds.connectAttr( 'lowJaw_dir.ty', jawScaleDownMult+'.input1X')
        cmds.connectAttr( 'Swivel_ctrl.ty', jawScaleDownMult+'.input1Y')
        cmds.connectAttr( 'jaw_UDLR.ty', jawScaleDownMult+'.input1Z')
        cmds.setAttr ( jawScaleDownMult+'.input2', .2,.5,.3 )
        cmds.connectAttr ( jawScaleDownMult+'.outputX', jawSemiScalePlus + '.input1D[0]')
        cmds.connectAttr ( jawScaleDownMult+'.outputY', jawSemiScalePlus + '.input1D[1]')
        cmds.connectAttr ( jawScaleDownMult+'.outputZ', jawSemiScalePlus + '.input1D[2]')  
        cmds.connectAttr ( jawSemiScalePlus + '.output1D', jawSemiScaleXRemap + '.inputValue' ) 
        
        #lowCheekP follow jawSemi + loCheekCtls
        semiPos = cmds.xform ('jawSemi', q=1, ws = 1, t =1)
        cmds.xform ('l_lowCheekP','r_lowCheekP', ws =1, rotatePivot = semiPos )        
        lowCheekCtl = 'loCheek_ctl'
        prefix = ['l_','r_']
        for n in prefix:
            lowCheekAvg = cmds.shadingNode ( 'plusMinusAverage', asUtility=True, n = n+'lowCheek'+'_plus')
            cmds.connectAttr ('jawSemi.tx', lowCheekAvg + '.input3D[0].input3Dx')
            cmds.connectAttr ( n + lowCheekCtl + '.tx', lowCheekAvg + '.input3D[1].input3Dx')
            cmds.connectAttr ('jawSemi.ty', lowCheekAvg + '.input3D[0].input3Dy')
            cmds.connectAttr ( n + lowCheekCtl + '.ty', lowCheekAvg + '.input3D[1].input3Dy')
            cmds.connectAttr ('jawSemi.tz', lowCheekAvg + '.input3D[0].input3Dz')
            cmds.connectAttr ('jawSemi.rotate', n + 'lowCheekP.rotate')
            cmds.connectAttr (lowCheekAvg + '.output3D', n + 'lowCheekP.translate') 
                                                 
        
lipCrvToJoint( )




#lipJotP input
cmds.setAttr (swivelTranYMult + '.input2', 2, 0 ,1)
swivel ty * input2 X = lipJotP ty
swivel ty * input2 Z = loLipJotX* rx

cmds.setAttr (swivelTranXMult + '.input2', 1, .3, 20)
swivel tx * 1 = lipJotP tx
swivel tx * 0.3 = loLipJotX* ry
swivel tx * 20 = lipJotP rz


#lipJotP input
cmds.setAttr ( jawScaleDownMult+'.input2', .2,.5,.3 )
swivel ty * 0.5 = jawSemi.sx 
















import maya.cmds as cmds 
def indiCrvSetup(name, posX, posY, typeAB ):
    #select upLip curves that need joints control ('upJawOpen_crv', 'upUDLR_crv'... )  
    crv = 'up'+ name + '_crv'
    loCrv = crv.replace('up', 'lo', 1)
    crvShape = cmds.listRelatives ( crv, c=1, type = 'nurbsCurve')
    crvCVs = cmds.ls ( crv + '.cv[*]', fl = 1 )
    cvNum = len ( crvCVs ) 
       
    lipCrvStartPos = cmds.xform (crvCVs[0], q=1, ws =1, t = 1 )
    lipCrvEndPos = cmds.xform (crvCVs[cvNum-1], q=1, ws =1, t = 1 )
    nCrvPoc = cmds.shadingNode ( 'pointOnCurveInfo', asUtility =True, n = 'cnt' + name + '_poc' )
    cmds.connectAttr ( crvShape[0]+'.worldSpace',  nCrvPoc + '.inputCurve')   
    cmds.setAttr ( nCrvPoc + '.turnOnPercentage', 1 )    
    cmds.setAttr ( nCrvPoc + '.parameter', .5)
    lipCrvMidPos = cmds.getAttr( nCrvPoc + '.position')
    
    lipCrvStart = cmds.group (em = 1, n = name + 'Start_grp' )
    cmds.xform ( lipCrvStart, ws = 1, t = lipCrvStartPos )
    rCorner = cmds.joint ( n= 'rCorner'+ name+'_jnt', p= lipCrvStartPos ) 
    
    uplipCrvMid = cmds.group (em = 1, n = 'up' + name + 'Mid_grp' ) 
    cmds.xform ( uplipCrvMid, ws = 1, t = list(lipCrvMidPos[0]) ) 
    midUpJnt = cmds.joint ( n = 'cntUp' + name + '_jnt', relative = True, p = [ 0, 0, 0] )  

    lolipCrvMid = cmds.group (em = 1, n = 'lo' + name + 'Mid_grp') 
    cmds.xform ( lolipCrvMid, ws = 1, t = list(lipCrvMidPos[0]) ) 
    midLoJnt = cmds.joint ( n = 'cntLo' + name + '_jnt', relative = True, p = [ 0, 0, 0] )

    lipCrvEnd = cmds.group (em = 1, n = name + 'End_grp' ) 
    cmds.xform ( lipCrvEnd, ws = 1, t = lipCrvEndPos ) 
    lCorner = cmds.joint ( n= 'lCorner' + name + '_jnt', relative = True, p = [ 0, 0, 0] )  
    crvList = cmds.listRelatives ( 'crv_grp', allDescendents = 1, type = 'transform' )
    if objExists(name + ) in crvList:
        indiCrvs = fnmatch.filter ( crvList, '*%s*'% name)
        indiGrp = cmds.group ( lipCrvStart, uplipCrvMid, lolipCrvMid, lipCrvEnd, indiCrvs, n = name + '_indiGrp' ) 
        cmds.parent (indiGrp, 'lipCrv_grp' )
        cmds.setAttr( indiGrp + '.tx', posX )
        cmds.setAttr( indiGrp + '.ty', posY )
        #skinning (cv skin weight input)
        cmds.skinCluster ( rCorner, midUpJnt, lCorner, crv, toSelectedBones = 1 )    
        cmds.skinCluster ( rCorner, midLoJnt, lCorner, loCrv, toSelectedBones = 1 )

    if type == 'B':
                
        cornerMult = cmds.shadingNode ( 'multiplyDivide', asUtility=True, n = name +'_mult' )
        dampMult = cmds.shadingNode ( 'multiplyDivide', asUtility=True, n = name + 'damp_mult' )
        txAvg = cmds.shadingNode ( 'plusMinusAverage', asUtility=True, n = name + 'TX_plus')  
        
        #?ty? ? ?? ????? inputX,Y?  ??? tx ? tz?  inputZ ? ??.
        txzPick = ['.' + myAttr ]
        cmds.connectAttr ( midLoJnt+ '.ty', cornerMult+ '.input1X' )  
        cmds.connectAttr ( midLoJnt+ '.ty', cornerMult+ '.input1Y' )  
        cmds.connectAttr ( midLoJnt + txzPick, cornerMult+ '.input1Z' ) 
        cmds.setAttr ( cornerMult + '.input2X', .1) #= lCorner jnts move inside(tx) as jaw open
        cmds.setAttr ( cornerMult + '.input2Y', .1) #= rCorner jnts move inside(tx) as jaw open 
        cmds.setAttr ( cornerMult + '.input2Z', -.3) #= corner jnts (tx or tz) go along as jaw moving tx

        cmds.connectAttr ( cornerMult + '.outputX', txAvg + '.input3D[0].input3Dx' )
        cmds.connectAttr ( cornerMult + '.outputY', txAvg + '.input3D[0].input3Dy' )
        cmds.connectAttr ( cornerMult + '.outputZ', txAvg + '.input3D[1].input3Dx' )
        cmds.connectAttr ( cornerMult + '.outputZ', txAvg + '.input3D[1].input3Dy' )
        cmds.connectAttr ( txAvg + '.output3Dx', lCorner +  txzPick)
        cmds.connectAttr ( txAvg + '.output3Dy', rCorner + txzPick )

        # lip corners translateY go along with jaw open
        cmds.connectAttr ( midLoJnt+ '.ty', dampMult + '.input1X' )  
        cmds.connectAttr ( midLoJnt+ '.ty', dampMult + '.input1Y' )  
        cmds.connectAttr ( midLoJnt + txzPick, dampMult + '.input1Z' ) 

        cmds.setAttr ( dampMult+ '.input2X', .05) #= ??? ??? ??? ?ty?
        cmds.setAttr ( dampMult+ '.input2Y', .35) #= corner jnts ?ty? go along with jaw open
        cmds.setAttr ( dampMult+ '.input2Z', .05) #=  ??? ??? ??? ?tx? or ?tz?

       
        cmds.connectAttr ( dampMult + '.outputX',  midUpJnt+'.ty')
        cmds.connectAttr ( dampMult + '.outputY',  lCorner+'.ty')
        cmds.connectAttr ( dampMult + '.outputY',  rCorner+'.ty')
        cmds.connectAttr ( dampMult + '.outputZ',  midUpJnt + txzPick)
        
indiCrvSetup( 'JawOpen', -0, 2)




upLO_crv upLHappy_crv upLSad_crv upLM_crv uplERollYZ_crv / upURoll_crv
# for E, happy, U, M...start with Capial Letter / ?? ??
import fnmatch
import maya.cmds as cmds 
def indiShapeCrvRig(name, posX, posY):
    #select upLip curves that need joints control ('upJawOpen_crv', 'upUDLR_crv'... )  
    upLCrv = 'upL'+ name + '_crv'
    loLCrv = upLCrv.replace('up', 'lo', 1)

    crvShape = cmds.listRelatives ( upLCrv, c=1, type = 'nurbsCurve')
    crvCVs = cmds.ls ( upLCrv + '.cv[*]', fl = 1 )
    cvNum = len ( crvCVs ) 
       
    lipCrvStartPos = cmds.xform (crvCVs[0], q=1, ws =1, t = 1 )
    lipCrvEndPos = cmds.xform (crvCVs[cvNum-1], q=1, ws =1, t = 1 )   
    nCrvPoc = cmds.shadingNode ( 'pointOnCurveInfo', asUtility =True, n = 'cnt' + name + '_poc' )
    cmds.connectAttr ( crvShape[0]+'.worldSpace',  nCrvPoc + '.inputCurve')   
    cmds.setAttr ( nCrvPoc + '.turnOnPercentage', 1 )    
    cmds.setAttr ( nCrvPoc + '.parameter', .5)    
    lipCrvMidPos = cmds.getAttr( nCrvPoc + '.position')    
    
    lipCrvStart = cmds.group (em = 1, n = name + 'Start_grp' )
    cmds.xform ( lipCrvStart, ws = 1, t = lipCrvStartPos )
    upRCorner = cmds.joint ( n= 'upRCorner'+ name+'_jnt', p= lipCrvStartPos )
    cmds.select ( lipCrvStart, r=1 )
    loRCorner = cmds.joint ( n= 'loRCorner'+ name+'_jnt', p= lipCrvStartPos )  
    
    lipCrvMid = cmds.group (em = 1, n = name + 'Mid_grp' ) 
    cmds.xform ( lipCrvMid, ws = 1, t = list(lipCrvMidPos[0]) ) 
    midUpJnt = cmds.joint ( n = 'cntUp' + name + '_jnt', relative = True, p = [ 0, 0, 0] ) 
    cmds.select ( lipCrvMid, r=1 ) 
    midLoJnt = cmds.joint ( n = 'cntLo' + name + '_jnt', relative = True, p = [ 0, 0, 0] )

    lipCrvEnd = cmds.group (em = 1, n = name + 'End_grp' ) 
    cmds.xform ( lipCrvEnd, ws = 1, t = lipCrvEndPos ) 
    upLCorner = cmds.joint ( n= 'upLCorner' + name + '_jnt', relative = True, p = [ 0, 0, 0] )
    cmds.select (lipCrvEnd, r =1 )
    loLCorner = cmds.joint ( n= 'loLCorner' + name + '_jnt', relative = True, p = [ 0, 0, 0] )  
    
    cmds.parent ( lipCrvStart, lipCrvMid, lipCrvEnd, name+'Crv_indiGrp' ) 
    cmds.parent (indiGrp, 'lipCrv_grp' )
    cmds.setAttr( indiGrp + '.tx', posX )
    cmds.setAttr( indiGrp + '.ty', posY )
    #skinning (cv skin weight input)
    cmds.skinCluster ( upRCorner, midUpJnt, upLCorner, upLCrv, toSelectedBones = 1 )  
    cmds.skinCluster ( loRCorner, midLoJnt, loLCorner, loLCrv, toSelectedBones = 1 )
        
        # skin weight number / blendShape mirror weight!!!!!!!!!!!!!!!!
    
indiShapeCrvRig('O', 0, 4) 







import maya.cmds as cmds 
def indiShapeCrvRig(name, posX, posY, typeAB ):
    #select upLip curves that need joints control ('upJawOpen_crv', 'upUDLR_crv'... )  
    upLCrv = 'upL'+ name + '_crv'
    loLCrv = upLCrv.replace('up', 'lo', 1)
    upRCrv = 'upR'+ name + '_crv'
    loRCrv = upLCrv.replace('up', 'lo', 1)
    crvShape = cmds.listRelatives ( upLCrv, c=1, type = 'nurbsCurve')
    crvCVs = cmds.ls ( upLCrv + '.cv[*]', fl = 1 )
    cvNum = len ( crvCVs ) 
       
    lipCrvStartPos = cmds.xform (crvCVs[0], q=1, ws =1, t = 1 )
    lipCrvEndPos = cmds.xform (crvCVs[cvNum-1], q=1, ws =1, t = 1 )
    nCrvPoc = cmds.shadingNode ( 'pointOnCurveInfo', asUtility =True, n = 'cnt' + name + '_poc' )
    cmds.connectAttr ( crvShape[0]+'.worldSpace',  nCrvPoc + '.inputCurve')   
    cmds.setAttr ( nCrvPoc + '.turnOnPercentage', 1 )    
    cmds.setAttr ( nCrvPoc + '.parameter', .5)
    lipCrvMidPos = cmds.getAttr( nCrvPoc + '.position')
    
    lipCrvStart = cmds.group (em = 1, n = name + 'Start_grp' )
    cmds.xform ( lipCrvStart, ws = 1, t = lipCrvStartPos )
    rCorner = cmds.joint ( n= 'rCorner'+ name+'_jnt', p= lipCrvStartPos ) 
    
    uplipCrvMid = cmds.group (em = 1, n = 'up' + name + 'Mid_grp' ) 
    cmds.xform ( uplipCrvMid, ws = 1, t = list(lipCrvMidPos[0]) ) 
    midUpJnt = cmds.joint ( n = 'cntUp' + name + '_jnt', relative = True, p = [ 0, 0, 0] )  

    lolipCrvMid = cmds.group (em = 1, n = 'lo' + name + 'Mid_grp') 
    cmds.xform ( lolipCrvMid, ws = 1, t = list(lipCrvMidPos[0]) ) 
    midLoJnt = cmds.joint ( n = 'cntLo' + name + '_jnt', relative = True, p = [ 0, 0, 0] )

    lipCrvEnd = cmds.group (em = 1, n = name + 'End_grp' ) 
    cmds.xform ( lipCrvEnd, ws = 1, t = lipCrvEndPos ) 
    lCorner = cmds.joint ( n= 'lCorner' + name + '_jnt', relative = True, p = [ 0, 0, 0] )  
    
    crvList = cmds.listRelatives ( 'crv_grp', allDescendents = 1, type = 'transform' )
    if fnmatch.filter ( crvList, '*%s*'% name):
        indiCrvs = fnmatch.filter ( crvList, '*%s*'% name)
        indiGrp = cmds.group ( lipCrvStart, uplipCrvMid, lolipCrvMid, lipCrvEnd, indiCrvs, n = name + '_indiGrp' ) 
        cmds.parent (indiGrp, 'lipCrv_grp' )
        cmds.setAttr( indiGrp + '.tx', posX )
        cmds.setAttr( indiGrp + '.ty', posY )
        #skinning (cv skin weight input)
        cmds.skinCluster ( rCorner, midUpJnt, lCorner, upLCrv, toSelectedBones = 1 )  
        cmds.skinCluster ( rCorner, midUpJnt, lCorner, upRCrv, toSelectedBones = 1 )   
        cmds.skinCluster ( rCorner, midLoJnt, lCorner, loLCrv, toSelectedBones = 1 )
        cmds.skinCluster ( rCorner, midLoJnt, lCorner, loRCrv, toSelectedBones = 1 )
        
    # skin weight number / blendShape mirror weight!!!!!!!!!!!!!!!!

    if type == 'B':
                
        cornerMult = cmds.shadingNode ( 'multiplyDivide', asUtility=True, n = name +'_mult' )
        dampMult = cmds.shadingNode ( 'multiplyDivide', asUtility=True, n = name + 'damp_mult' )
        txAvg = cmds.shadingNode ( 'plusMinusAverage', asUtility=True, n = name + 'TX_plus')  
        
        #?ty? ? ?? ????? inputX,Y?  ??? tx ? tz?  inputZ ? ??.
        txzPick = ['.' + myAttr ]
        cmds.connectAttr ( midLoJnt+ '.ty', cornerMult+ '.input1X' )  
        cmds.connectAttr ( midLoJnt+ '.ty', cornerMult+ '.input1Y' )  
        cmds.connectAttr ( midLoJnt + txzPick, cornerMult+ '.input1Z' ) 
        cmds.setAttr ( cornerMult + '.input2X', .1) #= lCorner jnts move inside(tx) as jaw open
        cmds.setAttr ( cornerMult + '.input2Y', .1) #= rCorner jnts move inside(tx) as jaw open 
        cmds.setAttr ( cornerMult + '.input2Z', -.3) #= corner jnts (tx or tz) go along as jaw moving tx

        cmds.connectAttr ( cornerMult + '.outputX', txAvg + '.input3D[0].input3Dx' )
        cmds.connectAttr ( cornerMult + '.outputY', txAvg + '.input3D[0].input3Dy' )
        cmds.connectAttr ( cornerMult + '.outputZ', txAvg + '.input3D[1].input3Dx' )
        cmds.connectAttr ( cornerMult + '.outputZ', txAvg + '.input3D[1].input3Dy' )
        cmds.connectAttr ( txAvg + '.output3Dx', lCorner +  txzPick)
        cmds.connectAttr ( txAvg + '.output3Dy', rCorner + txzPick )

        # lip corners translateY go along with jaw open
        cmds.connectAttr ( midLoJnt+ '.ty', dampMult + '.input1X' )  
        cmds.connectAttr ( midLoJnt+ '.ty', dampMult + '.input1Y' )  
        cmds.connectAttr ( midLoJnt + txzPick, dampMult + '.input1Z' ) 

        cmds.setAttr ( dampMult+ '.input2X', .05) #= ??? ??? ??? ?ty?
        cmds.setAttr ( dampMult+ '.input2Y', .35) #= corner jnts ?ty? go along with jaw open
        cmds.setAttr ( dampMult+ '.input2Z', .05) #=  ??? ??? ??? ?tx? or ?tz?

       
        cmds.connectAttr ( dampMult + '.outputX',  midUpJnt+'.ty')
        cmds.connectAttr ( dampMult + '.outputY',  lCorner+'.ty')
        cmds.connectAttr ( dampMult + '.outputY',  rCorner+'.ty')
        cmds.connectAttr ( dampMult + '.outputZ',  midUpJnt + txzPick)
        
indiCrvSetup( 'JawOpen', -0, 2)














import maya.cmds as cmds 
def indiCrvSetup(name, posX, posY, typeAB ):
    #select upLip curves that need joints control ('upJawOpen_crv', 'upUDLR_crv'... )  
    crv = 'up'+ name + '_crv'
    loCrv = crv.replace('up', 'lo', 1)
    crvShape = cmds.listRelatives ( crv, c=1, type = 'nurbsCurve')
    crvCVs = cmds.ls ( crv + '.cv[*]', fl = 1 )
    cvNum = len ( crvCVs ) 
       
    lipCrvStartPos = cmds.xform (crvCVs[0], q=1, ws =1, t = 1 )
    lipCrvEndPos = cmds.xform (crvCVs[cvNum-1], q=1, ws =1, t = 1 )
    nCrvPoc = cmds.shadingNode ( 'pointOnCurveInfo', asUtility =True, n = 'cnt' + name + '_poc' )
    cmds.connectAttr ( crvShape[0]+'.worldSpace',  nCrvPoc + '.inputCurve')   
    cmds.setAttr ( nCrvPoc + '.turnOnPercentage', 1 )    
    cmds.setAttr ( nCrvPoc + '.parameter', .5)
    lipCrvMidPos = cmds.getAttr( nCrvPoc + '.position')
    
    lipCrvStart = cmds.group (em = 1, n = name + 'Start_grp' )
    cmds.xform ( lipCrvStart, ws = 1, t = lipCrvStartPos )
    rCorner = cmds.joint ( n= 'rCorner'+ name+'_jnt', p= lipCrvStartPos ) 
    
    uplipCrvMid = cmds.group (em = 1, n = 'up' + name + 'Mid_grp' ) 
    cmds.xform ( uplipCrvMid, ws = 1, t = list(lipCrvMidPos[0]) ) 
    midUpJnt = cmds.joint ( n = 'cntUp' + name + '_jnt', relative = True, p = [ 0, 0, 0] )  

    lolipCrvMid = cmds.group (em = 1, n = 'lo' + name + 'Mid_grp') 
    cmds.xform ( lolipCrvMid, ws = 1, t = list(lipCrvMidPos[0]) ) 
    midLoJnt = cmds.joint ( n = 'cntLo' + name + '_jnt', relative = True, p = [ 0, 0, 0] )

    lipCrvEnd = cmds.group (em = 1, n = name + 'End_grp' ) 
    cmds.xform ( lipCrvEnd, ws = 1, t = lipCrvEndPos ) 
    lCorner = cmds.joint ( n= 'lCorner' + name + '_jnt', relative = True, p = [ 0, 0, 0] )  
    crvList = cmds.listRelatives ( 'crv_grp', allDescendents = 1, type = 'transform' )
    if objExists(name + ) in crvList:
        indiCrvs = fnmatch.filter ( crvList, '*%s*'% name)
        indiGrp = cmds.group ( lipCrvStart, uplipCrvMid, lolipCrvMid, lipCrvEnd, indiCrvs, n = name + '_indiGrp' ) 
        cmds.parent (indiGrp, 'lipCrv_grp' )
        cmds.setAttr( indiGrp + '.tx', posX )
        cmds.setAttr( indiGrp + '.ty', posY )
        #skinning (cv skin weight input)
        cmds.skinCluster ( rCorner, midUpJnt, lCorner, crv, toSelectedBones = 1 )    
        cmds.skinCluster ( rCorner, midLoJnt, lCorner, loCrv, toSelectedBones = 1 )

    if type == 'B':
                
        cornerMult = cmds.shadingNode ( 'multiplyDivide', asUtility=True, n = name +'_mult' )
        dampMult = cmds.shadingNode ( 'multiplyDivide', asUtility=True, n = name + 'damp_mult' )
        txAvg = cmds.shadingNode ( 'plusMinusAverage', asUtility=True, n = name + 'TX_plus')  
        
        #?ty? ? ?? ????? inputX,Y?  ??? tx ? tz?  inputZ ? ??.
        txzPick = ['.' + myAttr ]
        cmds.connectAttr ( midLoJnt+ '.ty', cornerMult+ '.input1X' )  
        cmds.connectAttr ( midLoJnt+ '.ty', cornerMult+ '.input1Y' )  
        cmds.connectAttr ( midLoJnt + txzPick, cornerMult+ '.input1Z' ) 
        cmds.setAttr ( cornerMult + '.input2X', .1) #= lCorner jnts move inside(tx) as jaw open
        cmds.setAttr ( cornerMult + '.input2Y', .1) #= rCorner jnts move inside(tx) as jaw open 
        cmds.setAttr ( cornerMult + '.input2Z', -.3) #= corner jnts (tx or tz) go along as jaw moving tx

        cmds.connectAttr ( cornerMult + '.outputX', txAvg + '.input3D[0].input3Dx' )
        cmds.connectAttr ( cornerMult + '.outputY', txAvg + '.input3D[0].input3Dy' )
        cmds.connectAttr ( cornerMult + '.outputZ', txAvg + '.input3D[1].input3Dx' )
        cmds.connectAttr ( cornerMult + '.outputZ', txAvg + '.input3D[1].input3Dy' )
        cmds.connectAttr ( txAvg + '.output3Dx', lCorner +  txzPick)
        cmds.connectAttr ( txAvg + '.output3Dy', rCorner + txzPick )

        # lip corners translateY go along with jaw open
        cmds.connectAttr ( midLoJnt+ '.ty', dampMult + '.input1X' )  
        cmds.connectAttr ( midLoJnt+ '.ty', dampMult + '.input1Y' )  
        cmds.connectAttr ( midLoJnt + txzPick, dampMult + '.input1Z' ) 

        cmds.setAttr ( dampMult+ '.input2X', .05) #= ??? ??? ??? ?ty?
        cmds.setAttr ( dampMult+ '.input2Y', .35) #= corner jnts ?ty? go along with jaw open
        cmds.setAttr ( dampMult+ '.input2Z', .05) #=  ??? ??? ??? ?tx? or ?tz?

       
        cmds.connectAttr ( dampMult + '.outputX',  midUpJnt+'.ty')
        cmds.connectAttr ( dampMult + '.outputY',  lCorner+'.ty')
        cmds.connectAttr ( dampMult + '.outputY',  rCorner+'.ty')
        cmds.connectAttr ( dampMult + '.outputZ',  midUpJnt + txzPick)
        
indiCrvSetup( 'JawOpen', -0, 2)
