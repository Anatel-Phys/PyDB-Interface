from discarded import pop_discarded
import query_lib as ql
from math_lib import compute_correl, compute_covar
import math
import copy
import random

def distance(i, d, t, data):
    return math.sqrt((d - data['d'][i]) * (d - data['d'][i]) + (t - data['t'][i]) * (t - data['t'][i]))

def generate_dataset():
    data = ql.query_data(['d'], ['t','h'], ['d'])
    pop_discarded(data)

    sorted_dataset = ql.assemble_spectra_data(data)

    idx_list = [i for i in range(len(sorted_dataset['d']))]
    random.shuffle(idx_list)

    dataset = {'d' : [], 't' : [], 'h' : []}
    for idx in idx_list:
        dataset['d'].append(sorted_dataset['d'][idx])
        dataset['t'].append(sorted_dataset['t'][idx])
        dataset['h'].append(sorted_dataset['h'][idx])

    return dataset

def split_dataset(dataset, ratio):
    ds_size = len(dataset['d'])
    LS_size = round(ds_size*ratio)
    LS = {'d' : [dataset['d'][i] for i in range(0, LS_size)], 't' : [dataset['t'][i] for i in range(0, LS_size)], 'h' : [dataset['h'][i] for i in range(0, LS_size)]}
    TS = {'d' : [dataset['d'][i] for i in range(LS_size, ds_size)], 't' : [dataset['t'][i] for i in range(LS_size, ds_size)], 'h' : [dataset['h'][i] for i in range(LS_size, ds_size)]}

    return LS, TS

def test_model(model, TS):
    error = 0
    ts_size = len(TS['h'])
    for i in range(ts_size):
        predicted_haze = model.predict_haze(TS['d'][i], TS['t'][i])
        error += (TS['h'][i] - predicted_haze) * (TS['h'][i] - predicted_haze)
        #print("Real haze : " + str(TS['h'][i]) + ", predicted haze : " + str(predicted_haze))
    error /= ts_size
    return error