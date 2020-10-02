import PySimpleGUI as sg
import requests
from bs4 import BeautifulSoup as soup  # HTML data structure
# from urllib.request import urlopen as uReq  # Web client

# URl to web scrap from.
page_url = "https://www.worldometers.info/coronavirus/#countries"

# # opens the connection and downloads html page from url
# uClient = uReq(page_url)

# # parses html into a soup data structure to traverse html
# # as if it were a json data type.
# page_soup = soup(uClient.read(), "html.parser")
# uClient.close()

req = requests.get(page_url)
page_soup = soup(req.content, 'html.parser')

# finds each product from the store page
containers = page_soup.findAll("div", {"class": "main_table_countries_div"})

# header of csv file to be written
headers = ["Country","Total Cases","New Cases","Total Deaths","New Deaths","Total Recovered","Active Cases","Serious or Critical","Tot_Cases/1 Million population"]

all_data=[]
countries=[]
# get data from website
for container in containers:
    tr_all=container.tbody.findAll('tr',{"style":""})
    for i in tr_all:
        h=i.findAll("td")
        details=[]
        for t in h:
            num=t.text.strip()
            if num!="":
                details.append(num)
            else:
                details.append("0")
        all_data.append(details)
        countries.append(all_data[-1][1])
    break

# sort one list w.r.t other
zipped_pairs = zip(countries, all_data) 
all_data = [x for _, x in sorted(zipped_pairs)]
countries.sort()

sg.theme('DarkAmber')	# Add a touch of color
# Event Loop to process "events" and get the "values" of the inputs
while True:
    # All the stuff inside your window.
    layout = [  [sg.Text('Select country name to know CoronaVirus Cases')],
                [sg.Listbox(values=countries,size=(20, 12), key='-LIST-', enable_events=True)],
                [sg.Button('Exit')] ]

    # Create the Window
    window = sg.Window('CoronaVirus', layout)
    # print(listbox.selection_get())

    event, values = window.read()
    if event in (None, 'Exit'):	# if user closes window or clicks cancel
        break
    country_name=values['-LIST-'][0]
    stt=""
    for individual in all_data:
        if individual[1].lower()==country_name.lower():
            stt=stt+"CoronaVirus Case Details\n"
            for j in range(6):
                stt=stt+(f"{headers[j]} :- {individual[j+1]}\n")
            sg.Popup(stt)
    window.close()
window.close()