import asyncio
import uvicorn
import logging
import sys

from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse

STREAM_DELAY = 1  # second
RETRY_TIMEOUT = 15000  # milisecond
WORDS_PER_MESSAGE = 10  # number of words per message

app = FastAPI()

# A stream handler is created to write the log messages to the standard output (usually console).
# The stream handler is then added to the logger.

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

logger.info('SSE App is starting up')

@app.get("/")
async def root(request: Request):
    logger.info('Root endpoint:'+ str(request.headers))
    # logger.info(=====)
    return {"message": "Hello World"}

@app.get('/stream')
async def message_stream(request: Request):
    
    logger.info('Stream : endpoint'+ str(request.headers))
    
    async def event_generator():
        event_count=0 
        
        while True:
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                logger.info('Client disconnected')
                break

            msg = await read_lines(event_count*WORDS_PER_MESSAGE)
            
            if msg:
                yield { "event": "message",
                        "id": str(event_count),
                        "retry": RETRY_TIMEOUT,
                        "data": msg
                }
            else:
                logger.info('End of file reached')
                # close the connection
                break
            event_count+=1
            await asyncio.sleep(STREAM_DELAY)

    return EventSourceResponse(event_generator())

@app.post('/stream-post')
async def message_stream_post(request: Request):
    
    #get the body
    body = await request.body()
    body = body.decode('utf-8')
    #log
    logger.info('Stream Post : endpoint'+str(request.headers)+ ' body: '+body)

    async def event_generator():
        event_count=0 
        
        while True:
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                logger.info('Client disconnected')
                break

            msg = await read_lines(event_count*WORDS_PER_MESSAGE)
            
            if msg:
                yield { "event": str(body),
                        "id": str(event_count),
                        "retry": RETRY_TIMEOUT,
                        "data": msg
                }
            else:
                logger.info('End of file reached')
                # close the connection
                break
            event_count+=1
            await asyncio.sleep(STREAM_DELAY)

    return EventSourceResponse(event_generator())
    
def load_text(file_path:str='./data/lorem-ipsum-1000.txt'):
    with open(file_path) as f:
        text = f.read()
        text = [x for x in text.strip().strip('\n').split()]
        return text

async def read_lines(i:int):
    return ' '.join(text[i:i+WORDS_PER_MESSAGE])

file_path = './data/far-far-away-1000.txt'
text = load_text(file_path)

if __name__ == "__main__":
    # uvicorn.run(app, host="127.0.0.1", port=8000)
    uvicorn.run()