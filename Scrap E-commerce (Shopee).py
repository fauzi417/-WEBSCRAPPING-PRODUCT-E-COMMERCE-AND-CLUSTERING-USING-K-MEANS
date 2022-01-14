import requests
import csv
keyword=['tanaman%20hias','laptop','kulkas','whiskas','parfume']
page=[0,60,120,180,240,300,360,420,480,540,600]


for key in keyword:
    write = csv.writer(open('{}.csv'.format(key), 'w', newline=''))
    header = ['name', 'category', 'rating', 'shopid', 'price']
    write.writerow(header)
    for halaman in page:
        url2=(f'https://shopee.co.id/api/v4/search/search_items?by=relevancy&keyword={key}&limit=60&newest={halaman}&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2')
        r = requests.get(url2)
        jsonresult = r.json()
        product=jsonresult['items']
        for p in product:
            name= p['item_basic']['name']
            category= p['item_basic']['catid']
            rating=p['item_basic']['item_rating']['rating_star']
            shop_id=p['shopid']
            price=int(int(p['item_basic']['price'])/100000)
            write = csv.writer(open('{}.csv'.format(key), 'a', newline='',encoding="utf-8"))
            data = [name, category, rating, shop_id, price]
            write.writerow(data)

