'''main app entry point'''
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from routers import notes

app = FastAPI(
    title='Notes API',
    description='A simple REST API for managing notes',
    version='1.0'
)

app.include_router(notes.router)

@app.get('/')
def home_page():
    '''Welcome endpoint'''
    return {
        'message': 'Welcome to Notes API App',
        'endpoints': {
            'create_note': 'POST /notes',
            'list_notes': 'GET /notes',
            'get_note': 'GET /notes/{id}',
            'update_note': 'PUT /notes/{id}',
            'delete_note': 'DELETE /notes/{id}',
            'docs': '/docs'
        }
    }

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True
    )
