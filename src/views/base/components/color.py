BACKGROUND_COLOR = '#1D0011'

IS_SELECTED_BG_RED = '#f53333'
IS_SELECTED_BG_BLUE = '#0594e3'
IS_SELECTED_BG_MURDERER = '#111111'
IS_SELECTED_BG_NEUTRAL = '#eaece1'

NO_ANSWER_BG = '#4d4d4d'

IS_NOT_SELECTED_BG_RED = '#4d1111'
IS_NOT_SELECTED_BG_BLUE = '#02344d'
IS_NOT_SELECTED_BG_MURDERER = '#262626'
IS_NOT_SELECTED_BG_NEUTRAL = '#4d4d4d'

IS_SELECTED_MURDERER_FG = '#ffffff'
IS_SELECTED_NOT_MURDERER_FG = '#000000'
NO_ANSWER_FG = '#000000'
IS_NOT_SELECTED_MURDERER_FG = '#999999'
IS_NOT_SELECTED_NOT_MURDERER_FG = '#000000'

FORM_BG = '#881247'
FORM_BG_ACCENT_COLOR = '#430027'
FORM_LABEL_FG = '#fff'


def get_color_by_team(team):
    return {
        'red': IS_SELECTED_BG_RED,
        'blue': IS_SELECTED_BG_BLUE,
    }.get(team)


def get_word_background_color(show_answers, word):
    if word['is_selected']:
        return {
            'red': IS_SELECTED_BG_RED,
            'blue': IS_SELECTED_BG_BLUE,
            'murderer': IS_SELECTED_BG_MURDERER
        }.get(word['team'], IS_SELECTED_BG_NEUTRAL)

    if not show_answers:
        return NO_ANSWER_BG

    return {
        'red': IS_NOT_SELECTED_BG_RED,
        'blue': IS_NOT_SELECTED_BG_BLUE,
        'murderer': IS_NOT_SELECTED_BG_MURDERER
    }.get(word['team'], IS_NOT_SELECTED_BG_NEUTRAL)


def get_word_foreground_color(show_answers, word):
    if word['is_selected']:
        return {
            'murderer': IS_SELECTED_MURDERER_FG
        }.get(word['team'], IS_SELECTED_NOT_MURDERER_FG)
    if not show_answers:
        return NO_ANSWER_FG

    return {
        'murderer': IS_NOT_SELECTED_MURDERER_FG
    }.get(word['team'], IS_NOT_SELECTED_NOT_MURDERER_FG)
