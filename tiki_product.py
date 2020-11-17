import  requests
import  json
import  re
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
    