import  requests
import  json
import  re
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
