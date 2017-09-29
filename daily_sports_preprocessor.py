import os
from scipy import io
import numpy as np
import pandas as pd
import pickle


#TODO !!!!!
def sliding_window(dataset, window_size, overlay):
    
    # build sliding windows:
    # Major time consumer, any ideas how to overcome it?
    for i in range(0, dataset.shape[0] - window_size + 1, window_size - overlay):  
        
        temp_data = dataset[i:i + window_size, :]
        
        if i == 0: 
            data = temp_data.reshape(1, temp_data.shape[0] * temp_data.shape[1])
            
        else:
            data = np.concatenate((data, temp_data.reshape(1,temp_data.shape[0] * temp_data.shape[1])), axis = 0)
            
        
        del temp_data
    
    return data



#TODO
def load_set(window_size, overlay):
    
    #loading the data one subject at a time:
    
    #subjects (8)
    for i in range(1,9):
        
        data = np.array([]).reshape(0, 3 + window_size * 45)
        
        #activities (19)
        for j in range(1,20):
            
            print('Subject ' + str(i) + ' Activity ' + str(j))
            print('-------------------------------------------------------------------')
            
            #trials (60)
            for k in range(1,61):
                
                act_num = '0'
                if j > 9:
                    act_num = ''
                    
                trial_num = '0'
                if k > 9:
                    trial_num = ''
                    
                    
                #load data
                fname = 'a' + act_num + '' + str(j) + '/p' + str(i) + '/s' + trial_num + '' + str(k)
                raw_data = pd.read_csv('Daily and sports activities/data/' + fname + '.txt', sep=',', header=None)
                
                #sliding window over it
                raw_data = sliding_window(raw_data.values.astype(float), window_size, overlay)
                
                #append labels
                len_raw = raw_data.shape[0]
                raw_data = np.concatenate((np.repeat([[i]], len_raw, axis=0), np.repeat([[j]], len_raw, axis=0), np.repeat([[k]], len_raw, axis=0), raw_data), axis = 1)
                
                data = np.concatenate((data,raw_data), axis = 0)
                del raw_data
        
        #save to pickle TODO
        pickle.dump(data, open('Daily and sports activities/Subject' + str(i) + '_preprocessed.txt' ,'wb'), pickle.HIGHEST_PROTOCOL)
        
        print(data.shape)
        del data
                
    return 1


def merge_subjects(window_size):
    
    #make column names
    names = [
        'accx_',
        'accy_',
        'accz_',
        'gyrox_',
        'gyroy_',
        'gyroz_',
        'magx_',
        'magy_',
        'magz_'
    ]
    
    addons = [
        'T_',
        'RA_',
        'LA_',
        'RL_',
        'LL_',
    ]
    
    raw = [cols + '' + addons[j] + str(i) for j in range(0,5) for i in range(1, window_size + 1) for cols in names]
    columns = ['Activity', 'Trial']
    columns.extend(raw)
    
    #go through all subjects and merge them (8)
    for i in range(1,9):
        
        print('Subject ' + str(i))
        print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        
        if i == 1:
            data = pickle.load(open('Daily and sports activities/Subject' + str(i) + '_preprocessed.txt' ,'rb'))
        else:
            data = np.concatenate((data, pickle.load(open('Daily and sports activities/Subject' + str(i) + '_preprocessed.txt' ,'rb'))), axis = 0)
    
    
    print(len(columns))
    print(data.shape)
    
    #make dataframe
    data = pd.DataFrame(data[:,1:], index = data[:,0], columns = columns)
    data.index.name = 'Subject'
    
    #save data
    pickle.dump(data, open('Daily and sports activities/full_preprocessed.txt' ,'wb'), pickle.HIGHEST_PROTOCOL)
    
    del data
    del columns
    
    return 1



#OK 
def preprocess(window_size, overlay):
    
    if os.path.exists('Daily and sports activities'):
        print("Started preprocessing")
        load_set(window_size, overlay)
        merge_subjects(window_size)
        return 1
        
    else:
        print("The specified dataset is not available/doesnt exsist")
        