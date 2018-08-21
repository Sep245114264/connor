from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt,  pyqtSignal
import pyperclip,  re

class MyLineEdit(QLineEdit):
    tempString = ''
    _hideInput = pyqtSignal()
    def focusInEvent(self,  event):
        if self.text() == '#与AI交淡':
            #self.clear()
            pass
        else:
            self.selectAll()
        text = pyperclip.paste()
        addressRegex = re.compile('^(?=^.{3,255}$)(http(s)?:\/\/)?(www\.)?[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+(:\d+)*(\/\w+\.\w+)*[^\s]*$')
        res = addressRegex.search(text)
        if res != None:
            print(res.group())
            self.tempString = res.group()
        
        #self.selectAll()
        
        
    def focusOutEvent(self,  event):
        self.tempString = self.text()
        pyperclip.copy(self.tempString)
        self.hide()
        self._hideInput.emit()
