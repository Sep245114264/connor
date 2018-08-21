from PyQt5.QtWidgets import QSystemTrayIcon,  QMenu,  QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,  pyqtSignal,  QThread
import os,  winshell,  sys,  json,  requests,  webbrowser

workDir = os.path.abspath('.')
waitGif = workDir + r'\connor\connor_process_wait.gif'
iconPath = workDir + '.\\connor\\TIM截图20180730202129.ico'
versionConnor = r'1.1'

class TrayIcon(QSystemTrayIcon):
    class Update(QThread):
        _updateRes = pyqtSignal(str)
        def run(self):
            url = 'http://45.78.59.168/versionConnor/'
            sendMes = {
                'version': versionConnor
                }
            #mesJson = json.dumps(sendMes)
            #print(type(mesJson))
            self._updateRes.emit('正在请求升级许可...')
            response = requests.post(url,  sendMes)
            result = json.loads(response.text)
            tip = result['version']
            update = result['update']
            if update:
                url = 'http://45.78.59.168/downloadConnor/'
                webbrowser.open(url)
            else:
                pass
            self._updateRes.emit(tip)
        
    _exit = pyqtSignal()
    _settingResult = pyqtSignal(int)
    _waitAction = pyqtSignal(str)
    _synBookmark = pyqtSignal()
    _updateRes = pyqtSignal(str)
    windowHandler = None
    updateConnor = Update()
    def setupUi(self):
        self.setIcon(QIcon(iconPath))
        self.activated.connect(self.iconClied)
        self.messageClicked.connect(self.test)
        self.icon = self.MessageIcon()
        
    def showMenu(self,  MainWindow):
        self.windowHandler = MainWindow
        self.menu = QMenu()
        #self.action1 = QAction('显示信息',  self.windowHandler,  triggered=self.showM)
        self.synBookmarkAction = QAction('同步收藏夹',  self,  triggered=self.synBookmark)
        self.autoStart = QAction('开机自启',  self,  triggered=self.autoStartHandler)
        self.autoStart.setCheckable(True)
        #self.autoStart.setChecked(True)
        self.exit = QAction('退出',  self,  triggered=self.exitConnor)
        self.windowTop = QAction('置顶显示',  self,  triggered=self.setWindowTop)
        self.windowTop.setCheckable(True)
        self.windowTop.setChecked(True)
        self.checkUpdate = QAction('检查更新',  self, triggered=self.update)
        
        #self.menu.addAction(self.action1)
        self.menu.addAction(self.synBookmarkAction)
        self.menu.addAction(self.windowTop)
        self.menu.addAction(self.autoStart)
        self.menu.addAction(self.checkUpdate)
        self.menu.addAction(self.exit)
        self.setContextMenu(self.menu)
    
    def update(self):
        self.updateConnor.start()
      
    def synBookmark(self):
        self._synBookmark.emit()
    
    def exitConnor(self):
        #self.showMessage('test',  'test',  self.icon)
        self._exit.emit()
        
    def iconClied(self,  event):
        if event == QSystemTrayIcon.DoubleClick:
            self.windowHandler.activateWindow()
            self.windowHandler.show()
        elif event == QSystemTrayIcon.Context:
            print('右键菜单')
        
    def setWindowTop(self):
        #self.windowHandler.setWindowFlags(Qt.FramelessWindowHint|Qt.Tool|Qt.WindowStaysOnTopHint)
        if self.windowTop.isChecked():
            print('top')
            self.windowHandler.setWindowFlags(self.windowHandler.windowFlags() |Qt.FramelessWindowHint|Qt.Tool|Qt.WindowStaysOnTopHint)
            self.windowHandler.show()
        else:
            self.windowHandler.setWindowFlags(self.windowHandler.windowFlags()&~ Qt.WindowStaysOnTopHint)
            self.windowHandler.show()
            
    def test(self):
        print('text')
        
    #def showM(self):
        #self.windowHandler.setWindowFlags(self.windowHandler.windowFlags() &~ (Qt.FramelessWindowHint))
        #self.windowHandler.show()
        #self.showMessage('test',  'test',  self.icon)
    def autoStartHandler(self):
        if self.autoStart.isChecked():
            self.autoStart.setChecked(True)
            try:
                self.createShortcutToStartup()
                self._settingResult.emit(0)
            except FileNotFoundError:
                self._settingResult.emit(-99)
                self.autoStart.setChecked(False)
        else:
            self.autoStart.setChecked(False)
            try:
                self.delShortcutFromStartUp()
                self._settingResult.emit(0)
            except FileNotFoundError:
                self._settingResult.emit(-99)
                self.autoStart.setChecked(True)
            #pass
        #print(value)
        #print(type)
    def checkAutoState(self):
        try:
            open(os.path.join(winshell.startup(),  'connor.lnk'))
            self.autoStart.setChecked(True)
        except FileNotFoundError:
            self.autoStart.setChecked(False)
                       
    def createShortcutToStartup(self):    
        self._waitAction.emit(waitGif)
        winshell.CreateShortcut(
        Path=os.path.join(winshell.startup(),  'connor' + '.lnk'),  
        Target=sys.argv[0], 
        StartIn=os.path.dirname(sys.argv[0]), 
        Icon=(sys.argv[0], 0), 
        Description='connor'
        )
        
    def delShortcutFromStartUp(self):
        self._waitAction.emit(waitGif)
        defile = os.path.join(winshell.startup(),  'connor.lnk')
        winshell.delete_file(defile)

if __name__ == '__main__':
    update()
