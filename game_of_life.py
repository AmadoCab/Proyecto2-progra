import numpy as np

class Grid:
    # Properties
    def __init__(self,size):
        self.size = size
        if type(size) == type(6):

            self.grid = np.zeros((size,size))
        else:
            raise Exception('Only square boards available')
    iterations = 0
    live_cells = 0

    # Methods
    def randgen(self, cant):
        """Random generation of live cells"""
        puntos = set()
        if cant > self.size**2:
            cant = self.size**2
        else:
            pass
        while len(puntos) < cant:
            x, y = np.random.randint(self.size, size=2)
            puntos.add((x,y))
        for coordenada in puntos:
            self.grid[coordenada[1],coordenada[0]] = 1
        self.live_cells = contador(self.grid)

    def manualgen(self,coordinates):
        """Manual generation of live cells"""
        for coordenada in coordinates:
            self.grid[coordenada[1],coordenada[0]] = 1
        self.live_cells = contador(self.grid)
    
    def matrixgen(self, matrix):
        """Generation with live cells"""
        if len(matrix) != self.size:
            raise Exception('Length error')
        else:
            for row in matrix:
                if len(row) != self.size:
                    raise Exception('Length error')
            self.grid = np.array(matrix)

    def visualize(self):
        """Printable version of the game state"""
        length = '-'*self.size*2
        string_to_print = f'Generación:{self.iterations}'
        string_to_print += f'\nPoblación:{self.live_cells}'
        string_to_print += f'\n┌{length}┐\n'
        for i in self.grid:
            string_to_print += '|'
            for j in i:
                if j == 0:
                    string_to_print += '[]'
                elif j == 1:
                    string_to_print += '██'
            string_to_print += '|\n'
        string_to_print += f'└{length}┘\n'
        print(string_to_print)

    def step(self):
        """Generates the next game state with normal borders"""
        next_grid = self.grid.copy()
        for y in range(self.size):
            for x in range(self.size):
                if (y-1<0 and x-1<0):
                    miniarreglo = self.grid[y:y+2,x:x+2]
                elif (y+2>self.size and x+2>self.size):
                    miniarreglo = self.grid[y-1:y+1,x-1:x+1]
                elif (y-1<0 and x+2>self.size):
                    miniarreglo = self.grid[y:y+2,x-1:x+1]
                elif (x-1<0 and y+2>self.size):
                    miniarreglo = self.grid[y-1:y+1,x:x+2]
                elif y-1<0:
                    miniarreglo = self.grid[y:y+2,x-1:x+2]
                elif x-1<0:
                    miniarreglo = self.grid[y-1:y+2,x:x+2]
                elif y+2>self.size:
                    miniarreglo = self.grid[y-1:y+1,x-1:x+2]
                elif x+2>self.size:
                    miniarreglo = self.grid[y-1:y+2,x-1:x+1]
                else:
                    miniarreglo = self.grid[y-1:y+2,x-1:x+2]
                celulas_vivas = contador(miniarreglo)
                if self.grid[y, x] == 1:
                    celulas_vivas += -1
                    if (celulas_vivas==2 or celulas_vivas==3):
                        pass
                    else:
                        next_grid[y, x] = 0
                elif self.grid[y, x] == 0:
                    if celulas_vivas==3:
                        next_grid[y, x] = 1
                    else:
                        pass
                # print(f'({y},{x}): {celulas_vivas}')
                # print(miniarreglo,end='\n\n')
        self.grid = next_grid.copy()
        self.iterations += 1
        self.live_cells = contador(self.grid)

    def toroidal_step(self):
        """Generates the next game state with toroidal borders"""
        next_grid = self.grid.copy()
        for y in range(self.size):
            for x in range(self.size):
                if (y-1<0 and x-1<0):
                    miniarreglo = np.vstack([
                        np.hstack([self.grid[self.size-1:self.size+1,self.size-1:self.size+1],self.grid[self.size-1:self.size+1,x:x+2]]),
                        np.hstack([self.grid[y:y+2,self.size-1:self.size+1],self.grid[y:y+2,x:x+2]])
                        ])
                elif (y+2>self.size and x+2>self.size):
                    miniarreglo = np.vstack([
                        np.hstack([self.grid[y-1:y+1,x-1:x+1],self.grid[y-1:y+1,0:1]]),
                        np.hstack([self.grid[0:1,x-1:x+1],self.grid[0:1,0:1]])
                        ])
                elif (y-1<0 and x+2>self.size):
                    miniarreglo = np.vstack([
                    np.hstack([self.grid[self.size-1:self.size+1,x-1:x+1],self.grid[self.size-1:self.size+1,0:1]]),
                    np.hstack([self.grid[y:y+2,x-1:x+1],self.grid[y:y+2,0:1]])
                    ])
                elif (x-1<0 and y+2>self.size):
                    miniarreglo = np.vstack([
                    np.hstack([self.grid[y-1:y+1,self.size-1:self.size+1],self.grid[y-1:y+1,x:x+2]]),
                    np.hstack([self.grid[0:1,self.size-1:self.size+1],self.grid[0:1,x:x+2]])
                    ])
                elif y-1<0:
                    miniarreglo = np.vstack([
                    self.grid[self.size-1:self.size+1,x-1:x+2],
                    self.grid[y:y+2,x-1:x+2]
                    ])
                elif x-1<0:
                    miniarreglo = np.hstack([
                    self.grid[y-1:y+2,self.size-1:self.size+1],
                    self.grid[y-1:y+2,x:x+2]
                    ])
                elif y+2>self.size:
                    miniarreglo = np.vstack([
                    self.grid[y-1:y+1,x-1:x+2],
                    self.grid[0:1,x-1:x+2]
                    ])
                elif x+2>self.size:
                    miniarreglo = np.hstack([
                    self.grid[y-1:y+2,x-1:x+1],
                    self.grid[y-1:y+2,0:1]
                    ])
                else:
                    miniarreglo = self.grid[y-1:y+2,x-1:x+2]
                celulas_vivas = contador(miniarreglo)
                if self.grid[y, x] == 1:
                    celulas_vivas += -1
                    if (celulas_vivas==2 or celulas_vivas==3):
                        pass
                    else:
                        next_grid[y, x] = 0
                elif self.grid[y, x] == 0:
                    if celulas_vivas==3:
                        next_grid[y, x] = 1
                    else:
                        pass
                # print(f'({y},{x}): {celulas_vivas}')
                # print(miniarreglo,end='\n\n')
        self.grid = next_grid.copy()
        self.iterations += 1
        self.live_cells = contador(self.grid)

def docgen(route):
    """Creates an instance of the class «Grid» and the game state from a 
    document"""
    matrix = []
    with open(route, 'r') as document:
        n = document.readline().strip()
        n = int(n)
        cuadricula = Grid(n)
        for _ in range(n):
            linea = [float(i) for i in document.readline().strip().split(' ')]
            matrix.append(linea)
        cuadricula.matrixgen(matrix)
        return cuadricula

def contador(arreglo, target=1):
    """Counts the amount of elements contained in an array that are equal to 
    the target"""
    contador = 0
    for i in arreglo:
        for j in i:
            if j == target:
                contador += 1
            else:
                pass
    return contador

# Some interesting patterns to play
patterns = {
    'giros' : [(2,2),(2,3),(2,1)],
    'banano': [
        (5,5),(4,4),(4,5),(5,6),(5,4),(4,6),(6,4),(6,5),(6,6),(5,3),
        (5,7),(7,5),(3,5)],
    'GGG':[
        (0,5), (0,6), (1,5), (1,6), (10,5), (10,6), (10,7), (11,8), (12,9), 
        (13,9), (11,4), (12,3), (13,3), (14,6), (16,6), (17,6), (16,5), (16,7), 
        (15,4), (15,8), (20,5), (20,4), (20,3), (21,5), (21,4), (21,3), (22,2), 
        (22,6), (24,2), (24,1), (24,6), (24,7), (34,3), (35,3), (34,4), (35,4)],
    'ship':[(0,2),(1,2),(2,2),(2,1),(1,0)]
}

if __name__ == "__main__":
    # cuadricula = Grid(4)
    # cuadricula.randgen(6)
    # cuadricula.manualgen(patterns.get('GGG'))
    # cuadricula.visualize()
    # for i in range(500):
    #     cuadricula.toroidal_step()
    #     cuadricula.visualize()
    
    cuadricula = docgen('/Users/Macbook/Desktop/Python/PrograM/Proyecto 2/carga.pm2')
    cuadricula.visualize()

#