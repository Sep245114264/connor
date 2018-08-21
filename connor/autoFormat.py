from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtCore import Qt
from PyQt5 import QtGui,  QtWidgets
import math,  requests

def formatString(self,  string,  x,  y):
    font = QFont('Microsoft YaHei',  18)
    #font.setPixelSize(22)
    self.dialog.setFont(font)
    self.dialog.setStyleSheet("QLabel{border-radius:15;padding:15px;background: rgb(0,128,255);color:white;width:auto;height:auto;word-wrap: break-word}")
    self.dialog.setText(string)
    #字体宽高
    metr = QFontMetrics(self.dialog.font())
    stringWidth = metr.width(self.dialog.text())
    stringHeight = metr.height()
    lineCount = 1
    if stringWidth < 300:
        dialogWidth = stringWidth + 40
        dialogHeight = stringHeight * lineCount + 40
        dialogX = x+248/2-stringWidth + 60
    else:
        lineCount = math.ceil(stringWidth / 300)
        dialogWidth = 300 + 40
        dialogHeight = stringHeight * lineCount + 40
        dialogX = x+248/2-250
    
    dialogDetail = {'dialogX':  dialogX,  'dialogY': y-stringHeight*lineCount+20, 
                           'dialogWidth': dialogWidth,  'dialogHeight': dialogHeight}
    return dialogDetail
