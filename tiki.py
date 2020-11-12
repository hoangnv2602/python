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
        self.sub_3 = []
        self.sub_4 = []
        self.sub_5 = []
        self.sub_6 = []
    
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
                self.main_menu.append({'title' : title, 'link' : link , 'parent' : 0 , 'type' : 'main', 'total' : 0 , 'level' : 'NULL'})
        # print(self.main_menu)
        self.post_menu(self.main_menu)
        self.close()
        self.menu_1()
        
        
    def menu_1(self):
        if len(self.main_menu) > 0 :
            
            for i in range(0, len(self.main_menu) ) :
                self.open(self.main_menu[i]['link'])

                code_html_menu_1        = '//div[@class="list-group"]//div[@class="list-group-item is-child"]//a[@class="list-group-item"]'

                for n in self.driver.find_elements_by_xpath(code_html_menu_1):
                    titles   = (n.get_attribute('innerHTML')).strip()
                    title   = (titles.split('<span>')[0]).strip()
                    total   = (titles.split('<span>')[1]).strip()
                    total   = total.replace("(", "")
                    total   = total.replace(")", "")
                    total   = (total.replace("</span>", "")).strip()
                    link    = n.get_attribute('href')
                    
                    # print(total)
                    self.sub_1.append({'title' : title, 'link' : link , 'parent' : self.main_menu[i]['title'] , 'type' : 'main_1', 'total' : total})
                
                self.close()
                self.menu_2()

    def menu_2(self):
        if len(self.sub_1) > 0 :
            
            for i in range(0, len(self.sub_1) ) :
                
                self.open(self.sub_1[i]['link'])

                code_html_menu_1        = '//div[@class="list-group"]//div[@class="list-group-item is-child"]//a[@class="list-group-item"]'

                try:
                    n = self.driver.find_elements_by_xpath(code_html_menu_1)
                    if len(n) > 0 :
                        data = []
                        data.append(self.sub_1[i])
                        self.post_menu(data)
                        for n in self.driver.find_elements_by_xpath(code_html_menu_1):
                            titles   = (n.get_attribute('innerHTML')).strip()
                            title   = (titles.split('<span>')[0]).strip()
                            total   = (titles.split('<span>')[1]).strip()
                            total   = total.replace("(", "")
                            total   = total.replace(")", "")
                            total   = (total.replace("</span>", "")).strip()
                            link    = n.get_attribute('href')
                            self.sub_2.append({'title' : title, 'link' : link , 'parent' : self.sub_1[i]['title'] , 'type' : 'category', 'total' : total})
                        self.close()
                        self.menu_3()
                    else :
                        self.close()
                        data = []
                        self.sub_1[i]['level'] = 'end'
                        data.append(self.sub_1[i])
                        self.post_menu(data)
                        # print(1)
                except Exception as e:
                    print(e)
            self.sub_1 = []
        # print(n.get_attribute('innerHTML'))

    def menu_3(self) :

        if len(self.sub_2) > 0 :
            for i in range(0, len(self.sub_2) ) :
                
                self.open(self.sub_2[i]['link'])

                code_html_menu_1        = '//div[@class="list-group"]//div[@class="list-group-item is-child"]//a[@class="list-group-item"]'

                try:
                    n = self.driver.find_elements_by_xpath(code_html_menu_1)
                    if len(n) > 0 :
                        data = []
                        data.append(self.sub_2[i])
                        self.post_menu(data)
                        for n in self.driver.find_elements_by_xpath(code_html_menu_1):
                            titles   = (n.get_attribute('innerHTML')).strip()
                            title   = (titles.split('<span>')[0]).strip()
                            total   = (titles.split('<span>')[1]).strip()
                            total   = total.replace("(", "")
                            total   = total.replace(")", "")
                            total   = (total.replace("</span>", "")).strip()
                            link    = n.get_attribute('href')
                            self.sub_3.append({'title' : title, 'link' : link , 'parent' : self.sub_2[i]['title'] , 'type' : 'category', 'total' : total})
                        self.close()
                        self.menu_4()
                    else :
                        self.close()
                        data = []
                        self.sub_2[i]['level'] = 'end'
                        data.append(self.sub_2[i])
                        self.post_menu(data)
                        # print(1)
                except Exception as e:
                    print(e)
            self.sub_2 = []

    def menu_4(self) :
    
        if len(self.sub_3) > 0 :
            for i in range(0, len(self.sub_3) ) :
                
                self.open(self.sub_3[i]['link'])

                code_html_menu_1        = '//div[@class="list-group"]//div[@class="list-group-item is-child"]//a[@class="list-group-item"]'

                try:
                    n = self.driver.find_elements_by_xpath(code_html_menu_1)
                    if len(n) > 0 :
                        data = []
                        data.append(self.sub_3[i])
                        self.post_menu(data)
                        for n in self.driver.find_elements_by_xpath(code_html_menu_1):
                            titles   = (n.get_attribute('innerHTML')).strip()
                            title   = (titles.split('<span>')[0]).strip()
                            total   = (titles.split('<span>')[1]).strip()
                            total   = total.replace("(", "")
                            total   = total.replace(")", "")
                            total   = (total.replace("</span>", "")).strip()
                            link    = n.get_attribute('href')
                            self.sub_4.append({'title' : title, 'link' : link , 'parent' : self.sub_3[i]['title'] , 'type' : 'category', 'total' : total})
                        self.close()
                        self.menu_5()
                    else :
                        self.close()
                        data = []
                        self.sub_3[i]['level'] = 'end'
                        data.append(self.sub_3[i])
                        self.post_menu(data)
                        # print(1)
                except Exception as e:
                    print(e)
            self.sub_3 = []

    def menu_5(self) :
        
        if len(self.sub_4) > 0 :
            for i in range(0, len(self.sub_4) ) :
                
                self.open(self.sub_4[i]['link'])

                code_html_menu_1        = '//div[@class="list-group"]//div[@class="list-group-item is-child"]//a[@class="list-group-item"]'

                try:
                    n = self.driver.find_elements_by_xpath(code_html_menu_1)
                    if len(n) > 0 :
                        data = []
                        data.append(self.sub_5[i])
                        self.post_menu(data)
                        for n in self.driver.find_elements_by_xpath(code_html_menu_1):
                            titles   = (n.get_attribute('innerHTML')).strip()
                            title   = (titles.split('<span>')[0]).strip()
                            total   = (titles.split('<span>')[1]).strip()
                            total   = total.replace("(", "")
                            total   = total.replace(")", "")
                            total   = (total.replace("</span>", "")).strip()
                            link    = n.get_attribute('href')
                            self.sub_5.append({'title' : title, 'link' : link , 'parent' : self.sub_4[i]['title'] , 'type' : 'category', 'total' : total})
                        self.close()
                        self.menu_6()
                    else :
                        self.close()
                        data = []
                        self.sub_4[i]['level'] = 'end'
                        data.append(self.sub_4[i])
                        self.post_menu(data)
                        # print(1)
                except Exception as e:
                    print(e)
            self.sub_4 = []
    
    

    def menu_6(self) :
        
        if len(self.sub_5) > 0 :
            for i in range(0, len(self.sub_5) ) :
                
                self.open(self.sub_5[i]['link'])

                code_html_menu_1        = '//div[@class="list-group"]//div[@class="list-group-item is-child"]//a[@class="list-group-item"]'

                try:
                    n = self.driver.find_elements_by_xpath(code_html_menu_1)
                    if len(n) > 0 :
                        data = []
                        data.append(self.sub_5[i])
                        self.post_menu(data)
                        for n in self.driver.find_elements_by_xpath(code_html_menu_1):
                            titles   = (n.get_attribute('innerHTML')).strip()
                            title   = (titles.split('<span>')[0]).strip()
                            total   = (titles.split('<span>')[1]).strip()
                            total   = total.replace("(", "")
                            total   = total.replace(")", "")
                            total   = (total.replace("</span>", "")).strip()
                            link    = n.get_attribute('href')
                            self.sub_6.append({'title' : title, 'link' : link , 'parent' : self.sub_5[i]['title'] , 'type' : 'category', 'total' : total})
                        self.close()
                        self.menu_4()
                    else :
                        self.close()
                        data = []
                        self.sub_5[i]['level'] = 'end'
                        data.append(self.sub_5[i])
                        self.post_menu(data)
                        # print(1)
                except Exception as e:
                    print(e)
            self.sub_5 = []


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
        # print('closed!')

    def run(self):

        self.open(self.url)

        self.fetch_menu()


        
        


tiki = Tiki()

tiki.run()