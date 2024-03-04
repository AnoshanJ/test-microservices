import asyncio
import uvicorn
from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse

STREAM_DELAY = 1  # second
RETRY_TIMEOUT = 15000  # milisecond
WORDS_PER_MESSAGE = 10  # number of characters per message

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get('/stream')
async def message_stream(request: Request):
    
    file_path = './data/far-far-away-1000.txt'
    text = load_text(file_path)
       
    def new_messages(i):
        return read_lines(i, text)
        
    async def event_generator():
        event_count=0 
        
        
        while True:
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break

            # Checks for new messages and return them to client if any
            msg = new_messages(event_count*WORDS_PER_MESSAGE) #return the current index from where to retrieve
               
            if msg:
                yield { "event": "message",
                        "id": str(event_count),
                        "retry": RETRY_TIMEOUT,
                        "data": msg
                }
            else:
                # close the connection
                break
            event_count+=1
            await asyncio.sleep(STREAM_DELAY)

    return EventSourceResponse(event_generator())

def load_text(file_path:str='./data/lorem-ipsum-1000.txt'):
    with open(file_path) as f:
        text = f.read()
        return text
    
def read_lines(i:int, text:str):
    # read the lorem-ipsum.txt file 10 words at a time
    lines = [x for x in text.strip().strip('\n').split()]
    return ' '.join(lines[i:i+WORDS_PER_MESSAGE])
    
if __name__ == "__main__":
    # uvicorn.run(app, host="127.0.0.1", port=8000)
    uvicorn.run()