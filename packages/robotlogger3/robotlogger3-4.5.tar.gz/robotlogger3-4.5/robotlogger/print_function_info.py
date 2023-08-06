from __future__ import absolute_import
import traceback
import os
from robotlogger.robotlogger import *
from robotlogger.robotlogger import rlclass

#Global_Logging_List = []


def print_function_info2(func):
    def call(*args, **kwargs):
        rlc = rlclass()
        os.environ['CURRENT_FUNCTION'] = func.__name__
        current_intent_log = os.getenv('INDENT_LOG') or 0

        st = formatFunctionStringNew(rlc,func, *args, **kwargs)
        # add indent for loging before running script
        os.environ['INDENT_LOG'] = str(int(current_intent_log) + 5)
        try:
            result = func(*args, rlc=rlc,  **kwargs)
            os.environ['INDENT_LOG'] = str(int(os.environ['INDENT_LOG']) - 5)
            rlc.log_pass()
        except Exception as error:
            os.environ['INDENT_LOG'] = str(int(os.environ['INDENT_LOG']) - 5)
            tracebackString = traceback.format_exc()
            rlc.log_fail()
            raise Exception('error in function %s: %s' %(func.__name__,tracebackString))
        #GetFinishTime(func, st)
        GetFinishTimeNew(rlc, func, st)
        return result

    return call


def print_function_info(func):
    def call(*args, **kwargs):
        global_logging = int(os.getenv('USE_GLOBAL_LOGGING',0))
        if global_logging:
            try:

                log_robot_message('########## %s Starting ###########' %func.__name__)
                #log_robot_message('########## %s Starting ###########' %func.__name__,must_log=True)
                result = func(*args, **kwargs)
                #log_robot_message('########## %s Finished ###########' % func.__name__,must_log=True)
                log_robot_message('########## %s Finished ###########'%func.__name__)
                log_global_pass()


            except Exception as error:
                tracebackString = traceback.format_exc()
                log_robot_message('error in function %s: %s' % (func.__name__, tracebackString))
                log_global_fail()
                raise
                #raise
                # return None

            return result

        else:
            rlc = rlclass()
            os.environ['CURRENT_FUNCTION'] = func.__name__
            current_intent_log = os.getenv('INDENT_LOG') or 0

            st = formatFunctionString(func, *args, **kwargs)
            # add indent for loging before running script
            os.environ['INDENT_LOG'] = str(int(current_intent_log) + 5)
            try:
                result = func(*args,  **kwargs)
                os.environ['INDENT_LOG'] = str(int(os.environ['INDENT_LOG']) - 5)
                rlc.log_pass()
            except Exception as error:
                os.environ['INDENT_LOG'] = str(int(os.environ['INDENT_LOG']) - 5)
                tracebackString = traceback.format_exc()
                rlc.log_fail()
                log_robot_message('error in function %s: %s' %(func.__name__,tracebackString))
                raise
                #raise Exception('error in function %s: %s' %(func.__name__,tracebackString))
            GetFinishTime(func, st)
            return result

    return call

def GetFinishTime(f, st):
    et = time.time()
    if not os.getenv('DONT_PRINT_FUNC_INFO'):
        log_robot_message('============>finished executing %s. took %s seconds to complete function<====================' % (f.__name__, str(et - st)))

def GetFinishTimeNew(rlc, f, st):
    et = time.time()
    if not os.getenv('DONT_PRINT_FUNC_INFO'):
        rlc.log_always('============>finished executing %s. took %s seconds to complete function<====================' % (f.__name__, str(et - st)))

def formatFunctionStringNew(rlc, f,*args, **kwargs):
    formfunctionstring = '%s (' % f.__name__
    LogArgs = os.getenv('PF_LOG_ARGS') or kwargs.get('PF_LOG_ARGS') or False
    if LogArgs:
        LogArgs=int(LogArgs)


    formfunctionstring = '%s (' % f.__name__
    LogArgs = os.getenv('PF_LOG_ARGS') or False
    if LogArgs:
        LogArgs = int(LogArgs)

    if LogArgs:
        if args:
            for i in range(1, len(args)):
                try:
                    if len(args[i]) > 20:
                        formfunctionstring += '%s=%s...,' % (f.func_code.co_varnames[i], args[i][:20])
                    else:
                        formfunctionstring += '%s=%s,' % (f.func_code.co_varnames[i], args[i])
                        # Log('  function arg %s=%s' % (f.func_code.co_varnames[i], args[i]))
                except:
                    pass
        if kwargs:
            for k, v in kwargs.iteritems():
                formfunctionstring += '%s=%s,' % (k, v)
                # Log('  function kw %s=%s' % (k, v))

    try:
        formfunctionstring = formfunctionstring[:-1] + ')'
    except:
        formfunctionstring = formfunctionstring + ')'
    if not os.getenv('DONT_PRINT_FUNC_INFO'):
        rlc.log_always('============>Executing method %s<===========================' % formfunctionstring)
    st = time.time()
    # return start time
    return st

def formatFunctionString(f,*args, **kwargs):
    formfunctionstring = '%s (' % f.__name__
    LogArgs = os.getenv('PF_LOG_ARGS') or kwargs.get('PF_LOG_ARGS') or False
    if LogArgs:
        LogArgs=int(LogArgs)


    formfunctionstring = '%s (' % f.__name__
    LogArgs = os.getenv('PF_LOG_ARGS') or False
    if LogArgs:
        LogArgs = int(LogArgs)

    if LogArgs:
        if args:
            for i in range(1, len(args)):
                try:
                    if len(args[i]) > 20:
                        formfunctionstring += '%s=%s...,' % (f.func_code.co_varnames[i], args[i][:20])
                    else:
                        formfunctionstring += '%s=%s,' % (f.func_code.co_varnames[i], args[i])
                        # Log('  function arg %s=%s' % (f.func_code.co_varnames[i], args[i]))
                except:
                    pass
        if kwargs:
            for k, v in kwargs.iteritems():
                formfunctionstring += '%s=%s,' % (k, v)
                # Log('  function kw %s=%s' % (k, v))

    try:
        formfunctionstring = formfunctionstring[:-1] + ')'
    except:
        formfunctionstring = formfunctionstring + ')'
    if not os.getenv('DONT_PRINT_FUNC_INFO'):
        log_robot_message('============>Executing method %s<===========================' % formfunctionstring)
    st = time.time()
    # return start time
    return st


@print_function_info
def success_case():
    from time import sleep
    sleep(1)

@print_function_info
def fail_case():
    assert 1==2, '1!-2'

@print_function_info
def add_some_strings_together(str1, str2=None, str3=None, **kwargs):


    rlc = kwargs.get('rlc')

    rlc.log_if_pass('log if pass 1')
    rlc.log_if_pass('log if pass 2')
    rlc.log_if_pass('log if pass 3')
    rlc.log_if_fail('log if fail 1')
    rlc.log_if_fail('log if fail 2')
    rlc.log_if_fail('log if fail 3')


    combined_strings = ' '.join([str1,str2,str3])
    rlc.log_if_pass('combined strings: %s' %combined_strings)

if __name__ == '__main__':
    os.environ['LOGGING_LEVEL'] = '0'

    log_robot_message(False)
