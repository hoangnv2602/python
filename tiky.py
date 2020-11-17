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
        self.url = 'https://tiki.vn/'
        warnings.filterwarnings('ignore')
        self.data = []
    
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

    def get_url(self) :
        r = requests.get("http://banchongia.local.com/api/admin/v2/list_main")
        r = r.json()
        return r

    def fetch_menu(self) :

        self.open(self.url)

        code_html_menu = '//ul[@data-view-id="main_navigation"]//li[@data-view-id="main_navigation_item"]//a'

        for n in self.driver.find_elements_by_xpath(code_html_menu):
            if n.text != 'Thời trang - Phụ kiện' and n.text != 'Voucher - Dịch Vụ - Thẻ Cào':
                link    = n.get_attribute("href")
                title   = n.text
                self.data.append({'title' : title, 'link' : link , 'parent' : title , 'type' : 'main', 'total' : 0 , 'level' : 'NULL' , 'parent_id' : 0})
        # print(self.data)
        self.post_menu()
        self.close()
        
    def menu_menu_child(self):
        j = 1
        while j <= 7 :

            data = self.get_url()
            for i in data :
                if j == 1 :
                    types = 'category'
                else :
                    types = 'category'

                url_get = i['source']

                self.open(url_get)

                try:

                    code_html_menu_1        = '//div[@class="list-group"]//div[@class="list-group-item is-child"]//a[@class="list-group-item"]'
                    code_html_menu_2        = '//div[@class="block"]//div[@class="list collapsed"]//a[@style="padding-left:10px"]'
                    code_html_menu_3        = '//div[@class="block"]//div[@class="list collapsed"]//a[@style="padding-left: 10px"]'
                    n_1 = self.driver.find_elements_by_xpath(code_html_menu_1)
                    n_2 = self.driver.find_elements_by_xpath(code_html_menu_2)

                    n_3 = self.driver.find_elements_by_xpath(code_html_menu_3)

                    if (len(n_1) > 0) :
                        print('type 1')
                        for n in self.driver.find_elements_by_xpath(code_html_menu_1):
                            titles   = (n.get_attribute('innerHTML')).strip()
                            title   = (titles.split('<span>')[0]).strip()
                            link    = n.get_attribute('href')
                            # print(total)
                            self.data.append({'title' : title, 'link' : link , 'parent' : i['title'] , 'type' : types, 'total' : 0 , 'parent_update' : i['id']})
                        # print(self.data)
                        self.close()
                        self.post_menu()
                    if (len(n_2) > 0) :
                        print('type 2')
                        for n in self.driver.find_elements_by_xpath(code_html_menu_2):
                            title   = (n.get_attribute('innerHTML')).strip()
                            title   = re.sub('\(\d+\)','', title)
                            link    = n.get_attribute('href')
                            # print(title)
                            self.data.append({'title' : title, 'link' : link , 'parent' : i['title'] , 'type' : types, 'total' : 0, 'parent_update' : i['id']})
                        # print(self.data)
                        self.close()
                        self.post_menu()

                    if (len(n_3) > 0) :
                        print('type 3')
                        for n in self.driver.find_elements_by_xpath(code_html_menu_3):
                            title   = (n.get_attribute('innerHTML')).strip()
                            title   = re.sub('\(\d+\)','', title)
                            link    = n.get_attribute('href')
                            self.data.append({'title' : title, 'link' : link , 'parent' : i['title'] , 'type' : types, 'total' : 0, 'parent_update' : i['id']})
                        # print(self.data)
                        self.close()
                        self.post_menu()

                    if (len(n_1) == 0 and len(n_2) == 0 and len(n_3) == 0) :
                        print('khong du lieu')
                        self.data.append({'parent' : i['title'] , 'type' : types, 'total' : 0, 'parent_update' : i['id']})
                        self.post_menu()

                except Exception as e:
                    print(e)
            # break
            j = j + 1

    def post_menu(self):
        if len(self.data) > 0:
            print('post data api...')
            headers = {'X-API-TOKEN': 'your_token_here'}
            all_dt = json.dumps(self.data)
            payload = {'dataInsert': all_dt}
            r = requests.post("http://banchongia.local.com/api/admin/v2/make-category", data=payload, headers=headers)
            txt = r.text
            print(txt)
            # sleep(2)
            self.data = []

    def close(self):
        # print('closing driver...')
        self.driver.quit()
        print('closed!')

    def run(self):
        # self.fetch_menu()
        self.menu_menu_child()


        
        


tiki = Tiki()

tiki.run()