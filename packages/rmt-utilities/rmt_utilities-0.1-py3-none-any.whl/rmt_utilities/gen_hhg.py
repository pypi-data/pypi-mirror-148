"""
Utility for generating harmonic spectra from RMT output.
"""
from rmt_utilities.rmtutil import RMTCalc
from rmt_utilities.dipole_cli import get_command_line
import matplotlib.pyplot as plt


def main():
    args = get_command_line('harmonic')

    for f in args.files:
        calc = RMTCalc(f)
        l, v = calc.HHG()
        if args.plot:
            ax = plt.axes()
            if l is not None:
                ax = calc.length.plot(units=args.units, logy=True, ax=ax,
                                      label=[f"{x}_l" for x in
                                             calc.length.columns[1:]])
            if v is not None:
                ax = calc.velocity.plot(units=args.units, logy=True, ax=ax,
                                        label=[f"{x}_v" for x in
                                               calc.velocity.columns[1:]])
            plt.show()
        if args.output:
            if l is not None:
                calc.length.write(fname="Harm_len_", units=args.units)
            if v is not None:
                calc.velocity.write(fname="Harm_vel_", units=args.units)


if __name__ == "__main__":
    main()
