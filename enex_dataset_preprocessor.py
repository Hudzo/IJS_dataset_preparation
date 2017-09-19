import os
from scipy import io
import numpy as np
import pandas as pd
from scipy import stats
import pickle


#Energy expenditure dataset

def utils(dataset):
    
    #temp = dataset[1:,0:3]
    #tuples = list(zip(*temp.transpose()))
    #index = pd.MultiIndex.from_tuples(tuples, names=dataset[0,0:3])
    #df = pd.DataFrame(dataset[1:,3:], index=index, columns=dataset[0,3:])
    
    return 1 #df


def sliding_window(input_data, window_size, overlay, subject):
    
    # num of attributes -> 14
    data = np.array([]).reshape(0, window_size * 14)
        
    #sliding the sliding window on a slide -> for loo is still time consuming, any better ideas??
    for j in range(0, len(input_data) - window_size, window_size - overlay):
        data = np.concatenate((data, input_data[j:j + window_size, :].reshape(1, window_size * 14)), axis = 0)

    data = np.concatenate((np.repeat([[subject]], len(data), axis=0), data), axis = 1)
    
    return data


def load_set(window_size, overlay):
    
    path_dict = {1 : 'Traditional', 2 : 'Oscillating'}
    
    #collumn names
    att_names = ['HIP_accX_', 'HIP_accY_', 'HIP_accZ_', 'HIP_gyroX_', 'HIP_gyroY_', 'HIP_gyroZ_',
                 'ANKLE_accX_', 'ANKLE_accY_', 'ANKLE_accZ_', 'ANKLE_gyroX_', 'ANKLE_gyroY_', 'ANKLE_gyroZ_',
                 'MET', 'SPEED']
    columns = [atts + str(i) for i in range(1, window_size + 1) for atts in att_names]
    
    
    # 2 different sets of data -> traditional and oscillating
    for i in range(1,3):
            
        # 10 subjects per set
        for j in range(1,11):
                
                #read txt file as a numpy array
                if j == 1:
                    temp = pd.read_csv('EnEx/EnEx/' + path_dict[i] + '/dataset_'+ str(j) +'.txt', header = None, names = None).values
                    array = sliding_window(temp, window_size, overlay, j)
                    del temp
                    
                else:
                    temp = pd.read_csv('EnEx/EnEx/' + path_dict[i] + '/dataset_'+ str(j) +'.txt', header = None, names = None).values
                    array = np.concatenate( (array, sliding_window(temp, window_size, overlay, j) ), axis = 0)
                    del temp
        
        
        #do what you meant to do with array here!!!
        
        #TODO transform into dataFrame
        array = pd.DataFrame(array[:,1:], index=array[:,0], columns=columns)
        array.index.name = 'Subject'
        
        #TODO pickle the thingy
        pickle.dump(array, open('EnEx/processed_data_' + path_dict[i],'wb'), pickle.HIGHEST_PROTOCOL)
        del array
    
    
    return 1


#OK 
def preprocess(window_size, overlay):
    
    if window_size <= overlay:
        print("Error: Window size and/or overlay")
        exit()
    
    if os.path.exists('EnEx'):
        return load_set(window_size, overlay)
        
    else:
        print("The specified dataset is not available/doesnt exsist")
        