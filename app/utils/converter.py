import json
from flask import redirect, url_for
from classes.db_classes import BolasDoBingoJson


def converter_str_json(bolas_do_bingo_json) -> BolasDoBingoJson or redirect:
    try:
        if type(bolas_do_bingo_json) == str:
            bolas_do_bingo_json = \
                json.loads(bolas_do_bingo_json.replace("'", '"'))
    except Exception as e:
        print('Não conseguiu converter para Json. Erro: ', e)
        return redirect(url_for('bingo.index'))
    return bolas_do_bingo_json


def converter_str(df, coluna):
    df[coluna] = df[coluna].apply(str)
    return df
