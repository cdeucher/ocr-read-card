##https://www.devmedia.com.br/tkinter-interfaces-graficas-em-python/33956

from tkinter import *
from point import read

class Application:
    def __init__(self, master=None):
        self.fontePadrao = ("Arial", "10")
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

   
        self.quartoContainer = Frame(master)
        self.quartoContainer["pady"] = 20
        self.quartoContainer.pack()
  
        self.titulo = Label(self.primeiroContainer, text="Leitor de Gabarito")
        self.titulo["font"] = ("Arial", "10", "bold")
        self.titulo.pack()
   

        self.autenticar = Button(self.quartoContainer)
        self.autenticar["text"] = "Processar"
        self.autenticar["font"] = ("Calibri", "8")
        self.autenticar["width"] = 12
        self.autenticar["command"] = self.Processar
        self.autenticar.pack()
  
        self.mensagem = Label(self.quartoContainer, text="", font=self.fontePadrao)
        self.mensagem.pack()
  
    #Método verificar senha
    def Processar(self):
        read({'img': None})
          
  
  
root = Tk()
Application(root)
root.mainloop()