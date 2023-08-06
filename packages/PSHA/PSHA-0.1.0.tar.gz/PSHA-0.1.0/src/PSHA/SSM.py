import numpy as np
import matplotlib.pyplot as plt
import triangle as tr


class SeismicSource():
    def __init__(self, mmax, mmin, a, b, nm=10):
        self.mmax = mmax
        self.mmin = mmin
        self.a = a
        self.b = b
        self.beta = b * np.log(10)
        self.alpha = a * np.log(10)
        self.lambdaMin = np.exp(self.alpha-self.beta*self.mmin)
        self.nm = nm
        self.r = None
        self.Pr = None
        self.dm = (self.mmax-self.mmin)/self.nm
        self.m = np.linspace(self.mmin, self.mmax-self.dm, self.nm)+self.dm/2
        self.Pm = self.beta*np.exp(-self.beta*(self.m-self.mmin))/(
            1-np.exp(-self.beta*(self.mmax-self.mmin)))*self.dm

    def plotDistanceDistribution(self):
        try:
            dx = self.r[1]-self.r[0]
        except Exception as e:
            dx = 1
        plt.bar(self.r, self.Pr, width=0.8*dx, label='P(R=r)', ec='k')
        plt.show()
        dx = self.m[1]-self.m[0]
        plt.bar(self.m,
                self.Pm, width=0.8*dx, label='P(M=m)', ec='k')
        plt.show()


class Point(SeismicSource):
    def __init__(self, coords, mmax, mmin, a, b, **kargs):
        SeismicSource.__init__(self, mmax, mmin, a, b, **kargs)
        self.coords = coords

    def calculateDistanceDistribution(self, ip):
        self.r = np.linalg.norm(self.coords-ip, axis=1)
        self.Pr = np.zeros(self.r.shape)+1.0


class Line(SeismicSource):
    def __init__(self, coords, mmax, mmin, a, b, nr=10, ns=10, **kargs):
        self.coords = coords
        self.ns = ns
        self.nr = nr
        SeismicSource.__init__(self, mmax, mmin, a, b, **kargs)

    def calculateDistanceDistribution(self, ip):
        # FIXME hay una manera mas general
        dmin = np.linalg.norm(np.cross(
            self.coords[1]-self.coords[0], self.coords[0]-ip))/np.linalg.norm(self.coords[1]-self.coords[0])
        distancias_coords = np.linalg.norm(self.coords-ip, axis=1)

        dmax = max(*distancias_coords)
        n = self.nr

        self.r = np.linspace(1/n/2, 1-1/n/2, n)*(dmax-dmin)+dmin
        R = np.linspace(dmin, dmax, n+1)
        n = self.ns
        t = np.linspace(1/n/2, 1-1/n/2, n).reshape([n, 1])
        m = np.array([self.coords[1]-self.coords[0]])
        sampleo = t@m+self.coords[0]
        self.Pr = np.zeros([self.nr])
        d = np.linalg.norm(sampleo-ip, axis=1)
        for i in range(self.nr):
            seg = np.sum(((d >= R[i]) * (d < R[i+1]))*1)
            self.Pr[i] = seg/self.ns


class Area(SeismicSource):
    def __init__(self, coords, mmax, mmin, a, b, nr=10, **kargs):
        self.coords = coords
        self.nr = nr
        SeismicSource.__init__(self, mmax, mmin, a, b, **kargs)

    def mesh(self, fmt='qa'):
        B = tr.triangulate(dict(vertices=self.coords), fmt)
        self.vertices = B['vertices']
        self.elements = B['triangles']
        self.centros = np.average(self.vertices[self.elements], axis=1)

    def plotMesh(self):
        kilos = self.coords.tolist()
        kilos += [kilos[0]]
        kilos = np.array(kilos)
        plt.plot(*kilos.T, '-o', c='k')
        try:
            plt.plot(*self.vertices.T, 'o', c='b')
            for e in self.elements:
                kilos = self.vertices[e].tolist()
                kilos += [kilos[0]]
                kilos = np.array(kilos)
                plt.plot(*kilos.T, '-', c='gray')
        except Exception as e:
            pass
        plt.gca().set_aspect('equal')

    def calculateDistanceDistribution(self, ip):
        n = self.nr
        distancias_posibles = np.linalg.norm(self.vertices, axis=1)
        dmax = np.max(distancias_posibles)
        dmin = np.min(distancias_posibles)
        self.r = np.linspace(1/n/2, 1-1/n/2, n)*(dmax-dmin)+dmin
        self.Pr = np.zeros([self.nr])
        total = len(self.centros)
        R = np.linspace(dmin, dmax, n+1)
        d = np.linalg.norm(self.centros-ip, axis=1)
        for i in range(self.nr):
            seg = np.sum(((d >= R[i]) * (d < R[i+1]))*1)
            self.Pr[i] = seg/total


class Rectangle(Area):

    def __init__(self, coords, mmax, mmin, a, b, nr=10, **kargs):
        Area.__init__(self, coords, mmax, mmin, a, b, nr=nr, **kargs)

    def mesh(self, nx=10, ny=10):
        coords0 = self.coords-np.min(self.coords, axis=0)
        _a = coords0[1][0]
        _b = coords0[2][1]

        dx = _a/nx
        dy = _b/ny

        coords = []

        for i in range(nx+1):
            x = i*dx
            for j in range(ny+1):
                y = j*dy
                coords += [[x, y]]

        dicc = []

        def node(i, j): return i*(ny+1)+j

        for i in range(nx):
            for j in range(ny):
                node1 = node(i, j)
                node2 = node(i+1, j)
                node3 = node(i+1, j+1)
                node4 = node(i, j+1)
                dicc += [[node1, node2, node3, node4]]
        self.vertices = np.array(coords)+np.min(self.coords, axis=0)
        self.elements = np.array(dicc)
        self.centros = np.average(self.vertices[self.elements], axis=1)


class SeismicSourceModel():
    """docstring for SeismicSourceModel
    """

    def __init__(self, interest_point, sources=None):
        self.ip = interest_point
        self.sources = sources or []
        for s in self.sources:
            s.calculateDistanceDistribution(self.ip)

    def addSource(self, source):
        source.calculateDistanceDistribution(self.ip)
        self.sources.append(source)
