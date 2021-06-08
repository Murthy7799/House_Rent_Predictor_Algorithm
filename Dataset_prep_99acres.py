import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://www.99acres.com/property-for-rent-in-hyderabad-ffid"
agent = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/59.0.3071.115 Safari/537.36'}
agent1 = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
request = requests.get(url, headers=agent1)
content = request.content

# print(content)
soup = BeautifulSoup(content, "html.parser")
# print(soup.prettify())

"""all_c = soup.find_all("div", {"class": "srpTuple__tupleDetails srpTuple__fsl"})
# print(all_c[0].find("a", {"class": "body_med srpTuple__propertyName"}).text)
table = all_c[0].find("table", {"class": "srpTuple__tupleTable"})
t_row = table.findAll('tr')
print(t_row)
for i in t_row:
    t_c = i.findAll('td', {"class": "srpTuple__midGrid title_semiBold srpTuple__spacer16"})
    # print(t_c)
    desc = i.findAll('a', {"class": "body_med srpTuple__propertyName"})
    print("desc:", desc[0].find(text=True))
    if desc:
        description = desc[0].find(text=True)
    if t_c:
        # print(t_c[0])
        # print(t_c[1])
        price = int(t_c[0].find(text=True).split()[1].replace(',', ""))
        sq_feet = int(t_c[1].find(text=True).split()[0].replace(',', ""))
        print("price:", price, "square_feet:", sq_feet)"""

page_class = soup.find_all("div", {"class": "Pagination__srpPagination"})
page_num = page_class[0].find("div", {"class": "caption_strong_large"}).text.split()[-1]

print("pg:", page_num)

house_data = []
base_url = "https://www.99acres.com/property-for-rent-in-hyderabad-ffid-page-"
print(base_url)
# https://www.99acres.com/property-for-rent-in-hyderabad-ffid-page-2
for page in range(1, int(page_num), 1):
    print("url:", base_url+str(page))
    r = requests.get(base_url + str(page), headers=agent1)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    if page == 1:
        all_c = soup.find_all("div", {"class": "srpTuple__tupleDetails srpTuple__fsl"})
    else:
        all_c = soup.find_all("div", {"class": "srpTuple__tupleDetails"})

    # print(all_c[0].find("a", {"class": "body_med srpTuple__propertyName"}).text)
    for items in all_c:
        d = {}
        table = items.find("table", {"class": "srpTuple__tupleTable"})
        t_row = table.findAll('tr')
        # print(t_row)
        for i in t_row:
            t_c = i.findAll('td', {"class": "srpTuple__midGrid title_semiBold srpTuple__spacer16"})
            # print(t_c)
            desc = i.findAll('a', {"class": "body_med srpTuple__propertyName"})
            # print("desc:", desc[0].find(text=True))
            if desc:
                d['Description'] = desc[0].find(text=True)
            if t_c:
                # print(t_c[0])
                # print(t_c[1])
                d['Price'] = t_c[0].find(text=True).split()[1].replace(',', "")
                # try:
                #     d['Price'] = int(t_c[0].find(text=True).split()[1].replace(',', ""))
                # except:
                #     d['Price'] = None

                d['Sq_feet'] = int(t_c[1].find(text=True).split()[0].replace(',', ""))
                print("price:", d['Price'], "square_feet:", d['Sq_feet'])
                house_data.append(d)

print("house_data:", house_data)

data_frame = pd.DataFrame(house_data)
print(data_frame.shape)
data_frame.to_csv("/home/murthy/PycharmProjects/Lambton_classes/data_set_99acres2.csv")
