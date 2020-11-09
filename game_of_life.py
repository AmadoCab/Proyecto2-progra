import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.colors
import json
import datetime

class Grid:
    # Properties
    def __init__(self,size,start=0):
        self.size = size
        self.initial_state = start
        if type(size) == type(6):

            self.grid = np.zeros((size,size))
        else:
            raise Exception('Only square boards available')
    iterations = 0
    live_cells = 0
    color0 = 'k'
    color1 = 'w'
    gridc = 'darkgrey'
    fig, ax = plt.subplots()
    pause = False
    velocity = 20 # In milisecs

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
        self.initial_state = self.grid.copy()

    def manualgen(self,coordinates):
        """Manual generation of live cells"""
        for coordenada in coordinates:
            self.grid[coordenada[1],coordenada[0]] = 1
        self.live_cells = contador(self.grid)
        self.initial_state = self.grid.copy()
    
    def matrixgen(self, matrix):
        """Generation with live cells"""
        if len(matrix) != self.size:
            raise Exception('Length error')
        else:
            for row in matrix:
                if len(row) != self.size:
                    raise Exception('Length error')
            self.grid = np.array(matrix)
        self.live_cells = contador(self.grid)
        self.initial_state = self.grid.copy()

    def create_image(self, i):
        """Takes an screenshot of the actual game state"""
        texto = f'Generación: {self.iterations}    Celulas vivas: {self.live_cells}'
        plt.title(texto)
        cmap = matplotlib.colors.ListedColormap([self.color0,self.color1])
        self.ax.pcolor(np.flip(self.grid, 0), edgecolors=self.gridc, linewidths=1, snap=True, cmap=cmap)
        self.ax.axis('off')
        self.ax.set_aspect('equal')
        plt.tight_layout()
        plt.savefig('pic{:0>4}.png'.format(i))

    def frames(self, i):
        """Creates the frames for animation function with normal borders"""
        if self.pause:
            pass
        else:
            self.step()
        self.ax.clear()
        texto = f'Generación: {self.iterations}    Celulas vivas: {self.live_cells}'
        plt.title(texto)
        cmap = matplotlib.colors.ListedColormap([self.color0,self.color1])
        c = self.ax.pcolor(np.flip(self.grid, 0), edgecolors=self.gridc, linewidths=1, snap=True, cmap=cmap)
        self.ax.axis('off')
        self.ax.set_aspect('equal')
        plt.tight_layout()
        return c

    def toroidal_frames(self, i):
        """Creates the frames for animation function with toroidal borders"""
        if self.pause:
            pass
        else:
            self.toroidal_step()
        self.ax.clear()
        texto = f'Generación: {self.iterations}    Celulas vivas: {self.live_cells}'
        plt.title(texto)
        cmap = matplotlib.colors.ListedColormap([self.color0,self.color1])
        c = self.ax.pcolor(np.flip(self.grid, 0), edgecolors=self.gridc, linewidths=1, snap=True, cmap=cmap)
        self.ax.axis('off')
        self.ax.set_aspect('equal')
        plt.tight_layout()
        return c

    def animate(self, borders):
        """Animates the game"""
        if borders == 'normal':
            self.anim = FuncAnimation(self.fig, self.frames, frames=5, interval=self.velocity, repeat=(not self.pause))
            plt.show()
        elif borders == 'toroidal':
            self.anim = FuncAnimation(self.fig, self.toroidal_frames, frames=5, interval=self.velocity, repeat=(not self.pause))
            plt.show()
        else:
            print('todo mal')

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

    def keep(self,nombre=datetime.datetime.now()):
        """Keeps the current game state"""
        guardado = {
            'size':self.size,
            'grid':gen_positions(self.grid),
            'start state':gen_positions(self.initial_state),
            'generation':self.iterations,
            'live cells':self.live_cells,
            'deathcolor':self.color0,
            'livecolor':self.color1,
            'gridcolor':self.gridc
        }
        texto = f'{datetime.datetime.now()}\n{json.dumps(guardado)}'
        if type(nombre)==type('Marianita hermosa'):
            nombre = nombre.replace('.jvpm2','')
        with open(f'{nombre}.jvpm2', 'w') as guardar:
            guardar.write(texto)

def gen_positions(array):
    """Generates a list with the positions of live cells"""
    posiciones = []
    r, c = array.shape
    for row in range(r):
        for column in range(c):
            if array[row, column] == 1:
                posiciones.append((column, row))
            else:
                pass
    return posiciones

def dictgen(route):
    """Create an instance of 'Grid' from a document codified in JSON"""
    with open(route, 'r') as documento:
        fecha = documento.readline()
        jsonstr = documento.readline()
        estado = json.loads(jsonstr)
        cuadricula = Grid(estado.get('size'))
        cuadricula.manualgen(estado.get('grid'))
        cuadricula.initial_state = arreglar(estado.get('size') ,estado.get('start state'))
        cuadricula.iterations = estado.get('generation')
        cuadricula.live_cells = estado.get('live cells')
        cuadricula.color0 = estado.get('deathcolor')
        cuadricula.color1 = estado.get('livecolor')
        cuadricula.gridc = estado.get('gridcolor')
    return cuadricula

def docgen(route):
    """Creates an instance of the class "Grid" and the game state from a 
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

def arreglar(size, array):
    """Create a numpy array"""
    arreglo = np.zeros((size, size))
    for cor in array:
        arreglo[cor[1], cor[0]] = 1
    return arreglo

def press(array):
    """Print an array on an 'esthetic' way"""
    n, m = array.shape
    longitud = '-'*2*n
    imprimir = f'Generación:{0}\n'
    imprimir += f'Población:{contador(array)}\n'
    imprimir += f'┌{longitud}┐\n'
    for i in array:
        imprimir += '|'
        for j in i:
            if j == 1:
                imprimir += '██'
            elif j == 0:
                imprimir += '[]'
        imprimir += '|\n'
    imprimir += f'└{longitud}┘\n'
    print(imprimir)

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
    'ship':[(0,2),(1,2),(2,2),(2,1),(1,0)],
}

if __name__ == "__main__":
    """Generación normal"""
    cuadricula = Grid(40)
    # cuadricula.randgen(6)
    cuadricula.manualgen(patterns.get('GGG'))
    # cuadricula.visualize()
    # for i in range(500):
        # cuadricula.create_image(i)
    #     cuadricula.toroidal_step()
    #     cuadricula.visualize()
    # cuadricula.keep('intentando')
    
    """Generación documentos pm2"""
    # cuadricula = docgen('/Users/Macbook/Desktop/Python/PrograM/Proyecto 2/carga.pm2')
    # cuadricula.visualize()

    """Generación documentos jvpm2"""
    # cuadricula = dictgen('intentando.jvpm2')
    # press(cuadricula.initial_state)
    # cuadricula.visualize()
    cuadricula.animate('toroidal')
#
