#!/usr/bin/env python3
"""
Ice Cream Trail Mapper - Massachusetts Edition

Creates an interactive map showing driving routes from home to 10 ice cream stores
across Massachusetts, with real route calculations using OSRM API.

Author: Ahmad Ehtesham
Date: May 2026
"""

import pandas as pd
import folium
import requests
import time
from geopy.distance import geodesic


# Configuration
HOME_COORDS = {'lat': 42.2626, 'lng': -71.8023}
HOME_ADDRESS = "Highland St, Worcester, MA"

ICE_CREAM_STORES = [
    {
        "name": "Gibby's Famous Ice Cream",
        "address": "323 Greenwood St, Worcester, MA 01607",
        "lat": 42.2338,
        "lng": -71.7916
    },
    {
        "name": "Pinecroft Dairy and Restaurant",
        "address": "539 Prospect St, West Boylston, MA 01583",
        "lat": 42.3665,
        "lng": -71.8015
    },
    {
        "name": "Swirls and Scoops",
        "address": "100 Worcester St, North Grafton, MA 01536",
        "lat": 42.2286,
        "lng": -71.6857
    },
    {
        "name": "West End Creamery",
        "address": "481 Purgatory Rd, Whitinsville, MA 01588",
        "lat": 42.1118,
        "lng": -71.6662
    },
    {
        "name": "Rota Spring Farm",
        "address": "117 Chace Hill Rd, Sterling, MA 01564",
        "lat": 42.4359,
        "lng": -71.7601
    },
    {
        "name": "Murdock Farm and Dairy Bar",
        "address": "1143 Central St, Winchendon, MA 01475",
        "lat": 42.6876,
        "lng": -72.0437
    },
    {
        "name": "Shaw Farm Dairy",
        "address": "204 New Boston Rd, Dracut, MA 01826",
        "lat": 42.6762,
        "lng": -71.3020
    },
    {
        "name": "High Lawn Farm",
        "address": "535 Summer St, Lee, MA 01238",
        "lat": 42.3047,
        "lng": -73.2485
    },
    {
        "name": "Joyful Scoops",
        "address": "50 Harding St, Middleborough, MA 02346",
        "lat": 41.8945,
        "lng": -70.9080
    },
    {
        "name": "Alvin Rondeau's Dairy Bar",
        "address": "1335 Park St, Palmer, MA 01069",
        "lat": 42.1762,
        "lng": -72.3287
    }
]


def calculate_distances(home_coords, stores):
    """
    Calculate straight-line distance from home to each ice cream store.
    
    Args:
        home_coords (dict): Dictionary with 'lat' and 'lng' keys
        stores (list): List of store dictionaries with coordinates
        
    Returns:
        pd.DataFrame: Sorted dataframe with store information and distances
    """
    results = []
    
    for store in stores:
        dist_miles = geodesic(
            (home_coords['lat'], home_coords['lng']),
            (store['lat'], store['lng'])
        ).miles
        dist_km = geodesic(
            (home_coords['lat'], home_coords['lng']),
            (store['lat'], store['lng'])
        ).km
        
        results.append({
            'Store Name': store['name'],
            'Address': store['address'],
            'Distance (miles)': round(dist_miles, 2),
            'Distance (km)': round(dist_km, 2),
            'Latitude': store['lat'],
            'Longitude': store['lng']
        })
    
    df = pd.DataFrame(results)
    df = df.sort_values('Distance (miles)')
    return df


def get_route_color(distance):
    """
    Return color based on distance ranges.
    
    Args:
        distance (float): Distance in miles
        
    Returns:
        str: Hex color code
    """
    if distance <= 5:
        return '#00cc00'  # Bright Green
    elif distance <= 15:
        return '#ff9900'  # Orange  
    elif distance <= 30:
        return '#ff6600'  # Dark Orange
    else:
        return '#cc0000'  # Red


def create_ice_cream_trail_map(home_coords, stores_df, output_path='ice_cream_trail_map.html'):
    """
    Create an interactive Folium map with actual driving routes using OSRM API.
    
    Args:
        home_coords (dict): Home coordinates with 'lat' and 'lng' keys
        stores_df (pd.DataFrame): DataFrame with store information
        output_path (str): Path to save the HTML map
        
    Returns:
        folium.Map: The created map object
    """
    # Create base map
    m = folium.Map(
        location=[42.2, -71.8],
        zoom_start=8,
        tiles='CartoDB Voyager'
    )
    
    # Add Massachusetts state boundary
    print("📍 Loading Massachusetts state boundary...")
    try:
        ma_geojson_url = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"
        
        def style_function(feature):
            if feature['properties']['name'] == 'Massachusetts':
                return {
                    'fillColor': '#e3f2fd',
                    'color': '#1976d2',
                    'weight': 3,
                    'fillOpacity': 0.15
                }
            else:
                return {
                    'fillColor': 'transparent',
                    'color': 'transparent',
                    'weight': 0,
                    'fillOpacity': 0
                }
        
        folium.GeoJson(
            ma_geojson_url,
            style_function=style_function,
            highlight_function=None,
            tooltip=None,
            popup=None,
            show=True,
            overlay=True,
            control=False,
            smooth_factor=1.0
        ).add_to(m)
        
        print("  ✅ Massachusetts boundary loaded!")
    except Exception as e:
        print(f"  ⚠️ Could not load state boundary: {e}")
    
    # Add home marker
    folium.Marker(
        [home_coords['lat'], home_coords['lng']],
        popup='<b style="font-size:16px">🏠 HOME BASE</b><br><i>Highland St, Worcester, MA</i>',
        icon=folium.Icon(color='red', icon='home', prefix='fa', icon_color='white'),
        tooltip='🏠 Start Here!'
    ).add_to(m)
    
    print("🚗 Fetching actual driving routes from OSRM...")
    
    # Draw routes with actual road paths
    route_num = 1
    successful_routes = 0
    
    for idx, row in stores_df.iterrows():
        distance = row['Distance (miles)']
        route_color = get_route_color(distance)
        
        try:
            # Get actual driving route from OSRM public API
            url = f"http://router.project-osrm.org/route/v1/driving/{home_coords['lng']},{home_coords['lat']};{row['Longitude']},{row['Latitude']}"
            params = {
                'overview': 'full',
                'geometries': 'geojson'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data['code'] == 'Ok' and len(data['routes']) > 0:
                    # Extract route geometry
                    route_coords = data['routes'][0]['geometry']['coordinates']
                    route_coords = [[coord[1], coord[0]] for coord in route_coords]
                    
                    # Get driving distance and duration
                    route_distance_meters = data['routes'][0]['distance']
                    route_duration_seconds = data['routes'][0]['duration']
                    route_miles = route_distance_meters / 1609.34
                    route_minutes = route_duration_seconds / 60
                    
                    # Draw the actual route
                    folium.PolyLine(
                        locations=route_coords,
                        color=route_color,
                        weight=4,
                        opacity=0.85,
                        popup=f"<b>{row['Store Name']}</b><br>🚗 {route_miles:.1f} miles<br>⏱️ {route_minutes:.0f} min drive",
                        tooltip=f"Route #{route_num}: {row['Store Name']} - {route_miles:.1f} mi"
                    ).add_to(m)
                    
                    successful_routes += 1
                    print(f"  ✅ Route {route_num}: {row['Store Name']} - {route_miles:.1f} miles")
                else:
                    # Fallback to straight line
                    folium.PolyLine(
                        locations=[
                            [home_coords['lat'], home_coords['lng']],
                            [row['Latitude'], row['Longitude']]
                        ],
                        color=route_color,
                        weight=3,
                        opacity=0.6,
                        dash_array='5, 5',
                        popup=f"<b>{row['Store Name']}</b><br>📍 ~{distance} miles",
                        tooltip=f"Route #{route_num}: {row['Store Name']}"
                    ).add_to(m)
            
            # Rate limiting
            time.sleep(0.3)
            
        except Exception as e:
            print(f"  ⚠️ Error for {row['Store Name']}: {str(e)}")
            # Fallback to straight line
            folium.PolyLine(
                locations=[
                    [home_coords['lat'], home_coords['lng']],
                    [row['Latitude'], row['Longitude']]
                ],
                color=route_color,
                weight=3,
                opacity=0.6,
                dash_array='5, 5',
                popup=f"<b>{row['Store Name']}</b><br>📍 ~{distance} miles",
                tooltip=f"Route #{route_num}: {row['Store Name']}"
            ).add_to(m)
        
        # Add store marker
        folium.Marker(
            [row['Latitude'], row['Longitude']],
            popup=f'''
            <div style="width:220px">
                <b style="font-size:16px">🍦 #{route_num}: {row['Store Name']}</b><br>
                <i>{row['Address']}</i><br>
                <hr style="margin:5px 0">
                📍 {distance} miles away
            </div>
            ''',
            icon=folium.Icon(color='blue', icon='ice-cream', prefix='fa', icon_color='white'),
            tooltip=f"🍦 #{route_num}: {row['Store Name']}"
        ).add_to(m)
        
        route_num += 1
    
    # Add legend
    legend_html = '''
    <div style="position: fixed; 
                bottom: 20px; right: 20px; width: 180px; 
                background: rgba(255,255,255,0.97); 
                border: 3px solid #667eea; z-index:9999; 
                font-size:12px; padding: 10px; border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.4);">
        <p style="margin:0 0 8px 0; font-weight: bold; text-align: center; 
                  font-size: 14px; color: #667eea; border-bottom: 2px solid #ddd; padding-bottom: 6px;">
            🍦 Ice Cream Trail
        </p>
        <p style="margin: 6px 0; font-size: 11px;">
            <i class="fa fa-home" style="color:red"></i> Home
        </p>
        <p style="margin: 6px 0; font-size: 11px;">
            <i class="fa fa-ice-cream" style="color:blue"></i> Ice Cream Stores
        </p>
        <p style="margin: 6px 0 4px 0; font-weight: bold; font-size: 11px; 
                  border-top: 1px solid #ddd; padding-top: 6px;">
            Distance Colors:
        </p>
        <p style="margin: 4px 0; font-size: 11px; display: flex; align-items: center;">
            <span style="display: inline-block; width: 30px; height: 5px; 
                         background: #00cc00; margin-right: 8px; border-radius: 2px;"></span>
            <span>0-5 miles</span>
        </p>
        <p style="margin: 4px 0; font-size: 11px; display: flex; align-items: center;">
            <span style="display: inline-block; width: 30px; height: 5px; 
                         background: #ff9900; margin-right: 8px; border-radius: 2px;"></span>
            <span>5-15 miles</span>
        </p>
        <p style="margin: 4px 0; font-size: 11px; display: flex; align-items: center;">
            <span style="display: inline-block; width: 30px; height: 5px; 
                         background: #ff6600; margin-right: 8px; border-radius: 2px;"></span>
            <span>15-30 miles</span>
        </p>
        <p style="margin: 4px 0; font-size: 11px; display: flex; align-items: center;">
            <span style="display: inline-block; width: 30px; height: 5px; 
                         background: #cc0000; margin-right: 8px; border-radius: 2px;"></span>
            <span>30+ miles</span>
        </p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Add title
    title_html = '''
    <div style="position: fixed; 
                top: 10px; left: 50%; transform: translateX(-50%); 
                background: rgba(255,255,255,0.97); 
                padding: 10px 25px; border-radius: 25px;
                box-shadow: 0 3px 10px rgba(0,0,0,0.3);
                z-index: 9999;">
        <h3 style="margin:0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   background-clip: text; font-family: Arial, sans-serif;
                   text-align: center; font-size: 20px; font-weight: bold;">
            Ice Cream Trail
        </h3>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    print(f"\n✅ Map created with {successful_routes}/{len(stores_df)} actual driving routes!")
    
    # Save the map
    m.save(output_path)
    print(f"\n💾 Map saved to: {output_path}")
    
    return m


def print_summary_statistics(stores_df):
    """
    Print summary statistics about the ice cream trail.
    
    Args:
        stores_df (pd.DataFrame): DataFrame with store information
    """
    total_one_way = stores_df['Distance (miles)'].sum()
    total_round_trip = total_one_way * 2
    avg_distance = stores_df['Distance (miles)'].mean()
    closest = stores_df.iloc[0]
    farthest = stores_df.iloc[-1]
    
    print("\n" + "=" * 80)
    print("🚗 ICE CREAM TRAIL SUMMARY 🍦")
    print("=" * 80)
    print(f"\nTotal Stores: {len(stores_df)}")
    print(f"Total One-Way Distance: {total_one_way:.1f} miles")
    print(f"Total Round-Trip Distance: {total_round_trip:.1f} miles")
    print(f"Average Distance: {avg_distance:.1f} miles")
    print(f"\nClosest Store: {closest['Store Name']} ({closest['Distance (miles)']} miles)")
    print(f"Farthest Store: {farthest['Store Name']} ({farthest['Distance (miles)']} miles)")
    print("\n" + "=" * 80 + "\n")


def main():
    """
    Main execution function.
    """
    print("🍦 Ice Cream Trail Mapper - Massachusetts Edition 🗺️\n")
    
    # Calculate distances
    print("📏 Calculating distances to ice cream stores...")
    stores_df = calculate_distances(HOME_COORDS, ICE_CREAM_STORES)
    print(f"✅ Found {len(stores_df)} ice cream stores\n")
    
    # Print summary
    print_summary_statistics(stores_df)
    
    # Create map
    print("🗺️ Creating interactive map...\n")
    create_ice_cream_trail_map(HOME_COORDS, stores_df)
    
    print("\n🎉 All done! Open ice_cream_trail_map.html in your browser to view the map.")
    print("\n💡 Pro tip: Upload to GitHub Pages for a live interactive map!\n")


if __name__ == "__main__":
    main()
