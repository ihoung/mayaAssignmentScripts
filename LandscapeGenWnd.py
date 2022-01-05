from functools import partial
import maya.cmds as cmds
from maya.common.ui import LayoutManager
import LandscapeGenerator as lg

reload(lg)

class LandscapeGenWnd:
    def __init__(self):
        self.m_landscapeType = 'Grass'
        self.m_historyList = []

    def createGenWnd(self, pWindowTitle):
        windowID = 'LandscapeGenerator'
        if cmds.window(windowID, exists=True):
            cmds.deleteUI(windowID)
        
        wnd = cmds.window(windowID, title=pWindowTitle, sizeable=True, resizeToFitChildren=True)
        self.genWndGUI(windowID)
        cmds.showWindow(wnd)


    def genWndGUI(self, wndID):
        with LayoutManager(cmds.columnLayout(columnAttach=('left', 5), rowSpacing=10, cw=300)):
            typeMenu = cmds.optionMenu('LandscapeType', label='Type ')
            cmds.menuItem('Grass', label='Grass', parent=typeMenu)
            cmds.menuItem('Bush', label='Bush', parent=typeMenu)
            cmds.menuItem('Tree', label='Tree', parent=typeMenu)
            cmds.menuItem('Rock', label='Rock', parent=typeMenu)
            cmds.intSliderGrp('Density', field=True, label='Density ')
            with LayoutManager(cmds.columnLayout(columnAttach=('left', 5), rowSpacing=10, cw=300)) as ctrlTab:
                cmds.floatSliderGrp('MinScale', field=True, label='Min Scale ', minValue=0.0, value=1.0)
                cmds.floatSliderGrp('MaxScale', field=True, label='Max Scale ', minValue=0.0, value=1.0)
                cmds.optionMenu(typeMenu, e=True, changeCommand=partial(self.menuItemOnChg, ctrlTab=ctrlTab))
            
            cmds.separator()
            dirBtnGrp = cmds.radioButtonGrp('GrowingDirection', label='Growing Direction ', nrb=3, labelArray3=['Up', 'Surface Normal', 'Customized'], sl=2, changeCommand3=self.customizedBtnOnChg)
            cmds.floatFieldGrp('CustomizedDir', numberOfFields=3, label='xyz', v1=0.0, v2=1.0, v3=0.0, vis=False)
            cmds.checkBox('NaturalGrowing', label='Natural Growing',  parent=dirBtnGrp)

            cmds.separator()
            cmds.separator()
            cmds.separator()
            cmds.button('Undo', label='Undo', command=self.undoCallback)
        with LayoutManager(cmds.rowLayout(nc=3, adj=True, columnWidth=[(1,150), (2,150), (3,150)], columnAttach=[(1, 'both', 10), (2, 'both', 10), (3, 'both', 10)])):
            cmds.button('Accept', label='Accept', command=partial(self.acceptCallback, wndID))
            cmds.button('Apply', label='Apply', command=self.applyCallback)
            cmds.button('Cancel', label='Cancel', command=partial(self.cancelCallback, wndID))


    def menuItemOnChg(self, opt, ctrlTab):
        childUI = cmds.columnLayout(ctrlTab, q=True, childArray=True)
        # print(childUI)
        if childUI != None:
            for node in childUI:
                cmds.deleteUI(node)

        if opt == 'Rock':
            cmds.text('GeneralSize', label='General Size: ', parent=ctrlTab)
            cmds.floatSliderGrp('MinScale', field=True, label='Min Size ', minValue=0.0, value=1.0, parent=ctrlTab)
            cmds.floatSliderGrp('MaxScale', field=True, label='Max Size ', minValue=0.0, value=1.0, parent=ctrlTab)
            cmds.text('SingleRock', label='Shape Turbulence of Single Rock: ', parent=ctrlTab)
            cmds.floatSliderGrp('SizeTurb', field=True, label='Size Turbulence', minValue=0.0, value=0.0, parent=ctrlTab)
            cmds.floatSliderGrp('ShapeTurb', field=True, label='Shape Turbulence ', minValue=1.0, value=2.0, parent=ctrlTab)
        else:
            cmds.floatSliderGrp('MinScale', field=True, label='Min Scale ', minValue=0.0, value=1.0, parent=ctrlTab)
            cmds.floatSliderGrp('MaxScale', field=True, label='Max Scale ', minValue=0.0, value=1.0, parent=ctrlTab)

        self.m_landscapeType = opt


    def customizedBtnOnChg(self, sl):
        cmds.floatFieldGrp('CustomizedDir', e=True, vis=sl)

    
    def undoCallback(self, *args):
        numHistory = len(self.m_historyList)
        if numHistory == 0:
            cmds.warning('No operation history!')
            return
        undoNode = self.m_historyList[numHistory-1]
        cmds.delete(undoNode)
        self.m_historyList.remove(undoNode)
    
    
    def cancelCallback(self, wndID, *args):
        if(cmds.window(wndID, exists=True)):
            cmds.deleteUI(wndID)


    def acceptCallback(self, wndID, *args):
        self.applyCallback()
        self.cancelCallback(wndID)


    def applyCallback(self, *args):
        minScale = cmds.floatSliderGrp('MinScale', q=True, v=True)
        maxScale = cmds.floatSliderGrp('MaxScale', q=True, v=True)
        if maxScale < minScale:
            maxScale = minScale
            cmds.floatSliderGrp('MaxScale', e=True, v=minScale)

        density = cmds.intSliderGrp('Density', q=True, v=True)

        dirOptIndex = cmds.radioButtonGrp('GrowingDirection', q=True, sl=True)
        isNaturalGrw = cmds.checkBox('NaturalGrowing', q=True, v=True)
        customizedDir = cmds.floatFieldGrp('CustomizedDir', q=True, v=True)

        if self.m_landscapeType == 'Rock':
            sizeTurb = cmds.floatSliderGrp('SizeTurb', q=True, v=True)
            shapeTurb = cmds.floatSliderGrp('ShapeTurb', q=True, v=True)
            historyNode = lg.generateObj(self.m_landscapeType, density, minScale, maxScale, dirOptIndex, isNaturalGrw, sizeTurb, shapeTurb, customizedDir)
            self.m_historyList.append(historyNode)
        else:
            historyNode = lg.generateObj(self.m_landscapeType, density, minScale, maxScale, dirOptIndex, isNaturalGrw, customizedDir=customizedDir)    
            self.m_historyList.append(historyNode)



# creatGenWnd('Landscape Generator')
if __name__ == '__main__':
   LandscapeGenWnd().createGenWnd('Landscape Generator') 