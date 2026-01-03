import streamlit as st
from datetime import date, datetime, timedelta
import pytz
from astral import LocationInfo
from astral.sun import sun
import json
from icalendar import Calendar, Event


def get_season(date_obj):
    """Determine the season based on the date (Northern Hemisphere)"""
    month = date_obj.month
    day = date_obj.day
    
    # Spring: March 20 - June 20
    # Summer: June 21 - September 21
    # Autumn: September 22 - December 20
    # Winter: December 21 - March 19
    
    if (month == 3 and day >= 20) or month in [4, 5] or (month == 6 and day <= 20):
        return "spring"
    elif (month == 6 and day >= 21) or month in [7, 8] or (month == 9 and day <= 21):
        return "summer"
    elif (month == 9 and day >= 22) or month in [10, 11] or (month == 12 and day <= 20):
        return "autumn"
    else:
        return "winter"


def generate_daylight_calendar(city, country, latitude, longitude, timezone, start_date, end_date):
    try:
        tz = pytz.timezone(timezone)
        
        location = LocationInfo(
            name=city,
            region=country,
            timezone=timezone,
            latitude=latitude,
            longitude=longitude
        )
        
        cal = Calendar()
        cal.add("prodid", f"-//{city} Daylight Calendar//")
        cal.add("version", "2.0")
        
        current_date = start_date
        
        while current_date <= end_date:
            try:
                s = sun(location.observer, date=current_date, tzinfo=tz)
                sunrise = s["sunrise"]
                sunset = s["sunset"]
                daylight_duration = sunset - sunrise
                
                hours, remainder = divmod(daylight_duration.seconds, 3600)
                minutes = remainder // 60
                
                event = Event()
                event.add("summary", f"☀️ Daylight: {hours}h {minutes}min")
                # Format coordinates with correct direction
                lat_dir = "N" if latitude >= 0 else "S"
                lon_dir = "E" if longitude >= 0 else "W"
                
                # Format location string
                location_str = city
                if country:
                    location_str += f", {country}"
                
                event.add(
                    "description",
                    f"📍 Location: {location_str}\n"
                    f"🌐 Coordinates: {abs(latitude):.4f}°{lat_dir}, {abs(longitude):.4f}°{lon_dir}\n"
                    f"🕐 Timezone: {timezone}\n"
                    f"\n"
                    f"🌅 Sunrise: {sunrise.strftime('%H:%M:%S')}\n"
                    f"🌇 Sunset: {sunset.strftime('%H:%M:%S')}\n"
                    f"⏱️  Daylight Duration: {hours} hours {minutes} minutes\n"
                    f"\n"
                    f"📅 Date: {current_date.strftime('%A, %B %d, %Y')}\n"
                    f"\n"
                    f"💝 Made with love by Chloé"
                )
                
                event.add("dtstart", sunrise)
                event.add("dtend", sunset)
                event.add("dtstamp", datetime.now(tz))
                
                cal.add_component(event)
                
            except Exception:
                # Polar night / midnight sun
                # Format coordinates with correct direction
                lat_dir = "N" if latitude >= 0 else "S"
                lon_dir = "E" if longitude >= 0 else "W"
                
                # Format location string
                location_str = city
                if country:
                    location_str += f", {country}"
                
                event = Event()
                event.add("summary", "🌑 Polar Night / Midnight Sun")
                event.add(
                    "description",
                    f"📍 Location: {location_str}\n"
                    f"🌐 Coordinates: {abs(latitude):.4f}°{lat_dir}, {abs(longitude):.4f}°{lon_dir}\n"
                    f"\n"
                    f"No sunrise or sunset on this day.\n"
                    f"\n"
                    f"📅 Date: {current_date.strftime('%A, %B %d, %Y')}\n"
                    f"\n"
                    f"💝 Made with love by Chloé"
                )
                event.add("dtstart", current_date)
                event.add("dtend", current_date + timedelta(days=1))
                event.add("dtstamp", datetime.now(tz))
                
                cal.add_component(event)
            
            current_date += timedelta(days=1)
        
        return cal.to_ical()
    
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None


# Load page configuration from secrets
page_title = st.secrets.get("page", {}).get("page_title", "Daylight Calendar Generator")
page_icon = st.secrets.get("page", {}).get("page_icon", "☀️")

st.set_page_config(page_title=page_title, page_icon=page_icon, layout="centered")

# Hide menu if configured
hide_menu_style = st.secrets.get("page", {}).get("hide_menu_style", "")
if hide_menu_style:
    st.markdown(hide_menu_style, unsafe_allow_html=True)

st.image("assets/banner.png", width='stretch')
st.subheader("Track sunrise, sunset, and daylight hours")
st.markdown("""
**Sometimes light is a resource that needs to be optimized!**

Whether you're a **photographer** scheduling shoots in perfect sunlight, or you want to **align your calendar and daily life** with the sun's rhythm, this tool **generates iCal calendar files** with daily daylight information for any location.

Perfect for **planning trips** to high latitude locations, **tracking seasonal daylight changes**, or **optimizing your schedule** around sunrise and sunset times.
""")

st.divider()

st.subheader("Generate your calendar")

# Location input mode selection
location_mode = st.radio(
    "Location input method",
    ["Pre-configured city", "Custom coordinates"],
    horizontal=True
)

# Load locations from JSON file
with open("locations.json", "r", encoding="utf-8") as f:
    LOCATIONS = json.load(f)

if location_mode == "Pre-configured city":
    # City selection with autocomplete
    all_cities = sorted(LOCATIONS.keys())
    default_index = all_cities.index("Rovaniemi") if "Rovaniemi" in all_cities else 0
    selected_city = st.selectbox("City", all_cities, index=default_index)
    
    # Get location info from JSON
    location_data = LOCATIONS[selected_city]
    city = selected_city
    country = location_data["country"]
    latitude = location_data["latitude"]
    longitude = location_data["longitude"]
    default_timezone = location_data["timezone"]
    
    # Display the location details (updates immediately when city changes)
    st.info(f"Location: {city}, {country} | Coordinates: {latitude:.2f}, {longitude:.2f}")
else:
    # Custom coordinates input
    st.markdown("**Enter custom location coordinates:**")
    
    col1, col2 = st.columns(2)
    with col1:
        latitude = st.number_input(
            "Latitude",
            min_value=-90.0,
            max_value=90.0,
            value=66.5039,
            step=0.0001,
            format="%.4f",
            help="Latitude ranges from -90 (South Pole) to 90 (North Pole)"
        )
    with col2:
        longitude = st.number_input(
            "Longitude",
            min_value=-180.0,
            max_value=180.0,
            value=25.7294,
            step=0.0001,
            format="%.4f",
            help="Longitude ranges from -180 to 180 degrees. 0 at Greenwich (Prime Meridian)"
        )
    
    col3, col4 = st.columns(2)
    with col3:
        city = st.text_input("City name", value="", help="Required: Used for display purposes in the calendar")
    with col4:
        country = st.text_input("Country name", value="", help="Required: Used for display purposes in the calendar")
    
    # Default timezone for custom location (can be changed by user)
    default_timezone = "UTC"
    
    # Display the location details
    location_parts = []
    if city:
        location_parts.append(f"Location: {city}")
        if country:
            location_parts[-1] += f", {country}"
    location_parts.append(f"Coordinates: {latitude:.4f}, {longitude:.4f}")
    st.info(" | ".join(location_parts))

# Timezone selector with UTC offset
all_timezones = pytz.all_timezones

def get_utc_offset(tz_name):
    """Get UTC offset string for a timezone"""
    try:
        tz = pytz.timezone(tz_name)
        now = datetime.now(tz)
        offset = now.strftime('%z')
        if offset:
            # Format as UTC+HH:MM or UTC-HH:MM
            hours = int(offset[:3])
            minutes = int(offset[3:])
            if minutes == 0:
                return f"UTC{hours:+d}" if hours != 0 else "UTC"
            else:
                return f"UTC{hours:+d}:{minutes:02d}"
        return "UTC"
    except:
        return "UTC"

# Create timezone options with UTC offset
timezone_options = [f"{tz} ({get_utc_offset(tz)})" for tz in all_timezones]
timezone_index = all_timezones.index(default_timezone) if default_timezone in all_timezones else 0
selected_timezone_display = st.selectbox("Timezone", timezone_options, index=timezone_index)

# Extract the actual timezone name (remove the UTC offset part)
timezone = selected_timezone_display.split(" (")[0]

# Date range inputs
today = date.today()
end_date_default = today + timedelta(days=60)  # Approximately 2 months

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", value=today, format="DD/MM/YYYY")
with col2:
    end_date = st.date_input("End Date", value=end_date_default, format="DD/MM/YYYY")

ical_content = None

if st.button("Generate", type="primary"):
    if start_date > end_date:
        st.error("Start date must be before end date!")
    elif location_mode == "Custom coordinates" and (not city or not city.strip()):
        st.error("City name is required!")
    elif location_mode == "Custom coordinates" and (not country or not country.strip()):
        st.error("Country name is required!")
    else:
        ical_content = generate_daylight_calendar(
            city, country, latitude, longitude, timezone, start_date, end_date
        )
        if ical_content:
            st.success("Daylight calendar generated successfully!")

if ical_content:
    st.download_button(
        label="Download Calendar",
        data=ical_content,
        file_name="daylight_calendar.ics",
        mime="text/calendar"
    )
    # Show seasonal celebration animation
    current_season = get_season(date.today())
    if current_season in ["autumn", "winter"]:
        st.snow()
    else:  # spring or summer
        st.balloons()

# Footer banner - fixed at bottom (from secrets)
footer = st.secrets.get("page", {}).get("footer", "")
if footer:
    st.markdown(footer, unsafe_allow_html=True)

