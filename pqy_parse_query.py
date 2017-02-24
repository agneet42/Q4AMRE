

import os
import re


# Some tests of the parser


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
   

    return final_bracketed_parse



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




def pqy_tokenise( string ):

#    splitter = re.compile(r'([() ])')
    splitter = re.compile(r'([()\n ])')
    raw_tokens = splitter.split( string )
    not_wanted = [ '', ' ', '\n' ]
    processed_tokens = [ p for p in raw_tokens if p not in not_wanted ]
   
    return processed_tokens

