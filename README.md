# TridentAPI
Official TridentAPI
___

* **TridentAPI** - API for meteo-projects based on meteorological indexes (CAPE, CIN, ...). The API allows you to get the values of these meteo-indexes.
* **Base TridentAPI stack**: ```pip install fastapi siphon metpy```
___
# Endpoints
* **/get** - To get meteo-indexes.

# Params
```python
params = {
    'year': 2013,
    'month': 5,
    'day': 31,
    'hour_utc': 12,
    'station': 72357,
    'is_round': True
}
```
**EXAMPLE**
* **year: int, month: int, day: int, hour_utc: int, station: int, is_round: bool**
___

_Thanks for reading._