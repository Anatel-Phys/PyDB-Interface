import knn
import data_lib as data
import query_lib as ql
import matplotlib.pyplot as plt
import matplotlib as mpl
font = {'size'   : 22}
mpl.rc('font', **font)
x_fs = 30
y_fs = 30

n_cv_set = 5
n_means = 10
min_k = 1
max_k = 15
c_pen = 0.65

errors = {}
for k in range(min_k, max_k + 1):
    errors[k] = []

for n in range(n_means):
    ds = data.generate_dataset() #always shuffled in a new way
    ds_size = len(ds['d'])

    #split set
    splits = [0]
    for i in range(n_cv_set - 1):
        splits.append((i+1) * ds_size//n_cv_set)
    splits.append(ds_size)

    cv_sets = []
    for i in range(n_cv_set):
        cv_sets.append({'d' : [ds['d'][i] for i in range(splits[i], splits[i+1])], 
                        't' : [ds['t'][i] for i in range(splits[i], splits[i+1])],
                        'h' : [ds['h'][i] for i in range(splits[i], splits[i+1])]})

    for k in range(min_k, max_k + 1):
        for left_out in range(n_cv_set):
            LS = {'d' : [], 't' : [], 'h' : []}
            for i in range(n_cv_set):
                if i != left_out:
                    LS['d'].extend(cv_sets[i]['d'])
                    LS['t'].extend(cv_sets[i]['t'])
                    LS['h'].extend(cv_sets[i]['h'])
            
            model = knn.knn(LS, k, c_pen=c_pen)
            errors[k].append(data.test_model(model, cv_sets[left_out]))


for k in errors.keys():
    error = 0
    for err in errors[k]:
        error += err
    error/=n_means*n_cv_set
    errors[k] = error

k_arr = []
errors_arr = []
print(errors)

for k in errors.keys():
    k_arr.append(k)
    errors_arr.append(errors[k])

bins=[0.5, 1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5]
co, ax = plt.subplots(figsize=(10,10))
ax.plot(k_arr, errors_arr)
ax.set_xlabel("k", fontsize=x_fs)
ax.set_ylabel("MSE", fontsize=y_fs)
plt.show()






