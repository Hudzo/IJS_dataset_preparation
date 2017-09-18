import os
from subprocess import call
import WARD1_dataset_preprocesser as ward
import opportunity_dataset_preprocessor as opportunity


class Loader:
    
    dataset_name = ""
    dataset_url = ""
    dataset_unzip = ""

    def load_unzip(self):

        print("")

        #Load
        print("Downloading...")
        if not os.path.exists(self.dataset_name + '/' + self.dataset_name + '.zip'):
            call(
                'wget "'+ self.dataset_url + '" -P "' + self.dataset_name + '/"',
                shell=True
            )
            print("Downloading done.\n")
        else:
            print("Dataset already downloaded. Did not download twice.\n")


        #Unzip
        print("Extracting...")
        extract_directory = os.path.abspath(self.dataset_unzip + '/' + self.dataset_unzip)
        if not os.path.exists(extract_directory):
            call(
                'unzip -nq "' + self.dataset_name + '/' + self.dataset_name + '.zip"',
                shell=True
            )
            print("Extracting successfully done to {}.".format(extract_directory))
        else:
            print("Dataset already extracted. Did not extract twice.\n")

#Loads and preprocessing calls:

    def ward1_load(self):
        
        self.dataset_name = "WARD1"
        self.dataset_url = "https://people.eecs.berkeley.edu/~yang/software/WAR/WARD1.zip"
        self.dataset_unzip = "WARD1.0"
        
        self.load_unzip()
        
        
    def ward1_preprocess(window_size):
        return ward.preprocess(window_size,overlay)
      
        
    def opportunity_load(self):
        
        self.dataset_name = "OpportunityUCIDataset"
        self.dataset_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00226/OpportunityUCIDataset.zip"
        self.dataset_name = "OpportunityUCIDataset"
        
        self.load_unzip()
        
    
    def opportunity_preprocess(window_size):
        return opportunity.preprocess(window_size,overlay)
    
    
    
    
    