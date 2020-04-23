import numpy as np
from scipy import sparse
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

class ADImethod:
    
    def __init__(self, M, maxt, D):
        self.M = M
        self.x0 = 0
        self.xf = 1
        self.y0 = 0
        self.yf = 1
        self.maxt = maxt
        self.dt = 0.01
        self.D = D
        self.h = 1/self.M
        self.r = self.D*self.dt/(2*self.h**2)
        self.generateGrid()
        self.lhsMatrixA()
        self.rhsMatrixA()

            
    def generateGrid(self):
        self.X, self.Y = np.meshgrid(np.linspace(self.x0, self.xf, self.M), np.linspace(self.y0, self.yf,self. M))
        ic01 = np.logical_and(self.X >= 1/4, self.X <= 3/4)
        ic02 = np.logical_and(self.Y >= 1/4, self.Y <= 3/4)
        ic0 = np.multiply(ic01, ic02)
        self.U = ic0*1

    
    def lhsMatrixA(self):
        maindiag = (1+2*self.r)*np.ones((1, self.M))
        offdiag = -self.r*np.ones((1, self.M-1))
        a = maindiag.shape[1]
        diagonals = [maindiag, offdiag, offdiag]
        Lx = sparse.diags(diagonals, [0, -1, 1], shape=(a, a)).toarray()
        Ix = sparse.identity(self.M).toarray()
        self.A = sparse.kron(Ix, Lx).toarray()
        
        pos1 = np.arange(0,self.M**2,self.M)
        
        for i in range(len(pos1)):
            self.A[pos1[i], pos1[i]] = 1 + self.r
            
        pos2 = np.arange(self.M-1, self.M**2, self.M)
        
        for j in range(len(pos2)):
            self.A[pos2[j], pos2[j]] = 1 + self.r
        
    
    def rhsMatrixA(self):
        maindiag = (1-self.r)*np.ones((1, self.M))
        offdiag = self.r*np.ones((1, self.M-1))
        a = maindiag.shape[1]
        diagonals = [maindiag, offdiag, offdiag]
        Rx = sparse.diags(diagonals, [0, -1, 1], shape=(a, a)).toarray()
        Ix = sparse.identity(self.M).toarray()
        self.A_rhs = sparse.kron(Rx, Ix).toarray()
        
        pos3 = np.arange(self.M, self.M**2-self.M)
        
        for k in range(len(pos3)):
            self.A_rhs[pos3[k], pos3[k]] = 1 - 2*self.r
            
            
    def solve_and_plot(self):
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_zlim(0, 1)
        tc = 0
        nstep = round(self.maxt/self.h)
        while tc < nstep:
            b1 = np.flipud(self.U).reshape(self.M**2, 1)
            sol = np.linalg.solve(self.A, np.matmul(self.A_rhs, b1))
            self.U = np.flipud(sol).reshape(self.M, self.M)
            
            b2 = np.flipud(self.U).reshape(self.M**2, 1)
            sol = np.linalg.solve(self.A, np.matmul(self.A_rhs, b2))
            self.U = np.flipud(sol).reshape(self.M, self.M)
            tc += 1
            
        ax.plot_surface(self.X, self.Y, self.U, cmap=cm.coolwarm,linewidth=0, antialiased=False)
        plt.tight_layout()
        plt.show()
    


def main():
    simulator = ADImethod(20, 2.5, 0.01)
    simulator.solve_and_plot()

if __name__ == "__main__":
    main()