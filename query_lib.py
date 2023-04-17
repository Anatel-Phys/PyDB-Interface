import mysql.connector
from mysql.connector import errorcode
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from connect import logToDB

dataValIdx = {'amd' : 2, 'rs' : 3, 't' : 4, 'h' : 5}
spectraValIdx = {'article' : 1, 'mat' : 2, 'coat' : 3, 'd' : 4, 'l' : 5, 'fab' : 6}
db_name = {'d' : 'mean_d_nw', 'l' : 'mean_l_nw', 'h' : 'haze', 't' : 'trans', 'article' : 'article_key', 'mat' : 'material', 'coat' : 'coating', 'fab_met' : 'fabrication_method', 'pst_tmt' : 'post_treatment'}
spectra_name = {'t' : 'T', 'h' : 'Haze', 'rs' : 'Rs', 'amd' : 'amd'}
"""
Returns data in the format 
data = {
    spectrum1 : 
        {'val' : [val1, val2, val3, ...], 'otherval : [otherval1, ...]},
    spectrum2 :
        {...}
}

table : one of the tables od the DB
data_vals : 
    an array of values of interest from the data table
    Accepted values are amd, rs, t, h
spectra_vals:
    an array of the labels of value of interest from the spectra table
    Accepted values are d, l, article_key, mat, coat, fab
notnull : the values that should not be null in the spectrum medadata.
    Accepted values are mat, coat, d, l, fab_met, pst_tmt
"""
def query_data(spectra_vals, data_vals, notnull):
    cnx = logToDB()
    cursor = cnx.cursor()

    dic = {} 
    spectra = {}

    query = "SELECT * FROM spectra"
    if len(notnull) > 0:
        query += " WHERE " + str(db_name[notnull[0]]) + " IS NOT NULL"
    if len(notnull) > 1:
        for i in range(1, len(notnull)):
            query += " AND " + str(db_name[notnull[i]]) + " IS NOT NULL"

    cursor.execute(query)
    for spectrum in cursor:
        spectra[spectrum[0]] = {}
        for val in spectra_vals:
            if val == 'd' or val == 'l':
                spectra[spectrum[0]][val] = float(spectrum[spectraValIdx[val]])
            else:
                spectra[spectrum[0]][val] = spectrum[spectraValIdx[val]]

    for spectrum in spectra.keys():
        contains_val = True
        for val in data_vals:
            if "_" + str(spectra_name[val]) not in spectrum:
                contains_val = False
                break
        if contains_val:
            dic[spectrum] = {}
            for val in spectra_vals:
                dic[spectrum][val] = []
            for val in data_vals:
                dic[spectrum][val] = []
            
            query = "SELECT * FROM data WHERE spectrum_key = '" + str(spectrum) + "'"
            cursor.execute(query)
            for data in cursor:
                for val in spectra_vals:
                    dic[spectrum][val].append(spectra[spectrum][val])
                for val in data_vals:
                    dic[spectrum][val].append(float(data[dataValIdx[val]]))
    return dic

"""
dic = {
    spectra_1 : {
        val : [val, val2, ...],
        otherVal : [otherVal1, otherVal2, ...],
        ...
        },
    spectra_2 : {
        ...
    },
    ...
}
"""


def query_spectra_vals(vals):
    cnx = logToDB()
    cursor = cnx.cursor()

    dic = {}
    if len(vals) == 0:
        return dic
    query = "SELECT * FROM spectra WHERE "
    query += str(db_name[vals[0]]) + " IS NOT NULL "
    for i in range(1, len(vals)):
        query += "AND " + str(db_name[vals[i]]) + " IS NOT NULL "
    cursor.execute(query)
    for spectrum in cursor:
        dic[spectrum[0]] = {}
        for val in vals:
            if val == 'd' or val == 'l':
                dic[spectrum[0]][val] = float(spectrum[spectraValIdx[val]])
            else:
                dic[spectrum[0]][val] = spectrum[spectraValIdx[val]]


    return dic

def query_spectra_data(spectra, vals):
    cnx = logToDB()
    cursor = cnx.cursor()

    query = ""
    for spectrum in spectra:
        query = "SELECT * FROM data WHERE spectrum_key = '" + str(spectrum) + "'"
        cursor.execute(query)

def query_article_list(spectra):
    cnx = logToDB()
    cursor = cnx.cursor()

    spectra_articles = {}
    for spectrum in spectra:
        query = "SELECT * FROM spectra WHERE key_spectrum = '" + str(spectrum) + "'"
        cursor.execute(query)
        for i in cursor:
            spectra_articles[spectrum] = i[1]
            break

    return spectra_articles

def assemble_spectra_to_article(spectra):
    article_val = {}
    articles = query_article_list(spectra)

    for spectrum in spectra.keys():
        art = articles[spectrum]
        if art not in article_val.keys():
            article_val[art] = {}
            for val in spectra[spectrum].keys():
                article_val[art][val] = []
        for val_key in spectra[spectrum].keys():
            try:
                for val in spectra[spectrum][val_key]:
                    article_val[art][val_key].append(val)
            except TypeError:
                article_val[art][val_key].append(spectra[spectrum][val_key])


    return article_val

def query_spectra_with_data(spectra_vals, data_vals):
    cnx = logToDB()
    cursor = cnx.cursor()

    dic = {}

    query = "SELECT * FROM spectra"
    if len(spectra_vals) > 0:
        query += " WHERE " + str(db_name[spectra_vals[0]]) + " IS NOT NULL"
    if len(spectra_vals) > 1:
        for i in range(1, len(spectra_vals)):
            query += " AND " + str(db_name[spectra_vals[i]]) + " IS NOT NULL"
    
    cursor.execute(query)
    for spectrum in cursor:
        spectrum_key = spectrum[0]
        in_spectrum = True
        for val in data_vals:
            if "_" + str(spectra_name[val]) not in spectrum_key:
                in_spectrum = False
                break
        if in_spectrum:
            dic[spectrum[0]] = {}
            for val in spectra_vals:
                if val == 'd' or val == 'l':
                    dic[spectrum[0]][val] = float(spectrum[spectraValIdx[val]])
                else:
                    dic[spectrum[0]][val] = spectrum[spectraValIdx[val]]
    
    for spectrum in dic.keys():
        query = "SELECT * FROM data WHERE spectrum_key = '" + str(spectrum) + "'"
        cursor.execute(query)
        for val in data_vals:
            dic[spectrum][val] = []

        for data in cursor:
            for val in data_vals:
                dic[spectrum][val].append(float(data[dataValIdx[val]]))
    
    return dic
"""
dic = {
    spectra_1 : {
        spec_val1 : .., spec_val2 : ...,
        data_val1 : [x1, x2, ...], 
        data_val2 : [y1, y2, ...],
        ...
        }

}
"""

def assemble_spectra_data(data):
    assembled_data = {}
    keys = list(data.keys())
    for key in data[keys[0]].keys():
        assembled_data[key] = []
    
    for spectra in data:
        assembled_data['d'].extend(data[spectra]['d'])
        assembled_data['t'].extend(data[spectra]['t'])
        assembled_data['h'].extend(data[spectra]['h'])

    return assembled_data