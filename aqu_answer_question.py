
import pqy_parse_query
import typ_question_type
import music21
from itertools import groupby



def aqu_answer_question( question_text, music_file, divisions ):

    tokens = pqy_parse_query.pqy_tokenise( question_text )

    parse = []
    
    type = typ_question_type.typ_question_type( tokens, parse )
    print( 'type is: ' + type )
    score = music21.converter.parse( music_file )
    index = aqu_create_index( score )
    time_signature = aqu_find_time_signature( score )

    answer_list = aqu_obtain_answers(
                      tokens, parse, type, index, divisions, time_signature )

    answer_list2 = [ k for k, g in groupby( sorted( answer_list ) ) ]
    


    return answer_list2


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
           
    return( ans )



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
    
    chord_length = chord.duration.quarterLength
    

    for note_no in range( 0, len( chord ) ):

        note_data = aqu_get_data_from_note( chord[ note_no ], part_no )
        note_data[ 0 ] [ 'bar' ] = chord_bar_no
        note_data[ 0 ] [ 'length' ] = chord_length
        ans = ans + note_data

    return ans

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


def aqu_get_passage( note, divisions, time_signature ):

   passage = {}
   corrected_length = int( round( note[ 'length' ] * divisions, 0 ) )
   corrected_offset = int( round( note[ 'offset' ] * divisions, 0 ) )

  

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


def aqu_find_time_signature( score ):

    return [ 4, 4 ]
