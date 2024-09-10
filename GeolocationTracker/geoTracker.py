import requests
import folium


# Fetching data using api
def fetch_geolocation_data(ip_address):
    api_key = "54efab89290e426eadf7f8becfc4cc3b"
    api_url = f"https://ipgeolocation.abstractapi.com/v1/?api_key={api_key}&ip_address={ip_address}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # raise an HTTPError for bad response

        geolocation_data = response.json()

        # print(f"API Response: ", geolocation_data)

        return {
            "ip": geolocation_data.get("ip_address"),
            "city": geolocation_data.get("city"),
            "region": geolocation_data.get("region"),
            "country": geolocation_data.get("country"),
            "latitude": geolocation_data.get("latitude"),
            "longitude": geolocation_data.get("longitude"),
        }
    except requests.exceptions.HTTPError as http_error:
        print(f"HTTP error occurred: {http_error}")
    except Exception as error:
        print(f"An error occurred: {error}")
    return None


# Displaying location in the map
def display_on_map(latitude, longitude, location_name=""):
    map_ = folium.Map(location=[latitude, longitude], zoom_start=10)

    folium.Marker(
        location=[latitude, longitude],
        popup=location_name,
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(map_)

    map_.save("location_map.html")


# Drier code

ip_address = input("Enter IP Address: ")
location_data = fetch_geolocation_data(ip_address)

if location_data:
    print(f"IP Address: {location_data['ip']}")
    print(f"City: {location_data['city']}")
    print(f"Region: {location_data['region']}")
    print(f"Country: {location_data['country']}")
    print(f"Latitude: {location_data['latitude']}")
    print(f"Longitude: {location_data['longitude']}")
    display_on_map(location_data["latitude"], location_data["longitude"], location_data["city"])
else:
    print("Failed to fetch geolocation data.")
