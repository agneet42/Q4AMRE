#******************************************************************************

#                         typ_question_type.py

#                     Finds the type of a question

# The type is chosen from a fixed list. For each type we have a predefined
# means of answering it.
# 

#******************************************************************************

#------------------------------------------------------------------------------
# 
# tokens is the query tokenised and parse is the query parsed. Determines the
# type of the question, chosen from a fixed length.
# 
# This is just a placeholder.

def typ_question_type( tokens, parse ):

    if tokens[ 0 ] in [ 'semibreve', 'minim', 'crotchet', 'quaver' ]:
        return 'find_note_of_length'

    else: return 'find_note_of_pitch'
