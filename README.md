# Ice Cream Trail Mapper - Massachusetts Edition

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An interactive map visualization project that calculates and displays driving routes from Worcester, MA to 10 ice cream stores across Massachusetts. Built with Python, Folium, and the OSRM routing API.

![Ice Cream Trail Map](https://img.shields.io/badge/Status-Complete-success)

## Project Overview

This project creates a visually appealing, interactive map that shows:
- **Real driving routes** (not straight lines!) to 10 ice cream stores
- **Color-coded distances** based on proximity
- **Drive times** and distances for each route
- **Interactive popups** with store information
- **Massachusetts state boundary** for geographic context

### Key Features

* **Interactive Map**: Built with Folium for smooth pan/zoom functionality
* **Real Routes**: Uses OSRM API for actual driving directions
* **Color-Coded**: Green (0-5 mi), Orange (5-15 mi), Dark Orange (15-30 mi), Red (30+ mi)
* **10 Ice Cream Stores**: Carefully selected across Massachusetts
* **Summary Statistics**: Total distance, averages, closest/farthest stores
* **No API Keys Required**: Uses free OSRM public API

## Preview

The generated map includes:
- Home marker (red house icon) at Highland St, Worcester
- 10 ice cream store markers (blue ice cream icons)
- Colored routes following actual roads
- Professional legend and title overlay
- Massachusetts state outline

## Tech Stack

- **Python 3.8+**
- **Folium**: Interactive map visualization
- **Pandas**: Data manipulation and analysis
- **Geopy**: Geographic distance calculations
- **Requests**: HTTP requests to OSRM API
- **OSRM**: Open Source Routing Machine for driving routes

## Requirements

See `requirements.txt` for the full list of dependencies.

```txt
pandas>=1.3.0
folium>=0.12.0
geopy>=2.2.0
requests>=2.26.0
```

## Getting Started

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ahmadratth/ice-cream-trail-mapper.git
   cd ice-cream-trail-mapper
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Usage

**Run the script:**
```bash
python ice_cream_trail.py
```

This will:
1. Calculate distances to all ice cream stores
2. Fetch actual driving routes from OSRM
3. Generate an interactive HTML map (`ice_cream_trail_map.html`)
4. Print summary statistics

**Open the map:**
```bash
# On macOS
open ice_cream_trail_map.html

# On Linux
xdg-open ice_cream_trail_map.html

# On Windows
start ice_cream_trail_map.html
```

## Ice Cream Stores Included

1. **Gibby's Famous Ice Cream** - Worcester, MA (2.4 mi)
2. **Swirls and Scoops** - North Grafton, MA (7.9 mi)
3. **Pinecroft Dairy and Restaurant** - West Boylston, MA (8.3 mi)
4. **Rota Spring Farm** - Sterling, MA (14.4 mi)
5. **West End Creamery** - Whitinsville, MA (14.2 mi)
6. **Alvin Rondeau's Dairy Bar** - Palmer, MA (36.7 mi)
7. **Murdock Farm and Dairy Bar** - Winchendon, MA (37.1 mi)
8. **Shaw Farm Dairy** - Dracut, MA (44.1 mi)
9. **Joyful Scoops** - Middleborough, MA (62.4 mi)
10. **High Lawn Farm** - Lee, MA (87.9 mi)

**Total Distance**: 529.7 miles (round-trip to visit all 10 stores)

## Customization

### Change Home Location

Edit the `HOME_COORDS` dictionary in `ice_cream_trail.py`:

```python
HOME_COORDS = {'lat': YOUR_LATITUDE, 'lng': YOUR_LONGITUDE}
```

### Add More Stores

Add entries to the `ICE_CREAM_STORES` list:

```python
ICE_CREAM_STORES.append({
    "name": "Store Name",
    "address": "Full Address",
    "lat": LATITUDE,
    "lng": LONGITUDE
})
```

### Change Map Style

Modify the `tiles` parameter in `create_ice_cream_trail_map()`:

```python
m = folium.Map(
    location=[42.2, -71.8],
    zoom_start=8,
    tiles='OpenStreetMap'  # Options: 'OpenStreetMap', 'CartoDB Positron', etc.
)
```

## Deploy to GitHub Pages

1. **Create a new repo** on GitHub
2. **Push your code**:
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```
3. **Run the script** to generate `ice_cream_trail_map.html`
4. **Rename the file** to `index.html`
5. **Go to Settings** → **Pages** → **Deploy from branch** → **main** → **/(root)**
6. **Your live map** will be at: `https://ahmadratth.github.io/ice-cream-trail-mapper/`

## 📈 Project Structure

```
ice-cream-trail-mapper/
│
├── ice_cream_trail.py       # Main script
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .gitignore               # Git ignore rules
└── ice_cream_trail_map.html # Generated map (after running script)
```

## Contributing

Contributions are welcome! Feel free to:
- Add more ice cream stores
- Improve the map styling
- Add new features (route optimization, weather data, etc.)
- Fix bugs

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **OSRM Project**: For the free routing API
- **Folium**: For the excellent Python mapping library
- **OpenStreetMap**: For map data
- **PublicaMundi**: For US states GeoJSON data

## Future Improvements

- [ ] Add route optimization (shortest path to visit all stores)
- [ ] Include store ratings and reviews
- [ ] Add weather data integration
- [ ] Create a web interface for custom locations
- [ ] Add export to PDF/PNG functionality
- [ ] Include traffic data for route timing

## 📧 Contact

**Ahmad Ehtesham**
- GitHub: [@ahmadratth](https://github.com/ahmadratth)
- LinkedIn: [Connect with me](www.linkedin.com/in/mabe475)
- Email: ahmadehtesham10@gmail.com

---

⭐ If you found this project helpful, consider giving it a star on GitHub!

🍦 Happy ice cream hunting! 🍦
