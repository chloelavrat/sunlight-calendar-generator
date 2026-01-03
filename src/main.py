from datetime import date, datetime, timedelta
import pytz
from astral import LocationInfo
from astral.sun import sun
from icalendar import Calendar, Event

# -----------------------------
# CONFIG
# -----------------------------
CITY = "Rovaniemi"
COUNTRY = "Finland"
LATITUDE = 66.5039
LONGITUDE = 25.7294
TIMEZONE = "Europe/Helsinki"

START_DATE = date(2026, 1, 5)
END_DATE   = date(2026, 3, 2)

OUTPUT_FILE = "rovaniemi_daylight.ics"
# -----------------------------

tz = pytz.timezone(TIMEZONE)

location = LocationInfo(
    name=CITY,
    region=COUNTRY,
    timezone=TIMEZONE,
    latitude=LATITUDE,
    longitude=LONGITUDE
)

cal = Calendar()
cal.add("prodid", "-//Rovaniemi Daylight Calendar//")
cal.add("version", "2.0")

current_date = START_DATE

while current_date <= END_DATE:
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
            f"📍 Location: {CITY}, {COUNTRY}\n"
            f"🌐 Coordinates: {LATITUDE}°N, {LONGITUDE}°E\n"
            f"🕐 Timezone: {TIMEZONE}\n"
            f"\n"
            f"🌅 Sunrise: {sunrise.strftime('%H:%M:%S')}\n"
            f"🌇 Sunset: {sunset.strftime('%H:%M:%S')}\n"
            f"⏱️  Daylight Duration: {hours} hours {minutes} minutes\n"
            f"\n"
            f"📅 Date: {current_date.strftime('%A, %B %d, %Y')}\n"
            f"\n"
            f"💝 Made with love by Chloé"
        )

        # Timed event from sunrise to sunset
        event.add("dtstart", sunrise)
        event.add("dtend", sunset)
        event.add("dtstamp", datetime.now(tz))

        cal.add_component(event)

    except Exception:
        # Polar night / midnight sun → no sunrise or sunset
        event = Event()
        event.add("summary", "🌑 Polar Night / Midnight Sun")
        event.add(
            "description",
            "No sunrise or sunset on this day in Rovaniemi."
        )
        event.add("dtstart", current_date)
        event.add("dtend", current_date + timedelta(days=1))
        event.add("dtstamp", datetime.now(tz))

        cal.add_component(event)

    current_date += timedelta(days=1)

# Write file
with open(OUTPUT_FILE, "wb") as f:
    f.write(cal.to_ical())

print(f"iCal file generated: {OUTPUT_FILE}")

