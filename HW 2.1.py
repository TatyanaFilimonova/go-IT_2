from abc import ABC, abstractmethod
import ast
import json
import pickle


class SerializationInterface(ABC):

    @abstractmethod
    def serialize(self, data, file):
        pass

    @abstractmethod
    def deserialize(self, data, file):
        pass


class Serialization_json(SerializationInterface):
    
    def serialize(self, data, file):
        with open(file, 'w+') as write_file:
            json.dump(str(data), write_file)
                    

    def deserialize(self, file):
        with open(file, 'r') as read_file:
            data = json.load(read_file)
            res = ast.literal_eval(data)
            return res 
            

class Serialization_bin(SerializationInterface):
    
    def serialize(self, data, file):
        with open(file, 'wb') as write_file:
            pickle.dump(data, write_file)

    def deserialize(self, file):
        with open(file, 'rb') as read_file:
            return pickle.load(read_file)



test_list = [["list", 1, 2, 3],
             {"dictionary":1, 2:"1"},
             ("tuple",1,2),
             set(["set", 1, 2])
            ]

for data in test_list:
    sj = Serialization_json()
    sj.serialize(data, 'test.json')
    print("serialize data:    ",data)    
    print("deserialize  json: ", sj.deserialize('test.json'))
    assert (sj.deserialize('test.json') == data)
    sj1 = Serialization_bin()
    sj1.serialize(data, 'test.bin')
    print("deserialize  bin:  ", sj1.deserialize('test.bin'))
    print("Is deserialized data equal to source? ", sj.deserialize('test.json')==data)
    assert(sj1.deserialize('test.bin') == data)
    print("************************************************")

class Meta(type):
    children_number = 0

    def __init__(cls, *args):
       cls.class_number = Meta.children_number
       Meta.children_number+=1
        
Meta.children_number = 0

class Cls1(metaclass=Meta):
    def __init__(self, data):
        self.data = data
        

class Cls2(metaclass=Meta):
    def __init__(self, data):
        self.data = data

assert (Cls1.class_number, Cls2.class_number) == (0, 1)
a, b = Cls1(''), Cls2('')
assert (a.class_number, b.class_number) == (0, 1)

