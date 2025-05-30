#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
--- All Non-GUI Functions ---

    These functions are used by the GUI calls to perform the real work of the program

"""

def IsKey(Key):
    """Check if a key is valid. Keys should be a capital letter followed by a number."""
    try:
        return (len(Key) == 2 and 
                Key[0].isalpha() and Key[0].isupper() and 
                Key[1].isdigit() and 
                int(Key[1]) > 0)
    except (TypeError, IndexError, ValueError):
        return False

def NextKey(KeyList):
    """Generate the next key in sequence based on the list of existing keys."""
    if not KeyList:
        return "A1"

    # Get the last key
    LastKey = KeyList[-1]
    Letter = LastKey[0]
    Number = int(LastKey[1:])

    # If we've reached 9, move to the next letter
    if Number == 9:
        Letter = chr(ord(Letter) + 1)
        Number = 1
    else:
        Number += 1

    return f"{Letter}{Number}"

def ReplaceTemplate(TemplateFile, OutputFile, ReplaceDict):
    """Replace placeholders in a template file with values from a dictionary."""
    with open(TemplateFile, 'r', encoding='utf-8') as f:
        Template = f.read()

    for Key, Value in ReplaceDict.items():
        Template = Template.replace(f"{{{Key}}}", str(Value))

    with open(OutputFile, 'w', encoding='utf-8') as f:
        f.write(Template) 