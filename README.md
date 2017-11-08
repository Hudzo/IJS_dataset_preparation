## IJS dataset preparation and neural networks <br />

Loader.py as the name says loads and unzips the data set to the working directory using the code from loader.py

Preprocessing of various datasets is done by their respective DATASET_preprocessor.py files

To run the whole program open the standardized classifier and uncomment the two lines of code that load the desired data set.

To test the loader/pre-processor run the tester program and uncomment the lines of code reffering to the data set you want to test.


Currently the standardized shape of the output data set produced by the preprocessor code is the following:


#### Index: Subject number      |  Activity number   |  Trial number  |    X    |   Sliding window of raw data   | <br />

X ...... possible additional singular attributes (heart rate / scenario number ...) <br />


Note: <br />
-Skoda mini Checkopint and HCI datasets need to be downlaoded manually
