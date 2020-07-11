""" Renova livros da biblioteca da UFRJ através do portal 'https://minerva.ufrj.br'.
"""
import urllib.request as url
from urllib.parse import urlencode, quote_plus
from random import random

import sys
import os
import pickle

def get_home():
    if os.name == 'posix': ## Linux, Mac
        SUDO_USER = os.getenv("SUDO_USER")
        if SUDO_USER is None:
            return os.path.expanduser('~')
        else:
            return os.path.expanduser(f"~{SUDO_USER}/")
    elif os.name == 'nt': ## Windows
        return os.path.expanduser('~')
    else:
        raise SystemError(f'Installation Failed for your OS: `{os.name}`')

HOME = get_home()
MINERVA_DIR = os.path.join(HOME, '.minerva')
MINERVA_FNAME = os.path.join(HOME, '.minerva', 'minerva.info')

def follow_link(link, key, sep):
    answer = url.urlopen(link)
    source = str(answer.read())
    data = source.split(r'\n')

    new_link = str()
    for line in data:
        if key in line:
            new_link = line.split(sep)[1]
            break
        else:
            continue

    assert new_link

    return new_link
        
def _renew(user, pswd):
    URL = "http://minerva.ufrj.br"

    SESSION_KEY = int(random() * 1_000_000_000)

    FORM = urlencode({
        'func'            :'login-session',
        'bor_id'          : user,
        'bor_verification': pswd,
        'bor_library'     :'UFR50',
        'x'               :'0',
        'y'               :'0'
        }, quote_via=quote_plus)

    KEYS = [
        ('LOGIN-PAGE', '"'),
        ('action="', '"'),
        ('func=bor-info','"'),
        ('func=bor-loan',"'"),
        ('func=bor-renew-all&adm_library',"'"),
        ('func=file&file_name=logout',"'"),
        ('func=logout','"')
        ]

    LINKS = ["{}/F?RN={}".format(URL, SESSION_KEY)]
    
    for KEY, SEP in KEYS[:2]:
        LINKS.append(follow_link(LINKS[-1], KEY, SEP))

    LINKS.append("{}?{}".format(LINKS[-1], FORM))

    for KEY,SEP in KEYS[2:]:
        LINKS.append(follow_link(LINKS[-1], KEY, SEP))

def renew(user, pswd):
    try:
        _renew(user, pswd)
        print("[{}] renovado com sucesso.".format(user))
        return True
    except:
        print("Falha ao renovar [{}]".format(user))
        return False

def get_cache():
    try:
        with open(MINERVA_FNAME, 'rb') as file:
            try:
                data = pickle.load(file)
                if type(data) is not set:
                    raise EOFError
                else:
                    return data
            except EOFError:
                return set()
    except FileNotFoundError:
        return set()
        
def renew_all():
    data = get_cache()

    if not data:
        print("Não há credenciais salvas para renovar.")
        return
    else:
        for user, pswd in data:
            renew(user, pswd)

def add_cache(user, pswd):
    data = get_cache()
    data.add((user, pswd))
    try:
        with open(MINERVA_FNAME, 'wb') as file:
            pickle.dump(data, file)
    except FileNotFoundError:
        os.mkdir(MINERVA_DIR)
        with open(MINERVA_FNAME, 'wb') as file:
            pickle.dump(data, file)

def renew_and_cache(user, pswd, cache=False):
    if renew(user, pswd) and cache:
        add_cache(user, pswd)
    
def main():
    import argparse as ap

    class RenewAll(ap.Action):
        def __init__(self, option_strings, dest=ap.SUPPRESS, default=ap.SUPPRESS, help=None):
            super(RenewAll, self).__init__(option_strings=option_strings, dest=dest, default=default, nargs=0, help=help)

        def __call__(self, parser, namespace, values, option_string=None):
            renew_all()
            parser.exit()

    parser = ap.ArgumentParser(description=__doc__)

    ## username
    user_help = "Nome de usuário."
    parser.add_argument('user', type=str, help=user_help)
    ## password
    pswd_help = "Senha."
    parser.add_argument('pswd', type=str, help=pswd_help)

    ##cache
    cache_help = "Salva as credenciais."
    parser.add_argument('-c', '--cache', action='store_true', help=cache_help)

    ##renew-all
    renew_all_help = "Renova os livros de todas as credenciais salvas."
    parser.add_argument('-r', '--renew-all', action=RenewAll, help=renew_all_help)
    
    args = parser.parse_args()

    renew_and_cache(args.user, args.pswd, cache=args.cache)

if __name__ == '__main__':
    main()