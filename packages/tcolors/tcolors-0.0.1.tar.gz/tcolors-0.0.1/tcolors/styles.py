from collections.abc import Iterable
import re


# ANSI Control Sequence Introducer
CSI = '\033['

ESCAPE_CODE = '{csi}{{code}}m'.format(csi=CSI)

# Capturing regex for hex colors with length 6 and 3 and optional #
HEX_COLOR_PATTERN = re.compile(r'^#?(?:([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})|'
                               '([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F]))$')


class Style:
    """
    Main class to store the codes that will be formated to ANSI escape sequences when coloring.
    It supports addition with other Style instances, creating a new combined style, and with strings, creating a new
    string with the formatted escape sequence.

    It uses an ordered set (implemented with a dict with None values) to store internally the list of codes in order of
    insertion, so the last added colors take preference.
    Dicts remember the order of insertion since CPython 3.6 and since Python 3.7 as a language feature.

    The codes are the numeric parts (as strings) of the escape sequences excluding the CSI and the final m character.
    Eg: ESC[1;38;5;75m -> {'1': None, '38;5;75': None}
    """

    def __init__(self, styles):
        if isinstance(styles, str):
            style = styles
            self._styles = {style: None}
        elif isinstance(styles, dict):
            self._styles = styles
        elif isinstance(styles, Iterable):
            self._styles = {s: None for s in styles}
        else:
            raise TypeError('Invalid styles paramater. It must be an iterable or a string')

    def __add__(self, other):
        if isinstance(other, Style):
            new_styles = dict(self._styles)
            new_styles.update(other._styles)
            return Style(new_styles)
        elif isinstance(other, str):
            return str(self) + other
        else:
            raise TypeError('Can only concatenate styles with styles or styles with str')

    def __radd__(self, other):
        if isinstance(other, str):
            return other + str(self)
        else:
            raise TypeError('Can only concatenate styles with styles or styles with str')

    def __eq__(self, other):
        return self._styles == other._styles

    def __str__(self):
        code = ';'.join(self._styles)
        return ESCAPE_CODE.format(code=code)

    def __repr__(self):
        return '<{}.Style: {}>'.format(__name__, repr(str(self)))


class Color:
    BLACK = Style('30')
    RED = Style('31')
    GREEN = Style('32')
    YELLOW = Style('33')
    BLUE = Style('34')
    MAGENTA = Style('35')
    CYAN = Style('36')
    WHITE = Style('37')

    BRIGHT_BLACK = Style('90')
    BRIGHT_RED = Style('91')
    BRIGHT_GREEN = Style('92')
    BRIGHT_YELLOW = Style('93')
    BRIGHT_BLUE = Style('94')
    BRIGHT_MAGENTA = Style('95')
    BRIGHT_CYAN = Style('96')
    BRIGHT_WHITE = Style('97')


class BgColor:
    BLACK = Style('40')
    RED = Style('41')
    GREEN = Style('42')
    YELLOW = Style('43')
    BLUE = Style('44')
    MAGENTA = Style('45')
    CYAN = Style('46')
    WHITE = Style('47')

    BRIGHT_BLACK = Style('100')
    BRIGHT_RED = Style('101')
    BRIGHT_GREEN = Style('102')
    BRIGHT_YELLOW = Style('103')
    BRIGHT_BLUE = Style('104')
    BRIGHT_MAGENTA = Style('105')
    BRIGHT_CYAN = Style('106')
    BRIGHT_WHITE = Style('107')


class Mod:
    RESET = Style('0')
    BOLD = Style('1')
    DIM = Style('2')  # Faint, decreased intensity, or dimmed
    ITALIC = Style('3')
    UNDERLINE = Style('4')
    SLOW_BLINK = Style('5')  # Not widely supported
    RAPID_BLINK = Style('6')  # Not widely supported
    INVERT = Style('7')  # Swap foreground and background colors
    CONCEAL = Style('8')  # Conceal or hide. Not widely supported
    STRIKE = Style('9')  # Strikethrough


class ANSI256Meta(type):
    """
    Metaclass for auto-populating and caching Style attributes for each of the 256 ANSI colors.
    Color attributes have this format: C_{num} where num is a value from 0 to 255.

    ANSI colors are divided in 4 regions:
      - 0-7: 8 primary colors
      - 8-15: 8 bright colors
      - 16-231: 216 rgb colors
      - 232-255: 24 grayscale colors

    https://www.ditig.com/256-colors-cheat-sheet
    """

    def __new__(cls, name, bases, namespace):
        code = namespace['code']

        for i in range(0, 256):
            name = 'C_{}'.format(i)
            style = Style(code.format(color=i))
            namespace[name] = style

        return super().__new__(cls, name, bases, namespace)


class Color256(metaclass=ANSI256Meta):
    code = '38;5;{color}'


class BgColor256(metaclass=ANSI256Meta):
    code = '48;5;{color}'


class TrueColorBase(Style):
    """
    Base class for creating Style instances with True Color codes.
    True Color ANSI codes have this format: {prefix};2;{r};{g};{b}

    This base class supports defining the colors as:
      - long hex strings: #ddf18a or ddf18a
      - short hex strings: #a43 or a43
      - 3 positional arguments with the rgb values
      - 3 keyword arguments with the keys `r`, `g` and `b`
    """

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], str):
            r, g, b = self._hex_to_rgb(args[0])
        else:
            if len(args) == 3:
                r, g, b = args
            elif 'r' in kwargs and 'g' in kwargs and 'b' in kwargs:
                r = kwargs['r']
                g = kwargs['g']
                b = kwargs['b']
            else:
                raise AttributeError('Invalid color parameters. Use a string with the hex representation of the color, '
                                     'or 3 position arguments for r, g, b, or 3 keyword arguments with the keys '
                                     '`r`, `g`, `b`')

            self._check_rgb_bounds(r, g, b)

        super().__init__(self.code.format(r=r, g=g, b=b))

    @property
    def code(self):
        raise NotImplementedError('Subclasses of TrueColorBase require to declare a code property')

    def _hex_to_rgb(self, hex_color):
        """
        Given a string with a color in its hexadecimal representation (normal or shorter) return a tuple
        with the rgb values as ints.
        """
        match = HEX_COLOR_PATTERN.match(hex_color)
        if not match:
            raise AttributeError('Invalid hex color. Use the standard format with length 6 or 3: #aa119b or #9AD')

        r = int(match.group(1) or match.group(4), 16)
        g = int(match.group(2) or match.group(5), 16)
        b = int(match.group(3) or match.group(6), 16)

        if len(hex_color) <= 4:
            r = r << 4 | r
            g = g << 4 | g
            b = b << 4 | b

        return r, g, b

    def _check_rgb_bounds(self, r, g, b):
        """
        Check the rgb values are ints and are within the valid bounds: [0,255]
        """
        if not (isinstance(r, int) and isinstance(g, int) and isinstance(b, int) and
                0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            raise AttributeError('Invalid r, g, b values. They must be integers in the range [0, 255]')


class TrueColor(TrueColorBase):
    code = '38;2;{r};{g};{b}'


class BgTrueColor(TrueColorBase):
    code = '48;2;{r};{g};{b}'
