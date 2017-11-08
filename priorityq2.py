'''This is an implementation of a priority queue that supports
the remove operation as well as insert and deletemin.
It is based on the heapdict implementation at 
https://github.com/DanielStutzbach/heapdict
 S. Tanimoto, Oct. 20, 2017.

This data structure is provided to support implementations
of A* in Python.

'''
from heapdict import heapdict

class PriorityQ:
  def __init__(self):
    self.h = heapdict()

  def insert(self, elt, priority):
    if elt in self.h:
      raise Exception("Key is already in the priority queue: "+str(elt))
    self.h[elt] = priority

  def deletemin(self):
    # Returns the element having smallest priority value.
    return self.h.popitem()

  def remove(self, elt):
    # Removes an arbitrary element from the priority queue.
    # This allows updating a priority value for a key by
    # first removing it and then inserting it again with its
    # new priority value.
    del self.h[elt]  # invokes the __delitem__ method of heapdict.

  def __len__(self):
    return len(self.h)

  def __contains__(self, elt):
    return elt in self.h

  def __str__(self):
    return 'PriorityQ'+str(self.h.d)

  
