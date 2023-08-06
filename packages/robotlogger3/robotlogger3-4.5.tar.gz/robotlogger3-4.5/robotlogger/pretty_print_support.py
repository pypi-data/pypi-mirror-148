from __future__ import absolute_import
import json
import ast
import re
import types
import inspect

def determine_if_object_needs_inspecting(object):
    if isinstance(object, (type, types.MethodType)):
        return 'Instance'
    if isinstance(object,(type,types.FunctionType)):
        return 'Function'
    if callable(object):
        return 'InstanceMethod'
    return False


def Inspected_Object_To_Easy_Read_Dict(object):
    returnDict = {}
    if determine_if_object_needs_inspecting(object) == 'Instance':
        returnDict[object.__class__.__name__] = {}
        members = inspect.getmembers(object)
        for k,v in members:
            if "__" not in k:
                returnDict[object.__class__.__name__][k] = Inspected_Object_To_Easy_Read_Dict(v)
    elif determine_if_object_needs_inspecting(object) == 'InstanceMethod':
        returnDict = {
            "func_name": object.func_name,
            "func_defaults": object.func_defaults,
                         }
    elif determine_if_object_needs_inspecting(object) == 'Function':
        returnDict = {"func_name": object.func_name,
                      "func_defaults": object.func_defaults,
                      }
    else:
        return object
    return returnDict

def pretty_message(item,IndentString):

    if not item:
        #this may look like redundant logic but google.protobuf.pyext._message.RepeatedCompositeContainer types cant be compared with NONE
        if item == None:
            message = "NONE"
            MESSAGES = pretty_string_only_message(message, IndentString)
        else:
            MESSAGES = [str(item)]
    else:

        item = Inspected_Object_To_Easy_Read_Dict(item)

        if isinstance(item, dict):
            MESSAGES = pretty_message_dictionary_item(item,IndentString)
        elif isinstance(item, tuple) or isinstance(item, list) or isinstance(item, set) :
            MESSAGES = []
            for i in item:
                    MESSAGES += pretty_message(i,IndentString)

        elif isinstance(item,str):
            MESSAGES = pretty_message_string_item(item,IndentString)
        elif isinstance(item, int):
            message = str(item)
            MESSAGES = pretty_message_string_item(message, IndentString)

        else:
            MESSAGES = pretty_string_only_message(str(item), IndentString)
    return MESSAGES

def pretty_message_dictionary_item(item,IndentString):
    MESSAGES = []
    try:
        message = json.dumps(item, sort_keys=True, indent=4, separators=(',', ': '))
        for line in message.split('\n'):
            MESSAGES.append(IndentString + line + '\n')
    except:
        message= str(item)
        MESSAGES.append(message)

    return MESSAGES

def pretty_string_only_message(item,IndentString):
    MESSAGES = []
    MESSAGES.append(IndentString + item)
    return MESSAGES

def pretty_message_string_item(item,IndentString):
    MESSAGES = []
    messages = splitDictionaries_in_string(item)
    for message in messages:
        if isinstance(message, str):
            MESSAGES += pretty_string_only_message(message, IndentString)
        elif isinstance(message,dict):
            MESSAGES += pretty_message_dictionary_item(message, IndentString)
        elif isinstance(message,int):
            MESSAGES += pretty_string_only_message(str(message), IndentString)
    return MESSAGES


def splitDictionaries_in_string(STRING):
    assert isinstance(STRING,str), 'this needs to be a string but is a %s' %type(STRING)
    DictLevel = 0
    splittingString = ''
    DictSplitList = []
    for v in STRING:
        if DictLevel == 0 and splittingString =='':
            # Starting string
            splittingString = v
            if v == '{':
                DictLevel = 1

        elif DictLevel == 0 and splittingString != '':
            # this is not the start of the string but no dictionary found yet
            if v == '{':
                DictLevel = 1
                DictSplitList.append(splittingString)
                splittingString = v
            else:
                splittingString += v


        elif DictLevel != 0:
            # you are currenly inside a dictionary
            splittingString += v
            if v == '{':
                DictLevel += 1
            if  v == '}':
                DictLevel -= 1
                if DictLevel == 0:
                    DictSplitList.append(splittingString)
                    splittingString = ''
    if splittingString != '':
        DictSplitList.append(splittingString)

    MESSAGES = []
    for dictionary in DictSplitList:
        try:
            MESSAGES.append(ast.literal_eval(dictionary))
        except:
            MESSAGES.append(dictionary)
    return MESSAGES



def re_split_l(s):
    se = r'(\[.*?\])'
    lists = re.findall(se, s)

    MESSAGES = []
    nowAt = 0
    for l in lists:
        st = s[nowAt:s.find(l)]
        if st != '' and st != ' ':
            MESSAGES.append(st)
        MESSAGES.append(l)
        nowAt = s.find(l) + len(l) + 1
    return MESSAGES

