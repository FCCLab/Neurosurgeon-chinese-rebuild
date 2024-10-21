import pickle
import sklearn 

file = open("predictor\\config\\edge\\avgpool.pkl", 'rb')  # Use 'rb' for reading binary files
object_file = pickle.load(file)
file.close()  # Close the file after loading
