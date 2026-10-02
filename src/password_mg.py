import json
import sys
import os
from enum import Enum

class constants():
    META="meta"
    LOCK_FILE="LOCK_FILE"
    PASSWD_ENV_NAME="MA#TER_PA##WORD"
    PASSWD_FILE=os.environ.get("HOME")+"/.pa##word"

CONFIG = {
    constants.LOCK_FILE:False
}


def getpasswd():
    password=os.environ.get(constants.PASSWD_ENV_NAME)
    if password is None:
        raise(Exception("Password not given"))
    return password

def readfile():
    a=None
    with open(constants.PASSWD_FILE,"r") as fl:
        a=json.load(fl)

    if a is None:
        raise(Exception("error while reading file."))

    return a


class actions(Enum):
    GET_HINTS=("-q")
    GET_PASSWORD=("-g")
    PUT_PASSWORD=("-p")
    
    need_lock = lambda self: self in { actions.PUT_PASSWORD }
    need_password = lambda self: self in  { actions.GET_PASSWORD, actions.PUT_PASSWORD}
    def helper_wrapper(self,callback):
        password=None
        jsn=None
        
        if self.need_password():
            password=getpassword()
        
        if self.need_lock() and  CONFIG.get(constants.LOCK_FILE):
            pass
        jsn = readfile()

        callback(password, jsn)
        if self.need_lock() and  CONFIG.get(constants.LOCK_FILE):
            pass


    def do_stuff(self):
         match self:
            case actions.GET_HINTS:
                def get_hints(pwd,jsn):
                    meta  = jsn.get(constants.META).items()
                    for k, v in meta:
                        for V in v:
                            print(f"{k} -- {V}")
                self.helper_wrapper(get_hints)

            case actions.PUT_PASSWORD:
                print("getting password")
            case actions.GET_PASSWORD:
                print("getiing your password")
            



if __name__=='__main__':
    chosen=None
    if len(sys.argv)>1 :
        try:
            chosen=actions(sys.argv[1])
        except ValueError:
            pass
    else:
        raise(Exception("no action given"))

    if chosen is None:
        raise(Exception("invalid action given"))
    



    chosen.do_stuff()

    
    raise(Exception("MANUAL"))



   
    raw_jsonobj=None
    with open(constants.PASSWD_FILE) as f:
        raw_jsonobj= json.loads(f.read())
    
    





