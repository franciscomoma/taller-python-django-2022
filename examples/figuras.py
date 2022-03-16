
class Figura:
    color=""
    
    def __init__(self, color):
        self.color = color
    
    def pintar(self, color):
        self.color = color

class Piramide(Figura):
    caras=4
    
    def __init__(self, color, caras):
        super().__init__(color)
        self.caras = caras
        
class Cubo(Figura):
    caras=6
