# imports
import numpy as np
from scipy.interpolate import griddata

"""
Most of the code below is the same/similar to what was given in 'Steam_stem'.
"""

class steam:

    def __init__(self, pressure, T=None, x=None, h=None, s=None, name=''):

        self.p = pressure
        self.T = T
        self.x = x
        self.h = h
        self.s = s
        self.name = name
        self.v = None
        self.region = None
        self.calculate_properties()

    def calculate_properties(self):

        #ts, ps, hfs, hgs, sfs, sgs, vfs, vgs = np.loadtxt('sat_water_table.txt', skiprows=1, unpack=True)
        #t_super, h_super, s_super, p_super = np.loadtxt('superheated_water_table.txt', skiprows=1, unpack=True)
        """
        I kept on getting weird values. To try and fix the issue I changed the format of the '#' code above
        to what it is now (the code below this docstring).
        It's essentially the same as above, just formatted differently.
        """
        data_sat = np.loadtxt('sat_water_table.txt', skiprows=1)
        ts = data_sat[:,0]
        ps = data_sat[:,1]
        hfs = data_sat[:,2]
        hgs = data_sat[:,3]
        sfs = data_sat[:,4]
        sgs = data_sat[:,5]
        vfs = data_sat[:,6]
        vgs = data_sat[:,7]

        order = np.argsort(ps)
        ts = ts[order]
        ps = ps[order]
        hfs = hfs[order]
        hgs = hgs[order]
        sfs = sfs[order]
        sgs = sgs[order]
        vfs = vfs[order]
        vgs = vgs[order]

        data_sup = np.loadtxt('superheated_water_table.txt', skiprows=1)
        t_super = data_sup[:,0]
        h_super = data_sup[:,1]
        s_super = data_sup[:,2]
        p_super = data_sup[:,3]

        R = 8.314/(18/1000)
        Pbar = self.p / 100
        """
        The method function was not used in 'Steam_stem'. I used this function 
        in this program because I was getting incorrect outputs. I'm not entirely sure
        what this function is doing but I am going to assume it picks a value that the 
        variable is close to when solving a function. 
        """
        if Pbar < ps.min() or Pbar > ps.max():
            Tsat = float(griddata(ps, ts, Pbar, method='nearest'))
            hf = float(griddata(ps, hfs, Pbar, method='nearest'))
            hg = float(griddata(ps, hgs, Pbar, method='nearest'))
            sf = float(griddata(ps, sfs, Pbar, method='nearest'))
            sg = float(griddata(ps, sgs, Pbar, method='nearest'))
            vf = float(griddata(ps, vfs, Pbar, method='nearest'))
            vg = float(griddata(ps, vgs, Pbar, method='nearest'))
        else:
            Tsat = float(griddata(ps, ts, Pbar, method='linear'))
            hf = float(griddata(ps, hfs, Pbar, method='linear'))
            hg = float(griddata(ps, hgs, Pbar, method='linear'))
            sf = float(griddata(ps, sfs, Pbar, method='linear'))
            sg = float(griddata(ps, sgs, Pbar, method='linear'))
            vf = float(griddata(ps, vfs, Pbar, method='linear'))
            vg = float(griddata(ps, vgs, Pbar, method='linear'))

        if self.T is not None:
            if self.T > Tsat:
                self.region = 'Superheated'
                pts = np.column_stack((t_super, p_super))
                self.h = float(griddata(pts, h_super, (self.T, self.p)))
                self.s = float(griddata(pts, s_super, (self.T, self.p)))
                self.x = 1.0
                TK = self.T +273.15
                self.v = R * TK / (self.p * 1000)
                """ 
                Below are standard equations solving for enthalpy, entropy, specific volume, and pressure
                """
            else:
                self.region = 'Saturated'
                self.T = Tsat
                if self.x is None:
                    self.x = 1.0
                self.h = hf + self.x * (hg - hf)
                self.s = sf + self.x * (sg - sf)
                self.v = vf + self.x * (vg - vf)
        elif self.x is not None:
            self.region = 'Saturated'
            self.T = Tsat
            self.h = hf + self.x * (hg - hf)
            self.s = sf + self.x * (sg - sf)
            self.v = vf + self.x * (vg - vf)
        elif self.h is not None:
            self.x = (self.h - hf) / (hg - hf)
            if self.x <= 1.0:
                self.region = 'Saturated'
                self.T = Tsat
                self.s = sf + self.x * (sg - sf)
                self.v = vf + self.x * (vg - vf)
            else:
                self.region = 'Superheated'
                pts = np.column_stack((h_super, p_super))
                self.T = float(griddata(pts, t_super, (self.h, self.p)))
                self.s = float(griddata(pts, s_super, (self.h, self.p)))
                self.v = 0.001
        elif self.s is not None:
            self.x = (self.s - sf) / (sg - sf)
            if self.x <= 1.0:
                self.region = 'Saturated'
                self.T = Tsat
                self.h = hf + self.x * (hg - hf)
                self.v = vf + self.x * (vg - vf)
            else:
                self.region = 'Superheated'
                pts = np.column_stack((s_super, p_super))
                self.T = float(griddata(pts, t_super, (self.s, self.p)))
                self.h = float(griddata(pts, h_super, (self.s, self.p)))
                self.v = 0.001

    def print_properties(self):
        print("Name:", self.name)
        print("Region:", self.region)
        print("Pressure: {:.2f} kPa".format(self.p))
        print("Temperature: {:.2f} C".format(self.T))
        print("Enthalpy: {:.2f} kJ/kg".format(self.h))
        print("Entropy: {:.4f} kJ/(kg*K)".format(self.s))
        print("Specific Volume: {:.6f} m^3/kg".format(self.v))
        if self.region == 'Saturated':
            print("Quality: {:0.4f}".format(self.x))
        print()

    def print(self):
        self.print_properties()

if __name__ == '__main__':
    s = steam(8000, T=450, name='Test Steam')
    s.print_properties()