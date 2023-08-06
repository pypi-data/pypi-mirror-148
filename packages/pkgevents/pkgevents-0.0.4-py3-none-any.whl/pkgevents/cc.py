
import os
import threading
class event():
    def __init__(self):
      self.eventmanager = {}
    def subscribe(self, eventname, *functions):
      keyErro = False
      try:
        tryy = self.eventmanager[eventname]
      except:
        keyErro = True
      if keyErro:
        message = ' '.join([eventname,'Does not exist'])
        raise KeyError(message)
        
      self.eventmanager.update({eventname : list(functions)})
    def unsubscribe(self, eventname, *functions):
      output = self.eventmanager[eventname]
      
      for object in functions:
        output.remove(object)
        
      self.eventmanager.update({eventname:output})
    def blnk(self):
      pass
    def addevent(self, eventname):
      self.eventmanager.update({eventname:[(self.blnk,)]})
    def delevent(self, eventname):
      del self.eventmanager[eventname]
    def addevent_advanced(self, eventname):
      self.eventmanager.update({eventname+'_event_ARGS':None})
    
    def dispatch(self, eventname,*args):
      keyErro = False
      try:
        tryy = self.eventmanager[eventname]
      except:
        keyErro = True
      if keyErro:
        message = ' '.join([eventname,'Does not exist'])
        raise KeyError(message)
      if eventname.endswith('_event_ARGS'):
        for funct in self.eventmanager[eventname]:
          newfunc = funct[0]
          newfunc(tuple(args))
      else:
        for funct in self.eventmanager[eventname]:
        
          try:
            newfunc = funct[0]
          except:
            newfunc = funct

          newfunc()
    
      
      
class shrtEVN(event):
      def __init__(self):
        super().__init__()
        self.id = None
      def sub(self, eventname, *functions):
        super().subscribe(eventname, functions)
      def unsub(self, eventname, *functions):
        super().unsubscribe(eventname, functions)
      def addE(self, eventname):
        super().addevent(eventname)
      def delE(self, eventname):
        super().delevent(eventname)
      def __nouse__dispatcher(self, truu):
        self.id = os.getpid()
        while True:
          for obj in truu:
            global stop_threads
            stop_threads = False
            if stop_threads:
              break
            
            if truu[obj]:
            
              super().dispatch(obj)
      def pre_dispatcher(self, **truu):
        tru = truu
        threading.Thread(target=self.__nouse__dispatcher, args=(tru,),daemon=True).start()
      def event(self, func):
        super().subscribe(str(func.__name__), func)
      def cancel(self):
        os.system('kill ' + str(self.id))
        
          
        
        