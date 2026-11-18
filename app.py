import csv
from flask import Flask, render_template, request

app = Flask(__name__)

def load_plants():
    ###
    # Reading the plants from the csv file (columns separated by ";")
    ###
    plants = []
    with open(app.root_path + "/plants.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=";"):
            if row["Common name"]:   # the sheet ends with empty rows
                plants.append({"name": row["Common name"],
                               "latin": row["Latin name"],
                               "light": row["Sunlight exposure"].capitalize(),
                               "humidity": row["Humidity preference"],
                               "habit": row["Growth habit"],
                               "pets": row["Pet toxicity (cats and dogs)"]})
    return plants

def filter_plants(plants):
    light = request.args.get("light", "")
    humidity = request.args.get("humidity", "")
    pets = request.args.get("pets", "")
    filtered = []
    for plant in plants:
        if (((not light) or plant["light"] == light)
                and ((not humidity) or plant["humidity"] == humidity)
                and ((not pets) or plant["pets"].startswith("Non-toxic"))):
            filtered.append(plant)
    return filtered

@app.get("/")
def index():
    plants = load_plants()
    filtered = filter_plants(plants)
    return render_template("index.html",
                           plants=filtered,
                           lights=sorted({plant["light"] for plant in plants}),
                           humidities=sorted({plant["humidity"] for plant in plants}),
                           selected_light=request.args.get("light", ""),
                           selected_humidity=request.args.get("humidity", ""),
                           selected_pets=request.args.get("pets", ""),
                           submitted=bool(request.args),
                           total=len(plants),
                           error="")

if __name__ == "__main__":
    app.run()