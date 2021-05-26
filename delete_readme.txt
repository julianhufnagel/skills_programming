In diesem File werden wir festhalten, was genau wir erreichen wollen.

https://www.climacell.co/weather-api/

DATA
API Übersicht (hat bereits python code snippets, um auf Daten zuzugreifen) - https://docs.climacell.co/reference/api-overview

APP/WEBSITE
Streamlit (easy to use für Data Science Website ohne Security Layer)- https://docs.streamlit.io/en/stable/main_concepts.html
Alternativen: Flask, Django
Überall sind HTML, CSS und JS Modifikationen möglich

OUTPUT
Suchvorgang:
Dropdown
Geolocation suchen via IP
API zur strukturierten und formalisierten Suche von Orten -> geocoding (geopandas and geopy)
Idee:
Die wichtigsten Daten zum status quo graphisch aufbereitet
Percipitation/Niederschlag nach Ort (aktuell + 2 Tag) in Zahlenformat & Visuell
Erweiterung: Karte mit den verschiedenen Niederschlags Informationen angelehnt an https://www.meteoschweiz.admin.ch/home.html?tab=overview
Erweiterung: Heat Map für Temperaturen für bspw die gesamte Schweiz


AUFGABEN
1. Block (Janina)
API anknüpfen (Python: json,...)
Input des Nutzers einlesen
Data handling (Python: pandas, numpy, ...) -> Alle Daten strukturiert eingelesen

2. Block (Deniz)
Alle relevanten Darstellungen zu Temp (Python: seaborn, plotly, …)

3. Block (Elena)
Alle relevanten Darstellungen zu Nds (Python: seaborn, plotly, …)

4. Block (Julian)
Verbindung der relevanten Darstellungen zu Temp und Nds auf WebApp (Streamlit, HTML, CSS, Bootstrap, JS)




Daten:
Location im richtigen Format (geocoding input)
Temperatur mit Location (am besten über Zeit) (API) -> Evtl. eine Schweiz-Karte für HeatMap
Nds mit Location (am besten über Zeit) (API) 
