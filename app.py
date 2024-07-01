from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json.get('message')
    # Replace 'http://localhost:5005/webhooks/rest/webhook' with your Rasa server URL
    rasa_response = requests.post(
        'http://localhost:5005/webhooks/rest/webhook', 
        json={"message": user_message}
    )
    response_data = rasa_response.json()[0]  # Assuming the first response is sufficient
    bot_message = response_data.get('text')
    buttons = response_data.get('buttons', [])  # Get buttons if available
    
    if buttons:
        response = {"message": bot_message, "buttons": buttons}
    else:
        response = {"message": bot_message}
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
