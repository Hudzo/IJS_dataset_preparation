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
    dataset = np.delete(dataset,[0,1,8,15,22,29,36,43,50,57,64],1)
    
    for i in range(0, dataset.shape[0] - window_size + 1, window_size - overlay):  
        
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
    
    arms = ['left', 'right']
    
    # 1 subject 2 hands
    for i in range(0,2):
        
        print('Processing ' + arms[i] + ' arm sensors')
        
        raw_data = io.loadmat('Skoda Mini Checkpoint\SkodaMiniCP/'+ arms[i] +'_classall_clean.mat')[arms[i] + '_classall_clean']
        raw_data = sliding_window(raw_data, window_size, overlay)
        
        #append labels
        raw_data = np.insert(raw_data, 1, 1, axis = 1) #trial
        len_raw = raw_data.shape[0]
        raw_data = np.concatenate((np.repeat([[i]], len_raw, axis=0), raw_data), axis = 1)
        
        # dump that pickle
        pickle.dump(raw_data, open('Skoda Mini Checkpoint/' + arms[i] + '_arm_preprocessed.txt' ,'wb'), pickle.HIGHEST_PROTOCOL)
        
        print(raw_data.shape)
        print('-------------------------------------------------------------------')
    
        del raw_data
    
    return 1
    
    
    
    #delete rows with missings
    data.replace(['na','nan','NaN', 'NaT','inf','-inf','nan', np.inf, -np.inf], np.nan, inplace = True)
    data = data.dropna()
    #just to be sure transform everything to float
    data = data.astype(float)
    
    
    
    pickle.dump(data, open('WARD1/processed_data.txt','wb'), pickle.HIGHEST_PROTOCOL)
    
    return 1


#TODO
def merge_hands(window_size):
    
    #make column names
    names = [
        '_accX',
        '_accY',
        '_accZ',
        '_acc_rawX',
        '_acc_rawY',
        '_acc_rawZ',
    ]

    
    raw = [ str(j) + '_i' + str(i) + cols for j in range(1, window_size + 1) for i in range(1, 11) for cols in names]
    columns = ['Activity', 'Trial']
    columns.extend(raw)
    
    arms = ['left', 'right']
    
    #go through both arms and merge them
    for i in range(0,2):
        
        print(arms[i] + ' arm')
        print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        
        if i == 0:
            data = pickle.load(open('Skoda Mini Checkpoint/' + arms[i] + '_arm_preprocessed.txt' ,'rb'))
        else:
            data = np.concatenate((data, pickle.load(open('Skoda Mini Checkpoint/' + arms[i] + '_arm_preprocessed.txt' ,'rb'))), axis = 0)
    
    
    print(len(columns))
    print(data.shape)
    
    
    #make dataframe
    data = pd.DataFrame(data[:,1:], index = data[:,0], columns = columns)
    # 0 = left, 1 = right
    data.index.name = 'Arm'
    
    #delete rows with missings
    data.replace(['na','nan','NaN', 'NaT','inf','-inf','nan'], np.nan, inplace = True)
    data = data.dropna()
    
    print(data.shape)
    
    #save data
    pickle.dump(data, open('Skoda Mini Checkpoint/full_preprocessed.txt' ,'wb'), pickle.HIGHEST_PROTOCOL)
    
    del data
    del columns
    
    return 1
    

def preprocess(window_size, overlay):
    
    if window_size <= overlay:
        print("Error: Window size and/or overlay")
        exit()
    
    if os.path.exists('Skoda Mini Checkpoint/SkodaMiniCP'): 
        load_set(window_size, overlay)
        merge_hands(window_size)
        return 1
        
    else:
        print("The specified dataset is not available/doesnt exsist")
    
    
    