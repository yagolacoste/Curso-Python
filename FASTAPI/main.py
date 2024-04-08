from fastapi import FastAPI

app = FastAPI()

@app.get("/") ##es la dependencia de get
def root():
    return {"message": " Welcom to te api fast111"}

@app.get("/posts")
def get_posts():
    return {"data":"This is your posts"}


@app.post("/createposts")
def create_posts():
    return {"message":"succesfully created posts"}