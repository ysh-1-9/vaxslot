import time

from vaxslot import dist_start, dist_finish, db_data, db
from vaxslot.scripts.db_imports_exports import getDistrictIDs
from vaxslot.scripts.emailing import notify
from vaxslot.scripts.models import sesh, Center
from vaxslot.scripts.updateDB import updateDB


def automate():
    # timesfile = open('timesfile.json','r')           #change to append
    while True:
        start = time.time()
        districts = getDistrictIDs()
        finalsessions18 = []
        finalsessions45 = []
        finalcenters = []
        # file1 = open('center_counts.txt', 'w')
        # sum=0
        i = 1
        for districtID in districts:
            print('Updating', i, 'of',dist_finish-dist_start,'districts, districtID = ', districtID)
            sessions18,sesssions45,centers = updateDB(districtID)
            finalsessions18+=sessions18
            finalsessions45+=sesssions45
            centers+=centers
            print('Done updating', i, 'of',dist_finish-dist_start,'districts, districtID = ', districtID)
            print('Sending out emails for', i, 'th district, districtID = ', districtID)
            notify(districtID,sessions18,db_data[districtID][3],centers)             #multithreading multiproc
            notify(districtID,sesssions45,db_data[districtID][4],centers)
            i += 1
        sesh.query.delete()
        Center.query.delete()
        db.session.add_all(finalsessions18)
        db.session.add_all(finalsessions45)
        db.session.add_all(finalcenters)
        db.session.commit()
        stri = "%s seconds" % (time.time() - start)
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++Entire thing took ',stri)

