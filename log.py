'''
Provides standard output of definition execution

Created on Jun 3, 2016
:author: iitow
'''
from datetime import datetime
from pprint import pprint
import inspect
import json


class Message(object):
    '''
    Represents method of logging and tracing definitions as a decorator
    '''
    def __init__(self,
                 type='info',
                 msg=None,
                 entry=True,
                 returns=True):
        '''
        Constructor Message

        :param type: String, header | info | success | warning | fail | error
        :param msg: String, include an additional message
        :param entry: Boolean, print entry
        :param returns: Boolean, print returns
        '''
        self.type = type
        self.msg = msg
        self.entry = entry
        self.returns = returns

    def __call__(self, fn):
        '''
        passes function here
        '''
        decorator_self = self
        def inner(*args, **kwargs):
            '''
            introspection of function here
            '''
            msg = ''
            spec = inspect.getargspec(fn)
            module = inspect.getmodule(fn).__name__
            name_class = ''
            name_funct =  fn.__name__
            if 'self' in spec.args: # resolve class name
                cls = args[0].__class__
                name_class = cls.__name__
                path = "%s.%s.%s" % (module, name_class, name_funct)
            else: # resolve function only
                path = "%s.%s" % (module, name_funct)
            if self.msg is not None: # custom message format
                msg = '<%s>' % (str(self.msg))
            text = "[%s UTC] [%s] %s" % (str(datetime.now().strftime('%H:%M:%S')),
                                        path,
                                        msg)
            # print init into function
            if self.entry is True:
                print '\n' + msg_colors(text, self.type)
            funct = fn(*args, **kwargs)
            stamp = str(datetime.now().strftime('%H:%M:%S'))
            ret_tag = '[%s UTC] [%s] [return]:' % (stamp, path)
            # print return of function
            if isinstance(funct, dict): # format a dict
                if self.returns is True:
                    print msg_colors(ret_tag, self.type)
                    print msg_colors(json.dumps(funct, indent=2), self.type)
            else:
                if isinstance(funct, bool) and funct is True: # True is green
                    ret_str = '%s %s' % (ret_tag,
                                         msg_colors(funct,'success'))
                elif isinstance(funct, bool) and funct is False: # False is red
                    ret_str = '%s %s' % (ret_tag,
                                         msg_colors(funct,'fail'))
                else: # everything else is blue
                    ret_str = '%s %s' % (ret_tag,
                                         funct)
                if self.returns is True:
                    print msg_colors(ret_str, self.type) + '\n'
            return funct
        return inner


def header(text,pad=19):
    '''
    prints out at header 

    :param text: String
    :param pad: Int
    '''
    text_str = '\n\n'
    size = len(text)+4
    space = ''
    for i in range(1,pad+1):
        space = space + ' '
    line = '%s' % (space)
    for i in range(0,size):
        line = line+'#'
    text_str = text_str + line + "\n"
    text_str = text_str + '%s# %s #\n' % (space,text)
    text_str = text_str + line + '\n'
    return msg_colors(text_str, 'header')

def logo():
    return """
                                        ___    ,''''''.
                                    ,'''   '''''      `.
                                   ,'        _.         `._
                                  ,'       ,'              `''''.
                                 ,'    .-''`.    ,-'            `.
                                ,'    (        ,'                :
                              ,'     ,'           __,            `.
                        ,'''''     .' ;-.    ,  ,'  \             `''''.
                      ,'           `-(   `._(_,'     )_                `.
                     ,'         ,---. \ @ ;   \ @ _,'                   `.
                ,-'''         ,'      ,--'-    `;'                       `.
               ,'            ,'      (      `. ,'                          `.
               ;            ,'        \    _,','                            `.
              ,'            ;          `--'  ,'                              `.
             ,'             ;          __    (                    ,           `.
             ;              `____... ,`   `.                    ,'           ,'
             ;    ...----'''' )  _.-  ____,  `.                ,'    ,'    ,'
_....----''' '``      _..--'_.-:.-' .'        `.             ,''.   ,' `--'
              `' ... '' _.-'' .-'`-.:..___...--' `-._      ,-''   `-'
        _.--'       _.-'    .'   .' .'               `'''''
  __.-''        _.-'     .-'   .'  /
 '          _.-' .-'  .-'     /  .'
        _.-'  .-'  .-' .'  .'   /
    _.-'      .-'   .-'  .'   .'
_.-'       .-'    .'   .'    /
       _.-'    .-'   .'    .'
    .-'            .'
    """


def msg_colors(text, type):
    '''
    Types of terminal colors
    '''
    types = {'header': '\033[1m',
              'info': '\033[34m',
              'success': '\033[32m',
              'warning': '\033[33m',
              'fail': '\033[31m',
              'error': '\033[31m',
              'end': '\033[0m'}
    trans = types.get(type, 'info')
    text = trans+str(text)+types.get('end')
    return text
