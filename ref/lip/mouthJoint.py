#create face rig first ( parent group node for face curves, joints, ctrls ) ; 
‘’’입술 버텍스 선택하고 실행 -mouthJoint( 'hi', 'lo' ) 
가이드 커브에 따라 입술 조인트 생성 / 입술모양 커브 / 디테일 컨트롤러
select the upper or lower lip verts  and run
lip detail parent should be changed to "upLipDetailGrp" "loLipDetailGrp”
“loLipDetailGrp” tx= -2 / ty = -1.5 / sx = 4
upLipDetailGrp” tx= -2 / ty = 1.5 / sx = 4’’’

def mouthJoint( upLow ): 
    verts = cmds.ls( os = True, fl = True)  
    vNum = len (verts) + 2       
    lipEPos = cmds.xform( 'lipEPos', t = True, q = True, ws = True) 
    lipNPos = cmds.xform( 'lipNPos', t = True, q = True, ws = True) 
    lipSPos = cmds.xform( 'lipSPos', t = True, q = True, ws = True) 
    lipYPos = cmds.xform( 'lipYPos', t = True, q = True, r = True) 
    JawRigPos = cmds.xform( 'JawRigPos', t = True, q = True, ws = True) 
    
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
    lipCrvGrp = cmds.group ( n = upLow +'LipCrv_grp', em =True, p = 'faceMain|crv_grp' ) 
    templipCrv = cmds.curve ( d = 3, p =([0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0])) 
    cmds.rebuildCurve ( rt = 0, d = 3, kr = 0, s = 2)    
    lipCrv = cmds.rename (templipCrv, upLow +'Lip_crv')
    lipCrvShape = cmds.listRelatives ( lipCrv, c = True )
    cmds.parent ( lipCrv, lipCrvGrp )

    # lipTarget curve shape
    jawOpenCrv = cmds.duplicate ( lipCrv, n= upLow +'JawOpen_crv') 
    lipwideCrv = cmds.duplicate ( lipCrv, n= upLow +'lipWide_crv') 
    OCrv = cmds.duplicate ( lipCrv, n= upLow +'U_crv') 
    happyCrv = cmds.duplicate ( lipCrv, n= upLow +'Happy_crv') 
    lipCrvBS = cmds.blendShape ( jawOpenCrv[0], lipwideCrv[0], OCrv[0], happyCrv[0], lipCrv, n =upLow + 'LipCrvBS')
    cmds.blendShape( lipCrvBS[0], edit=True, w=[(0, 1), (1, 1), (2, 1), (3, 1)])   
    
    # lip controller curve shape ( different number of points (4), so can not be target of the blendShape)      
    templipCtlCrv = cmds.curve ( d = 3, p =([0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0])) 
    cmds.rebuildCurve ( rt = 0, d = 3, kr = 0, s = 2)   
    lipCtlCrv = cmds.rename ( templipCtlCrv, upLow +'LipCtl_crv')
    lipCtlCrvShape = cmds.listRelatives ( lipCtlCrv, c = True ) 
    cmds.parent (lipCtlCrv, lipCrvGrp) 
    # create lip joints parent group
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
        # create lipCtrl curve POC
        lipCrvPoc = cmds.shadingNode ( 'pointOnCurveInfo', asUtility =True, n = upLow +'LipCrv' + str(i) + '_poc'  )
        cmds.connectAttr ( lipCrvShape[0] + ".worldSpace",  lipCrvPoc + '.inputCurve')   
        cmds.setAttr ( lipCrvPoc  + '.turnOnPercentage', 1 )    
        cmds.setAttr ( lipCrvPoc  + '.parameter', increment*i ) 
        # create lipCtrl curve POC
        ctlPoc = cmds.shadingNode ( 'pointOnCurveInfo', asUtility =True, n = upLow +'LipCtl' + str(i) + '_poc' )
        cmds.connectAttr ( lipCtlCrvShape[0] + ".worldSpace",  ctlPoc + '.inputCurve')   
        cmds.setAttr ( ctlPoc  + '.turnOnPercentage', 1 )    
        cmds.setAttr ( ctlPoc  + '.parameter', increment*i )   

