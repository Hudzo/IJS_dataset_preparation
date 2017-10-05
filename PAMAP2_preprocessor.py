import os
from scipy import io
import numpy as np
import pandas as pd
from scipy import stats
import pickle


#TODO !!!!!
def sliding_window(dataset, window_size, overlay):
    
    #separate activity and raw data
    
    activity = dataset[:,1].reshape(dataset.shape[0],1)
    heart_rate = dataset[:,2].reshape(dataset.shape[0],1)
    dataset = np.delete(dataset,[1,2],1)
    
    # build sliding windows:
    # Major time consumer, any ideas how to overcome it?
    for i in range(0, dataset.shape[0] - window_size + 1, window_size - overlay):  
        
        temp_data = dataset[i:i + window_size, :]
        
        if i == 0: 
            activity_data = stats.mode(activity[i:i + window_size])[0]
            heart_data = stats.mode(heart_rate[i:i + window_size])[0]
            data = temp_data.reshape(1, temp_data.shape[0] * temp_data.shape[1])
            
        else:
            activity_data = np.concatenate((activity_data, stats.mode(activity[i : i + window_size])[0]), axis = 0)
            heart_data = np.concatenate((heart_data, stats.mode(heart_rate[i:i + window_size])[0]), axis = 0)
            data = np.concatenate((data, temp_data.reshape(1,temp_data.shape[0] * temp_data.shape[1])), axis = 0)
            
        
        del temp_data
        
        
    del dataset

    data = np.concatenate((activity_data, heart_data, data), axis = 1)
    del activity_data
    
    return data



#TODO
def load_set(window_size, overlay):
    
    #loading the data one subject at a time:
    
    #subjects (9)
    for i in range(1,10):
         
        print('Subject ' + str(i))

        #load data
        fname = 'subject10' + str(i)
        raw_data = pd.read_csv('PAMAP2/PAMAP2_Dataset/Protocol/' + fname + '.dat', sep=' ', header=None)
        
        #sliding window over it
        raw_data = sliding_window(raw_data.values.astype(float), window_size, overlay)
    
    
        #append labels
        raw_data = np.insert(raw_data, 1, 1, axis = 1)
        len_raw = raw_data.shape[0]
        raw_data = np.concatenate((np.repeat([[i]], len_raw, axis=0), raw_data), axis = 1)
        
        
        #save to pickle TODO
        pickle.dump(raw_data, open('PAMAP2/Subject' + str(i) + '_preprocessed.txt' ,'wb'), pickle.HIGHEST_PROTOCOL)
        
        print(raw_data.shape)
        print('-------------------------------------------------------------------')
        del raw_data
                
    return 1


def merge_subjects(window_size):
    
    #make column names
    names = [
        'timestamp_',
        
        'HAND_temp_', 'HAND_acc16_x_', 'HAND_acc16_y_', 'HAND_acc16_z_', 'HAND_acc6_x_', 'HAND_acc6_y_', 'HAND_acc6_z_', 'HAND_gyrox_', 'HAND_gyroy_', 'HAND_gyroz_', 'HAND_magx_', 'HAND_magy_', 'HAND_magz_', 'HAND_orientx_', 'HAND_orienty_', 'HAND_orientz_', 'HAND_orientw_',
        
        
                'CHEST_temp_', 'CHEST_acc16_x_', 'CHEST_acc16_y_', 'CHEST_acc16_z_', 'CHEST_acc6_x_', 'CHEST_acc6_y_', 'CHEST_acc6_z_', 'CHEST_gyrox_', 'CHEST_gyroy_', 'CHEST_gyroz_', 'CHEST_magx_', 'CHEST_magy_', 'CHEST_magz_', 'CHEST_orientx_', 'CHEST_orienty_', 'CHEST_orientz_', 'CHEST_orientw_',
        
        
                'ANKLE_temp_', 'ANKLE_acc16_x_', 'ANKLE_acc16_y_', 'ANKLE_acc16_z_', 'ANKLE_acc6_x_', 'ANKLE_acc6_y_', 'ANKLE_acc6_z_', 'ANKLE_gyrox_', 'ANKLE_gyroy_', 'ANKLE_gyroz_', 'ANKLE_magx_', 'ANKLE_magy_', 'ANKLE_magz_', 'ANKLE_orientx_', 'ANKLE_orienty_', 'ANKLE_orientz_', 'ANKLE_orientw_'
    ]

    
    raw = [cols + str(i) for i in range(1, window_size + 1) for cols in names]
    columns = ['Activity', 'Trial', 'Heart_rate']
    columns.extend(raw)
    
    #go through all subjects and merge them (9)
    for i in range(1,10):
        
        print('Subject ' + str(i))
        print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        
        if i == 1:
            data = pickle.load(open('PAMAP2/Subject' + str(i) + '_preprocessed.txt' ,'rb'))
        else:
            data = np.concatenate((data, pickle.load(open('PAMAP2/Subject' + str(i) + '_preprocessed.txt' ,'rb'))), axis = 0)
    
    
    print(len(columns))
    print(data.shape)
    
    #make dataframe
    data = pd.DataFrame(data[:,1:], index = data[:,0], columns = columns)
    data.index.name = 'Subject'
    
    #delete rows with missings
    data.replace(['na','nan','NaN', 'NaT','inf','-inf','nan'], np.nan, inplace = True)
    data = data.dropna()
    
    print(data.shape)
    
    #save data
    pickle.dump(data, open('PAMAP2/full_preprocessed.txt' ,'wb'), pickle.HIGHEST_PROTOCOL)
    
    del data
    del columns
    
    return 1



#OK 
def preprocess(window_size, overlay):
    
    if os.path.exists('PAMAP2'):
        print("Started preprocessing")
        load_set(window_size, overlay)
        merge_subjects(window_size)
        return 1
        
    else:
        print("The specified dataset is not available/doesnt exsist")
        