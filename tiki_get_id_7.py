import  requests
import  json
import  re
import  http.client
import  warnings
from    htmldom                         import htmldom
from    time                            import sleep
from    selenium                        import webdriver
from    selenium.common.exceptions      import TimeoutException
from    bs4                             import BeautifulSoup

class Tiki():
    def __init__(self):
        warnings.filterwarnings('ignore')
        self.data = []

    def post_data(self):
        if len(self.data) > 0:
            print('post data api...')
            headers = {'X-API-TOKEN': 'your_token_here'}
            all_dt = json.dumps(self.data)
            payload = {'dataInsert': all_dt}
            r = requests.post("http://banchongia.local.com/api/admin/v1/up-id", data=payload, headers=headers)
            txt = r.text
            print(txt)
            # sleep(2)
            self.data = []
    
    def fetch_data(self, url) :
        p = 1
        while 1 == 1 :
            http.client.HTTPConnection._https_vsn = 10
            http.client.HTTPConnection._https_vsn_str = 'HTTPS/1.0'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            print('get data page : ...' + url + '?page=' + str(p))
            data_ = requests.get(url + '?page=' + str(p), headers=headers)

            try:
                data = htmldom.HtmlDom().createDom(data_.text)
                lists = data.find('.product-item')
                if lists.length() > 0 :
                    for n in lists :
                        if n.attr('data-id') != 'Undefined Attribute':
                            ids = n.attr('data-id')
                        elif n.attr('href') != 'Undefined Attribute' :
                            ids = n.attr('href')
                            ids = re.findall(r"\-p\d+\.html",ids)[0]
                            ids = ids.replace('-p','')
                            ids = ids.replace('.html','')
                        
                        self.data.append({'id' : ids})
                    self.post_data()
                else :
                    break
            except Exception as e:
                print(e)
            p = p + 1

    def run(self):

        for i in range(141, 161) :
            print(i)
            r = requests.get('http://banchongia.local.com/api/admin/v1/list-menu?page=' + str(i))
            r = r.json()
            r = r['data']

            for data in r : 

                data['source'] = (data['source']).split('?src=')[0]

                self.fetch_data(data['source'])
                # self.open('https://tiki.vn/case-o-cung-hop-dung-hdd-box-dock-o-cung/c5350?src=c.1846.hamburger_menu_fly_out_banner')

        


tiki = Tiki()

tiki.run()
