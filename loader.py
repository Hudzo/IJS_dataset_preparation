import os
from subprocess import call
import WARD1_dataset_preprocesser as ward
import opportunity_dataset_preprocessor as opportunity
import daily_sports_preprocessor as daily_sports
import PAMAP2_preprocessor as pamap2
import skoda_preprocessor as skoda
import hci_preprocessor as hci
import chiron_first_preprocessor as chiron_first

class Loader:
    
    dataset_name = ""
    dataset_zip = ""
    dataset_url = ""
    dataset_unzip = ""

    def load_unzip(self):

        print("")

        #Load
        print("Downloading...")
        if not os.path.exists(self.dataset_zip):
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
        self.dataset_zip = "WARD1/WARD1.zip"
        
        self.load_unzip()
        
        
    def ward1_preprocess(self, window_size, overlay):
        return ward.preprocess(window_size, overlay)
      
        
 #OPPORTUNITY dataset

    def opportunity_load(self):
        
        self.dataset_name = "OpportunityUCIDataset"
        self.dataset_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00226/OpportunityUCIDataset.zip"
        self.dataset_unzip = "OpportunityUCIDataset/OpportunityUCIDataset"
        self.dataset_zip = "OpportunityUCIDataset/OpportunityUCIDataset.zip"
        
        self.load_unzip()
        
    
    def opportunity_preprocess(self, window_size, overlay):
        
        #produces a pickled file for every trial due to some RAM problems
        
        return opportunity.preprocess(window_size, overlay)
        
 
 #Daily and sports activities data set

    def daily_sports_load(self):
        
        self.dataset_name = "Daily and sports activities"
        self.dataset_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00256/data.zip"
        self.dataset_unzip = "Daily and sports activities/data"
        self.dataset_zip = "Daily and sports activities/data.zip"

        self.load_unzip()
        
        
    def daily_sports_preprocess(self, window_size, overlay):
        
        #makes 2 pickled files for two different approaches to measurement (traditional and oscillation)
        
        return daily_sports.preprocess(window_size, overlay)

    
# PAMAP2

    def pamap2_load(self):
        
        self.dataset_name = "PAMAP2"
        self.dataset_url = "http://archive.ics.uci.edu/ml/machine-learning-databases/00231/PAMAP2_Dataset.zip"
        self.dataset_unzip = "PAMAP2/PAMAP2_Dataset"
        self.dataset_zip = "PAMAP2/PAMAP2_Dataset.zip"

        self.load_unzip()
        
        
    def pamap2_preprocess(self, window_size, overlay):
        
        #makes 2 pickled files for two different approaches to measurement (traditional and oscillation)
        
        return pamap2.preprocess(window_size, overlay)
    
    
# Skoda mini Checkpoint

    def skoda_preprocess(self, window_size, overlay):
        
        #makes 2 pickled files for two different sensor locations (left and right)
        
        return skoda.preprocess(window_size, overlay)

    
# HCI data set

    def hci_preprocess(self, window_size, overlay):
        
        #makes 2 pickled files for two different sensor locations (left and right)
        
        return hci.preprocess(window_size, overlay)


# Chiron_first data set

    def chiron_first_load(self):
        
        self.dataset_name = "Chiron first"
        self.dataset_url = "https://dis.ijs.si/ami-repository/download.php?id=11"
        self.dataset_unzip = "Chiron first/Smart-first_phase.csv"
        self.dataset_zip = "Chiron first/Smart-first_phase.csv"

        self.load_unzip()
        
        
    def chiron_first_preprocess(self, window_size, overlay):
        
        #makes 2 pickled files for two different approaches to measurement (traditional and oscillation)
        
        return chiron_first.preprocess(window_size, overlay)

    
    
    
