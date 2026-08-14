from fastapi import FastAPI
from siphon.simplewebservice.wyoming import WyomingUpperAir as wua
from datetime import datetime
from metpy.units import units
from metpy import calc
from math import isnan


def smart_round(parameter):
    if isnan(float(parameter)):
        return None
    else:
        return round(parameter)


app = FastAPI()

@app.get('/get')
def get_data(year: int, month: int, day: int, hour_utc: int, station: int, is_round: bool) -> dict:
    try:
        date = datetime(year, month, day, hour_utc)
    except ValueError:
        return {"status": "error", "message": "Incorrect date or date format."}
    except OverflowError:
        return {"status": "error", "message": "The one of date parameter is too long."}

    try:
        data = wua.request_data(date, station)
    except ValueError:
        return {"status": "error", "message": "Incorrect hour (only 0 or 12 UTC) or incorrect station number or there is no data for this time."}
    except ConnectionError:
        return {"status": "error", "message": "Connection error."}
    
    temperature = data['temperature'].values * units.degC
    dewpoint = data['dewpoint'].values * units.degC
    pressure = data['pressure'].values * units.hPa
    u_wind, v_wind = data['u_wind'].values * units.knot, data['v_wind'].values * units.knot
    height = data['height'].values * units.meters

    parcel_profile = calc.parcel_profile(pressure, temperature[0], dewpoint[0])
    cape, cin = calc.cape_cin(pressure, temperature, dewpoint, parcel_profile)
    sbcape, sbcin = calc.surface_based_cape_cin(pressure, temperature, dewpoint)
    mucape, mucin = calc.most_unstable_cape_cin(pressure, temperature, dewpoint)
    lcl_p, lcl_t = calc.lcl(pressure[0], temperature[0], dewpoint[0])
    lcl_height = lcl_p * units.meters
    lfc_p, lfc_t = calc.lfc(pressure, temperature, dewpoint)
    el_p, el_t = calc.el(pressure, temperature, dewpoint)
    srh_pos_01, srh_neg_01, srh_01 = calc.storm_relative_helicity(height, u_wind, v_wind, depth=1 * units.km)
    srh_pos_03, srh_neg_03, srh_03 = calc.storm_relative_helicity(height, u_wind, v_wind, depth=3 * units.km)
    u_shear, v_shear = calc.bulk_shear(pressure, u_wind, v_wind, height, depth=6 * units.km)
    bulk_shear_06 = calc.wind_speed(u_shear, v_shear)
    li = calc.lifted_index(pressure, temperature, parcel_profile)
    stp = calc.significant_tornado(sbcape, lcl_height, srh_01, bulk_shear_06)

    result = {
                "temperature": temperature[0].m,
                "dewpoint": dewpoint[0].m,
                "pressure": pressure[0].m,
                "cape": cape.m,
                "cin": cin.m,
                "sbcape": sbcape.m,
                "sbcin": sbcin.m,
                "mucape": mucape.m,
                "mucin": mucin.m,
                "li": li.m,
                "stp": stp.m,
                "lcl_p": lcl_p.m,
                "lcl_t": lcl_t.m,
                "lfc_p": lfc_p.m,
                "lfc_t": lfc_t.m,
                "el_p": el_p.m,
                "el_t": el_t.m,
                "srh_pos_01": srh_pos_01.m,
                "srh_neg_01": srh_neg_01.m,
                "srh_01": srh_01.m,
                "srh_pos_03": srh_pos_03.m,
                "srh_neg_03": srh_neg_03.m,
                "srh_03": srh_03.m,
                "bulk_shear_06": bulk_shear_06.m
            }

    final_result = {}
    do_not_round = ['temperature', 'dewpoint', 'pressure']

    if is_round:
        for key, value in result.items():
            if key not in do_not_round:
                final_result[key] = smart_round(value)
            else:
                final_result[key] = value
        return final_result
    else:
        return result