import datetime

import requests

from vaxslot.scripts.get_slots import header
import time

def anal(sleeptime):
    districtID = 485
    currdate = datetime.datetime.now()
    datestr = (currdate).strftime('%d-%m-%Y')
    file1 = open('cowintimes.txt','w')
    for j in range(10):
        i = 1

        while(True):
            print('Successful Call ',i)
            slot7 = requests.get(
                'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=' + str(
                    districtID) + '&date=' + datestr, headers=header)
            i+=1
            try:
                slot7 = slot7.json()
            except:
                start = time.time()
                break

        stri = 'Number of calls till failure:'+str(i-1)+'\n'
        print(stri)
        file1.write(stri)
        i=0
        while(True):
            print('Sleeping')
            time.sleep(sleeptime)
            print('Awake again')
            slot7 = requests.get(
                'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=' + str(
                    districtID) + '&date=' + datestr, headers=header)
            i+=1
            try:
                slot7= slot7.json()
                stri = "%s seconds" % (time.time() - start)
                print('Successful Call ', i, 'at %s seconds' % (time.time() - start))
                print('Stayed Timed out for :'+stri+'\n')
                file1.write('Stayed Timed out for :'+stri+'\n')
                break
            except:
                print('Unsuccessful Call ',i, 'at %s seconds' % (time.time() - start))
                pass

anal(300)
