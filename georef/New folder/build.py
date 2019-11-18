
import sqlite3
import csv

DB = 'cities.db'
db = sqlite3.Connection(DB)
cur = db.cursor()

def orig():
    cur.execute('DROP TABLE IF EXISTS orig')
    cur.execute('''
                CREATE TABLE orig (geonameid integer,
                                    name text,
                                    asciiname text,
                                    alternatenames text,
                                    latitude real,
                                    longitude real,
                                    featureclass text,
                                    featurecode text,
                                    countrycode text,
                                    cc2 text,
                                    admin1code text,
                                    admin2code text,
                                    admin3code text,
                                    admin4code text,
                                    population integer,
                                    elevation integer,
                                    dem integer,
                                    timezone text,
                                    modificationdate text
                                    )
                ''')

    with open('cities15000.txt', 'r') as fobj:
        r = csv.reader(fobj, delimiter='\t')
        print r
        for row in r:
            row = [v.decode('latin') for v in row]
            #print row
            #continue
            insertstr = ', '.join(('?' for _ in row))
            cur.execute('INSERT INTO orig VALUES(%s)' % insertstr, row)

    db.commit()

    #for row in cur.execute('SELECT * FROM orig'):
    #    print row

    print list(cur.execute('SELECT COUNT(*) FROM orig'))
    
def prep():
    cur.execute('DROP TABLE IF EXISTS prepped')
    cur.execute('''
                CREATE TABLE prepped (id integer,
                                    iso text,
                                    name text,
                                    alternates text,
                                    lon real,
                                    lat real
                                    )
                ''')

    for row in cur.execute('SELECT geonameid, countrycode, name, asciiname, alternatenames, longitude, latitude FROM orig'):
        print row
        geonameid, countrycode, name, asciiname, alternatenames, longitude, latitude = row
        alternates = [name] + [asciiname] + alternatenames.split(',')
        row = geonameid, countrycode, name, ';'.join(alternates), longitude, latitude
        insertstr = ','.join(('?' for _ in row))
        print insertstr,row
        print 'INSERT INTO prepped VALUES (%s)' % insertstr
        continue
        cur.execute('INSERT INTO prepped VALUES (%s)' % insertstr, row)

    #cur.execute('UPDATE prepped SET "Soundex" = soundex(Name)')

    db.commit()

    for row in cur.execute('SELECT * FROM prepped'):
        print row



if __name__ == '__main__':
    orig()
    #prep()

    



