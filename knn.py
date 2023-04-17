import matplotlib as mpl
import matplotlib.pyplot as plt
from discarded import pop_discarded
import query_lib as ql
from math_lib import compute_correl, compute_covar
import math
import copy

HUGE_VAL = 9999

def distance(i, d, t, data):
    return math.sqrt((d - data['d'][i]) * (d - data['d'][i]) + (t - data['t'][i]) * (t - data['t'][i]))

class knn(object):
    def __init__(self, _LS, _k, c_pen = 1.):
        self.LS = copy.deepcopy(_LS)
        self.k = _k
        self.size = len(_LS['t'])
        self.t_shift = min(self.LS['t'])
        for i in range(self.size):
            self.LS['t'][i] -= self.t_shift
        self.t_fact = max(self.LS['t'])
        for i in range(self.size):
            self.LS['t'][i] /= self.t_fact

        self.d_shift = min(self.LS['d'])
        for i in range(self.size):
            self.LS['d'][i] -= self.d_shift
        self.d_fact = max(self.LS['d'])
        for i in range(self.size):
            self.LS['d'][i] /= self.d_fact

        self.closeness_pen = c_pen #weight of the furthest neighbour will be 1 - c_pen, parameter to be tuned

            
    def get_nearest_neighbours(self, diameter, transmittance):
        d = diameter
        t = transmittance
        d = (d - self.d_shift)/self.d_fact
        t = (t - self.t_shift)/self.t_fact

        nearest = [-1 for i in range(self.k)] #will contain the indices of the nearest neighbours
        nearest_dist = [HUGE_VAL for i in range(self.k)]
        for i in range(self.size):
            dist = distance(i, d, t, self.LS)

            largest_idx = -1
            largest_dist = 0
            for n in range(self.k):
                if dist < nearest_dist[n]:
                    if nearest_dist[n] > largest_dist:
                        largest_idx = n
                        largest_dist = nearest_dist[n] #pops the furthest nearest neaighbour
            if largest_idx != -1:
                nearest[largest_idx] = i
                nearest_dist[largest_idx] = dist
                
        return nearest, nearest_dist


    def predict_haze(self, diameter, transmittance):
        nearest, nearest_dist = self.get_nearest_neighbours(diameter, transmittance)
        closeness = []
        max_dist = max(nearest_dist)
        for i in range(self.k):
            if max_dist == 0:
                closeness.append(1)
            else:
                closeness.append((max_dist - self.closeness_pen * nearest_dist[i])/max_dist)

        closeness_sum = 0
        for i in range(self.k):
            closeness_sum += closeness[i]

        haze = 0
        for i in range(self.k):
            haze += self.LS['h'][nearest[i]] * closeness[i] #weighted by the dist
        if (closeness_sum == 0):
            return haze/self.k
        return haze/closeness_sum
