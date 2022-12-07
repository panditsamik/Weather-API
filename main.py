from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)
stationsi = pd.read_csv("api_files/stations.txt", skiprows=17)


@app.route("/")
def home():
    return render_template("APIWeatherData.html", data=stationsi.to_html())


@app.route("/api/v1/<station>/<data>")
def datetime(station, data):
    fileName = "api_files/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(fileName, skiprows=20, parse_dates=['    DATE'])
    temperature = df.loc[df['    DATE'] == data]['   TG'].squeeze() / 10
    return {
        "station": station,
        "data": data,
        "temperature": temperature
    }


@app.route("/api/v1/<station>")
def stations(station):
    fileName = "api_files/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(fileName, skiprows=20, parse_dates=['    DATE'])
    result = df.to_dict(orient="records")
    return result


@app.route("/api/v1/yearly/<station>/<year>")
def years(station, year):
    fileName = "api_files/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(fileName, skiprows=20)
    df['    DATE'] = df['    DATE'].astype(str)
    result = df[df['    DATE'].str.startswith(str(year))].to_dict(orient="records")
    return result


if __name__ == "__main__":
    app.run(debug=True, port=5000)
