from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import time
import pandas as pd
import csv

#Tässä valitaan halutut objektit nettisivun html:stä.
def selectObj( a, name ):
    year = Select(driver.find_element_by_id(a))
    year.select_by_visible_text(name)
    return;

#Funktio jonka avulla voidaan kommunikoida nettisivun kanssa
def driverClickOk():
    elem1 = driver.find_element_by_name("yt0")
    elem1.click()
    time.sleep(4)
    page=driver.page_source
    return page;

#Tässä suodatettu data muutetaan taulukkoon joka on oikeaa muotoa
def addArray( obj, table ):
    cells1=obj.findAll("td")
    num=cells1[0].text
    vuosi=cells1[2].text
    vuosi=int(vuosi)-year
    string=cells1[6].text
    time=string.replace("\n\xa0","")
    ntime=time.replace("00:","")
    #ntime=time.string.replace("00:","")
    table.append([num,vuosi,ntime])
    return;

#tässä kikkaillaan koska ei voida ihan suoraan ottaa aikoja järjestyksessä
def calc( a, table,year ):
    for i in a:
        addArray(i,table,year)

#suodatetaan data esim. muutetaan ajan muotoa, sekä lasketaan ikä.
def cleanData( page,year ):
    clean=soup(page,"html.parser")
    oddTable=[]
    evenTable=[]
    contain = clean.find("div",{"id":"result-grid"})
    odd =contain.findAll("tr",{"class":"odd"})
    even =contain.findAll("tr",{"class":"even"})
    calc(odd,oddTable,year)
    calc(even,evenTable,year)
    data=oddTable+evenTable
    data=sorted(data,key=lambda nro: nro[2])
    return data;

#Kirjoitetaan tulokset .csv tiedostoksi
def writeCsv( data, year ):
    df = pd.DataFrame(data)
    df.columns = ['pos', 'birth', 'time']
    path="C:\\Users\\Wiljam\\Documents\\"+year+".csv"
    df.to_csv(path,index=False)
    print("complete")

#Täällä valinnat mitä halutaan hakea suodatetaan dataa cleanData() funktiossa
def Main( year ):
    selectObj("Result_result_date",year)
    selectObj("Result_class", "Miehet")
    selectObj("Result_event_code","50m Vapaauinti" )
    selectObj("Result_pooltype","50")
    #selectObj("Result_competition_group","Suomen mestaruusuinnit")
    page=driverClickOk()
    data=cleanData(page,year)
    writeCsv(data,year)

#ohjelmaa aletaan suorittamaan täältä. Loopilla käydään kaikki vuodet läpi menemällä aina Main() funktioon
driver = webdriver.Firefox(executable_path='C:\geckodriver\geckodriver.exe')
driver.get("http://www.octoopen.fi/index.php?r=Result")
choices=["2017","2016","2015","2014","2013"]
for year in choices:
    Main(year)

driver.close()
