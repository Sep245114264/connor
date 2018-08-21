# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'G:\PyQt5\connor\Main.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!
#from label import MyLabel
#from animate import Animate
#from autoFormat import formatString
#from trayIcon import TrayIcon
#from lineEdit import MyLineEdit

from PyQt5 import QtCore, QtGui, QtWidgets,  sip
from PyQt5.QtCore import Qt,  pyqtSignal
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication
import  label,  animate,  autoFormat,  trayIcon,  lineEdit,  orderProcess,  uuid,  datetime,  os,  sys,  bookmark

workDir = os.path.abspath('.')
waitGif = workDir + r'\connor\connor_process_wait.gif'
arrowPic = workDir + r'\connor\dialogArrow.png'

class Ui_MainWindow(QtWidgets.QWidget):
    _hidden = pyqtSignal()
    netAccess = False
    action = 'exit'
    def setupUi(self, MainWindow):
        #stringTextWidth = len(text)*20

        MainWindow.setObjectName("MainWindow")
        #MainWindow.resize(1920, 1024)
        #MainWindow.move(0, 0)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        
        self.connor = label.MyLabel(self.centralWidget)
        self.connor.setGeometry(QtCore.QRect(150, 100, 248, 351))
        self.connor.setObjectName("connor")
        self.connor._exit.connect(self.exiting)
        self.connor._input.connect(self.inputFunction)
        self.connor._connorTip.connect(self.displayDialog)
        self.connor._shutdown.connect(self.exiting)
        
        self.moveWindow(MainWindow)
      
        MainWindow.setCentralWidget(self.centralWidget)
        
        self.animate = animate.Animate()
        self.animate.animateObj.connect(self.waitAction)
        self.animate.start()
        
        self.dialog = QtWidgets.QLabel(self.centralWidget)
        #self.dialog.setGeometry(270+248/2-60/2,  100-45+80,  24+25,  31+23)
        self.dialog.setTextFormat(Qt.RichText)    
        self.dialog.setWordWrap(True)
        self.dialog.setAlignment(Qt.AlignTop)
        
        self.dialogArrow = QtWidgets.QLabel(self.centralWidget)
        self.dialogArrow.setGeometry(0, 0, 50, 50)
        self.dialogArrow.setPixmap(QtGui.QPixmap(arrowPic))
        self.dialogArrow.move(self.connorX*(80/100)+248/2-60/2+30,  self.connorY/2*(50/100)-70+80+23)
            
        #self.connor.changeOpacity.connect(self.opacity)
        #设置对话框渐入渐出
        dialogOpacityEffect= QtWidgets.QGraphicsOpacityEffect(self.dialog)
        dialogArrowOpacityEffect = QtWidgets.QGraphicsOpacityEffect(self.dialogArrow)
        dialogOpacityEffect.setOpacity(0);
        dialogArrowOpacityEffect.setOpacity(0)
        self.dialog.setGraphicsEffect(dialogOpacityEffect);
        self.dialogArrow.setGraphicsEffect(dialogArrowOpacityEffect);
        self.dialogAnimation = QtCore.QPropertyAnimation(dialogOpacityEffect, b"opacity")
        self.dialogArrowAnimation = QtCore.QPropertyAnimation(dialogArrowOpacityEffect, b"opacity")
        self.dialogAnimation.setEasingCurve(QtCore.QEasingCurve.Linear)
        self.dialogArrowAnimation.setEasingCurve(QtCore.QEasingCurve.Linear)
        self.dialogAnimation.setDuration(1000)
        self.dialogArrowAnimation.setDuration(1000)
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.hiddenDialog)
        
        self.greetingsTimer = QtCore.QTimer()
        self.greetingsTimer.timeout.connect(self.greetings)
        self.greetingsTimer.start(3000)
        
        self.exitTimer = QtCore.QTimer()
        self.exitTimer.timeout.connect(self.exitConnor)
        
        self.toolIcon = trayIcon.TrayIcon()
        self.toolIcon.setupUi()
        self.toolIcon.showMenu(MainWindow)
        self.toolIcon.checkAutoState()
        self.toolIcon._exit.connect(self.exiting)
        self.toolIcon._settingResult.connect(self.displayDialog)
        self.toolIcon._waitAction.connect(self.waitAction)
        self.toolIcon._synBookmark.connect(self.synBookmark)
        self.toolIcon.updateConnor._updateRes.connect(self.displayDialog)
        self.toolIcon.show()
        
        #搜索框背景
        self.lineEditImage = QtWidgets.QLabel(self.centralWidget)
        self.lineEditImage.setStyleSheet('border-image:url(./connor/inputImage.jpg); border-style:solid; border-width: 1px;')
        self.lineEditImage.setGeometry(self.connorX/2-175,  self.connorY/2*(70/100)-25,  350,  100)
        self.lineEditImage.hide()
        
        #搜索框
        #self.inputContent = MyLineEdit(self.centralWidget)
        self.inputContent = lineEdit.MyLineEdit(self.centralWidget)
        self.inputContent.setGeometry(self.connorX/2-150,  self.connorY/2*(70/100),  300,  50)
        self.inputContent.setStyleSheet('QLineEdit{font-family:Microsoft YaHei;font-size:22px;border-style:none; border-width:2px; border-color:red;border-radius:10px;}')
        self.inputContent.returnPressed.connect(self.send)
        self.inputContent.hide()
        self.inputContent._hideInput.connect(self.hideInputImage)
        self.inputContent.textEdited.connect(self.textEdited)
        
        self.moveWindow(MainWindow)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint|Qt.Tool|Qt.WindowStaysOnTopHint)
        self.connor.createRightMenu()           #初始化右键菜单的内容
        self.waitAction(waitGif)
        
    def synBookmark(self):
        self.waitAction(waitGif)
        try:
            self.connor.bookmarkMenu.clear()
            self.folderHandler = locals()
            bookmarkDict = bookmark.readBookMark(self.folderHandler)
            if type(bookmarkDict) == int:
                self.displayDialog(bookmarkDict)
            else:
                bookmark.createBookmarkMenu(self.folderHandler, bookmarkDict, self.connor.bookmarkMenu)
                self.displayDialog('同步成功')
        except:
            self.diaplayDialog('同步失败')
        
    def textEdited(self):
        if self.inputContent.text() == '#与AI交淡':
            #print('ok')
            self.inputContent.clear()
    
    def hideInputImage(self):
        self.lineEditImage.hide()
        
    def send(self):
        if self.inputContent.isVisible():
            '''self.inputContent.hide()
            self.lineEditImage.hide()
            self.inputContent.clearFocus()'''
            pass
        if self.inputContent.text() != '' and self.inputContent.text() != '#与AI交淡':
            #self.inputContent.setFocus()
            self.queryThread = orderProcess.queryInfo(self.inputContent.text())
            self.queryThread._errMessage.connect(self.displayDialog)
            self.queryThread._answer.connect(self.displayAnswer)
            self.queryThread.start()
            self.inputContent.clear()
            self.waitAction(waitGif)
        
    def displayAnswer(self,  answer):
        self.displayDialog(answer)
        
    def moveWindow(self,  MainWindow):
        _desktop = QApplication.desktop()
        desktopRect = _desktop.availableGeometry()
        self.connorX = desktopRect.width()
        self.connorY = desktopRect.height()
        #MainWindow.resize(desktopRect.width(),  desktopRect.height())
        self.connor.move(self.connorX*(80/100),  self.connorY/2*(50/100))
        #self.inputContent.move(desktopRect.width()/2,  desktopRect.height()*(5/6))
        MainWindow.resize(self.connorX,  self.connorY /2)
        MainWindow.move(0,  self.connorY/2-50)
        
    def waitAction(self,  filePath):
        self.gif = QtGui.QMovie(filePath)
        self.connor.setMovie(self.gif)
        self.gif.start()
        self.gif.finished.connect(self.animateFinished)
        
    def inputFunction(self):
        if not self.inputContent.isVisible():
            self.inputContent.show()
            self.lineEditImage.show()
            
            #输入框获得焦点
            self.inputContent.setFocus()
            if self.inputContent.tempString == '':
                self.inputContent.setText('#与AI交淡')
                self.inputContent.selectAll()
            else:
                self.inputContent.setText(self.inputContent.tempString)
                self.inputContent.selectAll()
        
    def animateFinished(self):
        pass
        
    def opacity(self,  changeType):
        if changeType == '淡出':
            self.dialogAnimation.setStartValue(1);
            self.dialogAnimation.setEndValue(0);
            self.dialogArrowAnimation.setStartValue(1);
            self.dialogArrowAnimation.setEndValue(0);
        elif changeType == '淡入' or changeType == '退出':
            self.dialogAnimation.setStartValue(0);
            self.dialogAnimation.setEndValue(1)
            self.dialogArrowAnimation.setStartValue(0);
            self.dialogArrowAnimation.setEndValue(1)
            self.timer.start(3000)
        if changeType == '退出':
            self.exitTimer.start(2000)
        self.dialogArrowAnimation.start(QtCore.QAbstractAnimation.KeepWhenStopped) 
        self.dialogAnimation.start(QtCore.QAbstractAnimation.KeepWhenStopped)  
        
    def hiddenDialog(self):
        self.opacity('淡出')
        self.timer.stop()
        
    def exitConnor(self):
        if self.action == 'exit':
            sys.exit();
        elif self.action == 'shutdown':
            self.exitTimer.stop()
            try:
                os.system('C:\\Windows\\System32\\SlideToShutDown.exe')
            except Exception as err:
                self.displayDialog(err)
            sys.exit()
        
    #根据当前时间，显示不同的问候语    
    def greetings(self):
        #if self.isTargetPC('d0bf9c96f196'):
        if self.isTargetPC('d07e35541cde'):
            if self.isBirthday(datetime.datetime(1997,  12,  7)):
                greetingsString = '生日快乐。'
            else:
                dt = datetime.datetime.now()
                hour = dt.hour
                if hour <= 8 and hour >=0:
                    greetingsString = '早晨好。'
                elif hour <= 11 and hour > 8:
                    greetingsString = '上午好。'
                elif hour <= 13 and hour > 11:
                    greetingsString = '中午好。'
                elif hour <= 16 and hour > 13:
                    greetingsString = '下午好。'
                elif hour <= 24 and hour > 16:
                    greetingsString = '晚上好。'
            dialogDetail = autoFormat.formatString(self, greetingsString,  self.connorX*(80/100),  self.connorY/2*(50/100))
            self.dialog.setGeometry(QtCore.QRect(dialogDetail['dialogX'],  dialogDetail['dialogY'], dialogDetail['dialogWidth'], dialogDetail['dialogHeight']))
            self.opacity('淡入')
            self.greetingsTimer.stop()
        
    def exiting(self,  action = 'exit'):
        self.action = action
        dt = datetime.datetime.now()
        hour = dt.hour
        if hour <= 24 and hour >= 21 or hour <= 6 and hour >= 0:
            exitingString = '晚安。'
        else:
            exitingString = '再见。'
        dialogDetail = autoFormat.formatString(self,  exitingString,  self.connorX*(80/100),  self.connorY/2*(50/100))
        self.dialog.setGeometry(QtCore.QRect(dialogDetail['dialogX'],  dialogDetail['dialogY'], dialogDetail['dialogWidth'], dialogDetail['dialogHeight']))
        self.opacity('退出')
        
    def displayDialog(self,  string):
        if type(string) == int:
            if string == -1:
                string = '没有chrome'
            elif string == -2:
                string = '没有360'
            elif string == -3:
                string = '无法找到书签目录'
            elif string == -99:
                string = '设置失败'
            elif string == 0:
                string = '设置成功'
        dialogDetail = autoFormat.formatString(self,  string,  self.connorX*(80/100),  self.connorY/2*(50/100))
        self.dialog.setGeometry(QtCore.QRect(dialogDetail['dialogX'],  dialogDetail['dialogY'], dialogDetail['dialogWidth'], dialogDetail['dialogHeight']))
        self.opacity('淡入')
        self.greetingsTimer.stop()
        
    def isTargetPC(self,  address):
        mac = hex(uuid.getnode())[2:]
        if mac !=  address:
            warning = '使用环境错误，无法正常运行。'
            dialogDetail = autoFormat.formatString(self,  warning,  self.connorX*(5/6),  self.connorY/2*(50/100))
            self.dialog.setGeometry(QtCore.QRect(dialogDetail['dialogX'],  dialogDetail['dialogY'], dialogDetail['dialogWidth'], dialogDetail['dialogHeight']))
            self.opacity('退出')
        else:
            return True
            
    def isBirthday(self,  birthday):
        today = datetime.datetime.now()
        if birthday.month == today.month and birthday.day == today.day:
            return True
        else:
            return False
            
    def checkNet(self,  netState):
        if netState:
            self.netAccess = False
        else:
            self.netAccess = True
        
        
class myWindow(QtWidgets.QMainWindow):
    moveFlag = False
    newMessage = False
    netAccess = False
    def mousePressEvent(self,  event):
        if event.button() == Qt.RightButton:
            self.moveFlag = False
            self.newMessage = False
            self.update()
        if event.button() == Qt.LeftButton and not ui.connor.showMenu:
            self.moveFlag = True
            self.movePosition = event.globalPos() - self.pos()
            #event.accept()
            self.newMessage = True
            self.update()
    def mouseMoveEvent(self,  event):
        if self.moveFlag:
            self.move(event.globalPos() - self.movePosition)
            #event.accept()
            
    def mouseReleaseEvent(self,  event):
        self.moveFlag = False
        #self.transformWindow()
        
    def keyPressEvent(self,  event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            #显示输入框
            
            if not ui.inputContent.isVisible(): #and not ui.inputContent.hasFocus():
                ui.inputContent.show()
                ui.lineEditImage.show()
                ui.inputContent.setFocus()
                if ui.inputContent.tempString == '':
                    ui.inputContent.setText('#与AI交淡')
                    ui.inputContent.selectAll()
                else:
                    ui.inputContent.setText(ui.inputContent.tempString)
                    ui.inputContent.selectAll()
            else:
                ui.inputContent.hide()
                ui.lineEditImage.hide()
                ui.inputContent.clearFocus()
                
    def transformWindow(self):
        pass
        
    def checkNet(self,  netState):
        if netState:
            self.netAccess = False
        else:
            self.netAccess = True
    
if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        #print(app.focusWidget())
        MainWindow = myWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.showMaximized()
        #MainWindow.show()
        sys.exit(app.exec_())
    except Exception as err:
        ui.displayDialog(err)

