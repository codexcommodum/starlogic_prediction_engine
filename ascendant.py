"""
Compute the ecliptic ascendant (rising sign + degree) from birth data.
Pure math - no external astronomy library required.

Formula references:
- Jean Meeus, "Astronomical Algorithms", 2nd ed., Ch. 12-13
- Standard tropical-zodiac Placidus-equivalent ascendant
"""
import math
from datetime import datetime, timedelta

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]


def julian_day(year: int, month: int, day: int, hour_utc: float) -> float:
    """Compute Julian Day Number for a UTC instant."""
    if month <= 2:
        year -= 1
        month += 12
    a = math.floor(year / 100)
    b = 2 - a + math.floor(a / 4)
    jd = (
        math.floor(365.25 * (year + 4716))
        + math.floor(30.6001 * (month + 1))
        + day
        + hour_utc / 24.0
        + b
        - 1524.5
    )
    return jd


def greenwich_sidereal_time(jd: float) -> float:
    """Return Greenwich Mean Sidereal Time in degrees (0-360)."""
    t = (jd - 2451545.0) / 36525.0
    gmst_deg = (
        280.46061837
        + 360.98564736629 * (jd - 2451545.0)
        + 0.000387933 * t * t
        - (t ** 3) / 38710000.0
    )
    gmst_deg = gmst_deg % 360.0
    if gmst_deg < 0:
        gmst_deg += 360.0
    return gmst_deg


def obliquity(jd: float) -> float:
    """Return true obliquity of the ecliptic in degrees for the given JD."""
    t = (jd - 2451545.0) / 36525.0
    eps = (
        23.43929111
        - 0.013004167 * t
        - 1.63889e-7 * t * t
        + 5.03611e-7 * t * t * t
    )
    return eps


def compute_ascendant(
    birth_date: str,
    birth_time: str,
    latitude: float,
    longitude: float,
    timezone_offset: float,
) -> dict:
    """
    Compute the ascending sign + degree for given birth data.

    Inputs:
      birth_date: "YYYY-MM-DD"
      birth_time: "HH:MM" (24-hour local time)
      latitude:   degrees, north positive
      longitude:  degrees, east positive (west negative)
      timezone_offset: hours east of UTC (e.g., -8 for PST, +7 for ICT)

    Returns:
      {
        "sign": "Libra",
        "degree": 14.73,    # 0-30 within the sign
        "longitude": 194.73 # 0-360 along ecliptic
      }
    """
    # Parse
    y, m, d = [int(x) for x in birth_date.split("-")]
    hh, mm = [int(x) for x in birth_time.split(":")]
    hour_local = hh + mm / 60.0
    hour_utc = hour_local - timezone_offset

    # Handle UTC date rollover
    dt_utc = datetime(y, m, d) + timedelta(hours=hour_utc)
    y_u, m_u, d_u = dt_utc.year, dt_utc.month, dt_utc.day
    hour_utc_adj = dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0

    # Julian day
    jd = julian_day(y_u, m_u, d_u, hour_utc_adj)

    # Local sidereal time (in degrees)
    gmst = greenwich_sidereal_time(jd)
    lst_deg = (gmst + longitude) % 360.0

    # Obliquity of ecliptic
    eps = obliquity(jd)

    # Convert to radians
    lst_rad = math.radians(lst_deg)
    eps_rad = math.radians(eps)
    lat_rad = math.radians(latitude)

    # Ascendant formula (Meeus eq. 13.5, standard form):
    #   tan(lambda_asc) = -cos(LST) / (sin(eps)*tan(phi) + cos(eps)*sin(LST))
    y_num = -math.cos(lst_rad)
    x_den = math.sin(eps_rad) * math.tan(lat_rad) + math.cos(eps_rad) * math.sin(lst_rad)
    asc_rad = math.atan2(y_num, x_den)
    asc_deg = math.degrees(asc_rad) % 360.0

    # Ensure ascendant is in the eastern hemisphere
    # (atan2 can land on the opposite point; adjust by 180 if needed by checking MC)
    # The standard check: ascendant should be >= MC by convention (rising > culminating)
    # Meeus' formula with atan2 above gives the correct quadrant directly.

    sign_idx = int(asc_deg // 30)
    degree_in_sign = asc_deg - (sign_idx * 30)

    return {
        "sign": SIGNS[sign_idx],
        "degree": round(degree_in_sign, 4),
        "longitude": round(asc_deg, 4),
    }


def determine_sect(sun_longitude: float, ascendant_longitude: float) -> str:
    """
    Determine sect (day/night) from Sun and Ascendant ecliptic longitudes.

    Classical rule:
    - Sun ABOVE horizon (houses 7-12 in traditional count, i.e.
      ascendant to descendant going through MC) = DAY sect
    - Sun BELOW horizon (houses 1-6) = NIGHT sect

    Simpler equivalent: compute the angle from ASC to Sun going clockwise
    through MC. If Sun's ecliptic longitude is 0-180 degrees ahead of ASC
    (measuring westward in the sky, which is counterclockwise in ecliptic
    coordinates), Sun is above the horizon = DAY.

    Returns "day" or "night".
    """
    diff = (sun_longitude - ascendant_longitude) % 360.0
    # Sun above horizon: it culminates 90 degrees past ASC, descends at 180 past ASC.
    # In ecliptic longitude, "past ASC" going westward is DECREASING longitude mod 360.
    # So Sun is above horizon when (ASC - Sun) mod 360 is between 0 and 180.
    asc_to_sun_west = (ascendant_longitude - sun_longitude) % 360.0
    return "day" if 0 < asc_to_sun_west < 180 else "night"
