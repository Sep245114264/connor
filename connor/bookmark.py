import json,  orderProcess,  functools,  register
from PyQt5.QtWidgets import QToolTip,  QAction
from PyQt5.QtGui import QFont
import label

def findBookmark():
    #inputFileName = 'C:\\Users\\hp\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks'
    inputFileName = register.getBrowserPath()
    if type(inputFileName) == int:
        return inputFileName
    else:
        inputFile = open(inputFileName,  'r', encoding='utf-8')
        content = json.loads(inputFile.read())
        return content['roots']['bookmark_bar']['children']
    
'''def createBookmarkMenu(fDirHandler):
    chilDir = findBookmark()
    walkDir(chilDir,  fDirHandler)
    
bookMarkList = []
def walkDir(chilDir, labelHandler ,  fDirHandler):
    tempDir = fDirHandler
    for children in chilDir:
        if children['type'] == 'folder':
            tempDir = fDirHandler.addMenu(children['name'])
            
            walkDir(children['children'],  tempDir)
        elif children['type'] == 'url':
            print(children['url'])
            bookMarkList.append(children['url'])
            fDirHandler.addAction(children['name']).triggered.connect(lambda: orderProcess.openUrl(children['url']))'''
#print(content['roots']['bookmark_bar']['children'][0]['children'])
def readBookMark(folder):
    chilDir = findBookmark()
    if type(chilDir) == int:
        return chilDir
    else:
        bookmark = {}
        bookmark = walkBookmark(chilDir,  folder)
        return bookmark

def walkBookmark(chilDir,  Ffolder):
    tempMark = {}
    for children in chilDir:
        if children['type'] == 'folder':
            Ffolder[children['name']] = children['name']
            tempMark[children['name']] = walkBookmark(children['children'],  Ffolder)
        elif children['type'] == 'url':
            tempMark[children['name']] = children['url']
    return tempMark

def createBookmarkMenu(folder, bookmarkDict,  fDirHandler):
    QToolTip.setFont(QFont('SansSerif',  10))
    #tempHandler = fDirHandler
    #print((bookmarkDict))
    for child in bookmarkDict:
        if type(bookmarkDict[child]) == dict:
            folder[child] = label.Menu(child)
            #tempHandler = fDirHandler.addMenu(child)
            fDirHandler.insertMenu(QAction(),  folder[child])
            createBookmarkMenu(folder, bookmarkDict[child],  folder[child])
        else:
            display = formatBookmark(child)
            #bookmarkUrl[child] = fDirHandler.addAction(child).triggered.connect(lambda: buttonUrl(child))
            #fDirHandler.addAction(display).triggered.connect(functools.partial(orderProcess.openUrl,  bookmarkDict[child]))
            temp = fDirHandler.addAction(display)
            #temp.hovered.connect(handler)
            temp.setToolTip(child)
            #print(type(fDirHandler))
            temp.triggered.connect(functools.partial(orderProcess.openUrl,  bookmarkDict[child]))
            
            #tipBookmark(child,  temp

def formatBookmark(name):
    length = 0
    count = 0
    for chars in name:
        count += 1
        length += get_width(ord(chars))
        if length >20:
            return name[:count] + '...'
    return name
    
def handler():
    print('tst')
    
widths = [
  (126,  1), (159,  0), (687,   1), (710,  0), (711,  1),
  (727,  0), (733,  1), (879,   0), (1154, 1), (1161, 0),
  (4347,  1), (4447,  2), (7467,  1), (7521, 0), (8369, 1),
  (8426,  0), (9000,  1), (9002,  2), (11021, 1), (12350, 2),
  (12351, 1), (12438, 2), (12442,  0), (19893, 2), (19967, 1),
  (55203, 2), (63743, 1), (64106,  2), (65039, 1), (65059, 0),
  (65131, 2), (65279, 1), (65376,  2), (65500, 1), (65510, 2),
  (120831, 1), (262141, 2), (1114109, 1),
]
def get_width( o ):
  """Return the screen column width for unicode ordinal o."""
  global widths
  if o == 0xe or o == 0xf:
    return 0
  for num, wid in widths:
    if o <= num:
      return wid
  return 1

if __name__ == '__main__':
    #walkDir(content['roots']['bookmark_bar']['children'])
    #print(readBookMark())
    #bookmark = readBookMark()
    #print(bookmark)
    #createBookmarkMenu(bookmark,  1)
    print(formatBookmark('一二三四五六一二三四五六一二三四五六一二三四五六一二三四五六'))
    print(formatBookmark('abcdefghij'))
