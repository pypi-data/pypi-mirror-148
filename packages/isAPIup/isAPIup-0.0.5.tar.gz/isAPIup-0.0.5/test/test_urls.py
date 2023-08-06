from flask import Flask, render_template, request, redirect,jsonify



#from gevent.pywsgi import WSGIServer

app = Flask(__name__)


@app.route('/test/a', methods=['GET','POST'])
def testa():
    return jsonify({"msg":"working fine"})

@app.route('/test/b', methods=['GET','POST'])
def testb():
    return jsonify({"msg":"error"})

@app.route('/test/c', methods=['GET','POST'])
def testc():
    return jsonify({"msg":"working fine"})

    
if __name__ == '__main__':     
    app.run(debug=True, host='0.0.0.0',port=5000)
