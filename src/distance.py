import math

def haversine_distance(a:dict[str, float], b:dict[str, float], r:float=6371e3) -> float:
    """
    Calculate the haversine distance between two points on a sphere.
    ### Parameters
    - `a:dict[str, float]` : {"lat": float, "lon": float} of point a, in degrees.
    - `b:dict[str, float]` : {"lat": float, "lon": float} of point b, in degrees.
    - `r:float=6371e3` : radius of the sphere, defaults to radius of the earth.
    """
    dlat = math.radians(b["lat"] - a["lat"])
    latm = math.radians(b["lat"] + a["lat"]) / 2
    dlon = math.radians(b["lon"] - a["lon"])
    haversine = 2 * r * math.asin(
        math.sqrt(
            (math.sin(dlat/2)**2 * math.cos(dlon/2)**2) + (math.cos(latm)**2 * math.sin(dlon/2)**2)
        )
    )
    return haversine

