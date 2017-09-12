import os
from scipy import io
import numpy as np

#WARD1

def sliding_window(dataset, window_size, overlay):
    
    #number of sliding windows we will get
    num_windows = int( (dataset[0,0].shape[0] - window_size) / (window_size - overlay) ) + 1

    raw_data = np.array([]).reshape(num_windows,0)
    #print('Num of measurements: ' + str(dataset[0,0].shape[0]))
    
    #Sliding window for each sensor
    for i in range(0,dataset.shape[1]):
        raw_sensor = X = np.empty(shape=[0, dataset[0,i].shape[1] * window_size])
        
        #sliding the window (+1 ??)
        for j in range(0, dataset[0,i].shape[0] - window_size +1, window_size - overlay):
            raw_window = np.array(dataset[0,i][j : j + window_size]).reshape(1, dataset[0,i].shape[1] * window_size)
            raw_sensor = np.concatenate( (raw_sensor, raw_window), axis=0 )
        
        #join the arrays/matrices
        raw_data = np.concatenate((raw_data, np.array(raw_sensor)), axis=1)
        
    #print(raw_data.shape)
        
        
    return raw_data




def load_set(window_size, overlay):
    
    #activity array
    activities = ["Rest at Standing",
                "Rest at Sitting",
                "Rest at Lying",
                "Walk forward",
                "Walk forward left-circle",
                "Walk forward right-circle",
                "Turn left",
                "Turn right",
                "Go upstairs",
                "Go downstairs",
                "Jog",
                "Jump",
                "Push"]
    
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
                    temp_labels = np.array([[i, activities[j-1], k]])
                
                    #concat matrices of processed raw data
                    if i == 1 and j == 1 and k == 1:
                        raw_data = sliding_window(sensors, window_size, overlay)
                        labels = np.repeat(temp_labels, raw_data.shape[0] , axis=0)
                    else:
                        raw_data = np.concatenate( (raw_data, sliding_window(sensors, window_size, overlay)), axis = 0)
                        labels = np.concatenate( (labels, np.repeat(temp_labels, raw_data.shape[0] - labels.shape[0], axis = 0)), axis = 0)
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
    
    #print("Raw_data shape: " + str(raw_data.shape))
    
    # add labels and attribute names to the raw data
    data = np.concatenate( (labels, raw_data), axis = 1)
    data = np.concatenate( (header, data), axis = 0 )
    
    #print("Data: " + str(data.shape))
    
    return data
    
    
    
    
def preprocess(window_size, overlay):
    
    
    if os.path.exists('WARD1/WARD1.0'):
        return load_set(window_size, overlay)
        
    else:
        print("The specified dataset is not available/doesnt exsist")
    
    
    