class Queue(object):
    def __init__(self, list=list, length=int, input=input):

        self.stream_size = len(list)
        self.i = input
        self.o = ''

        if self.stream_size < length:
            self.i = input
            list.insert(0,input)
        else:
            list.insert(0,input)
            list.pop()
            self.o = list[-1]

        self.q = list

    def __str__(self): return str(self.q)

    def output(self): return self.o
    def input(self): return self.i

    def infos(self): return f"{self.q}\nI: {self.i}\nO: {self.o if self.o!=''else 'None'}\n"
    def info(self): self.infos()

