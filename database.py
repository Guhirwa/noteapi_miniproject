'''Database module with the in-memory storage, global counter and basic CRUD operations'''
from datetime import datetime
from typing import Dict, Optional, List

notes_db: Dict[int, dict] = {}

note_counter: int = 1

def get_all_notes() -> List[dict]:
    """Retrieve all notes as a list"""
    return list(notes_db.values())


def get_note_by_id(note_id: int) -> Optional[dict]:
    """Retrieve a single note by ID, return None if not found"""
    return notes_db.get(note_id)


def create_note(title: str, content: str) -> dict:
    """Create a new note and store it"""
    global note_counter
    note = {
        "id": note_counter,
        "title": title,
        "content": content,
        "created_at": datetime.now().date().isoformat(),
    }
    notes_db[note_counter] = note
    note_counter += 1
    return note

def update_note(note_id: int, title: str, content: str) -> Optional[dict]:
    '''Update an existing note'''
    if note_id in notes_db:
        notes_db[note_id].update({
            'title': title,
            'content': content
        })
        return notes_db[note_id]
    return None

def delete_note(note_id: int) -> bool:
    '''Delete a note, return True if successful otherwise False'''
    if note_id in notes_db:
        del notes_db[note_id]
        return True
    return False
