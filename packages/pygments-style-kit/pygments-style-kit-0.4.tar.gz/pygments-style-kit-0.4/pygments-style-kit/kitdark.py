from pygments.style import Style
from pygments.token import Text, Keyword, Name, Comment, String, Number, Name

class KitdarkStyle(Style):
    # kit color definitions
    kitgreen = '#009682'
    kitpalegreen = '#82be3c'
    kitblue = '#4664aa'
    kityellow = '#fae614'
    kitorange = '#dca01e'
    kitbrown = '#a08232'
    kitred = '#a01e28'
    kitlilac = '#a00078'
    kitcyanblue = '#50aae6'
    kitseablue = '#32508c'
    kitblack = '#000000'

    # custom color definitions
    customwhite = '#ffffff'
    customdarkgrey = '#111111'
    customlightgrey = '#bbbbbb'

    # style configuration
    background_color = customdarkgrey
    default_style = "bg:" + customdarkgrey + " " + customwhite

    styles = {
        Text: customwhite,
        Comment: customlightgrey,
        Comment.Multiline: kitgreen,
        Keyword: kitbrown,
        Name.Decorator: kityellow,
        String: kitpalegreen,
        Number: kitcyanblue,
        Name.Function: kitorange
    }
