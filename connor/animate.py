#-*-coding:utf-8-*-
from PyQt5.QtCore import QThread,  pyqtSignal
import  random,  time,  os

workDir = os.path.abspath('.')
waitGif = workDir + '\\connor\\connor_process_wait.gif'
eyesGif = workDir + '.\\connor\\connor_wait_eyes.gif'

class Animate(QThread):
    animateObj = pyqtSignal(str)
    animateList = [waitGif, eyesGif]
    def __init__(self):
        super().__init__()
    
    def run(self):
        while(1):
            time.sleep(random.randint(30,  60))
            random.shuffle(self.animateList)
            #print(self.animateList[0])
            self.animateObj.emit(self.animateList[0])
    
