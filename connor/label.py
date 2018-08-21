# -*- coding: utf-8 -*-

#from PyQt5 import QtWidgets,  Qt
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt,  pyqtSignal,  QEvent
import bookmark

class MyLabel(QtWidgets.QLabel):
    moveFlag = False
    showMenu = False
    _exit = pyqtSignal()
    _input = pyqtSignal()
    _shutdown = pyqtSignal(str)
    _connorTip = pyqtSignal(int)
    #changeOpacity = pyqtSignal(str)
    def mousePressEvent(self,  event):
        if event.button() == Qt.RightButton:
            #self.createRightMenu()
            #self.customContextMenuRequested.connect(self.showRightMenu)
            self.showMenu = True
            event.ignore()
        
        if event.button() == Qt.LeftButton :
            self.showMenu = False
            #print('menu')
            event.ignore()
    
    def createRightMenu(self):
        #创建右键菜单必须将ContextMenuPolicy设置为Qt.CustomContextMenu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showRightMenu)
        
        #self.contextMenu = QtWidgets.QMenu(self)
        self.contextMenu = Menu(self)
        self.inputContent = self.contextMenu.addAction('信息查询')
        self.shutdown = self.contextMenu.addAction('关机')
        #self.bookMark = self.contextMenu.addMenu(Menu('收藏夹'))
        self.bookmarkMenu = Menu('收藏夹')
        self.contextMenu.insertMenu(QtWidgets.QAction(),  self.bookmarkMenu)
        
        #self.test = self.bookMark.addAction('test')
        self.actionExit = self.contextMenu.addAction('退出')
        #为菜单项添加触发函数
        self.folderHandler = locals()
        bookmarkDict = bookmark.readBookMark(self.folderHandler)
        if type(bookmarkDict) == int:
            self._connorTip.emit(bookmarkDict)
        else:
            bookmark.createBookmarkMenu(self.folderHandler, bookmarkDict,  self.bookmarkMenu)
        #self.test.triggered.connect(lambda: self.openUrl('test'))
        self.shutdown.triggered.connect(self.shutdownHandler)
        self.inputContent.triggered.connect(self.inputHandler)
        self.actionExit.triggered.connect(self.exitHandler)
        #print('create')
    
    def showRightMenu(self):
         self.showMenu = True
         self.contextMenu.exec_(QCursor.pos())      #通过鼠标位置确定右键菜单的显示位置
         
    def shutdownHandler(self):
        self._shutdown.emit('shutdown')
        #os.system('C:\\Windows\\System32\\SlideToShutDown.exe')
         
    def inputHandler(self):    
        self._input.emit()
        
    def exitHandler(self):
         self._exit.emit() 
       
class Menu(QtWidgets.QMenu):
    def event(self,  e):
        #print(e.type())
        if e.type() == QEvent.ToolTip:
            he = QHelpEvent(e)
            act = self.actionAt(he.pos())
            if act:
                QtWidgets.QToolTip.showText(he.globalPos(),  act.toolTip())
                return True
        else:
            QtWidgets.QMenu.event(self, e)
        return False
