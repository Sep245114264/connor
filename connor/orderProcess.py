from PyQt5.QtCore import QThread,  pyqtSignal
import requests,  webbrowser,  bs4,  re,  json,  os

class queryInfo(QThread):
    _answer = pyqtSignal(str)
    _errMessage = pyqtSignal(str)
    def __init__(self,  queryString):
        super().__init__()
        self.queryString = queryString
        
    def run(self):
        res = self.judgeType(self.queryString)
        answer = self.acceptString(res)
        if answer != None:
            self._answer.emit(answer)
    
    def acceptString(self,  contentEx):
        conType = contentEx['conType']
        string = contentEx['content']
        try:
            if conType == 'url':
                webbrowser.open(string)
            elif conType == 'inquire':
                address = 'http://www.baidu.com/s?wd=' + string
                res = requests.get(address)
                res.raise_for_status()
                
                soup = bs4.BeautifulSoup(res.text,  'html.parser')
                linkElems = soup.select('.t a')
                numOpen = min(3,  len(linkElems))
                for i in range(numOpen):
                    webbrowser.open(linkElems[i].get('href'))
                webbrowser.open(address)
            elif conType == 'robot':
                answer = self.talkRobot(string)
                return answer
        except Exception:
            self._errMessage.emit('网络环境错误，请检查后重试...')
            
    def judgeType(self, string):
        orderRegex = re.compile('^#')
        addressRegex = re.compile('^(?=^.{3,255}$)(http(s)?:\/\/)?(www\.)?[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+(:\d+)*(\/\w+\.\w+)*[^\s]*$')
        res = orderRegex.search(string)
        if res == None:
            res = addressRegex.search(string)
            if res == None:
                conType = 'inquire'
            else:
                conType = 'url'
        else:
            conType = 'robot'
        return {'content': string,  'conType': conType}
        
    def talkRobot(self, string):
        robotUrl = 'http://openapi.tuling123.com/openapi/api/v2'
        sendMes = {
            'perception':{
                'inputText':{
                    'text': '你好'
                }
            }, 
            'userInfo':{
                'apiKey': 'f9f34e0a8ef240f0aa3a973278dab80e', 
                'userId': '260596'
            }
        }
        sendMes['perception']['inputText']['text'] = string
        mesJson = json.dumps(sendMes)       #字典转换为json
        try:
            response = requests.post(robotUrl,  mesJson)
            response.raise_for_status()
            results = json.loads(response.text)
            return results['results'][0]['values']['text']
        except Exception:
            self._errMessage.emit('网络环境错误，请检查后重试...')
        
class NetState(QThread):
    _netState = pyqtSignal(int)
    def run(self):
        netState = os.system('ping 8.8.8.8')
        self._netState.emit(netState)

def openUrl(tUrl):
    print(tUrl)
    webbrowser.open(tUrl)
    
def talkRobot(string):
        robotUrl = 'http://openapi.tuling123.com/openapi/api/v2'
        sendMes = {
            'perception':{
                'inputText':{
                    'text': '你好'
                }
            }, 
            'userInfo':{
                'apiKey': 'f9f34e0a8ef240f0aa3a973278dab80e', 
                'userId': '260596'
            }
        }
        sendMes['perception']['inputText']['text'] = string
        mesJson = json.dumps(sendMes)       #字典转换为json
        response = requests.post(robotUrl,  mesJson)
        response.raise_for_status()
        results = json.loads(response.text)
        return results['results']
    
if __name__ == '__main__':
    #acceptString('baidu.com',  1)
    groups = talkRobot('讲个笑话')
    for group in groups:
        if group['resultType'] == 'text':
            print(group['values']['text'])
        elif group['resultType'] == 'image':
            print(group['values']['image'])
    #print(talkRobot('讲个笑话'))
