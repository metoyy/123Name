import csv
from os import system
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar
import requests
from datetime import datetime

def clear():
    _=system('clear')

def getHtml(url:str):
    response=requests.get(url)
    return response.text

def getDepLinks(html):
    links=[]
    soup=BeautifulSoup(html,'lxml')
    catalog=soup.find('div',class_='grid-deputs')
    items=catalog.find_all('div',class_='dep-item')
    for i in items:
        link='http://kenesh.kg'
        a=f"{link}{i.find('a').get('href')}"
        links.append(a)
    return links

def getAllLinks():
    res=[]
    for i in range(1,6):
        url=f"http://kenesh.kg/ru/deputy/list/35?page={i}"
        html=getHtml(url)
        depLinks=getDepLinks(html)
        res.extend(depLinks)
    return res

def getDepsInfo():
    clear()
    depsList=getAllLinks()
    result=[]
    bar=IncrementalBar('Progress of Parsing',max=len(depsList))
    i=1
    for dep in depsList:
        try:
            a=getHtml(dep)
            soupDep=BeautifulSoup(a,'lxml')
            nameDep=soupDep.find('div',class_='deput-name').text.strip()
            fraction=soupDep.find_all('a',class_='deput-text')[0].text.strip()
            depInfo=soupDep.find_all('a',class_='deput-text')[1].text.strip()
            depBio=soupDep.find('div',class_='ck-editor').text.strip().replace('\n','').replace('\xa0','')
            oneDep=[nameDep,fraction,depInfo,depBio,dep]
            result.append(oneDep)
            bar.next()
            # bar.message(f'{i}{dep[x]} APPENDED')
            i+=1
            # print(f'{nameDep} APPENDED')
        except KeyboardInterrupt:
            break
        except:
            print('error')
            continue
    bar.finish()
    return result

def writeCSV(data:list,filename:str):
    with open(filename,'w') as file:
        # clear()
        writer=csv.writer(file)
        bar=IncrementalBar('Progress Of Writing',max=len(data))
        i=1
        writer.writerow(['ID','Name','Fraction','Info','Bio','URL Link'])
        for x in data:
            writer.writerow([i,x[0],x[1],x[2],x[3],x[4]])
            # bar.message(f'{i} - out of - {len(data)}')
            i+=1
            bar.next()
        bar.finish()
if __name__ == '__main__':    
    start=datetime.now()
    writeCSV(getDepsInfo(),'example.csv')
    finish=datetime.now()
    print(f'Time wasted {finish-start}')

# url='http://kenesh.kg/ky/deputy/list/35?page=1'
# html=getHtml(url)
# getDepLinks(html)
# getDepsInfo()