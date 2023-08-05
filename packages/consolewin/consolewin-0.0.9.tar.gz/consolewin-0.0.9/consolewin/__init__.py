import time
from os import system

try:
    from pynput.keyboard import Controller, Key
except:
    try:
        system(
            'pip install pynput || pip3 install pynput || pip install bullet || pip3 install bullet')
    except:
        print('Failed to import required packages.')
        system('pause>nul')


def title(titleS):
    system(f'title {titleS}')


def fullscreen():
    keyboard = Controller()
    keyboard.press(Key.f11)
    keyboard.release(Key.f11)


def clear():
    system('cls')




































import os
import pkg_resources
import re
import shutil
import sys
import zipfile
from optparse import OptionParser


DEFAULT_FONT = 'standard'

COLOR_CODES = {'BLACK': 30, 'RED': 31, 'GREEN': 32, 'YELLOW': 33, 'BLUE': 34, 'MAGENTA': 35, 'CYAN': 36, 'LIGHT_GRAY': 37,
               'DEFAULT': 39, 'DARK_GRAY': 90, 'LIGHT_RED': 91, 'LIGHT_GREEN': 92, 'LIGHT_YELLOW': 93, 'LIGHT_BLUE': 94,
               'LIGHT_MAGENTA': 95, 'LIGHT_CYAN': 96, 'WHITE': 97, 'RESET': 0
               }

RESET_COLORS = b'\033[0m'

if sys.platform == 'win32':
    SHARED_DIRECTORY = os.path.join(os.environ["APPDATA"], "consolefiglet")
else:
    SHARED_DIRECTORY = '/usr/local/share/consolepyfiglet/'


def figlet_format(text, font=DEFAULT_FONT, **kwargs):
    fig = Figlet(font, **kwargs)
    return fig.renderText(text)


def print_figlet(text, font=DEFAULT_FONT, colors=":", **kwargs):
    ansiColors = parse_color(colors)
    if ansiColors:
        sys.stdout.write(ansiColors)

    print(figlet_format(text, font, **kwargs))

    if ansiColors:
        sys.stdout.write(RESET_COLORS.decode('UTF-8', 'replace'))
        sys.stdout.flush()


class FigletError(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return self.error


class CharNotPrinted(FigletError):
    """
    Raised when the width is not sufficient to print a character
    """


class FontNotFound(FigletError):
    """
    Raised when a font can't be located
    """


class FontError(FigletError):
    """
    Raised when there is a problem parsing a font file
    """


class InvalidColor(FigletError):
    """
    Raised when the color passed is invalid
    """


class FigletFont(object):
    """
    This class represents the currently loaded font, including
    meta-data about how it should be displayed by default
    """

    reMagicNumber = re.compile(r'^[tf]lf2.')
    reEndMarker = re.compile(r'(.)\s*$')

    def __init__(self, font=DEFAULT_FONT):
        self.font = font

        self.comment = ''
        self.chars = {}
        self.width = {}
        self.data = self.preloadFont(font)
        self.loadFont()

    @classmethod
    def preloadFont(cls, font):
        """
        Load font data if exist
        """
        for extension in ('tlf', 'flf'):
            fn = '%s.%s' % (font, extension)
            if pkg_resources.resource_exists('pyfiglet.fonts', fn):
                data = pkg_resources.resource_string('pyfiglet.fonts', fn)
                data = data.decode('UTF-8', 'replace')
                return data
            else:
                for location in ("./", SHARED_DIRECTORY):
                    full_name = os.path.join(location, fn)
                    if os.path.isfile(full_name):
                        with open(full_name, 'rb') as f:
                            return f.read().decode('UTF-8', 'replace')
        else:
            raise FontNotFound(font)

    @classmethod
    def isValidFont(cls, font):
        if not font.endswith(('.flf', '.tlf')):
            return False
        f = None
        full_file = os.path.join(SHARED_DIRECTORY, font)
        if os.path.isfile(font):
            f = open(font, 'rb')
        elif os.path.isfile(full_file):
            f = open(full_file, 'rb')
        else:
            f = pkg_resources.resource_stream('pyfiglet.fonts', font)
        header = f.readline().decode('UTF-8', 'replace')
        f.close()
        return cls.reMagicNumber.search(header)

    @classmethod
    def getFonts(cls):
        all_files = pkg_resources.resource_listdir('pyfiglet', 'fonts')
        if os.path.isdir(SHARED_DIRECTORY):
            all_files += os.listdir(SHARED_DIRECTORY)
        return [font.rsplit('.', 2)[0] for font
                in all_files
                if cls.isValidFont(font)]

    @classmethod
    def infoFont(cls, font, short=False):
        """
        Get informations of font
        """
        data = FigletFont.preloadFont(font)
        infos = []
        reStartMarker = re.compile(r"""
            ^(FONT|COMMENT|FONTNAME_REGISTRY|FAMILY_NAME|FOUNDRY|WEIGHT_NAME|
              SETWIDTH_NAME|SLANT|ADD_STYLE_NAME|PIXEL_SIZE|POINT_SIZE|
              RESOLUTION_X|RESOLUTION_Y|SPACING|AVERAGE_WIDTH|COMMENT|
              FONT_DESCENT|FONT_ASCENT|CAP_HEIGHT|X_HEIGHT|FACE_NAME|FULL_NAME|
              COPYRIGHT|_DEC_|DEFAULT_CHAR|NOTICE|RELATIVE_).*""", re.VERBOSE)
        reEndMarker = re.compile(r'^.*[@#$]$')
        for line in data.splitlines()[0:100]:
            if (cls.reMagicNumber.search(line) is None
                    and reStartMarker.search(line) is None
                    and reEndMarker.search(line) is None):
                infos.append(line)
        return '\n'.join(infos) if not short else infos[0]

    @staticmethod
    def installFonts(file_name):
        """
        Install the specified font file to this system.
        """
        if isinstance(pkg_resources.get_provider('pyfiglet'), pkg_resources.ZipProvider):

            location = SHARED_DIRECTORY
        else:

            location = pkg_resources.resource_filename('pyfiglet', 'fonts')

        print("Installing {} to {}".format(file_name, location))

        if not os.path.exists(location):
            os.makedirs(location)

        if os.path.splitext(file_name)[1].lower() == ".zip":

            with zipfile.ZipFile(file_name) as zip_file:
                for font in zip_file.namelist():
                    font_file = os.path.basename(font)
                    if not font_file:
                        continue
                    with zip_file.open(font) as src:
                        with open(os.path.join(location, font_file), "wb") as dest:
                            shutil.copyfileobj(src, dest)
        else:
            shutil.copy(file_name, location)

    def loadFont(self):
        """
        Parse loaded font data for the rendering engine to consume
        """
        try:

            data = self.data.splitlines()

            header = data.pop(0)
            if self.reMagicNumber.search(header) is None:
                raise FontError('%s is not a valid figlet font' % self.font)

            header = self.reMagicNumber.sub('', header)
            header = header.split()

            if len(header) < 6:
                raise FontError('malformed header for %s' % self.font)

            hardBlank = header[0]
            height, baseLine, maxLength, oldLayout, commentLines = map(
                int, header[1:6])
            printDirection = fullLayout = None

            # these are all optional for backwards compat
            if len(header) > 6:
                printDirection = int(header[6])
            if len(header) > 7:
                fullLayout = int(header[7])

            # if the new layout style isn't available,
            # convert old layout style. backwards compatability
            if fullLayout is None:
                if oldLayout == 0:
                    fullLayout = 64
                elif oldLayout < 0:
                    fullLayout = 0
                else:
                    fullLayout = (oldLayout & 31) | 128

            # Some header information is stored for later, the rendering
            # engine needs to know this stuff.
            self.height = height
            self.hardBlank = hardBlank
            self.printDirection = printDirection
            self.smushMode = fullLayout

            # Strip out comment lines
            for i in range(0, commentLines):
                self.comment += data.pop(0)

            def __char(data):
                """
                Function loads one character in the internal array from font
                file content
                """
                end = None
                width = 0
                chars = []
                for j in range(0, height):
                    line = data.pop(0)
                    if end is None:
                        end = self.reEndMarker.search(line).group(1)
                        end = re.compile(re.escape(end) + r'{1,2}$')

                    line = end.sub('', line)

                    if len(line) > width:
                        width = len(line)
                    chars.append(line)
                return width, chars

            # Load ASCII standard character set (32 - 127)
            for i in range(32, 127):
                width, letter = __char(data)
                if ''.join(letter) != '':
                    self.chars[i] = letter
                    self.width[i] = width

            # Load ASCII extended character set
            while data:
                line = data.pop(0).strip()
                i = line.split(' ', 1)[0]
                if (i == ''):
                    continue
                hex_match = re.search('^0x', i, re.IGNORECASE)
                if hex_match is not None:
                    i = int(i, 16)
                    width, letter = __char(data)
                    if ''.join(letter) != '':
                        self.chars[i] = letter
                        self.width[i] = width

        except Exception as e:
            raise FontError('problem parsing %s font: %s' % (self.font, e))

    def __str__(self):
        return '<FigletFont object: %s>' % self.font


unicode_string = type(''.encode('ascii').decode('ascii'))


class FigletString(unicode_string):
    """
    Rendered figlet font
    """

    # translation map for reversing ascii art / -> \, etc.
    __reverse_map__ = (
        '\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
        '\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f'
        ' !"#$%&\')(*+,-.\\'
        '0123456789:;>=<?'
        '@ABCDEFGHIJKLMNO'
        'PQRSTUVWXYZ]/[^_'
        '`abcdefghijklmno'
        'pqrstuvwxyz}|{~\x7f'
        '\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f'
        '\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f'
        '\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf'
        '\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf'
        '\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf'
        '\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf'
        '\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef'
        '\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff')

    # translation map for flipping ascii art ^ -> v, etc.
    __flip_map__ = (
        '\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
        '\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f'
        ' !"#$%&\'()*+,-.\\'
        '0123456789:;<=>?'
        '@VBCDEFGHIJKLWNO'
        'bQbSTUAMXYZ[/]v-'
        '`aPcdefghijklwno'
        'pqrstu^mxyz{|}~\x7f'
        '\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f'
        '\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f'
        '\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf'
        '\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf'
        '\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf'
        '\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf'
        '\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef'
        '\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff')

    def reverse(self):
        out = []
        for row in self.splitlines():
            out.append(row.translate(self.__reverse_map__)[::-1])

        return self.newFromList(out)

    def flip(self):
        out = []
        for row in self.splitlines()[::-1]:
            out.append(row.translate(self.__flip_map__))

        return self.newFromList(out)

    def newFromList(self, list):
        return FigletString('\n'.join(list) + '\n')


class FigletRenderingEngine(object):
    """
    This class handles the rendering of a FigletFont,
    including smushing/kerning/justification/direction
    """

    def __init__(self, base=None):
        self.base = base

    def render(self, text):
        """
        Render an ASCII text string in figlet
        """
        builder = FigletBuilder(text,
                                self.base.Font,
                                self.base.direction,
                                self.base.width,
                                self.base.justify)

        while builder.isNotFinished():
            builder.addCharToProduct()
            builder.goToNextChar()

        return builder.returnProduct()


class FigletProduct(object):
    """
    This class stores the internal build part of
    the ascii output string
    """

    def __init__(self):
        self.queue = list()
        self.buffer_string = ""

    def append(self, buffer):
        self.queue.append(buffer)

    def getString(self):
        return FigletString(self.buffer_string)


class FigletBuilder(object):
    """
    Represent the internals of the build process
    """

    def __init__(self, text, font, direction, width, justify):

        self.text = list(map(ord, list(text)))
        self.direction = direction
        self.width = width
        self.font = font
        self.justify = justify

        self.iterator = 0
        self.maxSmush = 0
        self.newBlankRegistered = False

        self.curCharWidth = 0
        self.prevCharWidth = 0
        self.currentTotalWidth = 0

        self.blankMarkers = list()
        self.product = FigletProduct()
        self.buffer = ['' for i in range(self.font.height)]

        # constants.. lifted from figlet222
        self.SM_EQUAL = 1    # smush equal chars (not hardblanks)
        self.SM_LOWLINE = 2    # smush _ with any char in hierarchy
        self.SM_HIERARCHY = 4    # hierarchy: |, /\, [], {}, (), <>
        self.SM_PAIR = 8    # hierarchy: [ + ] -> |, { + } -> |, ( + ) -> |
        self.SM_BIGX = 16    # / + \ -> X, > + < -> X
        self.SM_HARDBLANK = 32    # hardblank + hardblank -> hardblank
        self.SM_KERN = 64
        self.SM_SMUSH = 128

    # builder interface

    def addCharToProduct(self):
        curChar = self.getCurChar()

        # if the character is a newline, we flush the buffer
        if self.text[self.iterator] == ord("\n"):
            self.blankMarkers.append(
                ([row for row in self.buffer], self.iterator))
            self.handleNewLine()
            return None

        if curChar is None:
            return
        if self.width < self.getCurWidth():
            raise CharNotPrinted("Width is not enough to print this character")
        self.curCharWidth = self.getCurWidth()
        self.maxSmush = self.currentSmushAmount(curChar)

        self.currentTotalWidth = len(
            self.buffer[0]) + self.curCharWidth - self.maxSmush

        if self.text[self.iterator] == ord(' '):
            self.blankMarkers.append(
                ([row for row in self.buffer], self.iterator))

        if self.text[self.iterator] == ord('\n'):
            self.blankMarkers.append(
                ([row for row in self.buffer], self.iterator))
            self.handleNewLine()

        if (self.currentTotalWidth >= self.width):
            self.handleNewLine()
        else:
            for row in range(0, self.font.height):
                self.addCurCharRowToBufferRow(curChar, row)

        self.prevCharWidth = self.curCharWidth

    def goToNextChar(self):
        self.iterator += 1

    def returnProduct(self):
        """
        Returns the output string created by formatProduct
        """
        if self.buffer[0] != '':
            self.flushLastBuffer()
        self.formatProduct()
        return self.product.getString()

    def isNotFinished(self):
        ret = self.iterator < len(self.text)
        return ret

    # private

    def flushLastBuffer(self):
        self.product.append(self.buffer)

    def formatProduct(self):
        """
        This create the output string representation from
        the internal representation of the product
        """
        string_acc = ''
        for buffer in self.product.queue:
            buffer = self.justifyString(self.justify, buffer)
            string_acc += self.replaceHardblanks(buffer)
        self.product.buffer_string = string_acc

    def getCharAt(self, i):
        if i < 0 or i >= len(list(self.text)):
            return None
        c = self.text[i]

        if c not in self.font.chars:
            return None
        else:
            return self.font.chars[c]

    def getCharWidthAt(self, i):
        if i < 0 or i >= len(self.text):
            return None
        c = self.text[i]
        if c not in self.font.chars:
            return None
        else:
            return self.font.width[c]

    def getCurChar(self):
        return self.getCharAt(self.iterator)

    def getCurWidth(self):
        return self.getCharWidthAt(self.iterator)

    def getLeftSmushedChar(self, i, addLeft):
        idx = len(addLeft) - self.maxSmush + i
        if idx >= 0 and idx < len(addLeft):
            left = addLeft[idx]
        else:
            left = ''
        return left, idx

    def currentSmushAmount(self, curChar):
        return self.smushAmount(self.buffer, curChar)

    def updateSmushedCharInLeftBuffer(self, addLeft, idx, smushed):
        l = list(addLeft)
        if idx < 0 or idx > len(l):
            return addLeft
        l[idx] = smushed
        addLeft = ''.join(l)
        return addLeft

    def smushRow(self, curChar, row):
        addLeft = self.buffer[row]
        addRight = curChar[row]

        if self.direction == 'right-to-left':
            addLeft, addRight = addRight, addLeft

        for i in range(0, self.maxSmush):
            left, idx = self.getLeftSmushedChar(i, addLeft)
            right = addRight[i]
            smushed = self.smushChars(left=left, right=right)
            addLeft = self.updateSmushedCharInLeftBuffer(addLeft, idx, smushed)
        return addLeft, addRight

    def addCurCharRowToBufferRow(self, curChar, row):
        addLeft, addRight = self.smushRow(curChar, row)
        self.buffer[row] = addLeft + addRight[self.maxSmush:]

    def cutBufferCommon(self):
        self.currentTotalWidth = len(self.buffer[0])
        self.buffer = ['' for i in range(self.font.height)]
        self.blankMarkers = list()
        self.prevCharWidth = 0
        curChar = self.getCurChar()
        if curChar is None:
            return
        self.maxSmush = self.currentSmushAmount(curChar)

    def cutBufferAtLastBlank(self, saved_buffer, saved_iterator):
        self.product.append(saved_buffer)
        self.iterator = saved_iterator
        self.cutBufferCommon()

    def cutBufferAtLastChar(self):
        self.product.append(self.buffer)
        self.iterator -= 1
        self.cutBufferCommon()

    def blankExist(self, last_blank):
        return last_blank != -1

    def getLastBlank(self):
        try:
            saved_buffer, saved_iterator = self.blankMarkers.pop()
        except IndexError:
            return -1, -1
        return (saved_buffer, saved_iterator)

    def handleNewLine(self):
        saved_buffer, saved_iterator = self.getLastBlank()
        if self.blankExist(saved_iterator):
            self.cutBufferAtLastBlank(saved_buffer, saved_iterator)
        else:
            self.cutBufferAtLastChar()

    def justifyString(self, justify, buffer):
        if justify == 'right':
            for row in range(0, self.font.height):
                buffer[row] = (
                    ' ' * (self.width - len(buffer[row]) - 1)
                ) + buffer[row]
        elif justify == 'center':
            for row in range(0, self.font.height):
                buffer[row] = (
                    ' ' * int((self.width - len(buffer[row])) / 2)
                ) + buffer[row]
        return buffer

    def replaceHardblanks(self, buffer):
        string = '\n'.join(buffer) + '\n'
        string = string.replace(self.font.hardBlank, ' ')
        return string

    def smushAmount(self, buffer=[], curChar=[]):
        """
        Calculate the amount of smushing we can do between this char and the
        last If this is the first char it will throw a series of exceptions
        which are caught and cause appropriate values to be set for later.

        This differs from C figlet which will just get bogus values from
        memory and then discard them after.
        """
        if (self.font.smushMode & (self.SM_SMUSH | self.SM_KERN)) == 0:
            return 0

        maxSmush = self.curCharWidth
        for row in range(0, self.font.height):
            lineLeft = buffer[row]
            lineRight = curChar[row]
            if self.direction == 'right-to-left':
                lineLeft, lineRight = lineRight, lineLeft

            linebd = len(lineLeft.rstrip()) - 1
            if linebd < 0:
                linebd = 0

            if linebd < len(lineLeft):
                ch1 = lineLeft[linebd]
            else:
                linebd = 0
                ch1 = ''

            charbd = len(lineRight) - len(lineRight.lstrip())
            if charbd < len(lineRight):
                ch2 = lineRight[charbd]
            else:
                charbd = len(lineRight)
                ch2 = ''

            amt = charbd + len(lineLeft) - 1 - linebd

            if ch1 == '' or ch1 == ' ':
                amt += 1
            elif (ch2 != ''
                    and self.smushChars(left=ch1, right=ch2) is not None):
                amt += 1

            if amt < maxSmush:
                maxSmush = amt

        return maxSmush

    def smushChars(self, left='', right=''):
        """
        Given 2 characters which represent the edges rendered figlet
        fonts where they would touch, see if they can be smushed together.
        Returns None if this cannot or should not be done.
        """
        if left.isspace() is True:
            return right
        if right.isspace() is True:
            return left

        # Disallows overlapping if previous or current char has a width of 1 or
        # zero
        if (self.prevCharWidth < 2) or (self.curCharWidth < 2):
            return

        # kerning only
        if (self.font.smushMode & self.SM_SMUSH) == 0:
            return

        # smushing by universal overlapping
        if (self.font.smushMode & 63) == 0:
            # Ensure preference to visiable characters.
            if left == self.font.hardBlank:
                return right
            if right == self.font.hardBlank:
                return left

            # Ensures that the dominant (foreground)
            # fig-character for overlapping is the latter in the
            # user's text, not necessarily the rightmost character.
            if self.direction == 'right-to-left':
                return left
            else:
                return right

        if self.font.smushMode & self.SM_HARDBLANK:
            if (left == self.font.hardBlank
                    and right == self.font.hardBlank):
                return left

        if (left == self.font.hardBlank
                or right == self.font.hardBlank):
            return

        if self.font.smushMode & self.SM_EQUAL:
            if left == right:
                return left

        smushes = ()

        if self.font.smushMode & self.SM_LOWLINE:
            smushes += (('_', r'|/\[]{}()<>'),)

        if self.font.smushMode & self.SM_HIERARCHY:
            smushes += (
                ('|', r'|/\[]{}()<>'),
                (r'\/', '[]{}()<>'),
                ('[]', '{}()<>'),
                ('{}', '()<>'),
                ('()', '<>'),
            )

        for a, b in smushes:
            if left in a and right in b:
                return right
            if right in a and left in b:
                return left

        if self.font.smushMode & self.SM_PAIR:
            for pair in [left+right, right+left]:
                if pair in ['[]', '{}', '()']:
                    return '|'

        if self.font.smushMode & self.SM_BIGX:
            if (left == '/') and (right == '\\'):
                return '|'
            if (right == '/') and (left == '\\'):
                return 'Y'
            if (left == '>') and (right == '<'):
                return 'X'
        return


class Figlet(object):
    """
    Main figlet class.
    """

    def __init__(self, font=DEFAULT_FONT, direction='auto', justify='auto',
                 width=80):
        self.font = font
        self._direction = direction
        self._justify = justify
        self.width = width
        self.setFont()
        self.engine = FigletRenderingEngine(base=self)

    def setFont(self, **kwargs):
        if 'font' in kwargs:
            self.font = kwargs['font']

        self.Font = FigletFont(font=self.font)

    def getDirection(self):
        if self._direction == 'auto':
            direction = self.Font.printDirection
            if direction == 0:
                return 'left-to-right'
            elif direction == 1:
                return 'right-to-left'
            else:
                return 'left-to-right'

        else:
            return self._direction

    direction = property(getDirection)

    def getJustify(self):
        if self._justify == 'auto':
            if self.direction == 'left-to-right':
                return 'left'
            elif self.direction == 'right-to-left':
                return 'right'

        else:
            return self._justify

    justify = property(getJustify)

    def renderText(self, text):
        # wrapper method to engine
        return self.engine.render(text)

    def getFonts(self):
        return self.Font.getFonts()


def color_to_ansi(color, isBackground):
    if not color:
        return ''

    if color.count(';') > 0 and color.count(';') != 2:
        raise InvalidColor(
            'Specified color \'{}\' not a valid color in R;G;B format')
    elif color.count(';') == 0 and color not in COLOR_CODES:
        raise InvalidColor(
            'Specified color \'{}\' not found in ANSI COLOR_CODES list'.format(color))

    if color in COLOR_CODES:
        ansiCode = COLOR_CODES[color]
        if isBackground:
            ansiCode += 10
    else:
        ansiCode = 48 if isBackground else 38
        ansiCode = '{};2;{}'.format(ansiCode, color)

    return '\033[{}m'.format(ansiCode)


def parse_color(color):
    foreground, _, background = color.partition(":")
    ansiForeground = color_to_ansi(foreground, isBackground=False)
    ansiBackground = color_to_ansi(background, isBackground=True)
    return ansiForeground + ansiBackground










































class color():
    # Light-Colors :

    Lightblack = '\u001b[30;1m'

    Lightred = '\u001b[31;1m'

    Lightgreen = '\u001b[32;1m'

    Lightyellow = '\u001b[33;1m'

    Lightblue = '\u001b[34;1m'

    Lightmagenta = '\u001b[35;1m'

    Lightcyan = '\u001b[36;1m'

    Lightwhite = '\u001b[37;1m'

    # Normal Colors :

    Black = '\u001b[30m'

    Red = '\u001b[31m'

    Green = '\u001b[32m'

    Yellow = '\u001b[33m'

    Blue = '\u001b[34m'

    Magenta = '\u001b[35m'

    Cyan = '\u001b[36m'

    White = '\u001b[37m'

    # RESETS ALL COLORS :

    Reset = '\u001b[0m'
    reset = '\u001b[0m'

    # Non-Capital colors :

    black = '\u001b[30m'

    red = '\u001b[31m'

    green = '\u001b[32m'

    yellow = '\u001b[33m'

    blue = '\u001b[34m'

    magenta = '\u001b[35m'

    cyan = '\u001b[36m'

    white = '\u001b[37m'

    # Non-Capital Light-colors :

    lightblack = '\u001b[30;1m'

    lightred = '\u001b[31;1m'

    lightgreen = '\u001b[32;1m'

    lightyellow = '\u001b[33;1m'

    lightblue = '\u001b[34;1m'

    lightmagenta = '\u001b[35;1m'

    lightcyan = '\u001b[36;1m'

    lightwhite = '\u001b[37;1m'


def countdown(text, num):
    for i in range(num):
        system('cls')
        print(text + f'...({num})')
        time.sleep(1)
        num = num - 1


def help():

    print("""


    __  __     __                
   / / / /__  / /___       _     
  / /_/ / _ \/ / __ \     (_)    
 / __  /  __/ / /_/ /    _       
/_/ /_/\___/_/ .___/    (_)      
            /_/                  



          
1. title() 		=		Changes title of the command prompt you're using.

2. fullscreen()		=		Changes the program or command program you're using to fullscreen.

3. clear()		=		Clear console/command prompt.

4. color		=		A class with alot of different colors to change the color of anything.

5. countdown()		=		It countdowns the specific amount of seconds you specify after the text you want to put.

6. size()		=		it changes width,height to the amount you specify.

7. pause()		=		Pauses console/cmd until you press any key. Useful to exit program.

7 (2). pause(True)	=		Pauses console/cmd and writes "Press any key to continue..." (recommended for exiting programs)

8. wait()       	= 		Waits amount of seconds you input(only works with integers, Use common sense.)

9. asciiprint()		=		It converts whatever you wrote in the brackets to ascii and then prints it.


======================     USAGE   ==========================================

1. title('Made by Objective!')

2. fullscreen()

3. clear()

4. color.red(or any color, There is a total of 16+ colors)	|| it will change the color of everything after this command to red unless you use color.reset

5. countdown('Program done', 3) 	                        || it will output as Program done...(3) and countdown from 3.

6. size(120,30)		                                        || 120,30 is the default size!!

7. pause()							|| it will freeze the command prompt until you press any key...

7 (2). pause(True)						|| it will do the same as pause() but will write "Press any key to continue..."

8. wait(3)							|| it will wait 3 seconds before executing the next line of code.

9. asciiprint('Made by Objective!')				|| it will print "Made by Objective!" as ascii art.





                                                    ˜”*°•.˜”*°• Press any key to exit. •°*”˜.•°*”˜
""")
    fullscreen()
    system('pause > nul')


def size(width, height):
    system(f'mode {width},{height}')


def pause(bool=False):
    if bool == False:
        system('pause>nul')
    elif bool == True:
        system('pause')


def wait(int):
    try:
        time.sleep(int)
    except:
        print(f'{color.red}Invalid number.{color.reset}')


def asciiprint(msg):
    print(figlet_format(msg))

