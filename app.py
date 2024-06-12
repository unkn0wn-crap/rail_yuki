from flask import Flask

app = Flask(__yuki__)

@app.route('/')

def hello_world():

return 'YukiOnna Bot running on Flask'

if __yuki__ == "__main__":

app.run(