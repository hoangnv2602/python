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
        # self.url = 'https://tiki.vn/'
        warnings.filterwarnings('ignore')
        r        = requests.get('http://banchongia.local.com/api/admin/v1/get_menu')
        r = r.json()
        self.total = r['last_page']
        self.url = r['path']
        self.main_menu = []
        self.list = []
    
    def start_driver(self):
        self.driver = webdriver.PhantomJS("D:/Python/phantomjs2.1.1/bin/phantomjs")
        self.driver.implicitly_wait(5)
        self.driver.set_page_load_timeout(5)
        sleep(1)

    def open(self, url):
        print('getting page...', url)
        try: 
            self.start_driver()
            self.driver.get(url)
        except TimeoutException as e:
            print(e)
        print('page opened...')

    def fetch_link(self, cate_id) :
        code_link = '//div[@class="product-box-list"]//div[@class="product-item       "]'
        try:
            for n in self.driver.find_elements_by_xpath(code_link) : 
                title   = n.get_attribute('data-title')
                brand   = n.get_attribute('data-brand')
                cate    = n.get_attribute('data-category')
                img     = n.find_elements_by_xpath('.//a//div//span[@class="image"]//img')[0].get_attribute('src')
                localship = n.find_elements_by_xpath('.//a//div//span[@class="image"]//img')[0].get_attribute('src')
                link    = n.find_elements_by_xpath('.//a[@class=""]')[0].get_attribute('href')
                self.list.append({'title' : title, 'source' : link , 'brand_id' : brand, 'category_detail' : cate, 'thumnail' : img , 'category_id' : cate_id , 'localship' : localship})
                # print(self.list)
                # break
        except Exception as e:
            print(e)
        self.close()
    
    def post_post(self):
        if len(self.list) > 0:
            print('post data api...')
            headers = {'X-API-TOKEN': 'your_token_here'}
            all_dt = json.dumps(self.list)
            payload = {'dataInsert': all_dt}
            r = requests.post("http://banchongia.local.com/api/admin/v1/insert_data", data=payload, headers=headers)
            txt = r.text
            print(txt)
            sleep(2)

    def close(self):
        # print('closing driver...')
        self.driver.quit()
        print('closed!')

    def run(self):
        for i in range(1, self.total + 1) :
            r        = requests.get('http://banchongia.local.com/api/admin/v1/get_menu?page=' + str(i))
            for url in r.json()['data'] :
                cate_id = url['id']
                total_page = int(url['total']/52)
                if total_page >= 25 :
                    total_page = 25
                    
                for j in range(1, total_page + 1) :
                    self.open(url['source'] + '?page=' + str(j))
                    self.fetch_link(cate_id)
                    self.post_post()
 


tiki = Tiki()

tiki.run()