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



#Test compositioned class where attributes functions are used through an observer.   
@dataclass
class Compositioned_cls():
    
    _observer = defaultdict(list)
    traitval = [Strength(natval = 0.2, curval = 0.1)]
    utilities = [Inventory(invsize = 0.1)]
        
    #A function which subscribes functions 
    def _compile_subscribers(self, func: callable = None):

        #Used when initializing the compositioned class
        if func == None:
            for attributes in [properties for properties in dir(self) if not properties.startswith("_") and not callable(properties)]:
                print(attributes)
                for obj in getattr(self, str(attributes)):
                    for function in [func for func in dir(obj) if func.endswith("_sub")]:
                            subscription = getattr(obj, function)
                            self._observer[str(function[:-4])].append(subscription)

    #Uses the observer to execute functions.
    def _post_event(self, func : str, *args, **kwargs):
        
        for subscribers in self._observer[str(func)]:
            for function in subscribers:
                function(*args, **kwargs)
    
    #Subscribes functions to the observer after initialisation.                
    def __post_init__(self):
        self._compile_subscribers()
    
#Tests the global and class observers.
def main():
    
    #Creates and tests the global observer 
    kalle = Attribute_1(val_1=10)
    pelle = Attribute_2(val_1=20)
    global_subscribe("ch_val", pelle.ch_val)
    
    global_post("ch_val", 30)
    print(f"Kalle val: {kalle.val_1}\nPelle val: {pelle.val_1}")
    kalle.ch_val(10)
    print(f"Kalle val: {kalle.val_1}\nPelle val: {pelle.val_1}")
    
    #Creates the compositioned class and tests
    sten = Compositioned_cls()
    global_observer["ch_natstr"].append(sten.traitval[0].ch_natstr_sub)
    print(global_observer)
    print(sten._observer)

    
    
if __name__ == "__main__":
    
    main()
    


