"""
data classes for holding RMT outputs and computed observables
"""
import pandas as pd
import numpy as np
from pathlib import Path, PosixPath
from _io import TextIOWrapper


def convertpath(path):
    """
    Utility function for converting paths to PosixPath type. If path is already
    PosixPath, do nothing. If it is a str, convert to PosixPath.


    Note: type TextIOWrapper passes through unchanged as it is needed for several
    internal functions.
    """
    tt = type(path)
    if (tt == str):
        return Path(path)
    elif (tt == PosixPath or tt == TextIOWrapper):
        return path
    else:
        raise TypeError(f"The path supplied ({path}) is of type {tt}: please \
                        supply type str or PosixPath")


class Hfile():
    def __init__(self, path):
        self.path = convertpath(path)
        self.path = self.path / 'H'
        try:
            with open(self.path, 'rb') as f:
                self.rmatr = np.fromfile(f, dtype=float, count=4)[-1]
        except (FileNotFoundError, IndexError):
            print("Error reading H file: using default R-matrix boundary of 20 a.u.")
            self.rmatr = 20.0


class UnitError(NameError):
    def __init__(self, units, cls):
        message = f"""{units} is not a valid unit for {cls}.
To use custom units, use atomic units (select units='au') and apply scaling factors in postprocessing"""
        super().__init__(message)


class distribution(np.ndarray):
    """ storage and utilities for 2d polar representation of density/momentum distributions

    Provides method ``.plot()`` for displaying the data

    Parameters
    -----------
    path : pathlib.Path or str
        absolute or relative path to datafile
    rootcalc : rmtutil.RMTCalc
        RMT calculation from which the distribution file is derived
    rskip : int
        for momentum distributions, skip the first rskip a.u of space before
        transforming

    Attributes
    ----------
    path : pathlib.Path
        absolute or relative path to the source datafile
    theta : np.ndarray
        array containing the azimuthal angles for the 2-d polar distribution
        together with ``r`` forms a meshgrid for plotting the distribution
    r : np.ndarray
        array containing the radial grid points for the 2-d polar distribution.
        together with ``theta`` forms a meshgrid for plotting the distribution
    """
    def __new__(cls, path, rootcalc, rskip=0):
        # Input array is an already formed ndarray instance
        # We first cast to be our class type
        obj = np.asarray(np.loadtxt(path, unpack=True)).view(cls)
        obj.path = convertpath(path)
        obj.theta = 0
        obj.r = 0
        return obj

    def __array_finalize__(self, obj):
        # see InfoArray.__array_finalize__ for comments
        if obj is None:
            return
        self.theta = getattr(obj, 'theta', None)
        self.r = getattr(obj, 'r', None)

    def plot(self, normalise=False, log=False, rmax=None):
        """
        Plot the requested distribution in polar form with colourbar. Optionally
        normalise the yield, show on a log scale or limit the maximum radial
        value displayed.

        Note that the actual data is not modified- only the view expressed in
        the plot.

        Parameters
        -----------
        normalise : bool, default False
            normalise the distribution

        log : bool, default False
            show the distribution on a log scale

        rmax : float, default None
            limit the radial extent of the plot.


        Returns
        -------
        ax : matplotlib.axes.SubplotBase
            handle for axes holding the plotted distibution

        cbar : matplotlib.colorbar.Colorbar
            handle for colorbar object
        """
        import matplotlib.pyplot as plt
        from matplotlib import cm

        Psi = np.copy(self)
        cbar_label_info = []

        if normalise:
            Psi /= np.max(Psi)
            cbar_label_info.append('Normalised Scale')

        if log:
            Psi = -np.log10(Psi+1e-10)
            cbar_label_info.append('(log scale, $10^{-x}$)')

        plt.figure(1, figsize=(8, 9))

        ax = plt.subplot(polar=True)
        ax.set_theta_zero_location("E")

        levels = np.linspace(0.0, np.amax(Psi), 200)
        CS = plt.contourf(self.theta, self.r, Psi, levels, cmap=cm.jet)
        if rmax:
            ax.set_rmax(rmax)
        cbar = plt.colorbar(CS)
        cbar.set_label(' '.join(cbar_label_info))

        return ax, cbar


class density(distribution):
    """
    Storage and utilities for 2d polar representation of density distribution
    """
    def __new__(cls, path, rootcalc, rmatr=None, *args, **kwargs):
        obj = super().__new__(cls, path, rootcalc, *args, **kwargs)

        if rmatr is None:
            rmatr = Hfile(rootcalc.path).rmatr
        dR = rootcalc.config['deltar']
        Nr, Nphi = obj.shape
        zeniths = rmatr + dR * np.arange(0, Nr)
        phi = np.linspace(0, 360, num=Nphi)
        angle = np.radians(-phi)
        obj.theta, obj.r = np.meshgrid(angle, zeniths)
        return obj


class momentum(distribution):
    """
    Storage and utilities for 2d polar representation of momentum distribution
    """
    def __new__(cls, path, rootcalc, rskip=200, *args, **kwargs):
        obj = super().__new__(cls, path, rootcalc, rskip=rskip, *args, **kwargs)

        nskip = int(rskip/rootcalc.config['deltar'])
        Nt = rootcalc.config['num_out_pts'] - nskip

        dK = (2.0*np.pi)/(rootcalc.config['deltar']*Nt)
        Nr, Nphi = obj.shape
        zeniths = dK*np.arange(0, Nr)
        phi = np.linspace(0, 360, num=Nphi)
        angle = np.radians(-phi)
        obj.theta, obj.r = np.meshgrid(angle, zeniths)
        # Finally, we must return the newly created object:
        return obj


class Observable(pd.DataFrame):
    """ DataFrame plus routines for observables

    Provides methods ``.write()`` ``.plot()`` for storing and displaying data
    respectively.
    """

    def __init__(self, root=".", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = Path(root)

    def truncate(self, *args, **kwargs):
        """Truncate an observable (DataFrame), retaining the class definition"""
        return Observable(root=self.root, data=super().truncate(*args, **kwargs))

    def write(self, fname, units="eV"):
        """
        Write the observable data to separate output files: one for each
        column.  The output files will be named

        ``self.root/fname_column``

        where ``self.root`` is the location of the RMT calculation, ``fname`` is the
        provided filename prefix, and ``column`` is the column heading in the DataFrame

        optionally scale the x-axis data for different units: "eV" (default) or
        "au".
        """

        if units == "eV":
            from rmt_utilities.atomicunits import eV
            xscale = 1.0/eV
        elif units == "au":
            xscale = 1.0
        else:
            raise UnitError(units=units, cls=type(self))
        c1 = self.columns[0]
        tmpdf = self.copy()
        tmpdf[c1] = xscale * tmpdf[c1]
        for col in self.columns[1:]:
            filename = fname + col
            opf = self.root / filename
            with open(opf, "w") as f:
                tmpdf.to_csv(f, columns=[c1, col],
                             sep=" ", index=False, header=None)

    def plot(self, units="eV", *args, **kwargs):
        """ Plot the columns of the dataframe using the first column as the x
        axis.
        """
        if units == "eV":
            from rmt_utilities.atomicunits import eV
            xscale = 1.0/eV
        elif units == "au":
            xscale = 1.0
        else:
            raise UnitError(units=units, cls=type(self))
        c1 = self.columns[0]
        tmpdf = self.copy()
        tmpdf[c1] = xscale * tmpdf[c1]
        ax = tmpdf.plot(0, tmpdf.columns[1:], *args, **kwargs)
        ax.set_xlabel(f"Frequency ({units})")
        ax.set_ylabel("Amplitude (arb. units)")
        return ax


class Data(pd.DataFrame):
    """DataFrame plus additional methods.

    Provides method ``.FFT()`` for Fourier transforming the sanitised (zero-padded
    and windowed) data.

    Parameters
    -----------
    data : Pandas DataFrame
    """

    def __init__(self, data, sols=None, *args, **kwargs):
        super().__init__(data)

    def __bool__(self):
        """returns True"""
        return True

    def FFT(self, blackman=True, pad=1):
        """Apply a blackman window to all data columns, take fourier transform
        of the windowed input data, return DataFrame with transformed data

        Parameters
        ----------
        blackman : bool, optional
            Apply blackman window to data before Fourier Transforming
        pad : int, optional
            prepad the data with zeros before transforming: increases the length
            of the signal by factor ``pad`` and then rounds up to the nearest
            power of two
        """
        df = Observable()
        for col in self.columns[1:]:
            ydat = np.array(self[col])
            if blackman:
                ydat = np.blackman(len(ydat)) * ydat
            if pad:
                ydat = self._pad_with_zeros(ydat, factor=pad)
            Y = (np.fft.fft(ydat))[:len(ydat)//2]
            df[col] = Y
        X = np.arange(len(Y))*(((np.pi)/len(Y))/self.xstep)
        df.insert(0, "Freq", X)

        return df

    def _pad_with_zeros(self, ydat, factor=8):
        """pad ydat with zeros so that the length of ydat is a power of 2 and
        at least factor times the length of ydat on input."""

        pot = 2  # power of two
        while pot < (factor * len(ydat)):
            pot *= 2
        numzeros = pot-len(ydat)
        return np.concatenate([np.zeros(numzeros), np.transpose(ydat)])


class DataFile(Data):
    """DataFile with metadata from RMT output file

    Parameters
    -----------
    path : pathlib.Path or str
        absolute or relative path to datafile
    sols : list of str
        list of which solutions (column headings) to extract from data files.
        E.G ["0001_x", "0001_y"]

    Attributes
    ----------
    path : pathlib.Path
        absolute or relative path to the source datafile
    name : str
        name of the datafile
    xstep : float
        spacing between successive values in the first column of datafile
    len : int
        number of elements in each column of the datafile
    """

    def __init__(self, path, sols=None, *args, **kwargs):
        super().__init__(self._harvest(path, sols=sols))
        self.path = convertpath(path)
        self.name = self.path.parts[-1]
        self.xstep = self[self.columns[0]][1] - self[self.columns[0]][0]
        self.len = len(self)
        self.tolerance = 9  # number of decimal places to check agreement between calculations
        if self.name.startswith("expec_v_all"):
            self.phasefactor = -1j
            self.scalefactor = 2
        else:
            self.phasefactor = 1.0
            self.scalefactor = 4

    def _harvest(self, path, sols):
        """ Given the name of a file to read, harvest will read the data, return
        the column headers, and the (multicolumn) data as a numpy ndarray"""
        with open(path, 'r') as f:
            toprow = f.readline()
            try:
                float(toprow.split()[0])  # check to see if top row is headers
            except ValueError:  # top row is headers
                head = 0
            else:  # no column headings
                head = None

        df = pd.read_csv(path, delim_whitespace=True, header=head)

        if sols:
            cols = [df.columns[0]]
            for sol in sols:
                cols.extend([c for c in df.columns if c == sol])
            df = df[cols]

        return df

    def __eq__(self, other):
        if self.round(self.tolerance).equals(other.round(self.tolerance)):
            return True
        else:
            return False

    def __ne__(self, other):
        return (not self == other)
