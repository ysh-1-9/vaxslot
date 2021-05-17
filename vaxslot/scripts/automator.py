import json
import os
import sys
import time

from vaxslot import db
from vaxslot.scripts.db_imports_exports import getDistrictIDs, dist_finish,dist_start
from vaxslot.scripts.emailing import notify
from vaxslot.scripts.models import sesh, Center, User
from vaxslot.scripts.updateDB import updateDB


def automate():
    # timesfile = open('timesfile.json','r')           #change to append
    db_data = []
    user_data = []
    user_district = {}
    print('Starting Initialization')
    centerdict = []  # list of center dicts, indexed by center.id
    seshlist18 = []  # list of session dicts, age18, indexed by sesh.id
    seshlist45 = []  # list of session dicts, age45, indexed by sesh.id
    userlist18 = []  # list of user dicts, age18
    userlist45 = []  # list of user dicts, age45
    districtIDs = getDistrictIDs()
    state_district = stateToDistrict()
    with open("state_district.json", "w") as outfile:
        json.dump(state_district, outfile)
    for x in range(800):
        db_data.append([])
        user_data.append([])
        seshlist18.append({})
        seshlist45.append({})
        centerdict.append({})
        userlist18.append({})
        userlist45.append({})
    # with open(os.path.join(sys.path[0], 'districts_names.txt')) as f:
    #     lines = f.read().splitlines()
    # for x in lines:
    #     y = x.split(': ')
    #     districtname_to_id[y[1]] = int(y[0])

    centers = Center.query.all()
    for x in centers:
        centerdict[x.districtID][x.id] = x

    seshes = sesh.query.all()
    for x in seshes:
        if x.age == 18:
            seshlist18[x.districtID][x.id] = x
        else:
            seshlist45[x.districtID][x.id] = x

    users = User.query.all()
    for x in users:
        user_district[x.email] = x.district
        if x.age >= 45:
            userlist45[x.district][x.email] = x  # THIS WON'T RUN UNLESS USER CLASS KA PROTOTYPE IS CHANGED
        else:
            userlist18[x.district][x.email] = x

    for x in districtIDs:
        db_data[x] = [seshlist18[x], seshlist45[x], centerdict[x]]
        user_data[x] = [userlist18[x], userlist45[x]]
    print('Initialization Done')
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
            sessions18,sesssions45,centers = updateDB(districtID,db_data)
            finalsessions18+=sessions18
            finalsessions45+=sesssions45
            centers+=centers
            print('Done updating', i, 'of',dist_finish-dist_start,'districts, districtID = ', districtID)
            print('Sending out emails for', i, 'th district, districtID = ', districtID)
            notify(districtID,sessions18,user_data[districtID][0],db_data[districtID][2])             #multithreading multiproc
            notify(districtID,sesssions45,user_data[districtID][1],db_data[districtID][2])
            i += 1
        sesh.query.delete()
        Center.query.delete()
        db.session.add_all(finalsessions18)
        db.session.add_all(finalsessions45)
        db.session.add_all(finalcenters)
        db.session.commit()
        stri = "%s seconds" % (time.time() - start)
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++Entire thing took ',stri)

        users = User.query.all()
        for x in users:
            user_district[x.email] = x.district
            if x.age >= 45:
                userlist45[x.district][x.email] = x  # THIS WON'T RUN UNLESS USER CLASS KA PROTOTYPE IS CHANGED
            else:
                userlist18[x.district][x.email] = x

        for x in districtIDs:
            user_data[x] = [userlist18[x], userlist45[x]]


def stateToDistrict(start=dist_start,finish=dist_finish):

    # states = getStates()['states']
    # dic = {}
    # for x in states:
    #     districts_as_dicts = getDistricts(x['state_id'])
    #     districts_as_lists =  []
    #     for y in districts_as_dicts:
    #         districts_as_lists.append([y['district_name'],y['district_id']])
    #     dic[x['state_name']]=districts_as_lists
    # print(dic)
    # with open('district_data.json', 'w') as f:
    #     json.dump(dic, f)
    # return dic
    districts = getDistrictIDs(start,finish)
    districts_dict = {x:True for x in districts}

    dic  = {"Andaman and Nicobar Islands": [["Nicobar", 3], ["North and Middle Andaman", 1], ["South Andaman", 2]], "Andhra Pradesh": [["Anantapur", 9], ["Chittoor", 10], ["East Godavari", 11], ["Guntur", 5], ["Krishna", 4], ["Kurnool", 7], ["Prakasam", 12], ["Sri Potti Sriramulu Nellore", 13], ["Srikakulam", 14], ["Visakhapatnam", 8], ["Vizianagaram", 15], ["West Godavari", 16], ["YSR District Kadapa (Cuddapah)", 6]], "Arunachal Pradesh": [["Anjaw", 22], ["Changlang", 20], ["Dibang Valley", 25], ["East Kameng", 23], ["East Siang", 42], ["Itanagar Capital Complex", 17], ["Kamle", 24], ["Kra Daadi", 27], ["Kurung Kumey", 21], ["Lepa Rada", 33], ["Lohit", 29], ["Longding", 40], ["Lower Dibang Valley", 31], ["Lower Siang", 18], ["Lower Subansiri", 32], ["Namsai", 36], ["Pakke Kessang", 19], ["Papum Pare", 39], ["Shi Yomi", 35], ["Siang", 37], ["Tawang", 30], ["Tirap", 26], ["Upper Siang", 34], ["Upper Subansiri", 41], ["West Kameng", 28], ["West Siang", 38]], "Assam": [["Baksa", 46], ["Barpeta", 47], ["Biswanath", 765], ["Bongaigaon", 57], ["Cachar", 66], ["Charaideo", 766], ["Chirang", 58], ["Darrang", 48], ["Dhemaji", 62], ["Dhubri", 59], ["Dibrugarh", 43], ["Dima Hasao", 67], ["Goalpara", 60], ["Golaghat", 53], ["Hailakandi", 68], ["Hojai", 764], ["Jorhat", 54], ["Kamrup Metropolitan", 49], ["Kamrup Rural", 50], ["Karbi-Anglong", 51], ["Karimganj", 69], ["Kokrajhar", 61], ["Lakhimpur", 63], ["Majuli", 767], ["Morigaon", 55], ["Nagaon", 56], ["Nalbari", 52], ["Sivasagar", 44], ["Sonitpur", 64], ["South Salmara Mankachar", 768], ["Tinsukia", 45], ["Udalguri", 65], ["West Karbi Anglong", 769]], "Bihar": [["Araria", 74], ["Arwal", 78], ["Aurangabad", 77], ["Banka", 83], ["Begusarai", 98], ["Bhagalpur", 82], ["Bhojpur", 99], ["Buxar", 100], ["Darbhanga", 94], ["East Champaran", 105], ["Gaya", 79], ["Gopalganj", 104], ["Jamui", 107], ["Jehanabad", 91], ["Kaimur", 80], ["Katihar", 75], ["Khagaria", 101], ["Kishanganj", 76], ["Lakhisarai", 84], ["Madhepura", 70], ["Madhubani", 95], ["Munger", 85], ["Muzaffarpur", 86], ["Nalanda", 90], ["Nawada", 92], ["Patna", 97], ["Purnia", 73], ["Rohtas", 81], ["Saharsa", 71], ["Samastipur", 96], ["Saran", 102], ["Sheikhpura", 93], ["Sheohar", 87], ["Sitamarhi", 88], ["Siwan", 103], ["Supaul", 72], ["Vaishali", 89], ["West Champaran", 106]], "Chandigarh": [["Chandigarh", 108]], "Chhattisgarh": [["Balod", 110], ["Baloda bazar", 111], ["Balrampur", 112], ["Bastar", 113], ["Bemetara", 114], ["Bijapur", 115], ["Bilaspur", 116], ["Dantewada", 117], ["Dhamtari", 118], ["Durg", 119], ["Gariaband", 120], ["Gaurela Pendra Marwahi ", 136], ["Janjgir-Champa", 121], ["Jashpur", 122], ["Kanker", 123], ["Kawardha", 135], ["Kondagaon", 124], ["Korba", 125], ["Koriya", 126], ["Mahasamund", 127], ["Mungeli", 128], ["Narayanpur", 129], ["Raigarh", 130], ["Raipur", 109], ["Rajnandgaon", 131], ["Sukma", 132], ["Surajpur", 133], ["Surguja", 134]], "Dadra and Nagar Haveli": [["Dadra and Nagar Haveli", 137]], "Daman and Diu": [["Daman", 138], ["Diu", 139]], "Delhi": [["Central Delhi", 141], ["East Delhi", 145], ["New Delhi", 140], ["North Delhi", 146], ["North East Delhi", 147], ["North West Delhi", 143], ["Shahdara", 148], ["South Delhi", 149], ["South East Delhi", 144], ["South West Delhi", 150], ["West Delhi", 142]], "Goa": [["North Goa", 151], ["South Goa", 152]], "Gujarat": [["Ahmedabad", 154], ["Ahmedabad Corporation", 770], ["Amreli", 174], ["Anand", 179], ["Aravalli", 158], ["Banaskantha", 159], ["Bharuch", 180], ["Bhavnagar", 175], ["Bhavnagar Corporation", 771], ["Botad", 176], ["Chhotaudepur", 181], ["Dahod", 182], ["Dang", 163], ["Devbhumi Dwaraka", 168], ["Gandhinagar", 153], ["Gandhinagar Corporation", 772], ["Gir Somnath", 177], ["Jamnagar", 169], ["Jamnagar Corporation", 773], ["Junagadh", 178], ["Junagadh Corporation", 774], ["Kheda", 156], ["Kutch", 170], ["Mahisagar", 183], ["Mehsana", 160], ["Morbi", 171], ["Narmada", 184], ["Navsari", 164], ["Panchmahal", 185], ["Patan", 161], ["Porbandar", 172], ["Rajkot", 173], ["Rajkot Corporation", 775], ["Sabarkantha", 162], ["Surat", 165], ["Surat Corporation", 776], ["Surendranagar", 157], ["Tapi", 166], ["Vadodara", 155], ["Vadodara Corporation", 777], ["Valsad", 167]], "Haryana": [["Ambala", 193], ["Bhiwani", 200], ["Charkhi Dadri", 201], ["Faridabad", 199], ["Fatehabad", 196], ["Gurgaon", 188], ["Hisar", 191], ["Jhajjar", 189], ["Jind", 204], ["Kaithal", 190], ["Karnal", 203], ["Kurukshetra", 186], ["Mahendragarh", 206], ["Nuh", 205], ["Palwal", 207], ["Panchkula", 187], ["Panipat", 195], ["Rewari", 202], ["Rohtak", 192], ["Sirsa", 194], ["Sonipat", 198], ["Yamunanagar", 197]], "Himachal Pradesh": [["Bilaspur", 219], ["Chamba", 214], ["Hamirpur", 217], ["Kangra", 213], ["Kinnaur", 216], ["Kullu", 211], ["Lahaul Spiti", 210], ["Mandi", 215], ["Shimla", 208], ["Sirmaur", 212], ["Solan", 209], ["Una", 218]], "Jammu and Kashmir": [["Anantnag", 224], ["Bandipore", 223], ["Baramulla", 225], ["Budgam", 229], ["Doda", 232], ["Ganderbal", 228], ["Jammu", 230], ["Kathua", 234], ["Kishtwar", 231], ["Kulgam", 221], ["Kupwara", 226], ["Poonch", 238], ["Pulwama", 227], ["Rajouri", 237], ["Ramban", 235], ["Reasi", 239], ["Samba", 236], ["Shopian", 222], ["Srinagar", 220], ["Udhampur", 233]], "Jharkhand": [["Bokaro", 242], ["Chatra", 245], ["Deoghar", 253], ["Dhanbad", 257], ["Dumka", 258], ["East Singhbhum", 247], ["Garhwa", 243], ["Giridih", 256], ["Godda", 262], ["Gumla", 251], ["Hazaribagh", 255], ["Jamtara", 259], ["Khunti", 252], ["Koderma", 241], ["Latehar", 244], ["Lohardaga", 250], ["Pakur", 261], ["Palamu", 246], ["Ramgarh", 254], ["Ranchi", 240], ["Sahebganj", 260], ["Seraikela Kharsawan", 248], ["Simdega", 249], ["West Singhbhum", 263]], "Karnataka": [["Bagalkot", 270], ["Bangalore Rural", 276], ["Bangalore Urban", 265], ["BBMP", 294], ["Belgaum", 264], ["Bellary", 274], ["Bidar", 272], ["Chamarajanagar", 271], ["Chikamagalur", 273], ["Chikkaballapur", 291], ["Chitradurga", 268], ["Dakshina Kannada", 269], ["Davanagere", 275], ["Dharwad", 278], ["Gadag", 280], ["Gulbarga", 267], ["Hassan", 289], ["Haveri", 279], ["Kodagu", 283], ["Kolar", 277], ["Koppal", 282], ["Mandya", 290], ["Mysore", 266], ["Raichur", 284], ["Ramanagara", 292], ["Shimoga", 287], ["Tumkur", 288], ["Udupi", 286], ["Uttar Kannada", 281], ["Vijayapura", 293], ["Yadgir", 285]], "Kerala": [["Alappuzha", 301], ["Ernakulam", 307], ["Idukki", 306], ["Kannur", 297], ["Kasaragod", 295], ["Kollam", 298], ["Kottayam", 304], ["Kozhikode", 305], ["Malappuram", 302], ["Palakkad", 308], ["Pathanamthitta", 300], ["Thiruvananthapuram", 296], ["Thrissur", 303], ["Wayanad", 299]], "Ladakh": [["Kargil", 309], ["Leh", 310]], "Lakshadweep": [["Agatti Island", 796], ["Lakshadweep", 311]], "Madhya Pradesh": [["Agar", 320], ["Alirajpur", 357], ["Anuppur", 334], ["Ashoknagar", 354], ["Balaghat", 338], ["Barwani", 343], ["Betul", 362], ["Bhind", 351], ["Bhopal", 312], ["Burhanpur", 342], ["Chhatarpur", 328], ["Chhindwara", 337], ["Damoh", 327], ["Datia", 350], ["Dewas", 324], ["Dhar", 341], ["Dindori", 336], ["Guna", 348], ["Gwalior", 313], ["Harda", 361], ["Hoshangabad", 360], ["Indore", 314], ["Jabalpur", 315], ["Jhabua", 340], ["Katni", 353], ["Khandwa", 339], ["Khargone", 344], ["Mandla", 335], ["Mandsaur", 319], ["Morena", 347], ["Narsinghpur", 352], ["Neemuch", 323], ["Panna", 326], ["Raisen", 359], ["Rajgarh", 358], ["Ratlam", 322], ["Rewa", 316], ["Sagar", 317], ["Satna", 333], ["Sehore", 356], ["Seoni", 349], ["Shahdol", 332], ["Shajapur", 321], ["Sheopur", 346], ["Shivpuri", 345], ["Sidhi", 331], ["Singrauli", 330], ["Tikamgarh", 325], ["Ujjain", 318], ["Umaria", 329], ["Vidisha", 355]], "Maharashtra": [["Ahmednagar", 391], ["Akola", 364], ["Amravati", 366], ["Aurangabad ", 397], ["Beed", 384], ["Bhandara", 370], ["Buldhana", 367], ["Chandrapur", 380], ["Dhule", 388], ["Gadchiroli", 379], ["Gondia", 378], ["Hingoli", 386], ["Jalgaon", 390], ["Jalna", 396], ["Kolhapur", 371], ["Latur", 383], ["Mumbai", 395], ["Nagpur", 365], ["Nanded", 382], ["Nandurbar", 387], ["Nashik", 389], ["Osmanabad", 381], ["Palghar", 394], ["Parbhani", 385], ["Pune", 363], ["Raigad", 393], ["Ratnagiri", 372], ["Sangli", 373], ["Satara", 376], ["Sindhudurg", 374], ["Solapur", 375], ["Thane", 392], ["Wardha", 377], ["Washim", 369], ["Yavatmal", 368]], "Manipur": [["Bishnupur", 398], ["Chandel", 399], ["Churachandpur", 400], ["Imphal East", 401], ["Imphal West", 402], ["Jiribam", 410], ["Kakching", 413], ["Kamjong", 409], ["Kangpokpi", 408], ["Noney", 412], ["Pherzawl", 411], ["Senapati", 403], ["Tamenglong", 404], ["Tengnoupal", 407], ["Thoubal", 405], ["Ukhrul", 406]], "Meghalaya": [["East Garo Hills", 424], ["East Jaintia Hills", 418], ["East Khasi Hills", 414], ["North Garo Hills", 423], ["Ri-Bhoi", 417], ["South Garo Hills", 421], ["South West Garo Hills", 422], ["South West Khasi Hills", 415], ["West Garo Hills", 420], ["West Jaintia Hills", 416], ["West Khasi Hills", 419]], "Mizoram": [["Aizawl East", 425], ["Aizawl West", 426], ["Champhai", 429], ["Kolasib", 428], ["Lawngtlai", 432], ["Lunglei", 431], ["Mamit", 427], ["Serchhip", 430], ["Siaha", 433]], "Nagaland": [["Dimapur", 434], ["Kiphire", 444], ["Kohima", 441], ["Longleng", 438], ["Mokokchung", 437], ["Mon", 439], ["Peren", 435], ["Phek", 443], ["Tuensang", 440], ["Wokha", 436], ["Zunheboto", 442]], "Odisha": [["Angul", 445], ["Balangir", 448], ["Balasore", 447], ["Bargarh", 472], ["Bhadrak", 454], ["Boudh", 468], ["Cuttack", 457], ["Deogarh", 473], ["Dhenkanal", 458], ["Gajapati", 467], ["Ganjam", 449], ["Jagatsinghpur", 459], ["Jajpur", 460], ["Jharsuguda", 474], ["Kalahandi", 464], ["Kandhamal", 450], ["Kendrapara", 461], ["Kendujhar", 455], ["Khurda", 446], ["Koraput", 451], ["Malkangiri", 469], ["Mayurbhanj", 456], ["Nabarangpur", 470], ["Nayagarh", 462], ["Nuapada", 465], ["Puri", 463], ["Rayagada", 471], ["Sambalpur", 452], ["Subarnapur", 466], ["Sundargarh", 453]], "Puducherry": [["Karaikal", 476], ["Mahe", 477], ["Puducherry", 475], ["Yanam", 478]], "Punjab": [["Amritsar", 485], ["Barnala", 483], ["Bathinda", 493], ["Faridkot", 499], ["Fatehgarh Sahib", 484], ["Fazilka", 487], ["Ferozpur", 480], ["Gurdaspur", 489], ["Hoshiarpur", 481], ["Jalandhar", 492], ["Kapurthala", 479], ["Ludhiana", 488], ["Mansa", 482], ["Moga", 491], ["Pathankot", 486], ["Patiala", 494], ["Rup Nagar", 497], ["Sangrur", 498], ["SAS Nagar", 496], ["SBS Nagar", 500], ["Sri Muktsar Sahib", 490], ["Tarn Taran", 495]], "Rajasthan": [["Ajmer", 507], ["Alwar", 512], ["Banswara", 519], ["Baran", 516], ["Barmer", 528], ["Bharatpur", 508], ["Bhilwara", 523], ["Bikaner", 501], ["Bundi", 514], ["Chittorgarh", 521], ["Churu", 530], ["Dausa", 511], ["Dholpur", 524], ["Dungarpur", 520], ["Hanumangarh", 517], ["Jaipur I", 505], ["Jaipur II", 506], ["Jaisalmer", 527], ["Jalore", 533], ["Jhalawar", 515], ["Jhunjhunu", 510], ["Jodhpur", 502], ["Karauli", 525], ["Kota", 503], ["Nagaur", 532], ["Pali", 529], ["Pratapgarh", 522], ["Rajsamand", 518], ["Sawai Madhopur", 534], ["Sikar", 513], ["Sirohi", 531], ["Sri Ganganagar", 509], ["Tonk", 526], ["Udaipur", 504]], "Sikkim": [["East Sikkim", 535], ["North Sikkim", 537], ["South Sikkim", 538], ["West Sikkim", 536]], "Tamil Nadu": [["Aranthangi", 779], ["Ariyalur", 555], ["Attur", 578], ["Chengalpet", 565], ["Chennai", 571], ["Cheyyar", 778], ["Coimbatore", 539], ["Cuddalore", 547], ["Dharmapuri", 566], ["Dindigul", 556], ["Erode", 563], ["Kallakurichi", 552], ["Kanchipuram", 557], ["Kanyakumari", 544], ["Karur", 559], ["Kovilpatti", 780], ["Krishnagiri", 562], ["Madurai", 540], ["Nagapattinam", 576], ["Namakkal", 558], ["Nilgiris", 577], ["Palani", 564], ["Paramakudi", 573], ["Perambalur", 570], ["Poonamallee", 575], ["Pudukkottai", 546], ["Ramanathapuram", 567], ["Ranipet", 781], ["Salem", 545], ["Sivaganga", 561], ["Sivakasi", 580], ["Tenkasi", 551], ["Thanjavur", 541], ["Theni", 569], ["Thoothukudi (Tuticorin)", 554], ["Tiruchirappalli", 560], ["Tirunelveli", 548], ["Tirupattur", 550], ["Tiruppur", 568], ["Tiruvallur", 572], ["Tiruvannamalai", 553], ["Tiruvarur", 574], ["Vellore", 543], ["Viluppuram", 542], ["Virudhunagar", 549]], "Telangana": [["Adilabad", 582], ["Bhadradri Kothagudem", 583], ["Hyderabad", 581], ["Jagtial", 584], ["Jangaon", 585], ["Jayashankar Bhupalpally", 586], ["Jogulamba Gadwal", 587], ["Kamareddy", 588], ["Karimnagar", 589], ["Khammam", 590], ["Kumuram Bheem", 591], ["Mahabubabad", 592], ["Mahabubnagar", 593], ["Mancherial", 594], ["Medak", 595], ["Medchal", 596], ["Mulugu", 612], ["Nagarkurnool", 597], ["Nalgonda", 598], ["Narayanpet", 613], ["Nirmal", 599], ["Nizamabad", 600], ["Peddapalli", 601], ["Rajanna Sircilla", 602], ["Rangareddy", 603], ["Sangareddy", 604], ["Siddipet", 605], ["Suryapet", 606], ["Vikarabad", 607], ["Wanaparthy", 608], ["Warangal(Rural)", 609], ["Warangal(Urban)", 610], ["Yadadri Bhuvanagiri", 611]], "Tripura": [["Dhalai", 614], ["Gomati", 615], ["Khowai", 616], ["North Tripura", 617], ["Sepahijala", 618], ["South Tripura", 619], ["Unakoti", 620], ["West Tripura", 621]], "Uttar Pradesh": [["Agra", 622], ["Aligarh", 623], ["Ambedkar Nagar", 625], ["Amethi", 626], ["Amroha", 627], ["Auraiya", 628], ["Ayodhya", 646], ["Azamgarh", 629], ["Badaun", 630], ["Baghpat", 631], ["Bahraich", 632], ["Balarampur", 633], ["Ballia", 634], ["Banda", 635], ["Barabanki", 636], ["Bareilly", 637], ["Basti", 638], ["Bhadohi", 687], ["Bijnour", 639], ["Bulandshahr", 640], ["Chandauli", 641], ["Chitrakoot", 642], ["Deoria", 643], ["Etah", 644], ["Etawah", 645], ["Farrukhabad", 647], ["Fatehpur", 648], ["Firozabad", 649], ["Gautam Buddha Nagar", 650], ["Ghaziabad", 651], ["Ghazipur", 652], ["Gonda", 653], ["Gorakhpur", 654], ["Hamirpur", 655], ["Hapur", 656], ["Hardoi", 657], ["Hathras", 658], ["Jalaun", 659], ["Jaunpur", 660], ["Jhansi", 661], ["Kannauj", 662], ["Kanpur Dehat", 663], ["Kanpur Nagar", 664], ["Kasganj", 665], ["Kaushambi", 666], ["Kushinagar", 667], ["Lakhimpur Kheri", 668], ["Lalitpur", 669], ["Lucknow", 670], ["Maharajganj", 671], ["Mahoba", 672], ["Mainpuri", 673], ["Mathura", 674], ["Mau", 675], ["Meerut", 676], ["Mirzapur", 677], ["Moradabad", 678], ["Muzaffarnagar", 679], ["Pilibhit", 680], ["Pratapgarh", 682], ["Prayagraj", 624], ["Raebareli", 681], ["Rampur", 683], ["Saharanpur", 684], ["Sambhal", 685], ["Sant Kabir Nagar", 686], ["Shahjahanpur", 688], ["Shamli", 689], ["Shravasti", 690], ["Siddharthnagar", 691], ["Sitapur", 692], ["Sonbhadra", 693], ["Sultanpur", 694], ["Unnao", 695], ["Varanasi", 696]], "Uttarakhand": [["Almora", 704], ["Bageshwar", 707], ["Chamoli", 699], ["Champawat", 708], ["Dehradun", 697], ["Haridwar", 702], ["Nainital", 709], ["Pauri Garhwal", 698], ["Pithoragarh", 706], ["Rudraprayag", 700], ["Tehri Garhwal", 701], ["Udham Singh Nagar", 705], ["Uttarkashi", 703]], "West Bengal": [["Alipurduar District", 710], ["Bankura", 711], ["Basirhat HD (North 24 Parganas)", 712], ["Birbhum", 713], ["Bishnupur HD (Bankura)", 714], ["Cooch Behar", 715], ["COOCHBEHAR", 783], ["Dakshin Dinajpur", 716], ["Darjeeling", 717], ["Diamond Harbor HD (S 24 Parganas)", 718], ["East Bardhaman", 719], ["Hoogly", 720], ["Howrah", 721], ["Jalpaiguri", 722], ["Jhargram", 723], ["Kalimpong", 724], ["Kolkata", 725], ["Malda", 726], ["Murshidabad", 727], ["Nadia", 728], ["Nandigram HD (East Medinipore)", 729], ["North 24 Parganas", 730], ["Paschim Medinipore", 731], ["Purba Medinipore", 732], ["Purulia", 733], ["Rampurhat HD (Birbhum)", 734], ["South 24 Parganas", 735], ["Uttar Dinajpur", 736], ["West Bardhaman", 737]]}
    # print(districts_dict)
    newdic = {i: [a for a in j if a[1] in districts_dict] for i,j in dic.items()}
    # print(newdic)
    return newdic