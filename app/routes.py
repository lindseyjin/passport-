from app import app


@app.route('/')
def test():
    return "testing testing, hello world"
