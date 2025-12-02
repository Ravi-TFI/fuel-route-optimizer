import csv
import time
import requests
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from fuel_api.models import FuelStation

class Command(BaseCommand):
    help = 'Load fuel prices'

    def handle(self, *args, **kwargs):
        file_path = 'fuel-prices-for-be-assessment.csv'
        session = requests.Session()
        base_url = "https://nominatim.openstreetmap.org/search"
        headers = {'User-Agent': 'FuelAppTest/1.0'}

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            count = 0
            
            for row in reader:
                if FuelStation.objects.filter(opis_id=row['OPIS Truckstop ID']).exists():
                    continue

                # 1. Try Specific Address
                query = f"{row['Address']}, {row['City']}, {row['State']}, USA"
                point = self.fetch_geo(session, base_url, query, headers)

                # 2. Fallback: Try City, State only (if specific fails)
                if not point:
                    self.stdout.write(self.style.WARNING(f"Retrying with City/State: {row['City']}"))
                    query_city = f"{row['City']}, {row['State']}, USA"
                    point = self.fetch_geo(session, base_url, query_city, headers)

                if point:
                    FuelStation.objects.create(
                        opis_id=row['OPIS Truckstop ID'],
                        name=row['Truckstop Name'],
                        address=row['Address'],
                        city=row['City'],
                        state=row['State'],
                        retail_price=float(row['Retail Price']),
                        location=point
                    )
                    count += 1
                    if count % 100 == 0:
                        self.stdout.write(f"Saved {count} stations...")
                
                time.sleep(1.1)

    def fetch_geo(self, session, url, query, headers):
        try:
            resp = session.get(url, params={'q': query, 'format': 'json', 'limit': 1}, headers=headers)
            data = resp.json()
            if data:
                return Point(float(data[0]['lon']), float(data[0]['lat']))
        except:
            return None
        return None