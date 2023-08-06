from rmt_utilities.reform_cli import get_command_line
from rmt_utilities.rmtutil import RMTCalc
from rmt_utilities.dataobjects import momentum, density
import matplotlib.pyplot as plt


def main(objectstring='requested'):
    args = get_command_line(objectstring)
    calc = RMTCalc(args.dir)
    if objectstring == 'momentum':
        Psi = momentum(args.file, calc, rskip=args.rskip)
    elif objectstring == 'density':
        Psi = density(args.file, calc, rmatr=args.rmatr)

    Psi.plot(normalise=args.normalise_bar, log=args.log_scale, rmax=args.rmax)

    if args.output:
        plt.savefig(args.output)
    if args.plot:
        plt.show()


def plot_mom():
    main('momentum')


def plot_den():
    main('density')


if __name__ == '__main__':
    pass
