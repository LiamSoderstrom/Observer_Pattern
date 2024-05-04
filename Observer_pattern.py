"""
Created on Tue Mar 12 16:02:47 2024

@author: Liam Söderström
"""
# Tests the application of an observer pattern for cross attribute interaction in a compositioned class functionally and object orientated.

from dataclasses import dataclass
from collections import defaultdict


global_observer = defaultdict(list)

# Note the func in parameter only takes callables.
def global_subscribe(event: str, func: callable):
    global_observer[event].append(func)
    
def global_post(event: str, in_data):
    
    # Ignores subscriberless events
    if not event in global_observer:
        return f"{event} not in global subscriptions"
    
    for func in global_observer[event]:
        func(in_data)
        
#Test class to be used with global observer.
@dataclass
class Attribute_1():
    val_1 : int 
    
    def ch_val(self, val : int) -> None:
        self.val_1 = val
    
    def __setattr__(self, name, value):
        if name == "val_1":
            super().__setattr__(name, value)
            global_post("ch_val", value)

#Test class to be used with global observer.            
@dataclass
class Attribute_2():
    val_1 : int 
    
    def ch_val(self, val : int) -> None:
        self.val_1 = val

#Test class to be used with a composition class observer.        
@dataclass
class Strength():
    natval : float
    curval : float

    def ch_natstr_sub(self, num : float) -> None:
        if num <= 1 and num > 0:
            self.natval = num
        else:
            raise ValueError("Strength float is out of range 0 - 1")

#Test class to be used with a composition class observer.           
@dataclass
class Inventory():
    invsize : float

    def ch_natstr_sub(self, num : float) -> None:
        if num <= 1 and num > 0:
            self.natval = num
        else:
            raise ValueError("Strength float is out of range 0 - 1")



#Test compositioned class where attributes are checked for functions to be appended to the observer.   
class Compositioned_cls():
    
    def __init__(self, id : int = 42, first : object = Strength(natval = 0.2, curval = 0.1), second : object = Inventory(invsize = 0.1)):
        self._id = id
        self._observer = defaultdict(list)
        self.first = first
        self.second = second
        self._compile_subscribers()
        
    def _compile_subscribers(self, func: callable = None):

        if func == None:    
            for attribute in [attr for attr in self.__dict__ if not attr.startswith("_") and not callable(attr)]:
                for function in [func for func in dir(getattr(self, attribute)) if str(func).endswith("_sub")]:
                    self._observer[str(function[:-4])].append(function)
                
           

        


def main():
    kalle = Attribute_1(val_1=10)
    pelle = Attribute_2(val_1=20)
    global_subscribe("ch_val", pelle.ch_val)
    global_post("ch_val", 30)
    print(f"Kalle val: {kalle.val_1}\nPelle val: {pelle.val_1}")
    kalle.ch_val(10)
    print(f"Kalle val: {kalle.val_1}\nPelle val: {pelle.val_1}")
    sten = Compositioned_cls()
    print(sten._observer)

    
if __name__ == "__main__":
    main()
    


