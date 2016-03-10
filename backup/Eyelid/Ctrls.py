#create LidCurve
# UI = controller size, offset   
'''
select base joints and run the script  
premise : L/R eyeBall position is symetrical
upLoEyeLid : should be either one of "upLf" or "loLf"
'''

import maya.cmds as cmds
import Func
reload(Func)
import Base
reload(Base)

class Ctrls(Func.Func, Base.Base):
    def __init__(self, baseJnts, ctlSize = 1, rotateScale = 10, **kw):
        """
        initializing variables
        """
        self.initialX         = 0
        self.ctlSize          = ctlSize
        self.baseJnts         = baseJnts
        self.rotateScale      = rotateScale
        
        #- local variables
        Func.Func.__init__(self, **kw)
        Base.Base.__init__(self, **kw)

    def createLidCtrls (self, uplo = 'up'):
        
        if not (self.lEyeLoc):
            print "create the face locators"
            
        else: 
            eyeRotY = cmds.getAttr (self.lEyeLoc + '.ry' ) 
            eyeCenterPos = cmds.xform(self.lEyeLoc, t = True, q = True, ws = True) 
      
        for lr in self.prefix:
            #- left right + upper lower prefix
            uploPrefix = lr + uplo
            
            #- creating crv group nodes
            lidCrvGrp = cmds.group ( n = uploPrefix + 'crv' + self.grpSuffix, em =True )    
            topJnt = [jnt for jnt in self.baseJnts if jnt.startswith(lr)]
            tempJnts = cmds.listRelatives ( topJnt, ad =True )
            childJnts = cmds.ls (uploPrefix + '*%s*%s' %(self.blinkJntName, self.jntSuffix)) 
            wideJnts = cmds.ls (uploPrefix + '*%s*%s' %(self.wideJntName, self.jntSuffix))
            childJnts.sort()
            wideJnts.sort()
            jntNum = len(childJnts)/2
            
            lidsGrp = cmds.group (em=True, w =True, n = uploPrefix + 'Eyelid' + self.ctlSuffix + self.grpSuffix)
            if lr == self.prefix[0]:
                cmds.xform (lidsGrp, ws = True, t = eyeCenterPos)
                cmds.setAttr (lidsGrp + ".ry", eyeRotY)
            else:
                cmds.xform (lidsGrp, ws = True, t = (-eyeCenterPos[0], eyeCenterPos[1], eyeCenterPos[2]))
                cmds.setAttr (lidsGrp + ".ry", -eyeRotY)                
            
            #- final lid shape curve
            lidCrv = cmds.curve ( d = 3, p =([0,0,0],[0.33,0,0],[0.66,0,0],[1,0,0])) 
            cmds.rebuildCurve ( rt = 0, d = 1, kr = 0, s = jntNum-1 )  
            tempCrv = cmds.rename (lidCrv, uploPrefix +'LidCrv')
            cmds.parent (tempCrv, lidCrvGrp)
            lidCrvShape = cmds.listRelatives (tempCrv, c = True )
            
            wideJntCrv = cmds.duplicate ( tempCrv, n= uploPrefix +'WideJntCrv') 
            wideJntCrvShape = cmds.listRelatives ( wideJntCrv, c = True ) 

            #- eyelids controller curve shape ( different number of points, so can not be target of the blendShape)      
            lidCtlCrv = cmds.curve ( d = 3, p =([0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0], [1,0,0]))
            #- rebuildCurve? 
            #cmds.rebuildCurve ( rt = 0, d = 1, kr = 0, s = jntNum-1 )  
            tempCtlCrv = cmds.rename (lidCtlCrv, uploPrefix +'CtlCrv')
            lidCtlCrvShape = cmds.listRelatives ( tempCtlCrv, c = True ) 
            cmds.parent (tempCtlCrv, lidCrvGrp) 

            #- eyeClose(blink) lid shape        
            blinkCrv = cmds.duplicate ( tempCrv, n= uploPrefix +'BlinkCrv')
            
            #- eyeWide(suprise) lid shape        
            wideCrv = cmds.duplicate ( tempCrv, n= uploPrefix +'WideCrv')
                        
            #- eyeSquint lid shape        
            squintCrv = cmds.duplicate ( tempCrv, n= uploPrefix +'SquintCrv') 
                        
            if lr == self.prefix[1]: 
                cmds.hide (blinkCrv, wideCrv, squintCrv)
                        
            #- eyeDirection lid shape        
            lookUp = cmds.duplicate ( tempCrv, n= uploPrefix +'LookUpCrv') 


            lookDn = cmds.duplicate ( tempCrv, n= uploPrefix +'LookDnCrv') 
            lookLeft = cmds.duplicate ( tempCrv, n= uploPrefix +'LookLeftCrv')                 
            lookRight = cmds.duplicate ( tempCrv, n= uploPrefix +'LookRightCrv') 

            crvBS = cmds.blendShape ( blinkCrv[0], lookUp[0], lookDn[0], lookLeft[0], lookRight[0], tempCrv, n = uploPrefix + 'LidCrvBS' )
            cmds.blendShape( crvBS[0], edit=True, w=[(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)] )
              
            wideBS = cmds.blendShape ( wideCrv[0], squintCrv[0], wideJntCrv, n = uploPrefix + 'WideJntBS' )
            cmds.blendShape( wideBS[0], edit=True, w=[(0, 1), (1, 1)] )
            
            index = 0 
            indices = 0

            for jnt in childJnts:
                print 'jnt : ', jnt
                miValue = 1
                wideJnt = wideJnts[index]
                childJnt = cmds.listRelatives (jnt, c =True)
                childPos = cmds.xform ( childJnt[0], t = True, q = True, ws = True)
                jntIndex = jnt.split(self.jntSuffix)[0].split('Blink')[1]
                #pocNode on the final lid curve 
                pocNode = cmds.shadingNode ( 'pointOnCurveInfo', asUtility=True, n = uploPrefix + 'Poc' + jntIndex)
                cmds.connectAttr ( lidCrvShape[0] + ".worldSpace",  pocNode + '.inputCurve')   
                cmds.setAttr ( pocNode + '.turnOnPercentage', 1 )        
                increment = 1.0/(jntNum-1)
                cmds.setAttr ( pocNode + '.parameter', increment *index )     
                initialX = cmds.getAttr (pocNode + '.positionX')
                
                #- pocNode on the wideJnt curve
                wideJntPocNode = cmds.shadingNode ( 'pointOnCurveInfo', asUtility=True, n = uploPrefix + 'wideJntPoc' + jntIndex)
                cmds.connectAttr ( wideJntCrvShape[0] + ".worldSpace",  wideJntPocNode + '.inputCurve')   
                cmds.setAttr ( wideJntPocNode + '.turnOnPercentage', 1 )        
                cmds.setAttr ( wideJntPocNode + '.parameter', increment *index )  
                
                #- pocNode on the eyelids ctls curve
                ctlPocNode = cmds.shadingNode ( 'pointOnCurveInfo', asUtility=True, n = uploPrefix + 'CtlPoc' + jntIndex)
                cmds.connectAttr ( lidCtlCrvShape[0] + ".worldSpace", ctlPocNode + '.inputCurve')   
                cmds.setAttr ( ctlPocNode + '.turnOnPercentage', 1 )        
                cmds.setAttr ( ctlPocNode + '.parameter', increment *index ) 
                
                #- creating controller 
                lidCtl = cmds.circle ( n = uploPrefix + 'EyeLid' + jntIndex + self.ctlSuffix, ch=False, o =True, nr = ( 0, 0, 1), r = self.ctlSize*0.1 )
                cmds.xform ( lidCtl[0], ws = True, t = ( childPos[0], childPos[1], childPos[2]+ self.ctlSize*0.1)) 
                cmds.parent ( lidCtl[0], lidsGrp )
                print 'lidCtl : ', lidCtl
                lidCtlP = cmds.duplicate ( lidCtl[0], po = True, n = uploPrefix + 'EyeLid' + jntIndex + self.ctlSuffix + self.grpSuffix)
                cmds.parent ( lidCtl[0], lidCtlP[0] )
                cmds.parentConstraint ( childJnt[0], lidCtlP[0], mo = True)
                index = index + 1
                
                self.crvCtrlToJnt ( uploPrefix, lidCtl, jnt, wideJnt, pocNode, wideJntPocNode, ctlPocNode, initialX, self.rotateScale , miValue, index )