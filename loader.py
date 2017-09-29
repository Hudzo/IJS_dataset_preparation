import os
from subprocess import call
import WARD1_dataset_preprocesser as ward
import opportunity_dataset_preprocessor as opportunity
import daily_sports_preprocessor as daily_sports


class Loader:
    
    dataset_name = ""
    dataset_zip = ""
    dataset_url = ""
    dataset_unzip = ""
    dataset_unzipAdd = "Imagine"

    def load_unzip(self):

        print("")

        #Load
        print("Downloading...")
        if not os.path.exists(self.dataset_zip + '.zip'):
            call(
                'wget "'+ self.dataset_url + '" -P "' + self.dataset_name + '/"',
                shell=True
            )
            print("Downloading done.\n")
        else:
            print("Dataset already downloaded. Did not download twice.\n")


        #Unzip
        print("Extracting...")
        extract_directory = os.path.abspath(self.dataset_unzip)
        if not os.path.exists(extract_directory):
            call(
                'unzip -nq "' + self.dataset_unzip + '.zip"',
                shell=True
            )
            print("Extracting successfully done to {}.".format(extract_directory))
        else:
            print("Dataset already extracted. Did not extract twice.\n")

            
            
 #Loads and preprocessing calls:


 # WARD1 dataset
    
    def ward1_load(self):
        
        self.dataset_name = "WARD1"
        self.dataset_url = "https://people.eecs.berkeley.edu/~yang/software/WAR/WARD1.zip"
        self.dataset_unzip = "WARD1/WARD1.0"
        self.dataset_zip = "WARD1/WARD1"
        
        self.load_unzip()
        
        
    def ward1_preprocess(self, window_size, overlay):
        return ward.preprocess(window_size, overlay)
      
        
 #OPPORTUNITY dataset

    def opportunity_load(self):
        
        self.dataset_name = "OpportunityUCIDataset"
        self.dataset_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00226/OpportunityUCIDataset.zip"
        self.dataset_unzip = "OpportunityUCIDataset/OpportunityUCIDataset"
        self.dataset_zip = "OpportunityUCIDataset/OpportunityUCIDataset"
        
        self.load_unzip()
        
    
    def opportunity_preprocess(self, window_size, overlay):
        
        #produces a pickled file for every trial due to some RAM problems
        
        return opportunity.preprocess(window_size, overlay)
        
 
 #Daily and sports activities data set

    def daily_sports_load(self):
        
        self.dataset_name = "Daily and sports activities"
        self.dataset_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00256/data.zip"
        self.dataset_unzip = "Daily and sports activities/data"
        self.dataset_zip = "Daily and sports activities/data"

        self.load_unzip()
        
        
    def daily_sports_preprocess(self, window_size, overlay):
        
        #makes 2 pickled files for two different approaches to measurement (traditional and oscillation)
        
        return daily_sports.preprocess(window_size, overlay)

    
    
    
    
