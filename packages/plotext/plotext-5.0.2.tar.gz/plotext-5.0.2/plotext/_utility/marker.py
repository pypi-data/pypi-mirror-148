from plotext._utility import join, memorize, transpose
from plotext._utility.platform import platform

##############################################
##########    Default Markers      ###########
##############################################

space = ' ' # the default null character that appears as background to all plots

plot_marker = "hd" if platform == 'unix' else 'dot'

marker_codes = {'sd'         :'█',
                'dot'        :'•',
                'dollar'     :'$',
                'euro'       :'€',
                'bitcoin'    :'฿',
                'at'         :'@',
                'heart'      :'♥',
                'smile'      :'☺',
                'gclef'      :'𝄞',
                'note'       :'𝅘𝅥',
                'shamrock'   :'☘',
                'atom'       :'⚛',
                'snowflake'  :'❄',
                'lightning'  :'🌩',
                'queen'      :'♕',
                'king'       :'♔',
                'cross'      :'♰',
                'yinyang'    :'☯',
                'om'         :'ॐ',
                'osiris'     :'𓂀',
                'zero'       :'🯰',
                'one'        :'🯱',
                'two'        :'🯲',
                'three'      :'🯳',
                'four'       :'🯴',
                'five'       :'🯵',
                'six'        :'🯶',
                'seven'      :'🯷',
                'eight'      :'🯸',
                'nine'       :'🯹'}

hd_symbols = {'hd'  : '▞',
              'fhd' : '🬗'} # the markers that represents the higher definition characters

hd_codes = {(0,0,0,0): ' ', (1,0,0,0): '▘', (0,0,1,0): '▖', (0,0,0,1): '▗', (0,1,0,0): '▝', (1,0,1,0): '▌', (0,1,0,1): '▐', (0,0,1,1): '▄', (1,1,0,0):    '▀', (1,0,0,1): '▚',  (0,1,1,0): '▞', (1,1,1,0): '▛', (1,0,1,1): '▙', (0,1,1,1): '▟', (1,1,0,1): '▜', (1,1,1,1): '█'} # codes for high definition markers used to easily sum them; eg: '▘' + '▗' = '▚'
hd_markers = {hd_codes[el] : el for el in hd_codes}

fhd_codes = {(0,0,0,0,0,0): ' ', (1,0,1,0,1,0):'▌', (0,1,0,1,0,1): '▐', (1,1,1,1,1,1): '█', (1,0,0,0,0,0):'🬀', (0,1,0,0,0,0):'🬁', (1,1,0,0,0,0):'🬂', (0,0,1,0,0,0):'🬃', (1,0,1,0,0,0):'🬄', (0,1,1,0,0,0):'🬅', (1,1,1,0,0,0):'🬆', (0,0,0,1,0,0):'🬇', (1,0,0,1,0,0):'🬈', (0,1,0,1,0,0):'🬉', (1,1,0,1,0,0):'🬊', (0,0,1,1,0,0):'🬋', (1,0,1,1,0,0):'🬌', (0,1,1,1,0,0):'🬍', (1,1,1,1,0,0):'🬎', (0,0,0,0,1,0):'🬏', (1,0,0,0,1,0):'🬐', (0,1,0,0,1,0):'🬑', (1,1,0,0,1,0):'🬒', (0,0,1,0,1,0):'🬓', (0,1,1,0,1,0):'🬔', (1,1,1,0,1,0):'🬕', (0,0,0,1,1,0):'🬖', (1,0,0,1,1,0):'🬗', (0,1,0,1,1,0):'🬘', (1,1,0,1,1,0):'🬙', (0,0,1,1,1,0):'🬚', (1,0,1,1,1,0):'🬛', (0,1,1,1,1,0):'🬜', (1,1,1,1,1,0):'🬝', (0,0,0,0,0,1):'🬞', (1,0,0,0,0,1):'🬟', (0,1,0,0,0,1):'🬠', (1,1,0,0,0,1):'🬡', (0,0,1,0,0,1):'🬢', (1,0,1,0,0,1):'🬣', (0,1,1,0,0,1):'🬤', (1,1,1,0,0,1):'🬥', (0,0,0,1,0,1):'🬦', (1,0,0,1,0,1):'🬧', (1,1,0,1,0,1):'🬨', (0,0,1,1,0,1):'🬩', (1,0,1,1,0,1):'🬪', (0,1,1,1,0,1):'🬫', (1,1,1,1,0,1):'🬬', (0,0,0,0,1,1):'🬭', (1,0,0,0,1,1):'🬮', (0,1,0,0,1,1):'🬯', (1,1,0,0,1,1):'🬰', (0,0,1,0,1,1):'🬱', (1,0,1,0,1,1):'🬲', (0,1,1,0,1,1):'🬳', (1,1,1,0,1,1):'🬴', (0,0,0,1,1,1):'🬵', (1,0,0,1,1,1):'🬶', (0,1,0,1,1,1):'🬷', (1,1,0,1,1,1):'🬸', (0,0,1,1,1,1):'🬹', (1,0,1,1,1,1):'🬺', (0,1,1,1,1,1):'🬻'} # codes for full high definition markers used to easily sum them; eg: '🬐' + '🬇' = '🬗'
fhd_markers = {fhd_codes[el] : el for el in fhd_codes}

@memorize
def get_hd_marker(code):
   return hd_codes[code] if code in hd_codes else fhd_codes[code]

def marker_factor(markers, hd, fhd): # usefull to improve the resolution of the canvas for higher resolution markers
   if 'fhd' in markers:
       return fhd
   elif 'hd' in markers:
       return hd
   else:
       return 1
