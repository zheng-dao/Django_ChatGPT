'''
This is the script for getting the quatery data of all the required as upto year

'''


import requests
import zipfile,io
from lxml import html
import random
import os
OUPUT_PATH_FOR_ZIP = "./app/data/ncua/raw/"
PATH_FOR_FOLDER = './app/data/ncua/'

LIST_OF_USER_AGENTS = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
                       ]


def get_response(url):
    headers = {'User-Agent': random.choice(LIST_OF_USER_AGENTS)}
    try:
        response = requests.get(url=url, headers=headers)
    except:
        print("Some error is raised!")
        response = None
    if response is not None:
        return response
    else:
        return None

def crawl(year_input):
    url = "https://www.ncua.gov/analysis/credit-union-corporate-call-report-data/quarterly-data"
    response = get_response(url)
    print(response)
    if response is not None:
        tree = html.fromstring(response.content)
        rows = tree.xpath('//tbody/tr')
        for row in rows:
            year = row.xpath(".//text()")[0]
            if int(year) < int(year_input):
                break

            list_of_zip_file = row.xpath('.//td//@href')
            for zip_file in list_of_zip_file:
                name_of_zip_file = zip_file.split('/')[-1].lower()
                name_of_zip_file = name_of_zip_file.replace('call-report-data-','')
                name_of_zip_file = name_of_zip_file.replace('qcr','')
                if '-' not in name_of_zip_file:
                    name_of_zip_file = name_of_zip_file[:4] + '-' + name_of_zip_file[-6:-4]
               
                
                #z = zipfile.ZipFile(io.BytesIO(r.content))
                print(name_of_zip_file)
                if int(name_of_zip_file[:4]) == year_input:
                    if os.path.isfile(OUPUT_PATH_FOR_ZIP+name_of_zip_file):
                        folder_name = name_of_zip_file.replace('.zip','')
                        print(folder_name)
                        if os.path.isdir(PATH_FOR_FOLDER+folder_name):
                            print("Already there")
                        else:
                             with zipfile.ZipFile(OUPUT_PATH_FOR_ZIP+name_of_zip_file+'.zip') as file:
                                try:
                                    file.extractall(PATH_FOR_FOLDER+folder_name+'./')
                                except:
                                    os.mkdir(PATH_FOR_FOLDER+folder_name)
                                    file.extractall(PATH_FOR_FOLDER+folder_name+'./')
                    else:
                        r = get_response('https://www.ncua.gov'+zip_file)
                        try:
                            with open(OUPUT_PATH_FOR_ZIP+name_of_zip_file,'wb') as zp:
                                zp.write(r.content)
                                z = zipfile.ZipFile(io.BytesIO(r.content))
                                os.mkdir(PATH_FOR_FOLDER+name_of_zip_file.replace('.zip',''))
                                z.extractall(PATH_FOR_FOLDER+name_of_zip_file.replace('.zip','')+'/')     
                        except Exception as e:
                            try:
                                with open(OUPUT_PATH_FOR_ZIP+name_of_zip_file+'.zip','wb') as zp:
                                    zp.write(r.content)
                                    z = zipfile.ZipFile(io.BytesIO(r.content))
                                    os.mkdir(PATH_FOR_FOLDER+name_of_zip_file.replace('.zip',''))
                                    z.extractall(PATH_FOR_FOLDER+name_of_zip_file.replace('.zip','')+'/')
                            except:
                                print("Error on this file::",name_of_zip_file)    
                            
#if __name__ == "__main__":
#    crawl(2015)
#    pass
