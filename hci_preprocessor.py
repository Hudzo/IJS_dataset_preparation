import os
from scipy import io
import numpy as np
import pandas as pd
from scipy import stats
import pickle

#Skoda mini checkpoint

#TODO
def sliding_window(dataset, window_size, overlay):
    
    #extract activity id
    activity = dataset[:,0].reshape(dataset.shape[0],1)
    #delete sensor id -> not important
    dataset = np.delete(dataset,[0,1,8,15,22,29,36,43,50],1)
    
    
    for i in range(0, dataset.shape[0] - window_size, window_size - overlay):  
        
        temp_data = dataset[i:i + window_size, :]
        
        if i == 0: 
            activity_data = stats.mode(activity[i:i + window_size])[0]
            data = temp_data.reshape(1, temp_data.shape[0] * temp_data.shape[1])
            
        else:
            activity_data = np.concatenate((activity_data, stats.mode(activity[i : i + window_size])[0]), axis = 0)
            data = np.concatenate((data, temp_data.reshape(1,temp_data.shape[0] * temp_data.shape[1])), axis = 0)
            
        
        del temp_data
        
        
    del dataset
    
    
    data = np.concatenate((activity_data, data), axis = 1)
    
    
    del activity_data
    
    return data



#TODO
def load_set(window_size, overlay):
    
    moves = ['guided', 'freehand']
    
    # 1 subject 2 types of movement
    for i in range(0,2):
        
        print('Processing ' + moves[i] + ' movement')
        
        raw_data = io.loadmat('HCI/HCI/usb_hci_' + moves[i] + '.mat')['usb_hci_' + moves[i]]
        raw_data = sliding_window(raw_data, window_size, overlay)
            
        #append labels
        raw_data = np.insert(raw_data, 1, 1, axis = 1) #trial
        len_raw = raw_data.shape[0]
        raw_data = np.concatenate((np.repeat([[i]], len_raw, axis=0), raw_data), axis = 1)
        
        # dump that pickle
        pickle.dump(raw_data, open('HCI/' + moves[i] + '_preprocessed.txt' ,'wb'), pickle.HIGHEST_PROTOCOL)
        
        print(raw_data.shape)
        print('-------------------------------------------------------------------')
    
        del raw_data
    
    
    return 1


#TODO
def merge_hands(window_size):
    
    #make column names
    names = [
        '_acc1',
        '_acc2',
        '_acc3',
        '_acc4',
        '_acc5',
        '_acc6',
    ]
    
    sensor_id = ['3', '4', '18', '19', '20', '27', '29', '31']

    
    raw = [ str(j) + '_s' + s_id + cols for j in range(1, window_size + 1) for s_id in sensor_id for cols in names]
    columns = ['Activity', 'Trial']
    columns.extend(raw)
    
    moves = ['guided', 'freehand']
    
    #go through both arms and merge them
    for i in range(0,2):
        
        print(moves[i] + ' movement')
        print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        
        if i == 0:
            data = pickle.load(open('HCI/' + moves[i] + '_preprocessed.txt' ,'rb'))
        else:
            data = np.concatenate((data, pickle.load(open('HCI/' + moves[i] + '_preprocessed.txt' ,'rb'))), axis = 0)
    
    
    print(len(columns))
    print(data.shape)
    
    #make dataframe
    data = pd.DataFrame(data[:,1:], index = data[:,0], columns = columns)
    # 0 = left, 1 = right
    data.index.name = 'Movement'
    
    #delete rows with missings
    data.replace(['na','nan','NaN', 'NaT','inf','-inf','nan'], np.nan, inplace = True)
    data = data.dropna()
    
    print(data.shape)
    
    #save data
    pickle.dump(data, open('HCI/full_preprocessed.txt' ,'wb'), pickle.HIGHEST_PROTOCOL)
    
    del data
    del columns
    
    return 1
    

def preprocess(window_size, overlay):
    
    if window_size <= overlay:
        print("Error: Window size and/or overlay")
        exit()
    
    if os.path.exists('HCI/HCI'): 
        load_set(window_size, overlay)
        merge_hands(window_size)
        return 1
        
    else:
        print("The specified dataset is not available/doesnt exsist")
    
    
    