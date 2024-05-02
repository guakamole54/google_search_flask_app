import requests
from bs4 import BeautifulSoup
import json

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
CORS(app, resources={r"/search": {"origins": "http://localhost:5500"}})

def scrape_google(query: str):

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4703.0 Safari/537.36"
    }
    response = requests.get(f"https://www.google.com/search?q={query}", headers=headers)

    soup = BeautifulSoup(response.content, "html.parser")

    results = {}
    for num, el in enumerate(soup.select(".g")):
        results[num] = {}
        try:
            results[num]["title"] = el.select_one("h3").text
            results[num]["description"] = el.select_one(".VwiC3b").text
            results[num]["url"] = el.select_one("a")["href"]
        except AttributeError:
            pass

    return results


@app.route("/search", methods=["POST"])
def search():
    print("Request received")
    if request.method == "POST":
        print("POST request received")
        # Get the query from the request
        print(request)
        data = request.json
        query = data.get("query")

        # Check for valid query
        if not query:
            return jsonify({"error": "No query provided"}), 400

        # Scrape Google for the query results
        results = scrape_google(query)

        # Save results to JSON
        filename = "search_results.json"
        with open(filename, "w") as file:
            json.dump(results, file, indent=2, ensure_ascii=False)

        return send_file(filename, as_attachment=True)
        # Return a response
    else:
        return "Method not allowed", 405


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5500)
