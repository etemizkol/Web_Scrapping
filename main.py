import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
# Getting vehicle links
soup = BeautifulSoup(requests.get("https://gta.fandom.com/wiki/Vehicles_in_GTA_Online").content, features="html.parser")
print(soup)
table = soup.find("table", attrs={"border": "1px", "cellpadding": "0px", "cellspacing": "0px"})
print(table)
data = table.find_all(href=True)
links = []
for row in data:
    links.append("https://gta.fandom.com/" + row["href"])

def creating_car_dict(links,car_dict):

    class CarInfo():
        def __init__(self, model, data, labels):
            self.model = model
            self.data = data
            self.labels = labels

    time.sleep(1)
    for link in links:
        def get_raw_data(link=link):
            html = requests.get(link).text
            html = html.replace("<br>", "#")
            return html

        def get_car_info(html):
            soup = BeautifulSoup(html, features="html.parser")
            aside_element = soup.find("aside", attrs={"role": "region"})
            car_model = aside_element.find("h2", attrs={"data-source": "name"}).text
            car_data = aside_element.find_all("div", attrs={"class": "pi-data-value pi-font"})
            car_labels = aside_element.find_all("h3")
            return CarInfo(car_model, car_data, car_labels)

        html = get_raw_data()
        car_info = get_car_info(html)

        obtainded_data = [feature.text for feature in car_info.labels if feature.text in car_dict.keys()]
        unobtained_data = [feature for feature in car_dict.keys() if feature not in obtainded_data]
        for missing_col in unobtained_data:
            if missing_col !="Model":
                car_dict[missing_col].append(0)
        #print(obtainded_data,unobtained_data)
        car_dict["Model"].append(car_info.model)
        for row, label_ in zip(car_info.data, car_info.labels):
            if label_.text not in  car_dict.keys():
                continue
            car_dict[label_.text].append(row.text)

        #print(car_dict)
        print("car info added.. next..")
    print("finally done")

car_dict = {"Model": [], "Type": [], "Vehicle class(GTA V/GTA Online)": [], "Vehicle type": [], "Body style": [],
            "Capacity": [], "Appears in": [], "Manufacturer": [], "Price": [], "Variant(s)": [],
            "Similar vehicle(s)": []}

creating_car_dict(links,car_dict)

#checking variables len for creating df safely
#for key in car_dict:
#    print(key,len(car_dict[key]))

df = pd.DataFrame.from_dict(car_dict)
df.head()

df.to_csv('car_datas.csv')
