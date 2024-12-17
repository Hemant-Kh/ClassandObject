from fastapi import FastAPI

app = FastAPI() #this will help initialize your application / server


@app.get('/')
def test():
    return('Output: I am working')



def main():                                                     #this part is important for all API
    import uvicorn
    uvicorn.run(app, host = '127.0.0.1', port = 8000)


if __name__ == '__main__': #It will automatically get called, initially when you run
    main()