import requests
from bs4 import BeautifulSoup
import json
import os
from fake_useragent import UserAgent

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
CORS(app)

@app.route("/")
def index():
    return app.send_static_file("index.html")


def scrape_google(query: str):
    results = {}

    #while len(results) == 0:

        #ua = UserAgent()
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9,cs;q=0.8,sk;q=0.7",
        "cache-control": "no-cache",
        "cookie": "SOCS=CAISHAgCEhJnd3NfMjAyMzEwMDUtMF9SQzMaAmVuIAEaBgiA-rGpBg; SEARCH_SAMESITE=CgQInJoB; OTZ=7509116_48_52_123900_48_436380; SID=g.a000iwhSFoFke86lBOqObhlzESd3uXOu4i6CNps_rBL55BmiVmk71gXyOxQsst3J_SqpRXz4VgACgYKAXESAQASFQHGX2MiR2bvS7FHsxQnmdACM1SauxoVAUF8yKqOe5fP9Nd_feSMKc_KyVcf0076; __Secure-1PSID=g.a000iwhSFoFke86lBOqObhlzESd3uXOu4i6CNps_rBL55BmiVmk7SbceQ4MGQPfulRpfzkONWgACgYKAZ0SAQASFQHGX2MidNtyMPy6XjsuMnYtrynGKRoVAUF8yKpZ3V2cvG1AH0Sa6Tjkt_CN0076; __Secure-3PSID=g.a000iwhSFoFke86lBOqObhlzESd3uXOu4i6CNps_rBL55BmiVmk7LQIOqlEgCjr9cu7BVWwqhgACgYKAbESAQASFQHGX2Miy8ymWcbFIrgJvPt2-aKrphoVAUF8yKraZV0nNrPF7LSfgwVhfi810076; HSID=AD4tsSJUahSzVceYG; SSID=A3DpdEhs9ZxNunrKx; APISID=4Ehnfuaj9zO0nEG_/AhLQ1TTp-v5DiWlfs; SAPISID=C3w4xFm0VU4KVhFE/AIa2n0O3zThzKIXtH; __Secure-1PAPISID=C3w4xFm0VU4KVhFE/AIa2n0O3zThzKIXtH; __Secure-3PAPISID=C3w4xFm0VU4KVhFE/AIa2n0O3zThzKIXtH; AEC=AQTF6HzFMXC4vOaXBKV2YbIrZFrvrYszic5fPCipYjtK7qk6qPHznikMGA; 1P_JAR=2024-5-2-14; NID=513=TQmUTEGJgiDCN2he9L1Nb4ektKIdxAlfdfpw9vJ77kpcJ2-YHwHaKMzXazhljpf5xTJeB7n5z_m1ZukZYEGqfi9NDOredvFLXBJbpe1Vll1hORgtd4EmBYrAwNMWh5Z8GPU5NRGaq_lU5hAXdRY5NrIhN3sP8RTBL-dTEL5e4aA2I43ZoFHkUgr0F2-973g-1DqfabSqCbcFZDooTUglN1xvy8JGVmJ26A-b7zHqfSTyd8nSIAOTi8YcwgM309JoyIh_v5VSOhztrN_htIWgsWy4SE9Ng7u7TkJ1aMi-m2ztIO5bdr8EeVkbvwfXWvFQt5D02S-3t5QvOS9jmX-Pn5jCmO-MIM7kGIe6sI3uLBmhq6v9WWvi4-L409lP7Ft2PrhLg8VLShcfiD8oqKo1jJ0nqP_I9ZibvTtnkkE5tWAg9UXHHC_aYKVCJh1Pug9m3ZVQwCON3v44GdRCcwyTfhct_7L5SRRh6sJ-Lz6QCb98mzUC2ksoWSp82D47MMtY2Lb4OAaSX-yaqD-vhho2MLr5kqF0CJxHHLOk-ik1fQYQr_D8q5zl-Cul46WMhg; DV=wyo1EPL-8QVbsL45xLkJ8-TVhtOn85hw4P5MyRCtgwAAAMDhzkjRjHWQtQAAAKCB8PQiUMTiPgAAACDi14a58OXZEAAAAA; __Secure-1PSIDTS=sidts-CjIBLwcBXOYSvQIKYuWBi4Q2A6fUvjGMBt5J6fF0_aPtZcgdGsvWfC11s-T2ui4i6cr45BAA; __Secure-3PSIDTS=sidts-CjIBLwcBXOYSvQIKYuWBi4Q2A6fUvjGMBt5J6fF0_aPtZcgdGsvWfC11s-T2ui4i6cr45BAA; SIDCC=AKEyXzVYDg0nEDV-c9fych_cUar5wRDcCLCmN_ZmCoxMWfaXAngyPQd7g27Y0LUaUpUWQU_cLC8; __Secure-1PSIDCC=AKEyXzWh0eV2gwMKK8qtQ75bZQ7p9Vl4bjGkbYS5LtXXFJjhyMgtZ2P7B1LuhRpdYrXnkj0IqSk; __Secure-3PSIDCC=AKEyXzVgGnbmELz129XagwCW_qtpDMQNfX_FpIHKZPprCy-q-dev8bGLQ6_5E4HxdJZn6UCRtaUJ",
        "pragma": "no-cache",
        "referer": "https://www.google.com/",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    }

    params = {
            "rlz": "1C1GCEA_enCZ1075CZ1075",
            "q": query,
            "gs_lcrp": "EgZjaHJvbWUqDAgAECMYJxiABBiKBTIMCAAQIxgnGIAEGIoFMgoIARAuGNQCGIAEMg4IAhBFGCcYOxiABBiKBTIJCAMQRRg5GIAEMgcIBBAAGIAEMgcIBRAuGIAEMgcIBhAAGIAEMgoIBxAuGNQCGIAEMgcICBAuGIAEMgcICRAAGIAE0gEJMjkxMmowajE1qAIIsAIB",
            "sourceid": "chrome",
            "ie": "UTF-8"
    }
    
    response = requests.get(f"https://www.google.com/search", headers=headers, params=params)

    soup = BeautifulSoup(response.content, "html.parser")

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
    port = int(os.getenv("PORT", 10000))
    app.run(debug=True, host="0.0.0.0", port=port)
