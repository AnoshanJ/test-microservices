from flask import Flask, request

app = Flask(__name__)

books = []

@app.route('/health', methods=['GET'])
def get_echo():
    return "Service Running!", 200, {'Content-Type': 'text/plain'}

@app.route('/echo', methods=['POST'])
def echo():
    # Retrieve the data from the POST request
    data = request.data.decode('utf-8')

    # Return the same data as plain text
    return data, 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run()
