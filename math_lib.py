import math


def compute_covar(x, y):
    covar = [[0.,0.],[0.,0.]]
    mean_y = 0
    mean_x = 0
    mean_xy = 0
    mean_xx = 0
    mean_yy = 0
    for i in range(len(x)):
        mean_x += x[i]
        mean_y += y[i]
        mean_xy += x[i] * y[i]
        mean_yy += y[i] * y[i]
        mean_xx += x[i] * x[i]
    mean_x /= len(x)
    mean_y /= len(y)
    mean_xx /= len(x)
    mean_xy /= len(x)
    mean_yy /= len(x)

    covar[0][0] = mean_xx - mean_x * mean_x
    covar[0][1] = mean_xy - mean_x * mean_y
    covar[1][0] = mean_xy - mean_x * mean_y
    covar[1][1] = mean_yy - mean_y * mean_y

    return covar

def compute_correl(covar):
    return covar[1][0]/(math.sqrt(covar[0][0]) * math.sqrt(covar[1][1]))

def chi_square(model, x, y, sigma):
    chis = 0
    size = len(x)
    for i in range(size):
        pred = model(x[i])
        chis += ((y[i] - pred)**2)/sigma[i]
    return chis
        
