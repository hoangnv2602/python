import  requests
import  json
import  re
<<<<<<< HEAD
import  http.client
import  random
import  time
import  warnings
from    htmldom                         import htmldom

url_id = 'http://banchongia.local.com/api/admin/v3/get-list?page='

i = 1

headers = []

headers.append("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36")
headers.append("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
headers.append("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.7")
headers.append("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56")
headers.append("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36")
headers.append("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36")
headers.append("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0")
headers.append("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36")
headers.append("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36")
headers.append("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36")
headers.append("Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
headers.append("Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko")
headers.append("Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.13) Gecko/20080311 Firefox/2.0.0.13")
headers.append("Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko")
headers.append("Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)")

while i <= 100000 :
    ids = requests.get('http://banchongia.local.com/api/admin/v3/get-list?page=' + str(i))
    ids = ids.json()['data']
    if len(ids) > 0 :
        
        for idd in ids :
            hd = random.randint(0, 14)
            header = headers[hd]
            print('get data page : ... https://tiki.vn/api/v2/products/' + idd['id_tiki'])
            data_ = requests.get('https://tiki.vn/api/v2/products/' + idd['id_tiki'], headers={'User-Agent': header})

            headers1 = {'X-API-TOKEN': 'your_token_here'}
            all_dt = json.dumps([data_.json()])
            payload = {'dataInsert': all_dt}
            r = requests.post("http://banchongia.local.com/api/admin/v3/up-data-id", data=payload, headers=headers1)
            txt = r.text
            print(txt)

            time.sleep(3)

    else :
        break

    # print(ids)

    i = i + 1
=======
from    htmldom     import htmldom

url = 'http://boonthelab.local.com/banchongia/api/admin/v3/list-product?page='

i = 1
while i < 1000000 :
    url_ = url + str(i)
    list_id_product = requests.get(url_)
    list_id_product = list_id_product.json()['data']
    
    if len(list_id_product) > 0 :
        # print(1)
        for j in list_id_product :
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            data_ = requests.get('https://tiki.vn/dien-thoai-may-tinh-bang/c1789?src=c.1789.hamburger_menu_fly_out_banner' , headers=headers)
            # data_ = requests.get('https://tiki.vn/api/v2/products/' + j['id_tiki'] , headers=headers)
            data = htmldom.HtmlDom().createDom(data_.text)

            for n in data.find('.product-item') :
                if n.attr('data-id') != 'Undefined Attribute':
                    ids = n.attr('data-id')
                elif n.attr('href') != 'Undefined Attribute' :
                    ids = n.attr('href')
                    ids = re.findall(r"\-p\d+\.html",ids)[0]
                    ids = ids.replace('-p','')
                    ids = ids.replace('.html','')
                print(ids)
                # print(n.text())
    else :
        break

    i = i + 1
    
>>>>>>> 0e7820db7a1a5565c4f484ab3ee00e4789a83c30
