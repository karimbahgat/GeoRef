
import sqlite3
import os
import csv
import difflib

# TODO: match each word separately...
# ...also check uniqueness of match...

ROOT = os.path.split(__file__)[0]
PATH_LOCODE = os.path.join(ROOT, 'LOCODE', 'cities.db')
PATH_GEONAMES = os.path.join(ROOT, 'GeoNames', 'cities.db')

def locode(iso):
    db = sqlite3.Connection(PATH_LOCODE)
    cur = db.cursor()
    for code,name1,name2 in cur.execute("select LOCODE,Name,NameWoDiacratics from orig where Iso = '%s'" % iso):
        names = [name1,name2]
        yield code,names

def geonames(iso):
    db = sqlite3.Connection(PATH_GEONAMES)
    cur = db.cursor()
    for row in cur.execute("select geonameid,name,asciiname,alternatenames from orig where countrycode = '%s'" % iso):
        geonameid,name,asciiname,alternatenames = row
        names = [name] + [asciiname] + alternatenames.split(',')
        yield geonameid,names

def splitabbrev(sub):
    if all((ch.isupper() for ch in sub)):
        return ' '.join([ch for ch in sub])
    else:
        return sub
    
def normalize(text):
    text = text.strip().replace(".","").replace("'","")
    text = text.replace("-"," ").replace(","," ").replace('_',' ')
    #text = " ".join(list((splitabbrev(word) for word in text.split())))
    text = text.lower()
    text = " ".join(sorted(text.split()))
    return text

stndlookup = {'islands':'island',
              'isl':'island',
              'is':'island',
              'mt':'mountain',
              'mount':'mountain',
              'mnt':'mountain',
              'cp':'cape',
              'region':'',
              'greater':'',
              }

def standardize(text):
    stnd = ' '.join((stndlookup.get(word, word)
                       for word in text.split()))
    return stnd

def prep(source):
    print 'loading'
    cities = dict()
    for code,names in source:
        if not code: continue
        offname = names[0]
        names = [normalize(n) for n in names]
        names = [standardize(n) for n in names]
        names = [n for n in names if n]
        #print code,names
        cities[code] = dict(name=offname, names=names)
    return cities

def match(cities, name):
    name = standardize(normalize(name))
    print 'searching for',name

    # compute diffs for all
    print 'computing'
    for code,dct in cities.items():
        for n in dct['names']:
            if name == n:
                sim = 1
                #longest = min(len(name), len(n))
        else:
            sim = 0
            #longest = 0
            for n in dct['names']:
                m = difflib.SequenceMatcher(None, name, n)
                sim = max(sim, m.ratio())
                #longest = max(longest,
                #              max((b.size for b in m.get_matching_blocks())) / float(len(n))
                #              )
        dct['sim'] = sim
        #dct['longest'] = longest
        dct['code'] = code
        #dct['final_max'] = max(sim, longest)
        #dct['final_avg'] = sum([sim, longest]) / 2.0

    # compute relative improvements
##    for ind in ['sim','longest']:
##        srt = sorted(cities.items(), key=lambda (code,d): -d[ind])
##        for i in range(len(srt)-1):
##            code1,dct1 = srt[i]
##            code2,dct2 = srt[i+1]
##            if dct2[ind] == 0:
##                reldiff = 0
##            else:
##                reldiff = dct1[ind] / dct2[ind]
##            dct1[ind+'_reldiff'] = reldiff
##        dct2[ind+'_reldiff'] = 0
    
    # choose best one, but only if there is a clear winner
##    srt = sorted(cities.items(), key=lambda (code,d): -d['final_avg'])
##    for i in range(len(srt)):
##        code1,dct1 = srt[i]
##        code2,dct2 = srt[i+1]
##        findiff = dct1['final_avg'] / dct2['final_avg']
##        print findiff
##        print dct1
##        print dct2
##        if findiff > 1.25:
##            return code1,dct1['names']
##        else:
##            raise Exception('There was no clear match. The two top ones were: %s and %s' % (dct1, dct2))

    print 'matching'
    srt = sorted(cities.items(), key=lambda (code,d): -d['sim'])
    if len(srt) == 1:
        frst = srt[0][1]
        if frst['sim'] > 0.6:
            return frst
        else:
            raise Exception('There was no clear match')
    for i in range(len(srt)-1):
        code1,dct1 = srt[i]
        code2,dct2 = srt[i+1]
        simdiff = dct1['sim'] / dct2['sim']
        #lengthdiff = dct1['longest'] / dct2['longest']
        #print simdiff,dct1,dct2
        if dct1['sim'] > 0.7: # and simdiff > 1.1 or lengthdiff > 1.1:
            return dct1
        else:
            raise Exception('There was no clear match. The two top ones were: %s and %s' % (dct1, dct2))

def find(name):
    name = standardize(normalize(name))
    print 'searching for',name

    # compute diffs for all
    print 'computing'

    matches = []

    db = sqlite3.Connection(PATH_GEONAMES)
    cur = db.cursor()
    for r in cur.execute('''
                            select geonameid,countrycode,name,asciiname,alternatenames,longitude,latitude
                            from orig
                            '''):
        gnid,countrycode,_name,asciiname,alterns,lon,lat = r
        r = gnid,countrycode,_name,asciiname,lon,lat

        names = [_name,asciiname]
        names = [normalize(n) for n in names]
        names = [standardize(n) for n in names]
        names = [n for n in names if n]
        for n in names:
            if name == n:
                sim = 1
                matches.append((r,sim))
        else:
            for n in names:
                m = difflib.SequenceMatcher(None, name, n)
                sim = m.ratio()
                if sim >= 0.8:
                    matches.append((r,sim))

    print 'matching'
    srt = sorted(matches, key=lambda (r,sim): -sim)
    return srt

if __name__ == '__main__':
    for m in find('apia'): print m
    fdsf
    
    lookup = prep(geonames('NG'))
    print match(lookup, 'Uyo')
    lookup = prep(geonames('NO'))
    print match(lookup, 'Stavanger')
    lookup = prep(geonames('US'))
    print match(lookup, 'Washington D.C.')

    



