
from main import RefData




# ideal...
load existing or create new refdata
setjoinconditions
for row in table:
    geocode(row, gaul)











# test load single refdata

cnt = RefData(r"C:\Users\karbah\Downloads\cshapes_0.6\cshapes.shp")
cnt.create("cshapes_single.db")

fdsfsdf







# test combining multiple refdata

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
