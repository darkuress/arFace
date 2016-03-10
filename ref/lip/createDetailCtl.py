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

