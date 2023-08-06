import pickle

def osave(path: str,obj: object):
    file = open(path, 'ab')
    pickle.dump(obj, file)
    file.close()
    
def oopen(path: str):
    file = open(path, 'rb')
    obj = pickle.load(file)
    file.close()
    return obj