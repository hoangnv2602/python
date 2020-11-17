import  requests
import  json
import  re
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

    def start_driver(self):
        self.driver = webdriver.Chrome("D:/Python/chromedriver.exe")
        self.driver.implicitly_wait(5)
        self.driver.set_page_load_timeout(5)

    def open(self, url):
        print('getting page...', url)
        try: 
            self.start_driver()
            self.driver.get(url)
        except TimeoutException as e:
            print(e)
        print('page opened...')

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

    def close(self):
        # print('closing driver...')
        self.driver.quit()
        print('closed!')
    
    def fetch_data(self, url) :
        p = 1
        while 1 == 1 :
            self.open(url + '?page=' + str(p))
            
            # self.driver.refresh()
            sleep(2)
            
            code_html_menu_1        = '//div[@class="product-box-list"]//div[@class="product-item       "]'
            code_html_menu_2        = '//a[@class="product-item"]'
            # code_html_menu_2        = '//body'

            try:
                n_1 = self.driver.find_elements_by_xpath(code_html_menu_1)
                n_2 = self.driver.find_elements_by_xpath(code_html_menu_2)

                if ( len( n_1 ) > 0 ) : 
                    print('type 1')
                    for n in self.driver.find_elements_by_xpath(code_html_menu_1) :
                        ids = n.get_attribute('data-id')
                        # print(ids)
                        # ids = re.findall(r"\-p\d+\.html",ids)[0]
                        # ids = ids.replace('-p','')
                        # ids = ids.replace('.html','')

                        self.data.append({'id' : ids})
                    
                    self.close()
                    self.post_data()

                if ( len( n_2 ) > 0 ) :
                    print('type 2')
                    for n in self.driver.find_elements_by_xpath(code_html_menu_2) :
                        ids = n.get_attribute('href')
                        # print(ids)
                        # print(ids)
                        ids = re.findall(r"\-p\d+\.html",ids)[0]
                        ids = ids.replace('-p','')
                        ids = ids.replace('.html','')

                        self.data.append({'id' : ids})
                    # print(self.data)
                    self.close()
                    self.post_data()
                if ( len( n_1 ) == 0 and len( n_2 ) == 0 ) :
                    self.data = []
                    self.close()
                    break
            except Exception as e:
                print(e)

            self.close()
            self.data = []
            p = p + 1

    def run(self):

        for i in range(120, 141) :
            r = requests.get('http://banchongia.local.com/api/admin/v1/list-menu?page=' + str(i))
            r = r.json()
            r = r['data']

            for data in r : 

                data['source'] = (data['source']).split('?src=')[0]

                self.fetch_data(data['source'])
                # self.open('https://tiki.vn/case-o-cung-hop-dung-hdd-box-dock-o-cung/c5350?src=c.1846.hamburger_menu_fly_out_banner')

        


tiki = Tiki()

tiki.run()