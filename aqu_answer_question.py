#******************************************************************************

#                         aqu_answer_question.py

#    Code for answering a question, given a music_file and divisions value

# NB This code is just to show proof of concept - it will not answer any
# questions correctly.

#******************************************************************************

import pqy_parse_query
import typ_question_type
import music21
from itertools import groupby

#------------------------------------------------------------------------------
#
# Answers question question_text using  music_file and specifying answers
# using the specified divisions which is an integer.
# The format of the answer is like this:
# [ { 'start_beats' : '4', 'start_beat_type' : '4',
#     'end_beats' : '4', 'end_beat_type' : '4',
#     'start_divisions' : '4', 'end_divisions' : '4',
#     'start_bar' : '2', 'start_offset' : '1',
#     'end_bar' : '2', 'end_offset' : '4' }, ... ]

def aqu_answer_question( question_text, music_file, divisions ):

    tokens = pqy_parse_query.pqy_tokenise( question_text )

    # UNCOMMENT THE FOLLOWING LINE TO USE STANFORD PARSER
    # parse = pqy_parse_query.pqy_parse_query( question_text )
    parse = []
    # DELETE THE LINE parse = [] TO USE STANFORD PARSER

    type = typ_question_type.typ_question_type( tokens, parse )
    print( 'type is: ' + type )
    score = music21.converter.parse( music_file )
    index = aqu_create_index( score )
    time_signature = aqu_find_time_signature( score )

    answer_list = aqu_obtain_answers(
                      tokens, parse, type, index, divisions, time_signature )

    answer_list2 = [ k for k, g in groupby( sorted( answer_list ) ) ]
    # http://stackoverflow.com/questions/11261493/
    # python-fast-way-to-remove-duplicates-in-this-list

    # This last step removes duplicate answers. This can occur for example if
    # we ask for 'semibreve' and these are played at the same time in different
    # parts - the part_no is not included in the answer according to the
    # C@merata 14 specification.


    return answer_list2

#------------------------------------------------------------------------------
#
# This is just for testing. It returns an arbitrary but valid answer list so
# that write functions etc can be tested.

def aqu_answer_question2( question_text, music_file, divisions ):

    print( 'question_text:' + question_text +
           ' music_file:' + music_file )

    print( 'testing' )

    answer_list = [

        { 'start_beats' : '4', 'start_beat_type' : '4',
          'end_beats' : '4', 'end_beat_type' : '4',
          'start_divisions' : '4', 'end_divisions' : '4',
          'start_bar' : '2', 'start_offset' : '1',
          'end_bar' : '2', 'end_offset' : '4' },
    
        { 'start_beats' : '4', 'start_beat_type' : '4',
          'end_beats' : '4', 'end_beat_type' : '4',
          'start_divisions' : '4', 'end_divisions' : '4',
          'start_bar' : '7', 'start_offset' : '5',
          'end_bar' : '7', 'end_offset' : '8' } ] 
          # Note that values must all be strings incl numbers.

    return answer_list

#------------------------------------------------------------------------------
#
# Create a basic index for the score. This consists of a list of dictionaries,
# one per note in the score. Thus we can conveniently look up a note which has
# certain properties as required by a question. To do this we can use a
# comprehension as follows:
# [ note for note in index if some_property( note )
# [note for note in [['1'],['2'],['3']] if note[0] == '2' ]
# [ note for note in ans if note['octave']==4 ]
# assuming ans is the index
#
# Important ASSUMPTIONS
# A score has .parts
# There are zero or more parts
# Each part contains one or more bars plus other things
# Each bar can contain notes, chords, voices and other things
# A chord contains zero or more notes
# A voice contains notes, chords and other things
#
# There may be other possibilities as yet undiscovered. This may lead to notes
# not being put in the score.

def aqu_create_index( score ):

    parts = score.parts
    index = []

    for part_no in range( 0, len( parts ) ):

        print( 'part:' + str( part_no ) )
        part = parts[ part_no ]

        for bit_no in range( 0, len( part ) ):

            possible_bar = part[ bit_no ]
            # print( 'bit:' + str( possible_bar ) )
            if 'Measure' in possible_bar.classes:

                # print( 'Is a bar!' )
                index = index + aqu_get_data_from_bar( possible_bar, part_no )
                # print( 'index:' + str( index ) )

    return index

#------------------------------------------------------------------------------
#
# Argument bar is guaranteed to be a bar (measure) in the score. We extract
# info from it and return a list containing two or more data lists.
# A bar can contain a stream with Notes or Chords in it. It can also contain a
# Voice which may further contain Notes or Chords.

def aqu_get_data_from_bar( bar, part_no ):

    ans = []

    for elem_no in range( 0, len( bar ) ):

        elem = bar[ elem_no ]
        class_list = elem.classes
        # print( 'class:', str( class_list ) )

        if 'Note' in class_list:
            ans = ans + aqu_get_data_from_note( elem, part_no )
        elif 'Chord' in class_list:
            ans = ans + aqu_get_data_from_chord( elem, part_no )
        elif 'Voice' in class_list:
            ans = ans + aqu_get_data_from_bar( elem, part_no )
            # Not picking up the voice number at present
            # We could do that by altering aqu_get_date_from_bar
            # To pick up the voice if it exists.

        # For other elems e.g. clef, time signature etc return nothing.

    return( ans )

#------------------------------------------------------------------------------
#
# Extracts info from note and returns it as a list containing one data list.

def aqu_get_data_from_note( elem, part_no ):

    note_name = elem.name
    note_letter = ''; accidental = ''
    [ note_letter, accidental ] = aqu_note_letter_and_accidental( note_name )

    note_pitch_class = elem.pitchClass
    note_octave = elem.octave

    note_bar = elem.measureNumber
    note_offset = elem.offset
    note_length = elem.duration.quarterLength

    return [ { 'name':note_name, 'letter':note_letter, 'accidental':accidental,
               'pitch_class':note_pitch_class, 'octave':note_octave,
               'bar':note_bar, 'offset':note_offset, 'length':note_length,
               'part':part_no } ]

#------------------------------------------------------------------------------
#
# Extracts info from chord and returns it.

def aqu_get_data_from_chord( chord, part_no ):

    ans = []
    chord_bar_no = chord.measureNumber
    # Notes in a chord have no bar number so we must pick it up here
    # and add it to the data below.
    chord_length = chord.duration.quarterLength
    # notes in a chord all have length 1, only the chord itself has the
    # correct length??
    # once again, add correct length after retrieval

    for note_no in range( 0, len( chord ) ):

        note_data = aqu_get_data_from_note( chord[ note_no ], part_no )
        note_data[ 0 ] [ 'bar' ] = chord_bar_no
        note_data[ 0 ] [ 'length' ] = chord_length
        ans = ans + note_data

    return ans

#------------------------------------------------------------------------------
#
# Argument is a note name e.g. 'A', 'A-', 'A#' or 'A##'. Returns a list
# containing the bare note name e.g. 'A' and the accidental(s) e.g. '' or '-'.

def aqu_note_letter_and_accidental( note ):

    l = len( note )
    if l == 0:
        return [ '', '' ]
        #should never happen

    elif l == 1:
        return [ note, '' ]

    else:
        return [ note[ 0 ], note[1:l] ]

#------------------------------------------------------------------------------
#
# Based on the type (third argument, chooses a function to answer the question.

def aqu_obtain_answers(
    tokens, parse, type, score_index, divisions, time_signature ):

    if type == 'find_note_of_length':

        return aqu_find_note_of_length(
               tokens, parse, score_index, divisions, time_signature )

    elif type == 'find_note_of_pitch':

        return aqu_find_note_of_pitch(
               tokens, parse, score_index, divisions, time_signature )

    else:

        return []

#------------------------------------------------------------------------------
# 
# This returns an arbitrary answer list and is just for testing.

def aqu_obtain_answers2( tokens, parse, type, score, divisions ):

    answer_list = [

        { 'start_beats' : '4', 'start_beat_type' : '4',
          'end_beats' : '4', 'end_beat_type' : '4',
          'start_divisions' : '4', 'end_divisions' : '4',
          'start_bar' : '2', 'start_offset' : '1',
          'end_bar' : '2', 'end_offset' : '4' },
    
        { 'start_beats' : '4', 'start_beat_type' : '4',
          'end_beats' : '4', 'end_beat_type' : '4',
          'start_divisions' : '4', 'end_divisions' : '4',
          'start_bar' : '7', 'start_offset' : '5',
          'end_bar' : '7', 'end_offset' : '8' } ] 
          # Note that values must all be strings incl numbers.

    return answer_list

#------------------------------------------------------------------------------
#

def aqu_find_note_of_pitch( tokens, parse, score_index,
                              divisions, time_signature ):

    print( 'aqu_find_note_of_pitch called' )

    answer_list = [

        { 'start_beats' : '4', 'start_beat_type' : '4',
          'end_beats' : '4', 'end_beat_type' : '4',
          'start_divisions' : '4', 'end_divisions' : '4',
          'start_bar' : '2', 'start_offset' : '1',
          'end_bar' : '2', 'end_offset' : '4' } ]

    return answer_list

#------------------------------------------------------------------------------
#
# Based on a query like 'crotchet' finds all notes of the stated length.
# Ignores tied notes.

def aqu_find_note_of_length( tokens, parse, score_index,
                               divisions, time_signature ):

    required_length = aqu_note_name_length( tokens[ 0 ] )
    # Assuming query is something like [ 'semibreve' ]
    print( 'note length:' + str( required_length ) )

    raw_answers = [ note for note in score_index
                    if note[ 'length' ] == required_length ]

    print( 'raw answers:' + str( raw_answers ) )
    final_answers = []
    for note in raw_answers:

        final_answers = final_answers + [ aqu_get_passage( note, divisions,
                                                             time_signature ) ]

    print( 'Raw:' + str( raw_answers ) )
    print( 'Pass:' + str( final_answers ) )
    return final_answers

#------------------------------------------------------------------------------
#
# Return the length of a note name such as crotchet or semibreve in crotchets
# as an integer. Extremely rough and ready.

def aqu_note_name_length( note_name ):

    conversion = { 'crotchet': 1, 'minim': 2, 'semibreve' : 4 }

    try:
        return( conversion[ note_name ] )

    except Exception: return( 1000 )
    # For now return a big number which is unlikely to match anything
    # - even in Giovanni Gabrieli!

#------------------------------------------------------------------------------
#
# Inputs are a dictionary containing a note spec as extracted from the score,
# and an integer divisions value, as specified in the original question.
# Output is a passage spec for that note - see the top of this file. The exact
# algorithm (not necessarily correct) is as follows:
#
# Take length and offset, multiply each by divisions and convert to integer,
# giving corrected_length and corrected_offset
# start_offset = corrected_offset + 1
# end_offset = start_offset + corrected_length - 1
#
# Concerning the other attributes:
# start_beats = end_beats = time_signature[ 0 ]
# start_beat_type = end_beat_type = time_signature[ 1 ]
# start_divisions = end_divisions = divisions
# start_bar = end_bar = bar
#
# Getting the time signature:
# score.parts[0][1][3].numerator
# score.parts[0][1][3].denominator

def aqu_get_passage( note, divisions, time_signature ):

   passage = {}
   corrected_length = int( round( note[ 'length' ] * divisions, 0 ) )
   corrected_offset = int( round( note[ 'offset' ] * divisions, 0 ) )

   # I am not at all sure about these sorts of calculations. Music21 uses
   # floating point numbers (I think) for note lengths etc. So quaver triplets
   # have length 0.333. Choosing divisions 12, say, results in
   # int( round( 0.333 * 12 ) ) = 4 which is correct. Of course, you need
   # to choose a suitable divisions value but in C@merata this is specified
   # in the question to get around this problem. Whether these calculations
   # will always work, I cannot be certain.

   passage[ 'start_offset' ] = str( corrected_offset + 1 )
   passage[ 'end_offset' ] = str( corrected_offset + 1 + corrected_length -1 )
   # I am putting the +1 and -1 to make it clear.

   passage[ 'start_beats' ] = str( time_signature[ 0 ] )
   passage[ 'end_beats' ] = str( time_signature[ 0 ] )
   passage[ 'start_beat_type' ] = str( time_signature[ 1 ] )
   passage[ 'end_beat_type' ] = str( time_signature[ 1 ] )
   passage[ 'start_divisions' ] = str( divisions )
   passage[ 'end_divisions' ] = str( divisions )
   passage[ 'start_bar' ] = str( note[ 'bar' ] )
   passage[ 'end_bar' ] = str( note[ 'bar' ] )

   # Note that all values are converted to strings.


   return passage

#------------------------------------------------------------------------------
#
# score is a music21 parse of an input score. Result is the time signature
# extracted from the score, e.g. [ 4, 4 ].
# ASSUMES: All parts have the same time signature and that this is constant
# throughout the score.

def aqu_find_time_signature( score ):

    return [ 4, 4 ]
