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

    lipRollJot = cmds.joint(n = upLow + 'lipRollJot' + str(i) + '_jnt', relative = True, p = [ 0, 0, 0] ) 

