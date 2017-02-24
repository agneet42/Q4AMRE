import xml.etree.ElementTree as ET

from aqu_answer_question import *
from pqy_parse_query import *
from typ_question_type import *
from music21 import *

def cam_camerata():
    root = []
    cam_answer_questions( 'questions.xml', 'answers.xml', 'rtag01',
                          'An Organisation', 'RTAG' )

def cam_answer_questions( question_file, answer_file, runtag,
                          organisation, group ):
    tree = ET.parse( question_file )
    questions_elem = tree.getroot()
    questions_elem.set( 'runtag', runtag )
    questions_elem.set( 'organisation', organisation )
    questions_elem.set( 'group', group )
    
    for question_elem in questions_elem:
         print( question_elem.attrib[ 'music_file' ] )
        print( question_elem.attrib[ 'divisions' ] )
        print( question_elem.find( 'text' ).text )
        print( question_elem.find( 'answer' ) )
        
        question_text = question_elem.find( 'text' ).text
        music_file = question_elem.attrib[ 'music_file' ]
        divisions = int( question_elem.attrib[ 'divisions' ] )
        answer_list = aqu_answer_question(question_text, music_file, divisions )
        
         answer_elem = question_elem.find( 'answer' )

        for passage_spec in answer_list:

            passage_elem = ET.SubElement( answer_elem, 'passage' )
            passage_elem.set( 'start_beats', passage_spec[ 'start_beats' ] )
            passage_elem.set( 'start_beat_type',
                              passage_spec[ 'start_beat_type' ] )
            passage_elem.set( 'end_beats', passage_spec[ 'end_beats' ] )
            passage_elem.set( 'end_beat_type',
                              passage_spec[ 'end_beat_type' ] )
            passage_elem.set( 'start_divisions',
                              passage_spec[ 'start_divisions' ] )
            passage_elem.set( 'end_divisions',
                              passage_spec[ 'end_divisions' ] )
            passage_elem.set( 'start_bar',
                              passage_spec[ 'start_bar' ] )
            passage_elem.set( 'start_offset',
                              passage_spec[ 'start_offset' ] )
            passage_elem.set( 'end_bar',
                              passage_spec[ 'end_bar' ] )
            passage_elem.set( 'end_offset',
                              passage_spec[ 'end_offset' ] )


     tree.write( answer_file )
         

        
