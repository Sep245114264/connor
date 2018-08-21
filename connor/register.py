#from PyQt5.QtCore import pyqtSignal
import winreg,  os,  getpass,  re

def getDefaultBrowser():
    key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT,  r'http\shell\open\command')
    name,  value,  type = winreg.EnumValue(key,  0)
    #del value[:-8]
    defaultPath = value[1:-9]
    defaultPath = os.path.basename(defaultPath)
    return defaultPath

def getBrowserPath():
    #360
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,  r'Software\Microsoft\Windows\CurrentVersion\Uninstall\360se6')
        value,  type = winreg.QueryValueEx(key,  'InstallLocation')
        bookmarkPath = value + r'\..\User Data\Default\Bookmarks'
        #bookmarkPath = value + r'\..\Application\\'
        #bookmarkPath += findVersion(os.listdir(bookmarkPath)) + r'\bookmarks'
        return bookmarkPath
    except:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,  r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\360se6.exe')
            value,  type = winreg.QueryValueEx(key,  'Path')
            bookmarkPath = value + r'\..\User Data\Default\Bookmarks'
            #bookmarkPath = value + r'\..\Application\\'
            #bookmarkPath += findVersion(os.listdir(bookmarkPath)) + r'\bookmarks'
            return bookmarkPath
        except:
            return -3
    
    #chrome
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,  r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths')
        key = winreg.OpenKeyEx(key,  'chrome.exe')
        #value,  type = winreg.QueryValueEx(key,  'Path')
        username = getpass.getuser()
        bookmarkPath = r'C:\users\\' + username + r'\AppData\Local\Google\Chrome\User Data\Default\Bookmarks'
        return bookmarkPath
        #print(f.read())
    except:
        return -1
    
    
            
def findVersion(dirName):
    print(dirName)
    versionRegex = re.compile(r'^[0-9]+.[0-9]+.[0-9]+.[0-9]+')
    for name in dirName:
        if versionRegex.search(name) != None:
            return versionRegex.search(name) .group()
    
if __name__ == '__main__':
    #print(type(getDefaultBrowser()))
    getBrowserPath()
