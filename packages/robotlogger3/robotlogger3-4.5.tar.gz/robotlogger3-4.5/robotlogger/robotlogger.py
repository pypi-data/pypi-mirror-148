from __future__ import absolute_import
import time
import os
from robot.libraries.BuiltIn import BuiltIn
from .pretty_print_support import *
import copy
import base64
import zlib


Global_Logging_List = []

class rlclass():
    def __init__(self):
        self.clear_messages()

    def add_failed_message(self,
                           message):
        self.messages[len(self.messages)]= {'type':'failed',
                                             'msg':message}
    def add_passed_message(self,
                           message):
        self.messages[len(self.messages)] = {'type': 'passed',
                                              'msg': message}

    def add_normal_message(self,
                           message):
        self.messages[len(self.messages)] = {'type': 'normal',
                                              'msg': message}
    def clear_messages(self):
        self.messages={}

    def log_if_fail(self,
                    *args,
                    **kwargs):
        MSG = construct_message(*args,
                                **kwargs)
        self.add_failed_message(MSG)
    def log_if_pass(self,
                    *args,
                    **kwargs):

        MSG = construct_message(*args,
                                **kwargs)
        self.add_passed_message(MSG)
    def log_always(self,
                   *args,
                   **kwargs):

        MSG = construct_message(*args,
                                **kwargs)
        self.add_normal_message(MSG)

    def log_pass(self):
        for i in range(len(self.messages.keys())):
            if self.messages[i].get('type') != 'failed':
                log_robot_message(self.messages[i].get('msg'))

    def log_fail(self):
        self.add_normal_message('failed method')
        for i in range(len(self.messages.keys())):
            if self.messages[i].get('type') != 'passed':
                log_robot_message(self.messages[i].get('msg'))



def set_Log_params(**kwargs):

    severity = kwargs.get('severity',1)

    Indent = kwargs.get('Indent') or os.getenv('INDENT_LOG') or 0

    logShowLevel = kwargs.get('logShowLevel') or os.getenv('LOGGING_LEVEL') or 'warning'


    if str(logShowLevel).lower() == 'debug':
        logShowLevel = 0
    elif str(logShowLevel).lower() == 'info':
        logShowLevel = 20
    elif str(logShowLevel).lower() == 'warning':
        logShowLevel = 30
    elif str(logShowLevel).lower() == 'error':
        logShowLevel = 40
    elif str(logShowLevel).lower() == 'critical':
        logShowLevel = 50
    else:
        logShowLevel = int(logShowLevel)



    return severity, Indent, logShowLevel

def log_global_pass():
    global Global_Logging_List
    for log in sorted(Global_Logging_List, key=lambda i: i['time_of_log']):
        dlp = int(os.getenv('DONT_LOG_PASSED',0))
        args = log.get('args', [])
        kwargs = log.get('kwargs', {})
        if not 'severity' in kwargs:
            kwargs['severity'] = 1
        severity = kwargs.get('severity')
        try:
            severity = int(severity)
        except ValueError:
            if isinstance(severity,str):
                if severity.lower() == 'info':
                    severity = 1
                elif severity.lower() == 'debug':
                    severity = 0
                else:
                    severity = 2
        if severity == 1 and dlp:
            kwargs['severity'] = 0
        elif isinstance(severity,int) and severity > 1:
            functionAncestry = log.get('function_ancestry')
            sarg = '->'.join(functionAncestry)
            args = [sarg]+list(args)
            #args = tuple(args)
        if kwargs.get('must_log'):
            kwargs['severity'] = 1

        kwargs['Indent'] = log.get('indent_of_log',0) *2
        log_robot_message(*args, forceLog=True, **kwargs)
    Global_Logging_List = []

def log_global_fail():
    global Global_Logging_List
    for log in sorted(Global_Logging_List, key=lambda i: i['time_of_log']):
        args = log.get('args', [])
        kwargs = log.get('kwargs', {})
        kwargs['Indent'] = log.get('indent_of_log', 0) * 3
        if kwargs.get('must_log'):
            kwargs['severity'] = 1

        log_robot_message(*args, forceLog=True, **kwargs)

    Global_Logging_List = []

def get_function_ancestry(stack_start=2,  #0 is the current method get_function_ancestry so ignore that, 1 is log_global_message
                          stack_end=-1):

    stack = inspect.stack()
    #0 is the current method get_function_ancestry so ignore that
    #-1 is modules so ignore that too
    ancestry_chain = stack[stack_start:-1]
    return [a[3] for a in ancestry_chain]


def log_global_message(*args, **kwargs):
    '''
        :param args: message content
        :param kwargs: severity,Indent,logginglevel
        :return:
        '''
    # setting all the variables
    # read all current pickle messages
    # Function_calling_log_pickle = whosdaddy()
    # print 'Function_calling_log_pickle', Function_calling_log_pickle
    global Global_Logging_List
    ancestry = get_function_ancestry()
    log_dict = {
        'time_of_log': time.time(),
        'indent_of_log': len(ancestry),
        'function_ancestry': ancestry,
        'must_log':kwargs.get('must_log',False),
        'args': args,
        'kwargs': kwargs
    }

    Global_Logging_List.append(log_dict)
    #print 'troubleshoot print at',time.time(), args



def construct_message(*args,
                      **kwargs):

    severity, Indent, logShowLevel = set_Log_params(**kwargs)
    Indent = ' ' * (int(Indent) + 1)


    MESSAGES = []
    for message in args:
        MESSAGES += pretty_message(message, Indent)

        #    MESSAGES += pretty_string_only_message(str(message))
    MSG = ' '.join(MESSAGES)

    return MSG

def log_robot_message(*args,
                      **kwargs):
    '''
    :param args: message content
    :param kwargs: severity,Indent,logginglevel
    :return:
    '''
    EncodeLarge=int(os.getenv('ENCODE_LARGE_LOGS',0))
    EncodeSize=int(os.getenv('LOG_SIZE_MAX',200))

    glboal = int(os.getenv('USE_GLOBAL_LOGGING',0))
    if not kwargs.get('forceLog'):
        if glboal:
            log_global_message(*args, **kwargs)
            return

    if kwargs.get('as_html'):
        html = True
    else:
        html = False
    if kwargs.get('as_repr'):
        repr = True
    else:
        repr = False

    MSG = construct_message(*args,
                            **kwargs)

    if EncodeLarge > 0 :
        if len(MSG) > EncodeSize:
            # print ('MSG BEGIN', len(MSG))
            message_bytes = MSG.encode('ascii')
            MSG = zlib.compress(message_bytes)
            # MSG = base64.b64encode(message_bytes)
            MSG = str(MSG)

            # print ('MSG END', len(MSG))

    severity, Indent, logShowLevel = set_Log_params(**kwargs)

    TURN_OFF_ROBOT_LOGGING = os.getenv('TURN_OFF_ROBOT_LOGGING',0)
    TURN_OFF_ROBOT_LOGGING = int(TURN_OFF_ROBOT_LOGGING)
    LOG_TO_FILE = os.getenv('LOG_TO_FILE')


    if LOG_TO_FILE:
        if not os.path.exists(LOG_TO_FILE):
            file = open(LOG_TO_FILE,'w')
        else:
            file = open(LOG_TO_FILE, 'a')


    if (severity == 0) or (str(severity).lower() == 'debug'):
        if logShowLevel <= 0:
            if LOG_TO_FILE:
                file.write(time.asctime() + ' DEBUG:  ' + MSG + '\n')
            else:
                if TURN_OFF_ROBOT_LOGGING:
                    print (time.asctime() + ' DEBUG:  ' + MSG)
                else:
                    BuiltIn().log(MSG,
                                  level='DEBUG',
                                  html=html,
                                  console=True,
                                  #repr=repr,
                                  )
        else:
            if LOG_TO_FILE:
                file.write(time.asctime() + ' DEBUG:  ' + MSG + '\n')
            else:
                #not going to print out this message
                # if TURN_OFF_ROBOT_LOGGING:
                #     print (time.asctime() + ' DEBUG:  ' + MSG)
                # else:
                BuiltIn().log(MSG,
                              level='DEBUG',
                              html=html,
                              #repr=repr,
                              console=False,
                              )
    elif (severity == 1) or (str(severity).lower() == 'info'):

        # logging.info(str(message))
        if logShowLevel <= 20:
            if LOG_TO_FILE:
                file.write(time.asctime() + ' INFO:  ' + MSG + '\n')
            else:
                if TURN_OFF_ROBOT_LOGGING:
                    print (time.asctime() + ' INFO:  ' + MSG)
                else:
                    BuiltIn().log(  # bcolors.OKBLUE +  MSG,
                        MSG,
                        level='INFO',
                        html=html,
                        #repr=repr,
                        console=True,
                    )
        else:
            if LOG_TO_FILE:
                file.write(time.asctime() + ' INFO:  ' + MSG + '\n')
            else:
                # not going to print out this message
                # if TURN_OFF_ROBOT_LOGGING:
                #     print (time.asctime() + ' INFO:  ' + MSG)
                # else:
                BuiltIn().log(MSG,
                              level='INFO',
                              html=html,
                              #repr=repr,
                              console=False,
                              )

    elif (severity == 2) or (str(severity).lower() == 'warning'):
        if logShowLevel <= 30:
            if LOG_TO_FILE:
                file.write(time.asctime() + ' WARN:  ' + MSG + '\n')
            else:

                if TURN_OFF_ROBOT_LOGGING:
                    print (time.asctime() + ' WARN:  ' + MSG)
                else:
                    BuiltIn().log(  # bcolors.WARNING + MSG,
                        MSG,
                        level='WARN',
                        html=html,
                        #repr=repr,
                        console=True,
                    )
        else:
            if LOG_TO_FILE:
                file.write(time.asctime() + ' WARN:  ' + MSG + '\n')
            else:

                if TURN_OFF_ROBOT_LOGGING:
                    print (time.asctime() + ' WARN:  ' + MSG)
                else:
                    BuiltIn().log(MSG,
                                  level='WARN',
                                  html=html,
                                  #repr=repr,
                                  console=False,
                                  )
    elif (severity == 3) or (str(severity).lower() == 'error'):
        if logShowLevel <= 40:
            if LOG_TO_FILE:
                file.write(time.asctime() + ' ERROR:  ' + MSG + '\n')
            else:

                if TURN_OFF_ROBOT_LOGGING:
                    print (time.asctime() + ' ERROR:  ' + MSG)
                else:
                    BuiltIn().log(  # bcolors.FAIL + '[ERROR]:' + MSG,
                        '[ERROR]:' + MSG,
                        level='WARN',
                        html=html,
                        #repr=repr,
                        console=True,
                    )
        else:
            if LOG_TO_FILE:
                file.write(time.asctime() + ' ERROR:  ' + MSG + '\n')
            else:

                if TURN_OFF_ROBOT_LOGGING:
                    print (time.asctime() + ' ERROR:  ' + MSG)
                else:
                    BuiltIn().log('[ERROR]:' + MSG,
                              level='WARN',
                              html=html,
                              #repr=repr,
                              console=False,
                              )
    elif (severity == 4) or (str(severity).lower() == 'critical'):
        # logging.critical(str(message))
        if logShowLevel <= 50:
            if LOG_TO_FILE:
                file.write(time.asctime() + ' CRITICAL:  ' + MSG + '\n')
            else:

                if TURN_OFF_ROBOT_LOGGING:
                    print (time.asctime() + ' CRITICAL:  ' + MSG)
                else:
                    BuiltIn().log(  # bcolors.FAIL + '[CRITICAL]:' + MSG,
                        '[CRITICAL]:' + MSG,
                        level='WARN',
                        html=html,
                        console=True,
                )
        else:
            if LOG_TO_FILE:
                file.write(time.asctime() + ' CRITICAL:  ' + MSG + '\n')
            else:

                if TURN_OFF_ROBOT_LOGGING:
                    print (time.asctime() + ' CRITICAL:  ' + MSG)
                else:
                    BuiltIn().log('[CRITICAL]:' + MSG,
                              level='WARN',
                              html=html,
                              console=False,
                              )


if __name__ == '__main__':

    os.environ['LOGGING_LEVEL'] = '0'
