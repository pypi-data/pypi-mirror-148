"""
Utility for generating absorption spectra from RMT output.
"""
from rmt_utilities.rmtutil import RMTCalc
from rmt_utilities.dipole_cli import get_command_line
import matplotlib.pyplot as plt


def main():
    args = get_command_line('absorption')

    for f in args.files:
        calc = RMTCalc(f)
        if calc.ATAS() is not None:
            if args.plot:
                calc.TAS.plot(units=args.units)
                plt.show()
            if args.output:
                calc.TAS.write(fname="TAS_", units=args.units)


if __name__ == "__main__":
    main()
