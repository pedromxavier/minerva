#!/usr/bin/python3

import urllib.request as url
from urllib.parse import urlencode, quote_plus

import sys

from random import random

ARGC = len(sys.argv)
ARGV = sys.argv

def HyperLink(link, key, sep):
    "___READ___"
    answer = url.urlopen(link);
    source = str(answer.read());
    data   = source.split(r'\n');

    "____SEEK____"
    new_link = str();
    for line in data:
        if key in line:
            new_link = line.split(sep)[1];
            break;
        else:
            continue;
    assert new_link;

    return new_link;
        
def main(usr, psw):
    "___SCRIPT___"
    URL         = "http://minerva.ufrj.br";
    SESSION_KEY = int(random()*(10**9));

    FORM        = urlencode({'func'            :'login-session',
                             'bor_id'          : usr,
                             'bor_verification': psw,
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

    LINKS       = ["{}/F?RN={}".format(URL, SESSION_KEY)];
    
    j=0;
    for KEY, SEP in KEYS[:2]:
        LINKS.append(HyperLink(LINKS[j], KEY, SEP));
        j+=1;

    LINKS.append("{}?{}".format(LINKS[j], FORM));
    j+=1;

    for KEY,SEP in KEYS[2:]:
        LINKS.append(HyperLink(LINKS[j], KEY, SEP));
        j+=1;
    return 0;
    "__END__"

if __name__ == '__main__':
    if ARGC == 1:
        print("usr psw missing.")
    elif ARGC == 2:
        print("psw missing.")
    elif ARGC == 3:
        usr, psw = ARGV[1:]
        status = main(usr, psw)
        sys.exit(status)
    else:
        print("Too much args, expected 2 (usr psw)")

    sys.exit(1)
		
    
