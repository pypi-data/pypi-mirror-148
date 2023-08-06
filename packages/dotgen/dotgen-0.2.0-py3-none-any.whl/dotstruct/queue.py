class Queue: 
    def __init__(self):
        """ Lining Up for a Queue. FIFO """
        self.items = []
    
    def isEmpty(self):
        return self.items == []
    
    def enqueue(self, item):
        """ Add to the end of the queue. O(n) """
         self.items.insert(0,item)
        
    def dequeue(self):
        """ Remove from the front of the queue. O(1) """
        return self.items.pop()
    
    def size(self):
        return len(self.items)
    
if __name__ =="__main__": 
    callQueue = Queue()
    callQueue.enqueue(1)
    callQueue.enqueue(2)
    callQueue.enqueue(3)
    print(callQueue.items)
    callQueue.dequeue()
    print(callQueue.items)
  


    