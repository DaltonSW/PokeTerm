from termcolor import COLORS, colored

def GetBoldText(text) -> str:
    return colored(text, attrs=['bold'])

def GetStatFormatting(statName: str) -> (COLORS, str):
    outName = statName
    match statName:
        case 'hp':
            color = 'light_magenta'
            outName = 'HP'
        case 'attack':
            color = 'light_red'
            outName = 'Attack'
        case 'defense':
            color = 'light_yellow'
            outName = 'Defense'
        case 'special-attack':
            color = 'light_blue'
            outName = 'Sp. Attack'
        case 'special-defense':
            color = 'light_green'
            outName = 'Sp. Defense'
        case 'speed':
            color = 'light_cyan'
            outName = 'Speed'
        case 'accuracy':
            color = 'white'
            outName = 'Accuracy'
        case 'evasion':
            color = 'light_gray'
            outName = 'Evasion'
        case _:
            color = None      # color will be None if none of the cases match

    return color, outName


def GetMoveClassColor(moveClass: str) -> COLORS:
    color = None
    match moveClass:
        case 'physical':
            color = 'light_red'
        case 'special':
            color = 'light_magenta'
        case 'status', _:
            color = 'white'

    return color


def GetTypeColor(checkType: str) -> COLORS:
    color = None
    match checkType:
        case 'normal':
            color = 'white'
        case 'fire':
            color = 'red'
        case 'water':
            color = 'blue'
        case 'electric':
            color = 'yellow'
        case 'grass':
            color = 'green'
        case 'ice':
            color = 'light_cyan'
        case 'fighting':
            color = 'red'
        case 'poison':
            color = 'magenta'  # Using magenta as replacement for purple
        case 'ground':
            color = 'light_yellow'  # Using light yellow as replacement for brown
        case 'flying':
            color = 'light_blue'
        case 'psychic':
            color = 'magenta'  # Using magenta as replacement for light_purple
        case 'bug':
            color = 'light_green'
        case 'rock':
            color = 'dark_grey'  # Using dark gray as replacement for grey
        case 'ghost':
            color = 'dark_grey'
        case 'dragon':
            color = 'red'  # Using red as replacement for dark_red
        case 'dark':
            color = 'blue'  # Using blue as replacement for dark_blue
        case 'steel':
            color = 'light_grey'  # Using light gray as replacement for silver
        case 'fairy', _:
            color = 'light_red'  # Using light red as replacement for pink

    return color
