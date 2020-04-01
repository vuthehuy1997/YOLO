import requests
from bs4 import BeautifulSoup
import os
import urllib
import urllib.request
import sys

def getImageObject(searchName, count):
    result = []
    pageIndex = 0
    while len(result) < count:
         # use "tbs=sur:fmc" in the query for search the legal data.
        url = 'https://www.dreamstime.com/search.php?srh_field='+searchName+'&s_all=n&s_ph=n&s_il=n&s_video=n\
                &s_audio=n&s_ad=n&s_wp=y&s_sl0=y&s_sl1=y&s_sl2=y&s_sl3=y&s_sl4=y&s_sl5=y&s_rf=y&s_ed=y&s_orp=y\
                &s_orl=y&s_ors=y&s_orw=y&s_clc=y&s_clm=y&s_rsf=0&s_rst=7&s_st=new&s_sm=all&s_mrg=1&s_mrc1=y\
                &s_mrc2=y&s_mrc3=y&s_mrc4=y&s_mrc5=y&s_exc=&pg='+str(pageIndex)
        pageIndex += 1
        try :
            html_text = requests.get(url).text

            # Parse html text
            tree = BeautifulSoup(html_text, 'html.parser')
            imTable = tree.find('div', {'class': 'item-list'})
            if imTable == None:
                break
                
            arr = imTable.find_all('img')
            if arr == None:
                break
            for i in arr:
                result.append(i['src'])
        except:
            print("Can not request: " + url)
    return result

# Rename file in foler as format 'index.jpg'

def renameDataDirectory(path):
    listDir = os.listdir(path)
    for index, file in enumerate(listDir):
        os.rename(path + file, path + file[1:])
    listDir = os.listdir(path)
    for index, file in enumerate(listDir):
        os.rename(path + file, path + '/' + str(index) + '.jpg')

def main():
    # Crawl data about flowers

    flowers = ['rose flower', 'sunflower']
    flowerLinks = []
    numberImages = 5000
    for f in flowers:
        flowerLinks.append(getImageObject(f, numberImages))
    # Create folder for store data

    currentPath = os.getcwd() 
    path = "./data/raw_data/"
    # define the access rights
    access_rights = 0o755
    for p in range(len(flowers)):
        try:  
            os.makedirs(path + str(p), access_rights)
        except OSError:  
            print ("Creation of the directory %s failed" % (path + str(p)))
    # Download data

    for i in range(len(flowerLinks)):
        for index, url in enumerate(flowerLinks[i]):
            urllib.request.urlretrieve(url.encode('utf-8').decode('ascii', 'ignore'), path + str(i) + '/' + str(index) +'.jpg')

if __name__ == '__main__':
    sys.exit(main())
    