import streamlit as st
from datetime import date, datetime, timedelta
import pytz
from astral import LocationInfo
from astral.sun import sun
import json
from icalendar import Calendar, Event


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
                event.add(
                    "description",
                    f"📍 Location: {city}, {country}\n"
                    f"🌐 Coordinates: {latitude}°N, {longitude}°E\n"
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
                event = Event()
                event.add("summary", "🌑 Polar Night / Midnight Sun")
                event.add(
                    "description",
                    f"📍 Location: {city}, {country}\n"
                    f"🌐 Coordinates: {latitude}°N, {longitude}°E\n"
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


st.set_page_config(page_title="Daylight Calendar Generator", page_icon=":sunny:")
st.image("banner.png", width='stretch')
st.subheader("Track sunrise, sunset, and daylight hours")
st.markdown("""
**Sometimes light is a resource that needs to be optimized!**

Whether you're a **photographer** scheduling shoots in perfect sunlight, or you want to **align your calendar and daily life** with the sun's rhythm, this tool **generates iCal calendar files** with daily daylight information for any location.

Perfect for **planning trips** to high latitude locations, **tracking seasonal daylight changes**, or **optimizing your schedule** around sunrise and sunset times.
""")

st.divider()

st.subheader("Generate your calendar")

# Load locations from JSON file
with open("locations.json", "r", encoding="utf-8") as f:
    LOCATIONS = json.load(f)

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
    st.balloons()

# Footer banner - fixed at bottom
st.markdown(
    """
    <style>
    a:link, a:visited {
        color: blue;
        background-color: transparent;
        text-decoration: underline;
    }
    a:hover, a:active {
        color: red;
        background-color: transparent;
        text-decoration: underline;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f0f2f6;
        color: #666;
        text-align: center;
        padding: 15px 0;
        border-top: 1px solid #e0e0e0;
    }
    </style>
    <div class="footer">
        <p style="margin: 0;">☀️ Made with love by <a href="https://chloelavrat.com" target="_blank"><bold>Chloé Lavrat</bold></a> ❤️</p>
    </div>
    """,
    unsafe_allow_html=True
)

