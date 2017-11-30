## IJS dataset preparation and neural networks <br />

Loader.py as the name says loads and unzips the data set to the working directory using the code from loader.py

Preprocessing of various datasets is done by their respective DATASET_preprocessor.py files

To run the whole program open the standardized classifier and uncomment the two lines of code that load the desired data set.

To test the loader/pre-processor run the tester program and uncomment the lines of code reffering to the data set you want to test.


Currently the standardized shape of the output data set produced by the preprocessor code is the following:


#### Index: Subject number      |  Activity number   |  Trial number  |    X    |   Sliding window of raw data   | <br />

X ...... possible additional singular attributes (heart rate / scenario number ...) <br />


Note: <br />
-Skoda mini Checkopint and HCI datasets need to be downlaoded manually <br />

#### Instructions: <br />

1) Run the stadardized classifier in jupyter notebook
2) In the second wrapper uncomment the dataset you want to use <br />
  2.1) Uncomment _load() and _preprocess for preprocessing the dataset (can be done once and left commented after that) <br />
  2.2) Uncomment Path="name of dataset" and df = pickle.load(dataset) <br />
  2.3) Set sliding window and overlay (use the comments on the right of the _preprocess() as a guide) <br />
  2.4) Comment all of the other lines that you will not be using <br />
3) Run all the wrappers untill the title Basic Regression
4) Run the Neural nets you want
5) After a neural net finishes running the results are located in "dataset_name"/Results/"neural_net_you_just_ran"
