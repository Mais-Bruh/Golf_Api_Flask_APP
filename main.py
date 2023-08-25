from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    url = "https://live-golf-data.p.rapidapi.com/stats"
    querystring = {
        "year": "2022",
        "statId": "186"
    }
    headers = {
        "X-RapidAPI-Key": "YourApiKey ",  # Replace with your API key
        "X-RapidAPI-Host": "live-golf-data.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    letter = request.args.get('letter', '').upper()  # Get the submitted letter and convert to uppercase

    player_data = []
    for player in data['rankings']:
        player_name = f"{player['firstName']} {player['lastName']}"
        player_info = {
            'name': player_name,
            'rank': player['rank']['$numberInt'],
            'events': player['events']['$numberInt'],
            'total_points': player['totalPoints']['$numberDouble']
        }
        if not letter or player_name.startswith(letter):
            player_data.append(player_info)

    return render_template('index.html', player_data=player_data, letter=letter)

if __name__ == '__main__':
    app.run(debug=True)
