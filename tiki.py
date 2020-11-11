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
        self.main_menu = []
        self.sub_1 = []
        self.sub_2 = []
    
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

    def fetch_menu(self) :
        code_html_menu = '//ul[@data-view-id="main_navigation"]//li[@data-view-id="main_navigation_item"]//a'

        for n in self.driver.find_elements_by_xpath(code_html_menu):
            if n.text != 'Thời trang - Phụ kiện' and n.text != 'Voucher - Dịch Vụ - Thẻ Cào':
                link    = n.get_attribute("href")
                title   = n.text
                self.main_menu.append({'title' : title, 'link' : link , 'parent' : 0 , 'type' : 'main'})
        # print(self.main_menu)
        self.post_menu(self.main_menu)
        self.close()
        self.menu_1()
        
        
    def menu_1(self):
        if len(self.main_menu) > 0 :
            
            for i in range(0, len(self.main_menu) - 1) :
                self.open(self.main_menu[i]['link'])

                code_html_menu_1        = '//div[@class="list-group"]//div[@class="list-group-item is-child"]//a[@class="list-group-item"]'

                for n in self.driver.find_elements_by_xpath(code_html_menu_1):
                    title   = (n.get_attribute('innerHTML')).strip()
                    title   = (title.split('<span>')[0]).strip()
                    link    = n.get_attribute('href')
                    self.sub_1.append({'title' : title, 'link' : link , 'parent' : self.main_menu[i]['title'] , 'type' : 'main_1'})
                self.close()
                self.menu_2()

    def menu_2(self):
        if len(self.sub_1) > 0 :
            
            for i in range(0, len(self.sub_1) - 1) :
                
                self.open(self.sub_1[i]['link'])

                code_html_menu_1        = '//div[@class="list-group"]//div[@class="list-group-item is-child"]//a[@class="list-group-item"]'

                try:
                    n = self.driver.find_elements_by_xpath(code_html_menu_1)
                    if len(n) > 0 :
                        data = []
                        data.append(self.sub_1[i])
                        self.post_menu(data)
                        for n in self.driver.find_elements_by_xpath(code_html_menu_1):
                            title   = (n.get_attribute('innerHTML')).strip()
                            title   = (title.split('<span>')[0]).strip()
                            link    = n.get_attribute('href')
                            self.sub_2.append({'title' : title, 'link' : link , 'parent' : self.sub_1[i]['title'] , 'type' : 'category'})
                        self.close()
                        self.menu_3()
                    else :
                        data = []
                        data.append(self.sub_1[i])
                        self.post_menu(data)
                        # print(1)
                except Exception as e:
                    print(e)
            self.sub_1 = []
        # print(n.get_attribute('innerHTML'))

    def menu_3(self) :

        if len(self.sub_2) > 0 :
            for i in range(0, len(self.sub_2) - 1) :
                
                self.open(self.sub_2[i]['link'])

                code_html_menu_1        = '//div[@class="list-group"]//div[@class="list-group-item is-child"]//a[@class="list-group-item"]'

                try:
                    n = self.driver.find_elements_by_xpath(code_html_menu_1)
                    if len(n) > 0 :
                        data = []
                        data.append(self.sub_2[i])
                        self.post_menu(data)
                        for n in self.driver.find_elements_by_xpath(code_html_menu_1):
                            title   = (n.get_attribute('innerHTML')).strip()
                            title   = (title.split('<span>')[0]).strip()
                            link    = n.get_attribute('href')
                            self.sub_2.append({'title' : title, 'link' : link , 'parent' : self.sub_2[i]['title'] , 'type' : 'category_child'})
                        self.close()
                        self.menu_3()
                    else :
                        data = []
                        data.append(self.sub_2[i])
                        self.post_menu(data)
                        # print(1)
                except Exception as e:
                    print(e)
            self.sub_2 = []


    def post_menu(self, data):
        if len(data) > 0:
            print('post data api...')
            headers = {'X-API-TOKEN': 'your_token_here'}
            all_dt = json.dumps(data)
            payload = {'dataInsert': all_dt}
            r = requests.post("http://banchongia.local.com/api/admin/v1/make-category", data=payload, headers=headers)
            txt = r.text
            print(txt)
            sleep(2)

    def close(self):
        # print('closing driver...')
        self.driver.quit()
        print('closed!')

    def run(self):

        self.open(self.url)

        self.fetch_menu()


        
        


tiki = Tiki()

tiki.run()