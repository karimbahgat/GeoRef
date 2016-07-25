
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

import shapefile as pyshp
import shapely
from shapely.geometry.geo import asShape, mapping
from shapely.prepared import prep
import rtree

# refdata has unlimited fields containing match names
class RefData:
    def __init__(self, filepath):
        self.reader = pyshp.Reader(filepath)
        self.fields = [f[0] for f in self.reader.fields[1:]]
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
        writer = pyshp.Writer(savepath)
        writer.fields = self.reader.fields[1:]
        for tag in self.relationships.keys():
            writer.field(tag, "C", 40)

        for tag,subdict in self.relationships.items():
            subdict["spindex"] = rtree.index.Index()
            for i,shp in enumerate(subdict["refdata"].reader.iterShapes()):
                bbox = [shp.points[0][0],shp.points[0][1],shp.points[0][0],shp.points[0][1]] if shp.shapeType == pyshp.POINT else shp.bbox
                subdict["spindex"].insert(i, bbox)
            
        for row,shp in zip(self.reader.iterRecords(), self.reader.iterShapes()):
            #if dict(zip(self.fields, row))["SOV0NAME"] != "Russia": continue
            print "...",row[1] #row[4],row[14]
            prepped = prep(asShape(shp)) # prepares geometry for many intersection tests (maybe only useful if is polygon and other is points, but not sure)
            
            for tag,subdict in self.relationships.items():
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
                        name = dict(zip(refdata.fields, otherrow))[namefield]
                        subdict["matches"].append(name)
                subdict["matches"] = "|".join(subdict["matches"])

            row = list(row)
            row.extend([subdict["matches"] or "" for subdict in self.relationships.values()])
            print "--->", row[-1]
            writer.record(*row)
            writer._shapes.append(shp)

        writer.save(savepath)



if __name__ == "__main__":
    cnt = RefData(r"C:\Users\kimo\Downloads\cshapes_0.5-1\cshapes.shp")
    prv = RefData(r"C:\Users\kimo\Downloads\ne_10m_admin_1_states_provinces\ne_10m_admin_1_states_provinces.shp")
    plc = RefData(r"C:\Users\kimo\Downloads\ne_10m_populated_places\ne_10m_populated_places.shp")

    #cnt.add_relationship("cities", plc, "NAME")
    #cnt.create("hmmm.shp")

    cnt.add_relationship("provs", prv, "name")
    cnt.create("hmmm.shp")

    #plc.add_relationship("country", cnt, "CNTRY_NAME")
    #plc.create("hmmm.shp")
    


