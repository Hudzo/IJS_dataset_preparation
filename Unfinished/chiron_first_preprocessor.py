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
    activity = dataset[:,41].reshape(dataset.shape[0],1)
    subject = [dataset[0,1]]
    labels = [dataset[0,2], dataset[0,0]]
    
    #delete frame + timestamp -> shouldnt be important for classification
    #only raw data remains
    dataset = np.delete(dataset,[0,1,2,3,4,41], 1)
    
    
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
    
    subject = np.repeat([subject],data.shape[0],0)
    labels = np.repeat([labels],data.shape[0],0)
    #print("Subjects: " + str(subject.shape))
    #print("labels: " + str(labels.shape))
    #print("Data: " + str(data.shape))
    #print("Act: " + str(activity_data.shape))
    
    data = np.concatenate((subject, activity_data, labels, data), axis = 1)
    
    del subject
    del labels
    del activity_data
    
    return data



#TODO
def load_set(window_size, overlay):
    
        
    print('Processing Data')

    raw_data = pd.read_csv('Chiron first/Smart-first_phase.csv', sep=',')
    
    
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
    #subject (3)
    num = 1
    for person in raw_data['Person'].unique():
        
        #scenario (max 8)
        for scene in raw_data.loc[(raw_data['Person'] == person), 'Scenario'].unique():
            
            #iteration (max 10)
            index = 0
            for it in raw_data.loc[(raw_data['Person'] == person) & (raw_data['Scenario'] == scene), 'Iteration'].unique():
                
                temp = raw_data.loc[(raw_data['Person'] == person) & (raw_data['Scenario'] == scene) & (raw_data['Iteration'] == it)]
                
                if index == 0:
                    data = sliding_window(temp.astype(float).values, window_size, overlay)
                else:
                    data = np.concatenate((data, sliding_window(temp.astype(float).values, window_size, overlay)), axis = 0 )
                
                index += 1
                del temp
                
        columns = np.concatenate(([raw_data.columns.values[1]],[raw_data.columns.values[41]],[raw_data.columns.values[2]],[raw_data.columns.values[0]]))
        names = raw_data.columns.values[5:41]
        names = [str(i) + '_' + name for i in range(1, window_size + 1) for name in names]
        
        ###################################  TODO ######################################
        ############### dej te dva arraya skupi da maš pol imena za columns !!!!!!!!!!!
        
        data = pd.DataFrame(data, columns = columns)
        
        #pickle the results for each individual
        pickle.dump(data, open('Chiron first/Subject_' + str(num) + '_preprocessed.txt' ,'wb'), pickle.HIGHEST_PROTOCOL)
        
        num += 1
        print(data)
        del data
        return 1
    
    del raw_data
    return len(subjects)






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
def merge_hands(window_size, num_subjects):
    
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
    
    if os.path.exists('Chiron first/Smart-first_phase.csv'): 
        num = load_set(window_size, overlay)
        #merge_hands(window_size, num)
        return 1
        
    else:
        print("The specified dataset is not available/doesnt exsist")
    
    
    