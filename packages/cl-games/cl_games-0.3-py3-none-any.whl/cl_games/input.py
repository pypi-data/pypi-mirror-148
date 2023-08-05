from pynput import keyboard
class InputHandler(object):
    """This handles input and output"""
    keys = []
    listener = None
    onTaps = []
    def __init__(self):
        self.keys = []
        self.listener = None
        self.onTaps = []
    def startListening(self):
        self.listener = keyboard.Listener(
            on_press=self.handleDown,
            on_release=self.handleUp
        )
        self.listener.start()
    def handleDown(self, key):
        if len(str(key)) == 3 and str(key)[0] == "'":
            say = str(key)[1]
        else:
            say = str(key)
        for func in self.onTaps:
            func(say)
        if len(str(key)) == 3 and str(key)[0] == "'":
            if str(key)[1] not in self.keys: self.keys.append(str(key)[1])
        else:
            if str(key) not in self.keys: self.keys.append(str(key))
    def handleUp(self, key):
        if len(str(key)) == 3 and str(key)[0] == "'":
            if str(key)[1] in self.keys: self.keys.remove(str(key)[1])
        else:
            if str(key) in self.keys: self.keys.remove(str(key))
    def getKey(self, key):
        if key in self.keys:
            return True
        else:
            return False
    def addListener(self, func):
        self.onTaps.append(func)
