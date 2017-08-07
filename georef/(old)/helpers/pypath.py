import sys,os,time

class Folder:
    """
    A class that holds info about a folder, which can be accessed via attributes
    - folderpath must be the full path incl drive letter, or a list of path name elements to be joined together
    - **exists is optional boolean that must be set to false if dealing with imaginary paths that dont yet exist
    """
    def __init__(self, *folderpath, **kwargs):
        if kwargs.get("exists","not specified") != "not specified":
            exists = kwargs["exists"]
        else:
            exists = True
        #concatenate path elements if multiple given
        folderpath = os.path.join(*folderpath)
        #full normalized path (make into absolute path if relative)
        folderpath = os.path.abspath(folderpath)
        self.fullpath = os.path.normpath(folderpath)
        #split entire path into components
        pathsplit = []
        head,tail = os.path.split(self.fullpath)
        while head != "":
            pathsplit.insert(0,tail)
            if os.path.ismount(head):
                drive = head
                break
            head,tail = os.path.split(head)
        #parent folder path
        if drive:
            self._oneup = drive+os.path.join(*pathsplit[:-1])
        else:
            self._oneup = os.path.join(*pathsplit[:-1])
        self.foldername = pathsplit[-1]
        if exists:
            self.content = os.listdir(self.fullpath)
    def Up(self):
        newpath = self._oneup
        self.__init__(newpath)
    def Down(self, foldername):
        if foldername in self.content:
            newpath = os.path.join(self.fullpath,foldername)
            if os.path.isdir(newpath):
                self.__init__(newpath)
    def Loop(self, filetype=""):
        return FolderLoop(self.fullpath, filetype)
    def Get(self, filenames=[], foldernames=[]):
        """
        Return a list of file and folder instances for those specified by user
        """
        fileobjs = []
        for filename in filenames:
            if filename in self.content:
                fileobjs.append( File(os.path.join(self.fullpath,filename)) )
        return fileobjs

class File:
    """
    A class that holds info about a file, which can be accessed via attributes
    - filepath must be the full path incl drive letter and filetype extension, or a list of path name elements to be joined together
    - **exists is optional boolean that must be set to false if dealing with imaginary paths that dont yet exist
    """
    def __init__(self, *filepath, **kwargs):
        if kwargs.get("exists","not specified") != "not specified":
            exists = kwargs["exists"]
        else:
            exists = True
        #concatenate path elements if multiple given
        filepath = os.path.join(*filepath)
        #full normalized path (make into absolute path if relative)
        filepath = os.path.abspath(filepath)
        self.fullpath = os.path.normpath(filepath)
        #split entire path into components
        pathsplit = []
        head,tail = os.path.split(self.fullpath)
        while head != "":
            pathsplit.insert(0,tail)
            if os.path.ismount(head):
                drive = head
                break
            head,tail = os.path.split(head)
        #folder path
        if drive:
            self.folder = drive+os.path.join(*pathsplit[:-1])
        else:
            self.folder = os.path.join(*pathsplit[:-1])
        #filename and type
        fullfilename = pathsplit[-1]
        filename,filetype = os.path.splitext(fullfilename)
        self.filename = filename #".".join(fullfilename.split(".")[:-1])
        self.filetype = filetype #"." + fullfilename.split(".")[-1]
        if exists:
            #filesize
            filesize = os.path.getsize(self.fullpath)
            kb,mb,gb = 1000, 1000*1000, 1000*1000*1000
            if filesize < mb:
                filesize = filesize/float(kb)
                sizeunit = "kb"
            elif filesize < gb:
                filesize = filesize/float(mb)
                sizeunit = "mb"
            else:
                filesize = filesize/float(gb)
                sizeunit = "kb"
            self.filesize = "Size: %.3f %s" %(filesize,sizeunit)
            #last changed
            self.lastchanged = "Last changed: %s" %time.ctime(os.path.getmtime(self.fullpath))

def CurrentScript():
    curfile = File(sys.argv[0])
    return curfile.fullpath

def CurrentFolder():
    curfile = File(sys.argv[0])
    return curfile.folder

def FolderLoop(folder, filetype=""):
    """
    A generator that iterates through all files in a folder tree, either in a for loop or by using next() on it.
    Filetype can be set to only grab files that have the specified file-extension. If filetype is a tuple then grabs all filetypes listed within it.
    """
    folder = os.path.abspath(folder)
    alldirs = os.walk(folder)
    # loop through and run unzip function
    for eachdirinfo in alldirs:
        eachdir = eachdirinfo[0]
        dirfiles = eachdirinfo[2]
        for eachfile in dirfiles:
            if eachfile.endswith(filetype):
                yield File(os.path.join(eachdir,eachfile))

if __name__ == "__main__":
    for e in FolderLoop(r"C:/Users\\BIGKIMO/Desktop"):
        print("File:")
        for each in (e.folder,e.filename,e.filetype,e.filesize,e.lastchanged):
            print("\t"+each)
    print( CurrentScript() )
    print( CurrentFolder() )
    folder = Folder(r"C:/Users\\BIGKIMO/Desktop")
    print( folder.fullpath,folder.foldername,folder.content )
    for e in folder.Get(filenames=["desktop.ini","Downloads.lnk"]):
        print( e.filename )
    folder.Up()
    print( folder.fullpath )
    for e in folder.Loop():
        pass #print e.fullpath
    folder.Down("Desktop")
    print( folder.fullpath )
