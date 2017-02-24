
# This is just a placeholder.

def typ_question_type( tokens, parse ):

    if tokens[ 0 ] in [ 'semibreve', 'minim', 'crotchet', 'quaver' ]:
        return 'find_note_of_length'

    else: return 'find_note_of_pitch'
