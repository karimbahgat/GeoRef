"""
Datamanager submodule
Part of GeoRef, Python Offline Georeferencer
by Karim Bahgat, 2014

Creates and keeps track of all available data sources on the machine.

Unfinished alpha version
"""

import sys,os,shutil,time,csv,threading,pickle
from helpers import messages,pypath

class RefData:
    """
    The class that holds the lookup reference data

    A refdata instance has two datasources:

    1. Geodata (preexisting)
       Links to an external geographic shapefile used for georeferencing.
       Data is kept as is.
    2. Namelink data (which it creates)
       Holds record of prepped name variations files, ie link-files that link a name to geography.
       The user decides where to create the namelink data.
    """
    def __init__(self, datapath):
        self.datapath = datapath
        self.preprules = []
        #load as table
        #...
    def PrepNamelinkData(self, namelinkpath):
        self.namelinkpath = namelinkpath
        #create normal names
        #...
        #then add preprule names
        for preprule in self.preprules:
            #create prep variation
            #add variation to preprules names list
            pass
        #save all preprule names lists to pickle
        #...
    def AddPrepRule(self, preprule):
        #process preprule
        #...
        self.preprule.append(preprule)
    def SaveToPickle(self):
        pass
    def _CreateVariations(self):
        pass
    def _PickleVariationLists(self):
        pass
    def _GatherDataLinkFiles(self, newlocation):
        """
        Copy datafiles from their link paths to a new location, and change link paths to point to the new location.
        """
        pass
class RefDataManager:
    """
    A manager class that has an overview of all datasources,
    and sets and retrieves information from them
    """
    def __init__(self, managerpath=None):
        #first set picklepath, ie the memory of the refdatamanager
        if not managerpath:
            managerpath = "default_datamanager.pkl" #default manager path
        self.managerpath = pypath.File(managerpath, exists=False).fullpath
        #create new datasources pickle file if not found
        if not os.path.lexists(self.managerpath):
            datasourcesfile = open(self.managerpath,"w")
            pickle.dump(None, datasourcesfile)
            datasourcesfile.close()
    def __iter__(self):
        for name,datasource in self.ListAllDataSources().iteritems():
            yield name,datasource
    def ListAllDataSources(self):
        datasourcesfile = open(self.managerpath,"r")
        datasources = pickle.load(datasourcesfile)
        datasourcesfile.close()
        return datasources
    def GetDataSource(self, dataname):
        pass
    def AddDataSource(self, refdata, dataname):
        existingdatasources = self.ListAllDataSources()
        datasourcesfile = open(self.managerpath,"w")
        if existingdatasources:
            datasources = existingdatasources
            datasources[dataname] = refdata
        else:
            datasources = dict([(dataname,refdata)])
        pickle.dump(datasources, datasourcesfile)
        datasourcesfile.close()
    def ForgetAllDataSources(self):
        #maybe ask user to verify
        pass
    def GatherAllDataSources(self, newlocation):
        """
        Copy all datafiles from their link paths to a new location, and change link paths to point to the new location.
        """
        #create new datasources folder if doesnt exists
        newlocation = pypath.Folder(newlocation).fullpath
        if not os.path.lexists(newlocation):
            os.makedirs(newlocation)
        for name,datasource in self:
            subfolder = pypath.Folder(newlocation, name, exists=False).fullpath
            os.makedirs(subfolder)
            datasource._GatherDataLinkFiles(subfolder)
    def _VerifyDataSources(self):
        pass

if __name__ == "__main__":
    refmanager = RefDataManager()
    
    print(refmanager.ListAllDataSources())

# how a datasource should be added...
##    countrydata = RefData(r"D:\Test Data\cshapes")
##    countrydata.AddPrepRule("...")
##    countrydata.PrepNamelinkData("relativecountrynames.pkl")
##    refmanager.AddDataSource(countrydata, "countrydata")
    
    print(refmanager.ListAllDataSources())

    



