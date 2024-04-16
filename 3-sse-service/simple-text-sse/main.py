import asyncio
import uvicorn
import logging
import sys
import time
from datetime import datetime

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
from fastapi.responses import StreamingResponse


STREAM_DELAY = 0.2  # second
RETRY_TIMEOUT = 15000  # milisecond
WORDS_PER_MESSAGE = 10  # number of words per message

file_path = './data/far-far-away-10000.txt'

app = FastAPI()

class SpecificLogFilter(logging.Filter):
    def filter(self, record):
        # check if chunk or ping is in the message
        return "chunk" not in record.getMessage() and "ping" not in record.getMessage()

def setup_logging():
    # Since logging.basicConfig() should only be called once and it affects the root logger,
    # we ensure it's configured to our needs before modifying specific loggers.
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", stream=sys.stdout)

    # Get the 'asyncio' logger and set its level to DEBUG
    logger = logging.getLogger("asyncio")
    logger.setLevel(logging.DEBUG)
    # Logging an initial message (this will be shown based on your filter criteria)
    logger.info('SSE App is starting up')
    
    #remove the sse_starlette.sse logger
    logging.getLogger('sse_starlette.sse').addFilter(SpecificLogFilter())
    
    return logger

# Call setup_logging to configure your logging as required
logger = setup_logging()
    
class RequestResponseLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        logging_details = {
            "x-request-id": request.headers.get("x-request-id") or "N/A",
            "method": request.method,
            "url": request.url.path,
            "timestamp": datetime.now().isoformat(),
            "client_ip": request.client.host,
            "response_status_code": response.status_code,
            "response_time_ms": process_time,
        }
        # Log the request details
        logger.info(f"Request: {logging_details}") 
       
        return response

# Add middleware
app.add_middleware(RequestResponseLoggerMiddleware)

@app.get("/")
async def root(request: Request):
    return {"message": "Hello World"}

@app.get('/stream')
async def message_stream(request: Request):

    async def event_generator():
        event_count=0 
        while True:
          
            if await request.is_disconnected():
                logger.debug('x-request-id: '+str(request.headers.get('x-request-id'))+' Client disconnected')
                break              

            msg = await read_lines(event_count*WORDS_PER_MESSAGE)
            
            if msg:
                # yield { "event": "message",
                #         "id": str(event_count),
                #         "retry": RETRY_TIMEOUT,
                #         "data": msg
                # }
                yield f"data: {msg}\n\nid: {event_count}\nretry: {RETRY_TIMEOUT}\n"

            else:
                logger.info('x-request-id: '+str(request.headers.get('x-request-id'))+' End of file reached')
                # close the connection
                break
            event_count+=1
            await asyncio.sleep(STREAM_DELAY)

    # return EventSourceResponse(event_generator())
    # return EventStreamResponse(event_generator())
    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.post('/stream-post')
async def message_stream_post(request: Request):
    
    #get the body
    body = await request.body()
    body = body.decode('utf-8')
    logger.info('x-request-id: '+str(request.headers.get('x-request-id'))+' Body: '+str(body))
    async def event_generator():
        event_count=0 
        
        while True:
            # If client closes connection, stop sending events
            if await request.is_disconnected():                                   
                logger.info('x-request-id: '+str(request.headers.get('x-request-id'))+' Client disconnected')
                break

            msg = await read_lines(event_count*WORDS_PER_MESSAGE)
            
            if msg:
                yield f"data: {msg}\n\nid: {event_count}\nretry: {RETRY_TIMEOUT}\n"
            else:
                logger.info('x-request-id: '+str(request.headers.get('x-request-id'))+' End of file reached')
                # close the connection
                break
            event_count+=1
            await asyncio.sleep(STREAM_DELAY)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

    
def load_text(file_path:str='./data/lorem-ipsum-1000.txt'):
    try:
        with open(file_path) as f:
            text = f.read().strip().split()
            return text
    except Exception as e:
        logging.error(f"Failed to load text from {file_path}: {e}")
        return []

async def read_lines(i:int):
    return ' '.join(text[i:i+WORDS_PER_MESSAGE])

# logger = setup_logging()
text = load_text(file_path)

if __name__ == "__main__":
    # uvicorn.run(app, host="127.0.0.1", port=8000)    
    uvicorn.run()