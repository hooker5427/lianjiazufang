import  requests
def get_list( city ):
    import requests
    def get_html(url):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4167.0 Safari/537.36"
            }
            response = requests.get(url, headers=headers)

            print(response.status_code )
            if response.status_code == 200:
                return response.content.decode()
        except:
            pass
        return ''

    from lxml import etree
    url = f'https://{city}.lianjia.com/zufang'
    html = get_html(url)

    base_url = "https://sh.lianjia.com/"
    from urllib.parse import urljoin
    if html:
        mytree = etree.HTML(html)
        areas_list = mytree.xpath("//div[@id=\"filter\"]//ul[2]//li/a")
        area_info = []
        for area in areas_list:
            area_name = area.xpath("./text()")[0]
            area_link = area.xpath("./@href")[0]

            if area_name == '不限':
                continue
            area_link = urljoin(base_url, area_link)
            area_info.append( ( area_link , area_name ))

        if mytree.xpath("//a[text()=\"下一页\"]/preceding-sibling::a[1]//text()"):
            pns = int(mytree.xpath("//a[text()=\"下一页\"]/preceding-sibling::a[1]//text()"))
        else:
            pns = 1
        return pns, area_info
    else:
        return None, None

import  os
base_dir =  os.path.dirname(__file__)
if  not os.path.exists(  os.path.join( base_dir , 'data') ) :
    os.mkdir(os.path.join( base_dir , 'data')  )


# lianjiaSpider/data
citys = ["sh"]

data_dir = os.path.join(base_dir, 'data')
for city in citys:
    pns, area_list = get_list("sh")

    print (area_list )
    if pns and area_list:

        if not os.path.exists(os.path.join(data_dir, city)):
            os.mkdir(os.path.join(data_dir, city))
            city_dir = os.path.join(data_dir, city)
            for   url ,name   in area_list :
                print ( url )
                path1 = os.path.join( city_dir , name )
                print (path1 )
                if not os.path.exists( path1) :
                    os.mkdir( path1)


        # for  pn in  range(pns +1):
        #     url =  url +'pg{str(pn}/'
        #     print( url , name )