"""
Utility for comparing two RMT calculations to ensure the computed data agrees to
within a specified tolerance.
"""


def read_command_line():
    from argparse import ArgumentParser as AP
    parser = AP()
    parser.add_argument('fileA',
                        help="directory containing first rmt\
                        calculation for comparison")
    parser.add_argument('fileB',
                        help="directory containing first rmt\
                        calculation for comparison")
    parser.add_argument('-t', '--tolerance', help="optional tolerance (number \
                        of decimal places to which agreement is required, \
                        default = 9", type=int, default=9)

    return parser
#    args = vars(parser.parse_args())
#    return args['fileA'], args['fileB'], args['tolerance']


def compare(fileA, fileB, tolerance):
    import rmt_utilities.rmtutil as ru
    fA = ru.RMTCalc(fileA)
    fB = ru.RMTCalc(fileB)
    return fA.agreesWith(fB, tolerance)


def main():
    parser = read_command_line()
    args = vars(parser.parse_args())
    fileA = args['fileA']
    fileB = args['fileB']
    tolerance = args['tolerance']

    if not compare(fileA, fileB, tolerance):
        import sys
        sys.exit("Calculations do not agree to desired tolerance")


if __name__ == "__main__":
    main()
