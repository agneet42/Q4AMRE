#******************************************************************************

#                            pqy_parse_query.py

#         Very basic command line interface to the Stanford Parser

#                See instructions at the bottom of the file.

#******************************************************************************

import os
import re

#------------------------------------------------------------------------------
#
# Some tests of the parser
# 

def pqy_test():

    queries = [
        'passage in common time',
        'interval of a melodic sixth',
        'second',
        'C followed by Eb',
        'C followed by Eb in the bass clef',
        'semiquaver E natural',
        'sixteenth note E natural',
        'harmonic interval of a minor third',
        'minor third',
        'dotted quaver',
        'dotted eighth note',
        'harmonic perfect fifth',
        'simultaneous harmonic perfect fifth and harmonic eleventh' ]

    for query in queries:

        parse = pqy_parse_query( query )
        print( query )
        print( parse )
        print( '\n' )

#------------------------------------------------------------------------------
#
# Takes as input a bracketed parse tree as a string, as returned by the
# Stanford Parser:
#
# (ROOT
#   (NP (CD two) (NN semiquavers)))
#
# Tokenises to produce a list of strings:
#
# [ '(', 'ROOT', '(', 'NP', '(', 'CD', 'two', ')',
#   '(', 'NN', 'semiquavers', ')', ')', ')']
#
# Converts to a bracketed form and returns:
#
# [ 'ROOT', [ 'NP', [ 'CD', 'two' ], [ 'NN', 'semiquavers' ] ] ]

def pqy_parse_query( query_string ):

    if query_string == '': return []

    query_file = open( 'query.txt', 'w' )
    query_file.write( query_string )
    query_file.write( '\n' )
    query_file.close()

    print( 'About to parse query with Stanford Parser...' )
    os.popen( 'c:\stanford_parser\stanford-parser-2008-10-26\lexparser.bat query.txt > parse.txt' )
    print( 'Parsing has finished' )

    parse_file = open( 'parse.txt', 'r' )
    parse_string = parse_file.read()
    parse_file.close()

    tokenised_parse_string = pqy_tokenise( parse_string )
    bracketed_parse = pqy_bracket2( tokenised_parse_string )
    # First pqy_bracket() does not handle ( ( ) ( ) ). Second one does...

    if len( bracketed_parse ) > 0: final_bracketed_parse = bracketed_parse[ 0 ]
    else: final_bracketed_parse = bracketed_parse
    # There seems to be an extra pair of brackets on the answer, except null
    # answers.

    # print( tokenised_parse_string )
    # print( final_bracketed_parse )

    return final_bracketed_parse

#------------------------------------------------------------------------------
#
# Takes as input a tokenised parse from the Stanford Parser and produces as
# output a bracketed parse.
#
# Uses code from:
# http://stackoverflow.com/questions/17140850/how-to-parse-a-string-and-
# return-a-nested-array

def pqy_bracket( s ):
    def pqy_bracket_helper( level = 0 ):
        try:
            token = next( tokens )
        except StopIteration:
            if level != 0:
                raise Exception( 'missing closing paren' )
            else:
                return []
        if token == ')':
            if level == 0:
                raise Exception( 'missing opening paren' )
            else:
                return []
        elif token == '(':
            return [ pqy_bracket_helper( level + 1 ) ]
            + pqy_bracket_helper( level )
        else:
            return [ token ] + pqy_bracket_helper( level )
    tokens = iter( s )
    return pqy_bracket_helper()


#------------------------------------------------------------------------------
#
# Takes as input a tokenised parse from the Stanford Parser and produces as
# output a bracketed parse.
#
# Uses code from:
# http://stackoverflow.com/questions/17140850/how-to-parse-a-string-and-
# return-a-nested-array
# This one appears to work as we wish here!

def pqy_bracket2(xs):
    stack = [[]]
    for x in xs:
        if x == '(':
            stack[-1].append([])
            stack.append(stack[-1][-1])
        elif x == ')':
            stack.pop()
            if not stack:
                return 'error: opening bracket is missing'
                #raise ValueError('error: opening bracket is missing')
        else:
            stack[-1].append(x)
    if len(stack) > 1:
        return 'error: closing bracket is missing'
        #raise ValueError('error: closing bracket is missing')
    return stack.pop()



#------------------------------------------------------------------------------
#
# 
# Input is a string, namely a parse tree in bracketed form. Tokenises it.

def pqy_tokenise( string ):

#    splitter = re.compile(r'([() ])')
    splitter = re.compile(r'([()\n ])')
    raw_tokens = splitter.split( string )
    not_wanted = [ '', ' ', '\n' ]
    processed_tokens = [ p for p in raw_tokens if p not in not_wanted ]
    # This line is removing ' and ' ' from the list. Not nice at all; there
    # must be a way to change the regular expression to do this.
    return processed_tokens

#------------------------------------------------------------------------------

#                        INSTRUCTIONS FOR USE ON WINDOWS

# This is an extremely basic interface to the Stanford Parser. This parser is
# very well reputed and frequently used for all NLP tasks. It generally gives
# very good results and there is a large literature on its application.
# However, it may for all manner of reasons give unexpected results in the
# C@merata task due to the need for customisation in respect of tokenisation,
# capitalisation, terminology and so on.
#
# The way in which this interface works is as follows. It uses the command line
# interface to the parser where you can do something like this:
#
# c:\stanford_parser\stanford-parser-2008-10-26\lexparser.bat input.txt > output.txt
#

# lexparser.bat is a standard Windows shell script (bat file) which comes with
# the parser. It just runs the parser with some standard arguments. input.tex
# is a text file in the current directory which contains one or more sentences
# to be parsed, one per line. output.txt is a text file to which the parser
# writes the output.
# 
# An adapted copy of lexparser.bat is in this directory. There are some
# comments added in there which might be worth glancing at.
# 
# The first step is to obtain the Stanford Parser e.g. v3.3.1 from
# http://nlp.stanford.edu/software/lex-parser.shtml
# 
# Unpack the files to a suitable directory. e.g. it could be
# C:\stanford-parser-full-2014-01-04
# 
# Check you have java 1.6
# 
# Update lexparser.bat in the stanford parser directory you have chosen as
# above so that it uses absolute paths - see the example lexparser.bat included
# with this program for hints about how to do this.
# 
# Verify this works at the command line by calling lexparser.bat with one
# argument which is a text file containing something to be parsed.  e.g. if you
# have a file query.txt in the current directory you can do: lexparser.bat
# query.txt
# 
# In the code above for function pqy_parse_query you will see
# 
# os.popen( 'c:\stanford_parser\stanford-parser-2008-10-26\lexparser.bat
# query.txt > parse.txt' )
# 
# You will need to change this to make it the absolute path of lexparser in
# your stanford parser directory.
# 
# After that you should be able to use pqy_parse_query/1 in python.
#
#
