"""I have MacOS and in python module cmd tab-completion not working. I hope it will be work in other OS."""
import cmd
import shlex
from cowsay import list_cows, THOUGHT_OPTIONS, Bubble, cowsay, cowthink, make_bubble


class CowConsole(cmd.Cmd):
    prompt = '(cowsay) '
    use_rawinput = True
    def _parse_make_bubble(self, arg):
        parsed = shlex.split(arg)

        params = {
            'text': parsed[0],
            'brackets': THOUGHT_OPTIONS['cowsay'],
            'width': 40,
            'wrap_text': False
        }

        for i, p in enumerate(parsed[1:], start=1):
            if p == '--brackets':
                exec(r'params["brackets"] = {}'.format(parsed[i + 1].encode('unicode_escape').decode()))
            elif p == '-W':
                params['width'] = int(parsed[i + 1])
            elif p == '-n':
                params['wrap_text'] = True

        return params

    def _parse_cowsay(self, arg):
        parsed = shlex.split(arg)
        params = {
            'message': parsed[0],
            'cow': 'default',
            'eyes': 'oo',
            'tongue': '  '
        }

        for i, p in enumerate(parsed[1:], start=1):
            if p == '-f':
                params['cow'] = parsed[i + 1]
            elif p == '-e':
                params['eyes'] = parsed[i + 1]
            elif p == '-T':
                params['tongue'] = parsed[i + 1]
    
        return params


    def do_list_cows(self, arg):
        """List of cows
        
        Usage: list_cows [file]
        """
        if len(arg) == 0:
            print(list_cows())
        else:
            print(list_cows(shlex.split(arg)[0]))

    def do_make_bubble(self, arg):
        """Wraps text when passed --wrap_text, then pads text and sets inside a bubble.
        This is the text that appears above the cows.

        :param message: The message to de displayed
        :param brackets: --brakets: String with Bubble-class format
        :param width: -W: Message wrap width
        :param wrap_text: -n: To wrap the message

        
        Usage: make_bubble message [--brackets "Bubble('o', '(', ')', '(', ')', '(', ')', '(', ')')"] [-W 40] [-n]
        """
        params = self._parse_make_bubble(arg)
        print(make_bubble(**params))

    def do_cowsay(self, arg):
        """Similar to the cowsay command. Parameters (only cow, eyes, tongue) are listed with their
        corresponding options in the cowsay command. Returns the resulting cowsay
        string

        :param message: The message to de displayed
        :param cow: -f – the available cows can be found by calling list_cows
        :param eyes: -e or eye_string: Select the appearance of the cow\'s eyes. The first two characters will be used
        :param tongue: -T or tongue_string: Select cow tongue. Must be two chars long
        :param width: -W: Message wrap width
        :param wrap_text: -n: To wrap the message

        Usage: cowsay message [--f cow] [--eyes eye_string] [--T tongue_string] [-W width] [-n]
        """
        params = self._parse_cowsay(arg)
        print(cowsay(**params))

    def do_cowthink(self, arg):
        """Similar to the cowthink command. Parameters (only cow, eyes, tongue) are listed with their
        corresponding options in the cowthink command. Returns the resulting cowthink
        string
        
        :param message: The message to de displayed
        :param cow: -f – the available cows can be found by calling `list_cows`:
        :param eyes: -e or eye_string: Select the appearance of the cow\'s eyes. The first two characters will be used
        :param tongue: -T or tongue_string: Select cow tongue. Must be two chars long
        :param width: -W: Message wrap width
        :param wrap_text: -n: To wrap the message
        
        Usage: cowsay message [-f cow] [-e eye_string] [-T tongue_string] [-W width] [-n]
        """
        params = self._parse_cowsay(arg)
        print(cowthink(**params))

    def complete_make_bubble(self, text, line, beg, end):
        complets = ['-f', '-W', '-n']
        if text:
            return [t for t in complets if t.startswith(text)]
        else:
            return complets

    def complete_cowthink(self, text, line, beg, end):
        complets = ['-T', '-e', '-f']
        if text:
            return [t for t in complets if t.startswith(text)]
        else:
            return complets

    def complete_cowsay(self, text, line, beg, end):
        complets = ['-T', '-e', '-f']
        if text:
            return [t for t in complets if t.startswith(text)]
        else:
            return complets

    def do_exit(self, arg):
        return 0

if __name__ == '__main__':
    CowConsole().cmdloop()
