#create browDetail Controller (miNum = number of lidJoints )    
'''control parent name should be "browDetailCtrl0" and have the scale value ( 1, 1, 1) '''
import maya.cmds as cmds
def browDetailCtls ( miNum ):        
    browJnts = cmds.ls ( "*BrowBase*", fl = True, type = "joint" )
    jntNum = len(browJnts)
    browJnts.sort()
    z = [ browJnts[0] ]
    y = browJnts[1:jntNum/2+1]
    browJnts.reverse()
    x = browJnts[:jntNum/2]
    orderJnts = x + z + y    
    ctlP = "browDetailCtrl0"
    kids = cmds.listRelatives (ctlP, ad=True, type ='transform')   
    if kids:
        cmds.delete (kids)
        
    attTemp = ['scaleX','scaleY','scaleZ', 'rotateX','rotateY','rotateZ', 'tz', 'visibility' ]  
    index = 0
    for jnt in orderJnts:
                        
        detailCtl = cmds.circle ( n = 'browDetail' + str(index+1).zfill(2), ch=False, o =True, nr = ( 0, 0, 1), r = 0.2 )
        detailPlane = cmds.nurbsPlane ( ax = ( 0, 0, 1 ), w = 0.1,  lengthRatio = 10, degree = 3, ch=False, n = 'browDetail'+ str(index+1).zfill(2) + 'P' )
        increment = 2.0/(jntNum-1)
        cmds.parent (detailCtl[0], detailPlane[0], relative=True )
        cmds.parent (detailPlane[0], ctlP, relative=True )
        cmds.setAttr (detailPlane[0] + '.tx', -2 + increment*index*2 )
        cmds.xform ( detailCtl[0], r =True, s = (0.2, 0.2, 0.2))  
        cmds.setAttr (detailCtl[0] +".overrideEnabled", 1)
        cmds.setAttr (detailCtl[0] +"Shape.overrideEnabled", 1)
        cmds.setAttr( detailCtl[0]+"Shape.overrideColor", 20)        
        
        cmds.transformLimits ( detailCtl[0] , tx = ( -.4, .4), etx=( True, True) )
        cmds.transformLimits ( detailCtl[0], ty = ( -.8, .8), ety=( True, True) )
        
        for att in attTemp:
            cmds.setAttr (detailCtl[0] +"."+ att, lock = True, keyable = False, channelBox =False)
                
        index = index + 1

