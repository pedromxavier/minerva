#!/usr/bin/python3
""" Renova livros da biblioteca da UFRJ através do portal 'https://minerva.ufrj.br'.
"""
import urllib.request as url
from urllib.parse import urlencode, quote_plus

from random import random

import sys
import os
import pickle

def wrap_dir(callback):
    def new_callback(*args, **kwargs):
        cwd = os.getcwd()
        os.chdir(os.path.dirname(sys.argv[0]))

        try:
            ans = callback(*args, **kwargs)
        except Exception:
            os.chdir(cwd)
            raise
        finally:
            os.chdir(cwd)
            return ans

    return new_callback

def follow_link(link, key, sep):
    answer = url.urlopen(link)
    source = str(answer.read())
    data   = source.split(r'\n')

    new_link = str();
    for line in data:
        if key in line:
            new_link = line.split(sep)[1]
            break
        else:
            continue

    assert new_link

    return new_link
        
def _renew(user, pswd):
    URL         = "http://minerva.ufrj.br"
    SESSION_KEY = int(random() * 1_000_000_000)

    FORM        = urlencode({'func'            :'login-session',
                             'bor_id'          : user,
                             'bor_verification': pswd,
                             'bor_library'     :'UFR50',
                             'x'               :'0',
                             'y'               :'0'}, quote_via = quote_plus);

    KEYS        =  [('LOGIN-PAGE', '"'),
                    ('action="', '"'),
                    ('func=bor-info','"'),
                    ('func=bor-loan',"'"),
                    ('func=bor-renew-all&adm_library',"'"),
                    ('func=file&file_name=logout',"'"),
                    ('func=logout','"')];

    LINKS       = ["{}/F?RN={}".format(URL, SESSION_KEY)]
    
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
        with open('minerva.cache', 'rb') as file:
            return pickle.load(file)
    
    except FileNotFoundError:
        return set()
        
@wrap_dir
def renew_all():
    data = get_cache()

    if not data:
        print("Não há credenciais salvas para renovar.")
        return
    else:
        for user, pswd in data:
            main(user, pswd)

@wrap_dir
def add_cache(user, pswd):
    data = get_cache()

    data.add((user, pswd))

    with open('minerva.cache', 'wb') as file:
        pickle.dump(data, file)

def main(user, pswd, cache=False):
    if renew(user, pswd) and cache:
        add_cache(user, pswd)
    

if __name__ == '__main__':
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

    main(args.user, args.pswd, cache=args.cache)
