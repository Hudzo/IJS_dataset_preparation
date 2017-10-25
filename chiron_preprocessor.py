import os
from scipy import io
import numpy as np
import pandas as pd
from scipy import stats
import pickle

#Chiron dataset -> Activities and falls, Smart, first phase


def sliding_window(dataset, window_size, overlay):
    
    
    #extract activity id
    activity = dataset[:,41].reshape(dataset.shape[0],1)
    subject = [dataset[0,1]]
    labels = [dataset[0,2], dataset[0,0]]
    
    #delete frame + timestamp -> shouldnt be important for classification
    #only raw data remains
    dataset = np.delete(dataset,[0,1,2,3,4,41], 1)
    
    #data = np.array([[]])
    #activity_data = np.array([[]])
    
    for i in range(0, dataset.shape[0] - window_size, window_size - overlay):  
        
        #sliding window action
        temp_data = dataset[i:i + window_size, :]
        
        if i == 0: 
            activity_data = stats.mode(activity[i:i + window_size])[0]
            data = temp_data.reshape(1, temp_data.shape[0] * temp_data.shape[1])
            
        else:
            activity_data = np.concatenate((activity_data, stats.mode(activity[i : i + window_size])[0]), axis = 0)
            data = np.concatenate((data, temp_data.reshape(1,temp_data.shape[0] * temp_data.shape[1])), axis = 0)
            
        
        del temp_data
        
        
    del dataset
    
    subject = np.repeat([subject],data.shape[0],0)
    labels = np.repeat([labels],data.shape[0],0)
    
    data = np.concatenate((subject, activity_data, labels, data), axis = 1)
    
    del subject
    del labels
    del activity_data
    
    return data



#TODO
def load_set(window_size, overlay, num_set):
        
    print('Processing Data')
    
    path = ""
    
    if num_set == 1:
        raw_data = pd.read_csv('Chiron first/Smart-first_phase.csv', sep=',')
        path = "Chiron first/"
    elif num_set == 2:
        raw_data = pd.read_csv('Chiron second/Smart-second_phase.csv', sep=',')
        path = "Chiron second/"
    else:
        print('The given parameter doesnt match any datasets. Please use 1 for Smart-first_phase and 2 for Smart-second_phase')
        return 0
        
    #print(raw_data)
    #return
        
    #first of all delete the missing values:
    raw_data.replace(['na','nan','NaN', 'NaT','inf','-inf','nan','?'], np.nan, inplace = True)
    raw_data = raw_data.dropna()
    
    
    #replace strings in columns with integers
    
    #person
    subjects = raw_data['Person'].unique()
    for i in range (1, len(subjects) + 1):
        raw_data.loc[raw_data['Person'] == subjects[i - 1], 'Person'] = i
    
    #activity
    activities = raw_data['Activity'].unique()
    for i in range (1, len(activities) + 1):
        raw_data.loc[raw_data['Activity'] == activities[i - 1], 'Activity'] = i
    
    del activities
    
    #scenario
    scenarios = raw_data['Scenario'].unique()
    for i in range (1, len(scenarios) + 1):
        raw_data.loc[raw_data['Scenario'] == scenarios[i - 1], 'Scenario'] = i
    
    del scenarios
    
    
    #sliding window for each subject, each scenario and each iter:
    #subject (1: 3, 2: 5)
    num = 1
    for person in raw_data['Person'].unique():
        
        print('Subject ' + str(num))
        
        #scenario (1: max 8, 2: max 38)
        index = 0
        for scene in raw_data.loc[(raw_data['Person'] == person), 'Scenario'].unique():
            
            #iteration (1: max 10, 2: max 32)
            for it in raw_data.loc[(raw_data['Person'] == person) & (raw_data['Scenario'] == scene), 'Iteration'].unique():
                
                #read the data and create variables
                temp = raw_data.loc[(raw_data['Person'] == person) & (raw_data['Scenario'] == scene) & (raw_data['Iteration'] == it)]
                
                if index == 0:
                    data = sliding_window(temp.astype(float).values, window_size, overlay)
                    index += 1
                else:
                    new_data = sliding_window(temp.astype(float).values, window_size, overlay)
                    data = np.concatenate((data, new_data), axis = 0 )
                
                del temp
                
                
        #Making attribute names
        columns = np.concatenate(([raw_data.columns.values[1]],[raw_data.columns.values[41]],[raw_data.columns.values[2]],[raw_data.columns.values[0]]))
        names = raw_data.columns.values[5:41]
        names = [str(i) + '_' + name for i in range(1, window_size + 1) for name in names]
        
        #Attribute name concatenation and test output
        columns = np.concatenate((columns.reshape(1,4), np.array([names])), axis = 1)
        print('Columns shape: ' + str(columns.shape))
        print('Data shape:' + str(data.shape))
        
        #Make a dataframe
        data = pd.DataFrame(data[:,1:], columns = columns[0,1:], index = data[:,0])
        data.index.name = 'Subject'
        #pickle the results for each individual
        pickle.dump(data, open(path + 'Subject_' + str(num) + '_preprocessed.txt' ,'wb'), pickle.HIGHEST_PROTOCOL)
        
        #Increase the num value -> number of the next subject
        num += 1
        print(data.shape)
        del data
        
        print('-------------------------------------------------------------------')
    
    del raw_data
    return len(subjects)




#TODO
def merge_subjects(window_size, num_subjects, num_set):
    
    path = 'Chiron first/'
    if num_set == 2:
        path = 'Chiron second/'
    
    #merge all subjects
    for i in range(1, num_subjects + 1):
        if i == 1:
            data = pickle.load(open(path + 'Subject_' + str(i) + '_preprocessed.txt' ,'rb'))
        else:
            data = pd.concat([data, pickle.load(open(path + 'Subject_' + str(i) + '_preprocessed.txt' ,'rb'))])

            

    #export dataframe
    pickle.dump(data, open(path + 'Chiron_full_preprocessed.txt' ,'wb'), pickle.HIGHEST_PROTOCOL)

    print(data.shape)
    del data
    
    return 1
    

def preprocess(window_size, overlay, num_set):
    
    if window_size <= overlay:
        print("Error: Window size and/or overlay")
        exit()
    
    if (num_set == 1 and os.path.exists('Chiron first/Smart-first_phase.csv')) or (num_set == 2 and os.path.exists('Chiron second/Smart-second_phase.csv')): 
        num_subjects = load_set(window_size, overlay, num_set)
        merge_subjects(window_size, num_subjects, num_set)
        return 1
        
    else:
        print("The specified dataset is not available/doesnt exsist")
    
    
    