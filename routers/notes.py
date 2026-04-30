'''Grouped endpoints for note operations'''
from fastapi import APIRouter, HTTPException, Query
from typing import List
from schemas import NoteCreate, NoteUpdate, NoteResponse
from database import (
    get_all_notes,
    get_note_by_id,
    create_note,
    update_note,
    delete_note
)

router = APIRouter(
    prefix='/notes',
    tags=['notes'],
    responses={404: {'description': 'Note not found'}}
)

@router.post('', response_model=NoteResponse, status_code=201)
def create_note_endpoint(note: NoteCreate):
    '''Create a new note and return a created note with the generated unique ID'''
    new_note = create_note(title=note.title, content=note.content)
    return new_note

@router.get('', response_model=List[NoteResponse])
def get_notes_endpoint(
    limits: int = Query(None, ge=1, description='limit the number of notes returned if applicable'),
    filter_title: str = Query(None, description='filter notes by title (case insensitive)')
):
    '''Endpoint to select and return the notes, limited number or filtered notes '''
    notes = get_all_notes()

    if limits:
        notes = notes[:limits]

    if filter_title:
        notes = [
            n for n in notes
            if filter_title.lower() in n['title'].lower()
        ]

    return notes

@router.get('/{note_id}', response_model=NoteResponse)
def get_note_endpoint(note_id: int):
    '''Endpoint to get one note by ID'''
    note = get_note_by_id(note_id)
 
    if not note:
        raise HTTPException(
            status_code=404,
            detail=f'Note with id {note_id} not found'
        )

    return note

@router.put('/{note_id}', response_model=NoteResponse)
def update_note_endpoint(note_id: int, note: NoteUpdate):
    '''End point to edit/update the existing notes'''

    existing_note = get_note_by_id(note_id)

    if not existing_note:
        raise HTTPException(
            status_code=404,
            detail=f'Note with id {note_id} that you are trying to update not found'
        )

    title = (note.title if note.title is not None else existing_note['title'])
    content = (note.content if note.content is not None else existing_note['content'])

    updated_note = update_note(note_id, title, content)

    return updated_note

@router.delete('/{note_id}', response_model=NoteResponse)
def delete_note_endpoint(note_id: int):
    '''Endpoint to delete a note matched with the ID from the request'''

    success = delete_note(note_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail=f'Note with ID {note_id} that your\'re trying to delete not found'
        )
