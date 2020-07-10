# import   requests
#
#
# def get_html( url):
#     try:
#         headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4167.0 Safari/537.36"
#         }
#         response = requests.get( url  , headers =  headers   )
#         if response.status_code ==200:
#             return  response.content.decode()
#     except :
#         pass
#     return  ''
#
# url= 'https://nj.lianjia.com/zufang/pg1brp2312erp2406/'
# html = get_html( url)
# if html :
#     print ( html )