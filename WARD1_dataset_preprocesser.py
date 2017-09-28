import os
from scipy import io
import numpy as np
import pandas as pd
import pickle

#WARD1

def sliding_window(dataset, window_size, overlay):
    
    #number of sliding windows we will get
    num_windows = int( (dataset[0,0].shape[0] - window_size) / (window_size - overlay) ) + 1

    raw_data = np.array([]).reshape(num_windows,0)
    #print('Num of measurements: ' + str(dataset[0,0].shape[0]))
    
    #Sliding window for each sensor
    for i in range(0,dataset.shape[1]):
        raw_sensor = X = np.empty(shape=[0, dataset[0,i].shape[1] * window_size])
        
        #sliding the window
        for j in range(0, dataset[0,i].shape[0] - window_size +1, window_size - overlay):
            raw_window = np.array(dataset[0,i][j : j + window_size]).reshape(1, dataset[0,i].shape[1] * window_size)
            raw_sensor = np.concatenate( (raw_sensor, raw_window), axis=0 )
            
            del raw_window
            
        #join the arrays/matrices
        raw_data = np.concatenate((raw_data, np.array(raw_sensor)), axis=1)
        
        del raw_sensor
        
        
    return raw_data




def load_set(window_size, overlay):
    
    #activity array
    #what it should be -> now only integers
    #activities = ["Rest at Standing",
    #            "Rest at Sitting",
    #            "Rest at Lying",
    #            "Walk forward",
    #            "Walk forward left-circle",
    #            "Walk forward right-circle",
    #            "Turn left",
    #            "Turn right",
    #            "Go upstairs",
    #            "Go downstairs",
    #            "Jog",
    #            "Jump",
    #            "Push"]
    
    raw_data = []
    labels = []
    
    #load all subjects TODO (20)
    for i in range(1,21):
        #all activities for a subject TODO (13)
        for j in range(1,14):
            #all trials for an activity TODO (5)
            for k in range(1,6):
                
                #print('--------------------------------------------------------')
                #print(str(i)+' '+str(j)+' '+str(k))
                
                #load data
                try:
                    sensors = io.loadmat('WARD1/WARD1.0/Subject'+str(i)+'/a'+str(j)+'t'+str(k)+'.mat')['WearableData'][0,0][5]
                    # [subject, activity, trial]
                    temp_labels = np.array([[i, j, k]])
                
                    #concat matrices of processed raw data
                    if i == 1 and j == 1 and k == 1:
                        raw_data = sliding_window(sensors, window_size, overlay)
                        labels = np.repeat(temp_labels, raw_data.shape[0] , axis=0)
                    else:
                        raw_data = np.concatenate( (raw_data, sliding_window(sensors, window_size, overlay)), axis = 0)
                        labels = np.concatenate( (labels, np.repeat(temp_labels, raw_data.shape[0] - labels.shape[0], axis = 0)), axis = 0)
                        
                    del temp_labels
                #skip missing files
                except OSError as e:
                    continue
    
    # Generate Attribute Names
    header = np.array([["Subject", "Activity", "Trial"]])
    # 5 sensors
    for i in range(1,6):
        #5 measures
        for j in range(0, int(raw_data.shape[1] / (5*5))):
            # 5 measures -> triaxial accelometer (x,y,z) + biaxial gyroscope (x,y)
            measures = [["s"+str(i)+"_acc_x"+str(j),
                         "s"+str(i)+"_acc_y"+str(j),
                         "s"+str(i)+"_acc_z"+str(j),
                         "s"+str(i)+"_gyro_x"+str(j),
                         "s"+str(i)+"_gyro_y"+str(j)]]
            header = np.concatenate( (header, np.array(measures)), axis = 1)
    
    
    # add labels and attribute names to the raw data
    data = np.concatenate( (labels, raw_data), axis = 1)
    
    
    del labels
    del raw_data
    
    #print("Data: " + str(data.shape))
    
    data = pd.DataFrame(data[:,1:], index=data[:,0], columns=header[0,1:])
    data.index.name = header[0,0]
    
    del header
    
    
    #delete rows with missings
    data.replace(['na','nan','NaN', 'NaT','inf','-inf','nan', np.inf, -np.inf], np.nan, inplace = True)
    data = data.dropna()
    #just to be sure transform everything to float
    data = data.astype(float)
    
    
    
    pickle.dump(data, open('WARD1/processed_data.txt','wb'), pickle.HIGHEST_PROTOCOL)
    
    return 1
    
    
def preprocess(window_size, overlay):
    
    if window_size <= overlay:
        print("Error: Window size and/or overlay")
        exit()
    
    if os.path.exists('WARD1/WARD1.0'):
        return load_set(window_size, overlay)
        
    else:
        print("The specified dataset is not available/doesnt exsist")
    
    
    