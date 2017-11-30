import os
from scipy import io
import numpy as np
import pandas as pd
from scipy import stats
import pickle

#OPPORTUNITY


def get_attribute_names(window_size, overlay):

    # make attribute names and labels
    att_names = ['MILLISEC']
    label_names = ['Subject']
    collumn_name_file = 'OpportunityUCIDataset/OpportunityUCIDataset/dataset/column_names.txt'
    index = 1
    with open(collumn_name_file) as FileObj:
                for lines in FileObj:
                    if index > 3 and index < 246 :
                        temp = lines.strip().split(" ")
                        att_names.append(temp[3] + "_" + temp[4][0:-1])
                        del temp
                    if index == 249 :
                        label_names.append(lines.strip().split(" ")[2])
                    if index > 249:
                        label_names.append('Trial')
                        break
                    index += 1

    #duplicate attribute names
    att_names = np.array([att_names])
    att_names = np.repeat(att_names,window_size,axis=0).reshape(1,window_size * np.shape(att_names)[1])

    for i in range(0, window_size):
            for j in range(0,243):
                att_names[0, i * 243 + j] = str(i + 1) + "_" + att_names[0, i * 243 + j]


    atts = np.concatenate((np.array([label_names]), att_names), axis = 1)
    del label_names
    del att_names

    return atts


#TODO
def sliding_window(dataset, window_size, overlay):
    
    print("Start trial")
    
    #split into raw data and labels
    raw_data = dataset[:,0:243]
    labels = dataset[:,243]
    
    #build sliding windows:
    for i in range(0, dataset.shape[0] - window_size + 1, window_size - overlay):   # Major time consumer, any ideas how to overcome it?
        
        if i == 0:
            temp_data = raw_data[i:i + window_size, :]
            
            label_data = stats.mode(labels[i:i + window_size])[0]
            data = temp_data.reshape(1, temp_data.shape[0] * temp_data.shape[1])
            
            del temp_data
            
        else:
            temp_data = raw_data[i:i + window_size, :]
            
            label_data = np.concatenate((label_data, stats.mode(labels[i : i + window_size])[0]), axis = 0)
            data = np.concatenate((data, temp_data.reshape(1,temp_data.shape[0] * temp_data.shape[1])), axis = 0)
            
            del temp_data
    
    
    #concatenating the class vector with the array of raw data/sliding window results
    del raw_data
    data = np.concatenate((label_data.reshape(data.shape[0],1), data), axis = 1)
    del label_data
    
    print("Done wih the trial")
    
    return data
    

    
#TODO
def load_set(window_size, overlay):
    
    activities = []
    data = []
    
    atts = get_attribute_names(window_size, overlay) #get an array of attribute names

    
    #load all subjects TODO
    for i in range(1,5):
        
        #all daily activities / drill for a subject (5 + drill)
        for j in range(1,7):
            
                
            print('--------------------------------------------------------')
            print(str(i)+' '+str(j))
            
            fname = 'S' + str(i) + '-ADL' + str(j)
            if j==6:
                fname = 'S' + str(i) + '-Drill'
            
            #load data
            raw_data = pd.read_csv('OpportunityUCIDataset/OpportunityUCIDataset/dataset/' + fname + '.dat', sep=' ')
            del fname
            
                
            #sliding window processing (build the data array)
            data = sliding_window(np.array(raw_data), window_size, overlay)  #numpy array
            del raw_data
            
            data = np.insert(data, 1, j, axis=1)
            print("Added trial id collumn")
            
            data = np.concatenate((np.ones((data.shape[0], 1))*i, data), axis = 1)
            print("Added subject id collumn")   
              
            #MAKES THE WHOLE ARRAY TAKE 20 TIMES THE SPACE IT TOOK ONE LINE BEFORE
            #data = np.concatenate((atts, data), axis = 0)
            #print("Added collumn names")
            
            data = pd.DataFrame(data[1:,:], columns=atts[0,:]) # transform array to indexed dataFrame
            print("Transformed into a dataframe")
            
            
            pickle.dump(data, open('OpportunityUCIDataset/Subject_'+str(i)+ '-ADL' + str(j) + '_preprocessed.txt','wb'), pickle.HIGHEST_PROTOCOL)
            
            del data
        
    return 1


#concatenate the whole dataset -> might not be the optimal solution -> TODO find a better, more eficient way
def concat_frames():
    
    flag = 0
    
    #TODO -> (1,5)
    for i in range(1,5):
        for j in range(1,7):
            print(str(i) + " - " + str(j))
            temp_data = pickle.load(open('OpportunityUCIDataset/Subject_' + str(i) + '-ADL' + str(j) + '_preprocessed.txt', "rb"))
            if flag == 0:
                data = temp_data.values.astype(float)
                labels = temp_data.columns.values[1:]
                flag += 1
            else:
                data = np.concatenate((data,temp_data.values.astype(float)), axis=0)

            del temp_data
    
    print(data.shape)
    print(labels.shape)
    
    #indexed by subject, first two colums are activity label and trial number, others are data
    labels[1] = "Activity"
    data = pd.DataFrame(data[:,1:], index = data[:,0], columns = labels)
    data.index.name = 'Subject'
    
    #delete rows with missings
    data.replace(['na','nan','NaN', 'NaT','inf','-inf','nan'], np.nan, inplace = True)
    data = data.dropna()
    #just to be sure transform everything to float
    data = data.astype(float)
    
    
    # saving the file
    pickle.dump(data, open('OpportunityUCIDataset/full_preprocessed_dataset.txt','wb'), pickle.HIGHEST_PROTOCOL)
    
    return 1
    
    
    
#OK 
def preprocess(window_size, overlay):
    
    if os.path.exists('OpportunityUCIDataset/OpportunityUCIDataset/dataset'):
        load_set(window_size, overlay)
        concat_frames()
        
    else:
        print("The specified dataset is not available/doesnt exsist")
        
        