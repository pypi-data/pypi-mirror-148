import pkg_resources
import numpy as np


class GMM():
    """docstring for GMM
    """

    def __init__(self):
        self.name = "There's Nothing here!"


class AkkarEtAl_2014(GMM):
    """docstring for AkkarEtAl_2014
    """

    def __init__(self, vs30, dist='repi', Fm='N'):
        GMM.__init__(self)

        self.Vref = 750.0
        self.Vcon = 1000.0

        self.name = 'Akkar et al. (2014)'

        stream = pkg_resources.resource_stream(
            __name__, 'data/AkkarEtAl_2014_1.dat')
        self.indT = np.loadtxt(stream, delimiter='\t')

        stream = pkg_resources.resource_stream(
            __name__, 'data/AkkarEtAl_2014_repi.dat')
        self.repi = np.loadtxt(stream, delimiter='\t')

        stream = pkg_resources.resource_stream(
            __name__, 'data/AkkarEtAl_2014_rhyp.dat')
        self.rhyp = np.loadtxt(stream, delimiter='\t')

        stream = pkg_resources.resource_stream(
            __name__, 'data/AkkarEtAl_2014_rjb.dat')
        self.rjb = np.loadtxt(stream, delimiter='\t')

        self.T = self.rjb[:, 0]
        self.nT = len(self.T)

    def run(self, ss):
        pass
