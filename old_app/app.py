from flask import Flask, jsonify, render_template
import json
import random
import webbrowser

app = Flask(__name__)

def load_url_list(json_file_input_path):
    '''
    Description:
        reads json file (from Instagram data download) and parses and returns the
        relevant urls as python List
    '''

    # Load the JSON file
    with open(json_file_input_path, 'r') as file:
        data = json.load(file)

    # Find the start and end index of the relevant entries/Collection
    index = 0
    start_index = 0
    end_index = 0
    desired_collection_name = "Quotes"
    for entry in data["saved_saved_collections"]:
        # find the start of the "Quotes" Collection
        if entry.get("title") and entry["string_map_data"]["Name"]["value"] == desired_collection_name:
            start_index = index+1
            end_index = start_index + 0
            continue
        # if the start of the "Quotes" Collection has been found (and therefore currently
        # we are iterating through the middle of it)...
        if start_index != 0:
            # if we've reached the end (ie, begn. of new Collection), break
            if entry.get("title"): 
                break
            # else, increment the known scope of the Quotes collection by 1
            else:
                end_index += 1

    # print(f"Start index {start_index}, end index {end_index}")

    relevant_entries = data["saved_saved_collections"][start_index:end_index]
    urls = []
    for entry in relevant_entries:
        urls.append(entry["string_map_data"]["Name"]["href"])

    return urls

# Load the URLs from the JSON file once when the app starts
json_file_input_path = "urls.json"
urls = load_url_list(json_file_input_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/open-random-url')
def open_random_url():
    random_url = random.choice(urls)
    webbrowser.open(random_url)
    return jsonify({"message": "URL opened in your web browser", "url": random_url})


if __name__ == '__main__':
    app.run(debug=True)
