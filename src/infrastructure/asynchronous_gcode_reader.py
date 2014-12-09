import threading 

class AsynchronousGcodeReader(threading.Thread):
    def __init__(self, file, call_back, complete):
        threading.Thread.__init__(self)

    def run(self):
        pass
