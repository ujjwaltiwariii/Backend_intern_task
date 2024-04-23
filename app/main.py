#Package Import
from fastapi import FastAPI,Request,HTTPException


#Local Import
from app.routes import students
from app.db.session import get_client,close_db
from app.utils.config import get_settings
import aioredis 
from aioredis import Redis
from datetime import datetime,timedelta
# Get settings
settings = get_settings()


# Create FastAPI instance
app = FastAPI(title=settings.app_name,version=settings.version,description="This is a sample LMS API")

# Include routers
app.include_router(students.router,tags=["Students"])

#for now i am not adding any authentication to the api so you can pass any value of user in the header


@app.middleware("http")
async def count_user_requests(request: Request, call_next):
    if request.url.path not in ["/docs", "/redoc", "/openapi.json","/"]:
        redis = Redis.from_url(settings.redis)
        user = request.headers.get('user-id')
        if not user:
            raise HTTPException(status_code=400, detail="User header is required")

        today_in_iso = datetime.now().date().isoformat()
        today = datetime.now()


        end_of_day = (today + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)


        remaining_time_in_day = (end_of_day - today).total_seconds() # i am checking the remaining time in the day and if we want to reset the count exactly after 24 hours we can use the expiry time as 86400 seconds else we can use the remaining time in the day as the expiry time

        key = f"{user}:{today_in_iso}"

        if await redis.exists(key):
            await redis.incr(key)
        else:
            await redis.set(key, 1, ex=int(remaining_time_in_day))# here if we want to clean exactly after 24 hours we can assign ex=86400 seconds else we can assign the remaining time in the day as the expiry time

    response = await call_next(request)
    return response

@app.on_event('startup')
async def startup_event():
    get_client()

@app.on_event('shutdown')
async def shutdown_event():
    close_db()
    
