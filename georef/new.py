
# PLAN
# for each GNS placename shapefile
#   for each year
#     add relationship to gaul adm3 for that year
#     add relationship to gaul adm2 for that year
#     add relationship to gaul adm1 for that year
#     add relationship to gaul country for that year
#     for each gaul country relationship
#       save as country year specific placename shapefile

# - gaul country
#   - 1990
#   - 1991
#   - ....

# ...geomatch routine...
# for row in data:
#   matches = []
#   prov3data = getprovdata(findgaulcountryame(row[country]))
#   for refrow in prov3data:
#     citymatch = similar(row[city],refrow[city])
#     if citymatch > 80:
#       refrow[countrymatch] = similar(row[country],refrow[country])
#       refrow[countrymatch] = similar(row[adm1],refrow[adm1])
#       matches.append(refrow)

import sqlite3
import cPickle as pickle
from itertools import izip, groupby

import shapefile as pyshp
import shapely
from shapely.geometry.geo import asShape, mapping
from shapely.prepared import prep
import rtree

# refdata has unlimited fields containing match names
class RefData:
    def __init__(self, filepath, encoding="utf8"):
        self.reader = pyshp.Reader(filepath)
        self.fields = [f[0] for f in self.reader.fields[1:]]
        self.encoding = encoding
        self.relationships = dict()

    def add_relationship(self, tag, refdata, namefield, idfields=None):
        # refdata can either exist from before, or be created via spatial overlap
        self.relationships[tag] = dict(refdata=refdata, namefield=namefield)

    def create(self, savepath):
        # TODO: ALLOW TIME DIMENSION AND OTHER SUBGROUPINGS...
        # MAYBE EVEN NESTED SUBFOLDERS FOR SUPER QUICK ACCESS
        # MOST IMPORTANT: IF SELF IS POINTS AND OTHER IS POLYGON, THEN MUCH FASTER TO LOOP POLYS THEN JOIN WITH ALL MATCHING POINTS
        # PROB ALSO GOOD TO JOIN ENTIRE ROWS MULTIPLE TIMES INSTEAD OF KEEPING ONE ROW AND ONLY WRITING A SINGLE DELIMITED STRING
        # ...

        def rowdecode(row):
            return [val.decode(self.encoding) if isinstance(val, basestring) else val for val in row]

        # routine for geomatching one relationship
        def geomatch(tag, subdict):
            # optimize if self is points or has more items
            if self.reader.shapeType in (pyshp.POINT, pyshp.MULTIPOINT) or len(self.reader) > len(subdict["refdata"].reader):
                # create spindex
                if not hasattr(self, "spindex"):
                    self.spindex = rtree.index.Index()
                    for i,shp in enumerate(self.reader.iterShapes()):
                        bbox = [shp.points[0][0],shp.points[0][1],shp.points[0][0],shp.points[0][1]] if shp.shapeType == pyshp.POINT else shp.bbox
                        self.spindex.insert(i, bbox)

                # first reverse matching for speed
                def revmatches():
                    for row,shp in izip(subdict["refdata"].reader.iterRecords(), subdict["refdata"].reader.iterShapes()):
                        #if dict(zip(self.fields, row))["SOV0NAME"] != "Russia": continue
                        #print "...",row[1] #row[4],row[14]
                        print str(row)[:100]
                        prepped = prep(asShape(shp)) # prepares geometry for many intersection tests (maybe only useful if is polygon and other is points, but not sure)
                        bbox = [shp.points[0][0],shp.points[0][1],shp.points[0][0],shp.points[0][1]] if shp.shapeType == pyshp.POINT else shp.bbox
                        ilist = self.spindex.intersection(bbox)
                        for i in ilist:
                            othershp = self.reader.shape(i)
                            if prepped.intersects(asShape(othershp)):
                                yield row,i

                lookups = dict()
                key = lambda(row,i): i
                for i,items in groupby(sorted(revmatches(), key=key), key=key):
                    names = []
                    for matchrow,i in items:
                        name = dict(zip(subdict["refdata"].fields, matchrow))[subdict["namefield"]]
                        name = name.decode(subdict["refdata"].encoding) if isinstance(name, basestring) else name
                        names.append(name)

                    matches = "|".join(names)
                    lookups[i] = matches

                for i,row in enumerate(self.reader.iterRecords()):
                    matches = lookups.get(i, None)
                    print i, matches
                    yield matches

            else:
                # create spindex
                subdict["spindex"] = rtree.index.Index()
                for i,shp in enumerate(subdict["refdata"].reader.iterShapes()):
                    bbox = [shp.points[0][0],shp.points[0][1],shp.points[0][0],shp.points[0][1]] if shp.shapeType == pyshp.POINT else shp.bbox
                    subdict["spindex"].insert(i, bbox)

                # match each
                for row,shp in izip(self.reader.iterRecords(), self.reader.iterShapes()):
                    #if dict(zip(self.fields, row))["SOV0NAME"] != "Russia": continue
                    #print "...",row[1] #row[4],row[14]
                    prepped = prep(asShape(shp)) # prepares geometry for many intersection tests (maybe only useful if is polygon and other is points, but not sure)
                    
                    subdict["matches"] = []
                    refdata = subdict["refdata"]
                    namefield = subdict["namefield"]
                    spindex = subdict["spindex"]
                    bbox = [shp.points[0][0],shp.points[0][1],shp.points[0][0],shp.points[0][1]] if shp.shapeType == pyshp.POINT else shp.bbox
                    ilist = spindex.intersection(bbox)
                    for i in ilist:
                        othershp = refdata.reader.shape(i)
                        #for otherrow,othershp in zip(refdata.reader.iterRecords(), refdata.reader.iterShapes()):
                        if prepped.intersects(asShape(othershp)):
                            otherrow = refdata.reader.record(i)
                            otherrow = rowdecode(otherrow)
                            name = dict(zip(refdata.fields, otherrow))[namefield]
                            subdict["matches"].append(name)
                    subdict["matches"] = "|".join(subdict["matches"])

                    print row, subdict["matches"]

                    yield subdict["matches"]

        # create iterators for all relationships
        reliters = []
        for tag,subdict in self.relationships.items():
            reliters.append(list(geomatch(tag,subdict))) # must be list, to avoid simultaneous iterating

        # finally, zip original rows with all relationship iterators
        def outrows():
            matchrows = izip(*reliters) 
            for feat,matchrow in izip(self.reader.iterShapeRecords(), matchrows):
                newrow = rowdecode(feat.record) + [feat.shape.__geo_interface__] + list(matchrow)
                yield newrow

        # setup db writer (AND ADD REL FIELDS...)
        import os
        if os.path.exists(savepath) and input("Overwrite %s? " % savepath):
            os.remove(savepath)
        
        db = sqlite3.connect(savepath, detect_types=sqlite3.PARSE_DECLTYPES)
        sqlite3.register_adapter(dict, pickle.dumps)
        sqlite3.register_converter("dict", pickle.loads)

        def field2col(name,typ,size,deci):
            if typ == "C":
                return name,"text"
            elif typ == "N" and deci == 0:
                return name,"int"
            elif (typ == "N" and deci > 0) or typ == "F":
                return name,"real"
            else:
                raise Exception("Unknown type %s" % typ)

        fields = [f for f in self.reader.fields[1:]]
        columns = [field2col(name,typ,size,deci) for name,typ,size,deci in fields]
        columns += [("geojson","dict")]

        columns += [(tag,"text") for tag in self.relationships.keys()] # add extra fields (force text)
        
        columnstring = ", ".join(("%s %s" % (name,typ) for name,typ in columns))
        print columnstring

        db.execute("""
                    CREATE TABLE data (%s);
                    """ % columnstring
                   )

        # batch write to file
        question_marks = ", ".join("?" for _ in range(len(columns)))
        db.executemany("""
                    INSERT INTO data VALUES (%s);
                    """ % question_marks, outrows())
        db.commit()
        db.close()

       


if __name__ == "__main__":   
    cnt = RefData(r"C:\Users\kimo\Downloads\cshapes_0.6\cshapes.shp")
    prv = RefData(r"C:\Users\kimo\Downloads\ne_10m_admin_1_states_provinces\ne_10m_admin_1_states_provinces.shp", encoding="latin")
    plc = RefData(r"C:\Users\kimo\Downloads\ne_10m_populated_places\ne_10m_populated_places.shp")
    
    #cnt.add_relationship("cities", plc, "NAME")
    #cnt.add_relationship("provs", prv, "name")
    #cnt.create("countries.db")

    #prv.add_relationship("country", cnt, "CNTRY_NAME")
    #prv.create("provs.db")

    plc.add_relationship("country", cnt, "CNTRY_NAME")
    plc.add_relationship("provs", prv, "name")
    from time import time
    t = time()
    plc.create("places.db")
    print time()-t
    
    # TODO: should be only one db, saving multiple refdata as separate tables
    # ...
    


