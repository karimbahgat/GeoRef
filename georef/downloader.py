"""
Downloader submodule
Part of GeoRef, Python Offline Georeferencer
by Karim Bahgat, 2014

Downloads, structures, and formats necessary online reference/gazetteer
data for offline georeferencing use.

Unfinished alpha version
"""

import sys,os,shutil,time,csv,threading,urllib,zipfile
from helpers import messages,pypath

def DownloadCities(pointless=0):
    """
    Also note that USGS city provinces can be downloaded from http://earth-info.nga.mil/gns/html/GEOPOLITICAL_CODES.xls
    """
    
    #open loadwindow
    downloadwin = Toplevel()
    downloadwin.title("Downloading city coordinate gazetteers...")
    #text
    dltextlabel = Label(downloadwin, text="Initiating download process...")
    dltextlabel.pack(padx=10, pady=10)
    #progbar
    downloadprogress = IntVar()
    downloadprogress.set(1)
    dlprogbar = ttk.Progressbar(downloadwin, mode='determinate', name="downloadprogressbar", variable=downloadprogress, style="TProgressbar", length=framewidth*0.6)
    dlprogbar.pack(padx=20, pady=10)
    #position window
    window.update()
    frameposx = int(downloadwin.winfo_screenwidth()/2.0-downloadwin.winfo_width()/2.0)
    frameposy = int(downloadwin.winfo_screenheight()/3.0-downloadwin.winfo_height()/2.0)
    downloadwin.geometry("+"+txt(int(frameposx))+"+"+txt(int(frameposy)))
    downloadwin.grab_set()

    #download process

    def keepupdating(pointless=0):
        downloadwin.update()
        window.after(100, keepupdating)
        if downloadprogress.get() == -1:
            downloadwin.destroy()
    window.after(500, keepupdating)

    # RUN SHIT
    def actualdownload():
        #list all coord files in directory n add to list
        def download(filename):
            urllib.urlretrieve(urlsite + filename + suffix, downpath + "\\" + filename + suffix)
        def InsertFieldsAndReduce(oldtablepath, oldfieldslist, newtablepath, fieldstowrite, insertbool):
            oldtable = open(oldtablepath, "rU")
            output = open(newtablepath, "wt")
            if insertbool:
                for fields in fieldstowrite:
                    output.write(fields)
                    if fieldstowrite.index(fields)+1 >= len(fieldstowrite):
                        output.write("\n".encode("utf8"))
                    else:
                        output.write("\t".encode("utf8"))
            for row in oldtable:
                row = row.split("\t")
                columncount = 0
                for column in row:
                    if oldfieldslist[columncount].upper() in fieldstowrite:
                        try:
                            text = column.encode("utf8")
                        except:
                            text = str(column)
                        output.write(text)
                        if fieldstowrite.index(oldfieldslist[columncount].upper())+1 >= len(fieldstowrite):
                            output.write("\n".encode("utf8"))
                        else:
                            output.write("\t".encode("utf8"))
                    columncount += 1
            output.close()
            
        ### FIRST GEONAMES
##        urlsite = "http://download.geonames.org/export/dump/"#AFG_adm.zip
##        downpath = filespace + r"\Cities\GeoNames"
##        suffix = ".zip"
##        allfields = ["geonameid","name","asciiname","alternatenames","latitude","longitude","feature class","feature code","country code","cc2","admin1 code","admin2 code","admin3 code","admin4 code","population","elevation","dem","timezone","modification date"]
##        desiredfields = ["ASCIINAME", "ALTERNATENAMES", "LATITUDE", "LONGITUDE", "FEATURE CLASS"]
##        infilelist = ["AD","AE","AF","AG","AI","AL","AM","AO","AQ","AR","AS","AT","AU","AW","AX","AZ","BA","BB","BD","BE","BF","BG","BH","BI","BJ","BL","BM","BN","BO","BQ","BR","BS","BT","BV","BW","BY","BZ","CA","CC","CD","CF","CG","CH","CI","CK","CL","CM","CN","CO","CR","CU","CV","CW","CX","CY","CZ","DE","DJ","DK","DM","DO","DZ","EC","EE","EG","EH","ER","ES","ET","FI","FJ","FK","FM","FO","FR","GA","GB","GD","GE","GF","GG","GH","GI","GL","GM","GN","GP","GQ","GR","GS","GT","GU","GW","GY","HK","HM","HN","HR","HT","HU","ID","IE","IL","IM","IN","IO","IQ","IR","IS","IT","JE","JM","JO","JP","KE","KG","KH","KI","KM","KN","KP","KR","KW","KY","KZ","LA","LB","LC","LI","LK","LR","LS","LT","LU","LV","LY","MA","MC","MD","ME","MF","MG","MH","MK","ML","MM","MN","MO","MP","MQ","MR","MS","MT","MU","MV","MW","MX","MY","MZ","NA","NC","NE","NF","NG","NI","NL","NO","NP","NR","NU","NZ","OM","PA","PE","PF","PG","PH","PK","PL","PM","PN","PR","PS","PT","PW","PY","QA","RE","RO","RS","RU","RW","SA","SB","SC","SD","SE","SG","SH","SI","SJ","SK","SL","SM","SN","SO","SR","SS","ST","SV","SX","SY","SZ","TC","TD","TF","TG","TH","TJ","TK","TL","TM","TN","TO","TR","TT","TV","TW","TZ","UA","UG","UM","US","UY","UZ","VA","VC","VE","VG","VI","VN","VU","WF","WS","XK","YE","YT","ZA","ZM","ZW"]
##        dlprogbar["maximum"] = len(infilelist)
##        #loop thru list, create reader obj, list fields, loop rows n add to finaltablelist only if part of desired fields, save new cntry file in new dir
##        downstarttime = time.time()
##        for country in infilelist:
##            timeleft = ((time.time()-downstarttime)/downloadprogress.get())*(dlprogbar["maximum"]-downloadprogress.get())
##            if timeleft >= 60:
##                timeleft = str(round(timeleft/60.0, 1)) + " minutes"
##            else:
##                timeleft = str(int(timeleft)) + " seconds"
##            dltextlabel["text"] = "Cities data 1 of 2: GeoNames \nDownloading: "+country+suffix + " (" + str(int((downloadprogress.get()/float(dlprogbar["maximum"]))*100)) + "%)\nTime left: " + str(timeleft)
##            try: # check if lvl1 exists
##                open(downpath+"\\Coord\\"+country+".txt")
##            except: # if not exists then download
##                try:
##                    download(country)
##                    geonameszip = zipfile.ZipFile(downpath + "\\" + country + suffix, "r")
##                    geonameszip.extract(country+".txt", downpath)
##                    try:
##                        InsertFieldsAndReduce(oldtablepath=downpath+"\\"+country+".txt", oldfieldslist=allfields, newtablepath=downpath+"\\Coord\\"+country+".txt", fieldstowrite=desiredfields, insertbool=True)
##                    except:
##                        Status(statusdisplay,traceback.format_exc())
##                    geonameszip.close()
##                    os.remove(downpath + "\\" + country + suffix)
##                    os.remove(downpath + "\\" + country + ".txt")
##                except:
##                    try:
##                        os.remove(downpath + "\\" + country + suffix)
##                        os.remove(downpath + "\\" + country + ".txt")
##                    except:
##                        pass
##                
##            downloadprogress.set(downloadprogress.get()+1)

        ### THEN GNS............
        urlsite = "http://earth-info.nga.mil/gns/html/cntyfile/"#AFG_adm.zip
        downpath = filespace + r"\Cities\USGS"
        suffix = ".zip"
        allfields = ["RC","UFI","UNI","LAT","LONG","DMS_LAT","DMS_LONG","MGRS","JOG","FC","DSG","PC","CC1","ADM1","POP","ELEV","CC2","NT","LC","SHORT_FORM","GENERIC","SORT_NAME_RO","FULL_NAME_RO","FULL_NAME_ND_RO","SORT_NAME_RG","FULL_NAME_RG","FULL_NAME_ND_RG","NOTE","MODIFY_DATE","DISPLAY"]
        desiredfields = ["LAT", "LONG", "FC", "FULL_NAME_ND_RO"]
        infilelist = ["AF", "AL", "AG", "AN", "AO", "AV", "AC", "AR", "AM", "AS", "AU", "AJ", "SP", "BF", "BA", "BG", "BB", "BO", "BE", "BH", "BN", "BD", "BT", "BL", "BK", "BC", "BR", "BX", "BU", "UV", "BY", "CB", "CM", "CA", "SP", "CV", "CJ", "CT", "CD", "CI", "CH", "CO", "CN", "CF", "CG", "CW", "FR", "CS", "HR", "CU", "CY", "EZ", "EZ", "LO", "DA", "DJ", "DO", "DR", "GM", "EC", "EG", "ES", "EK", "ER", "EN", "ET", "FK", "FJ", "FI", "FR", "FG", "FP", "GB", "GA", "GG", "GM", "GH", "GI", "UK", "GR", "GL", "GJ", "GP", "GQ", "GT", "GV", "PU", "GY", "HA", "HO", "HK", "HU", "IC", "IN", "ID", "IR", "IZ", "EI", "IS", "IT", "IV", "JM", "JA", "JO", "IN", "PK", "KZ", "KE", "KR", "KN", "KS", "KV", "KU", "KG", "LA", "LG", "LE", "LT", "LI", "LY", "LH", "LU", "MC", "MK", "MA", "MI", "MY", "MV", "ML", "MT", "IM", "RM", "MB", "MR", "MF", "MX", "FM", "MD", "MG", "MJ", "MH", "MO", "MZ", "BM", "WA", "NP", "NL", "AA", "UC", "NL", "NN", "NC", "NZ", "NU", "NG", "NI", "NE", "KN", "YM", "UK", "CQ", "NO", "MU", "PK", "PS", "PM", "PP", "PA", "PE", "RP", "PL", "PO", "US", "QA", "RE", "ZI", "RO", "RS", "RW", "SH", "VC", "WS", "TP", "SA", "SG", "RI", "RI", "MJ", "SE", "SL", "SN", "LO", "SI", "BP", "SO", "SF", "KS", "SU", "VM", "YM", "AM", "AJ", "BO", "EN", "GG", "KZ", "KG", "LG", "LH", "MD", "RS", "TI", "UP", "UZ", "SP", "CE", "SC", "SU", "NS", "WZ", "SW", "SZ", "SY", "TW", "TI", "TZ", "TH", "TT", "TO", "TL", "TN", "TD", "TS", "TU", "TX", "TK", "TV", "UG", "UP", "AE", "US", "UY", "UZ", "NH", "VT", "VE", "VM", "VI", "US", "WF", "WE", "GZ", "GM", "WI", "YM", "HR", "KV", "MK", "MJ", "RI", "SI", "BK", "CG", "ZA", "ZI"]
        dlprogbar["maximum"] = len(infilelist)
        #loop thru list, create reader obj, list fields, loop rows n add to finaltablelist only if part of desired fields, save new cntry file in new dir
        downstarttime = time.time()
        for country in infilelist:
            country = country.lower()
            timeleft = ((time.time()-downstarttime)/downloadprogress.get())*(dlprogbar["maximum"]-downloadprogress.get())
            if timeleft >= 60:
                timeleft = str(round(timeleft/60.0, 1)) + " minutes"
            else:
                timeleft = str(int(timeleft)) + " seconds"
            dltextlabel["text"] = "Cities data 2 of 2: GNS \nDownloading: "+country+suffix + " (" + str(int((downloadprogress.get()/float(dlprogbar["maximum"]))*100)) + "%)\nTime left: " + str(timeleft)
            try: # check if lvl1 exists
                open(downpath+"\\Coord\\"+country+".txt")
            except: # if not exists then download
                try:
                    download(country)
                    gnszip = zipfile.ZipFile(downpath + "\\" + country + suffix, "r")
                    gnszip.extract(country+".txt", downpath)
                    try:
                        InsertFieldsAndReduce(oldtablepath=downpath+"\\"+country+".txt", oldfieldslist=allfields, newtablepath=downpath+"\\Coord\\"+country+".txt", fieldstowrite=desiredfields, insertbool=False)
                    except:
                        Status(statusdisplay,traceback.format_exc())
                    gnszip.close()
                    os.remove(downpath + "\\" + country + suffix)
                    os.remove(downpath + "\\" + country + ".txt")
                except:
                    try:
                        os.remove(downpath + "\\" + country + suffix)
                        os.remove(downpath + "\\" + country + ".txt")
                    except:
                        pass
                    
            # and then download USA separately
                
            downloadprogress.set(downloadprogress.get()+1)

        #all downloads complete
        downloadprogress.set(-1)
        downloaddatabutton.place(relx=-50)
        inputbutton["state"] = NORMAL
        downloadprogress.set(-1)

    newthread = threading.Thread(target=actualdownload)
    newthread.daemon = True
    newthread.start()

def DownloadGADM(downpath="Data/Provinces"):
    """
    Works, but:
    - print time until completion
    - clean up code and args!
    """

    #setup vars
    urlsite = "http://biogeo.ucdavis.edu/data/gadm2/shp/"#AFG_adm.zip
    infilelist = ["AFG","ALB","DZA","AND","AGO","ATG","ARG","ARM","AUS","AUT","AZE","BHS","BHR","BGD","BRB","BLR","BEL","BLZ","BEN","BTN","BOL","BIH","BWA","BRA","BRN","BGR","BFA","BDI","KHM","CMR","CAN","CAF","TCD","CHL","CHN","HKG","COL","COM","COG","COD","CRI","CIV","HRV","CUB","CYP","CZE","DNK","GRL","DJI","DMA","DOM","ECU","EGY","SLV","GNQ","ERI","EST","ETH","FJI","FIN","FRA","FRA","NCL","GAB","GEO","DEU","GHA","GRC","GRD","GTM","GIN","GNB","GUY","HTI","HND","HUN","ISL","IND","IDN","IRN","IRQ","IRL","ISR","PSE","ITA","JAM","JPN","JOR","KAZ","KEN","XKX","KWT","KGZ","LAO","LVA","LBN","LSO","LBR","LBY","LTU","LUX","MKD","MDG","MWI","MYS","MDV","MLI","MLT","MRT","MUS","MEX","MDA","MNG","MNE","MAR","ESH","MOZ","MMR","NAM","NPL","NLD","NZL","NIC","NER","NGA","PRK","NOR","OMN","PAK","PAN","PNG","PRY","PER","PHL","POL","PRT","QAT","ROU","RUS","RWA","SAU","SEN","SRB","SYC","SLE","SGP","SVN","SLB","SOM","ZAF","KOR","ESP","LKA","KNA","SDN","SDN","SUR","SWZ","SWE","CHE","SYR","TWN","TJK","TZA","THA","GMB","TLS","TGO","TTO","TUN","TUR","TKM","UGA","UKR","ARE","BMU","GBR","GBR","USA","VIR","URY","UZB","VUT","VEN","VNM","YEM","ZMB","ZWE","ASM","AIA","ESP","ESP","CPV","CYM","COK","DEU","ALA","GUF","PYF","GIB","GLP","GUM","KIR","MAC","IMN","MHL","MTQ","MYT","FSM","MSR","NIU","YEM","MNP","PLW","PRI","REU","ZWE","SHN","VCT","WSM","STP","SVK","VNM","YEM","TKL","TON","TCA","TUV","VAT","VGB","WLF","DEU","COD"]
    suffix = "_adm.zip"
    downloadtotal = len(infilelist)
    eachcntrleveltoget = [1,2,3]
    eachfiletype = ["dbf","prj","shx","shp"]
    # check and create folder structure
    datafolder = pypath.Folder(downpath,exists=False).fullpath
    shapesfolder = pypath.Folder(datafolder,"Shapes",exists=False).fullpath
    if not os.path.lexists(shapesfolder):
        os.makedirs(shapesfolder)
    namesfolder = pypath.Folder(datafolder,"Names",exists=False).fullpath
    if not os.path.lexists(namesfolder):
        os.makedirs(namesfolder)
    #main
    def actualdownload():
        #list all coord files in directory n add to list
        def download(filename,downloadpath):
            urllib.urlretrieve(urlsite + filename + suffix, downloadpath)
        #loop thru list, create reader obj, list fields, loop rows n add to finaltablelist only if part of desired fields, save new cntry file in new dir
        downstarttime = time.time()
        iterfiles = messages.ProgressReport(infilelist,text="Downloading GADM subnational boundary data...")
        for downloadprogress,country in enumerate(iterfiles):
            downloadprogress += 1 #to avoid float div error on first iteration
            lastlevel = eachcntrleveltoget[-1]
            timeleft = ((time.time()-downstarttime)/downloadprogress)*(downloadtotal-downloadprogress)
            if timeleft >= 60:
                timeleft = str(round(timeleft/60.0, 1)) + " minutes"
            else:
                timeleft = str(int(timeleft)) + " seconds"
            # maybe update time until completion...
            ###dltextlabel["text"] = "Downloading and extracting: "+country+suffix + " (" + str(int((downloadprogress.get()/float(dlprogbar["maximum"]))*100)) + "%)\nTime left: " + str(timeleft)

            # check if lvl1 exists
            try:
                lvl1path = pypath.File(datafolder,country+"_adm1.shp", exists=False).fullpath
                open(lvl1path)
            # if not exists then download
            except: 
                try:
                    #download zipfile
                    zippath = pypath.File(datafolder,country+".zip",exists=False).fullpath
                    download(country,zippath)
                    gadmshapeszip = zipfile.ZipFile(zippath, "r")
                    #extract polygon shapes
                    for level in eachcntrleveltoget:
                        try:
                            for filetype in eachfiletype:
                                gadmshapeszip.extract(country+suffix.split(".")[0]+str(level)+"."+filetype, shapesfolder)
                        except:
                            lastlevel = level-1
                            break
                    #extract lookup-names tables
                    if lastlevel > 0:
                        gadmshapeszip.extract(country+suffix.split(".")[0]+str(lastlevel)+".csv", namesfolder)
                        nametablepath = pypath.File(namesfolder,country+suffix.split(".")[0]+str(lastlevel)+".csv").fullpath
                        csvtotxtreader = csv.reader(open(nametablepath, "rb"), delimiter=",")
                        csvtotxtreader = list(csvtotxtreader)
                        newnametablepath = pypath.File(namesfolder,country+suffix.split(".")[0]+".txt",exists=False).fullpath
                        copytable = csv.writer(open(newnametablepath, "wb"), delimiter="\t")
                        for row in csvtotxtreader:
                            copytable.writerow(row)
                        gadmshapeszip.close()
                    #remove temp files
                    os.remove(zippath)
                    os.remove(nametablepath)
                except:
                    try:
                        os.remove(zippath)
                    except:
                        pass
        #all downloads complete

    #run downloads as separate process
    newthread = threading.Thread(target=actualdownload)
    newthread.daemon = True
    newthread.start()
    

def DownloadCShapes(pointless=0):

    #open loadwindow
    global downloadwin
    downloadwin = Toplevel()
    downloadwin.title("Downloading CShapes country shapefile...")
    #text
    dltextlabel = Label(downloadwin, text="Initiating download process...")
    dltextlabel.pack(padx=10, pady=10)
    #progbar
    downloadprogress = IntVar() # pointless, only to check if loading is finished and so mainwindow can destroy loadwin
    downloadprogress.set(1)
    dlprogbar = ttk.Progressbar(downloadwin, mode='indeterminate', name="downloadprogressbar", style="TProgressbar", length=framewidth*0.6)
    dlprogbar.pack(padx=20, pady=10)
    dlprogbar.start(10)
    #position window
    window.update()
    frameposx = int(downloadwin.winfo_screenwidth()/2.0-downloadwin.winfo_width()/2.0)
    frameposy = int(downloadwin.winfo_screenheight()/3.0-downloadwin.winfo_height()/2.0)
    downloadwin.geometry("+"+txt(int(frameposx))+"+"+txt(int(frameposy)))
    downloadwin.grab_set()

    #download process
    urlsite = "http://downloads.weidmann.ws/cshapes/Shapefiles"
    urlfile = "cshapes_0.4-2.zip"
    downpath = filespace + r"\Countries"
    downfile = "cshapes"

    def keepupdating(pointless=0):
        downloadwin.update()
        window.after(100, keepupdating)
        if downloadprogress.get() == -1:
            downloadwin.destroy()
    window.after(500, keepupdating)

    # RUN SHIT
    def actualdownload():
        #list all coord files in directory n add to list
        def download(urlfile):
            urllib.urlretrieve(urlsite+"/"+urlfile, downpath + "\\"+downfile+".zip")
        eachfiletype = ["dbf","prj","shx","shp"]
        #loop thru list, create reader obj, list fields, loop rows n add to finaltablelist only if part of desired fields, save new cntry file in new dir
        try: # check if lvl1 exists
            open(downpath+"/"+downfile+".shp")
        except: # if not exists then download
            try:
                dltextlabel["text"] = "Downloading and extracting: "+urlfile
                download(urlfile)
                gadmshapeszip = zipfile.ZipFile(downpath + "\\" + downfile + ".zip", "r")
                for filetype in eachfiletype:
                    gadmshapeszip.extract(downfile+"."+filetype, downpath)
                gadmshapeszip.close()
                os.remove(downpath + "\\" + downfile + ".zip")
            except:
                #Status(statusdisplay, traceback.format_exc())
                try:
                    os.remove(downpath + "\\" + downfile + ".zip")
                except:
                    pass

        #all downloads complete
        downloaddatabutton.place(relx=-50)
        inputbutton["state"] = NORMAL
        downloadprogress.set(-1)

    newthread = threading.Thread(target=actualdownload)
    newthread.daemon = True
    newthread.start()

#USER FUNCTIONS
def Download(data, downpath=None):
    if data == "cities":
        if downpath:
            DownloadCities(downpath)
        else:
            DownloadCities()
    elif data == "gadm":
        if downpath:
            DownloadGADM(downpath)
        else:
            DownloadGADM()
    elif data == "countries":
        if downpath:
            DownloadCShapes(downpath)
        else:
            DownloadCShapes()



