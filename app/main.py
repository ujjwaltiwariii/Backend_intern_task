#Package Import
from fastapi import FastAPI


#Local Import
from app.routes import students
from app.db.session import get_client,close_db
from app.utils.config import get_settings

# Get settings
settings = get_settings()


# Create FastAPI instance
app = FastAPI(title=settings.app_name,version=settings.version,description="This is a sample LMS API")

# Include routers
app.include_router(students.router,tags=["Students"])




@app.on_event('startup')
async def startup_event():
    get_client()

@app.on_event('shutdown')
async def shutdown_event():
    close_db()
    
