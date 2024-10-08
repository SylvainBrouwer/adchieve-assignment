import requests
import urllib


API_URL = "https://api.tomtom.com"


def geocode(query:str, api_key:str=None, **kwargs) -> list[dict]:
    """
    Query TomTom geocoding api endpoint.
    """
    query_quoted = urllib.parse.quote_plus(query)
    kwargs["key"] = api_key
    url = API_URL + "/search/2/geocode/" + query_quoted + ".json"
    try:
        response = requests.get(url, params=kwargs)
        response.raise_for_status()
        return response.json()["results"]        
    except requests.exceptions.HTTPError as httperr:
        print("HTTP Error")
        print(httperr.args[0])



def geocode_positions(query:str, api_key:str=None, **kwargs) -> list[dict]:
    """
    Query TomTom geocoding api endpoint, return only the found positions.
    Results are ordered by match confidence, descending.
    """
    results = geocode(query, api_key=api_key, **kwargs)
    if (results):
        positions = [r["position"] for r in results]
        confidences = [r["matchConfidence"]["score"]for r in results]
        return [p for _, p in sorted(zip(confidences, positions), key=lambda x: x[0], reverse=True)]
    return []


