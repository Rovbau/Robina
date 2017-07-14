import pickle

data = {'solvedPath': [[5, 0], [4, 0], [3, 0]],
         'path': [[150, 60], [170, 80], [190, 100]],
         'obstacles': [[4, 0, 3], [4, 8, 1], [4, 9, 7]]}
         
pickelPath=open( "PickleOby.p", "wb" )
pickle.dump(data, pickelPath)
pickelPath.close()
