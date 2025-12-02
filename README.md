# Fuel Route Optimizer API

A Django-based REST API built for Fuel Optimization Route API. This application calculates optimal driving routes between two locations in the USA, identifies cost-effective fuel stops based on a 500-mile vehicle range, and calculates the total fuel cost using a greedy optimization algorithm.

## 🚀 Features

- **Route Optimization:** Calculates precise driving paths using the OpenRouteService API.
- **Smart Fueling:** Uses a greedy algorithm to find the cheapest gas stations within the vehicle's range along the route.
- **Geospatial Intelligence:** Utilizes PostgreSQL + PostGIS to perform efficient spatial lookups (finding stations within a buffer of the highway).
- **Visual Output:** Returns GeoJSON data that can be rendered on maps (e.g., geojson.io).

## 🛠 Tech Stack

- **Language:** Python 3.12
- **Framework:** Django 5.x & Django Rest Framework (DRF)
- **Database:** PostgreSQL 15+ with PostGIS extension
- **Geospatial Libs:** GDAL / OSGeo4W
- **External API:** OpenRouteService (Routing), Nominatim (Geocoding)

## ⚙️ Prerequisites

1.**Python 3.10+**  
2.  **PostgreSQL** (Local installation)  
3.  **PostGIS** (Extension for PostgreSQL)  
4.  **OSGeo4W (Windows Only):** Required for GeoDjango binary dependencies.  
* Install from [trac.osgeo.org/osgeo4w](https://trac.osgeo.org/osgeo4w/).  
*   **Crucial:** Ensure `GDAL` is selected during the Express Install.

## 📥 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Ravi-TFI/fuel-route-optimizer.git
cd spotter_assignment
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv
# Windows
source venv/Scripts/activate
# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install django djangorestframework psycopg2-binary requests openrouteservice
```

### 4. Database Setup
Ensure PostgreSQL is running, then create the database and enable PostGIS:

```sql
CREATE DATABASE spotter_django;
\c spotter_django
CREATE EXTENSION postgis;
```

### 5. Configuration (`config/settings.py`)

1.**Database:** Update the `DATABASES` dictionary with your local PostgreSQL credentials (`USER`, `PASSWORD`).  
2.  **API Key:** Add your OpenRouteService API Key at the bottom of the file:
    ```python
    ORS_API_KEY = 'your_5b3ce..._key_here'
    ```  
3.  **Windows GDAL Path:** The `settings.py` includes a dynamic configuration script for OSGeo4W. Ensure your installation path matches `C:\Users\<user>\AppData\Local\Programs\OSGeo4W` or update the `OSGEO4W_ROOT` variable in `settings.py` accordingly.

## Running the Application

### 1. Run Migrations
Initialize the database schema:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Ingest Fuel Data
Run the custom management command to parse the CSV, geocode the addresses, and populate the database.
```bash
python manage.py load_fuel_data
```
*Note: This utilizes the free Nominatim API which has strict rate limits. The script includes delays to respect these limits. You may stop it (`Ctrl+C`) after it processes 50-100 stations for testing purposes.*

### 3. Start the Server
```bash
python manage.py runserver
```

## 📡 API Documentation

### Calculate Route
**Endpoint:** `GET /api/route/`

**Query Parameters:**
- `start`: The starting location (City, State).
- `finish`: The destination location (City, State).

**Example Request:**
```http
GET http://127.0.0.1:8000/api/route/?start=Austin, TX&finish=Dallas, TX
```

**Example Response:**
```json
{
    "route_map": {
        "type": "FeatureCollection",
        "features": [ ... ]
    },
    "total_miles": 195.4,
    "total_fuel_cost": 45.20,
    "stops": [
        {
            "station": "Buckee's",
            "city": "Temple",
            "price": 2.89,
            "estimated_cost_for_leg": 15.50
        }
    ]
}
```

## 🗺️ Visualization
To visualize the route:  
1.Copy the `route_map` object from the JSON response.  
2.Go to [geojson.io](https://geojson.io).  
3.Paste the object into the editor. The route line will appear on the map.

## 🐛 Troubleshooting

**Error: `ImproperlyConfigured: Could not find the GDAL library`**
*   This indicates Django cannot find the OSGeo4W binaries.
*   Check `config/settings.py` and ensure `OSGEO4W_ROOT` points to the correct folder on your machine.
*   Ensure you are using Python 3.8+ compatible code (the settings file includes `os.add_dll_directory` which is required for newer Python versions on Windows).

**Error: `Routing API Error`**
*   Ensure your `ORS_API_KEY` is valid and active.
*   Ensure you have internet connectivity.
