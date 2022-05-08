from flask import Flask
import folium

app = Flask(__name__)

KANOP_COORDS = (48.83505261412694, 2.37097587670811)


@app.route("/")
def index():
    folium_map = folium.Map(location=KANOP_COORDS, zoom_start=14)
    folium.Marker(
        location=KANOP_COORDS,
        popup="Kanop",
    ).add_to(folium_map)
    return folium_map._repr_html_()
