import argparse
import sys
import cowsay


COW_STYLES = {
    'b': 'Borg style',
    'd': 'Dead style',
    'p': 'State of paranoia',
    's': 'Stoned style',
    't': 'Tired style',
    'w': 'Excited style',
    'y': 'Youthful style',
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('message', nargs='?')
    parser.add_argument('-e', default='oo', metavar='eye_string', help='Select the appearance of the cow\'s eyes. The first two characters will be used')
    parser.add_argument('-f', default='default', metavar='cowfile', help='File to specify ASCII picture of cow')
    parser.add_argument('-l', action='store_true', help='List of cows')
    parser.add_argument('-n', action='store_false', help='Not wrap the message')
    parser.add_argument('-T', type=str, default='  ', metavar='tongue_string', help='Select cow tongue. Must be two chars long')
    parser.add_argument('-W', type=int, default=40, metavar='column', help='Message wrap width')

    group = parser.add_argument_group('Styles')

    for style, descr in COW_STYLES.items():
        group.add_argument(f'-{style}', action='store_true', help=descr)

    return parser.parse_args()


def main():
    args = parse_args()

    if args.l:
        print(*cowsay.list_cows())
    else:
        if args.message:
            msg = args.message
        else:
            msg = sys.stdin.read()
        cow = args.f

        # I've tried different version of this parameters, 
        # but it works only with one char.
        preset = None
        for style in COW_STYLES:
            if getattr(args, style):
                preset = style
                break

        eyes = args.e[:2]
        tongue = args.T[:2] # In description of script it MUST BE two chars long, but works as there
        width = args.W
        wrap_text = args.n

        if '/' in args.f:
            with open(args.f, 'r') as f:
                cowfile = cowfile.read_dot_cow(f)
        else:
            cowfile = None

        print(cowsay.cowsay(msg, cow, preset, eyes, tongue, width, wrap_text, cowfile))


if __name__ == '__main__':
    main()
