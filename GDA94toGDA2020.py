#!/usr/bin/env python3

# Script to convert GDA94 decimal coordinates to GDA2020 decimal coordinates

from math import radians, sin, cos, sqrt, atan, pi


def gda94to2020(input_latitude, input_longitude, input_height):
    # Ellipsoid variables
    a = 6378137
    f1 = 298.257222101
    f = 1 / f1
    e2 = 2 * f - f * f
    # Transformation variables
    tx = 0.06155
    ty = -0.01087
    tz = -0.04019
    rx = radians(-0.0394924 / 3600)
    ry = radians(-0.0327221 / 3600)
    rz = radians(-0.0328979 / 3600)
    scale = 1 + (-0.009994 / 1000000)

    # Convert lat long to radians
    lat_r = radians(input_latitude)  # input_latitude / 180 * pi
    lon_r = radians(input_longitude)  # input_longitude / 180 * pi

    # Convert Geodetic coordinates to Cartesian coordinates
    v = a / sqrt(1 - e2 * sin(lat_r) * sin(lat_r))
    x = (v + input_height) * cos(lat_r) * cos(lon_r)
    y = (v + input_height) * cos(lat_r) * sin(lon_r)
    z = ((1 - e2) * v + input_height) * sin(lat_r)

    # Transformation from GDA94 to GDA2020
    xs = ((cos(ry) * cos(rz)) * x + (cos(ry) * sin(rz)) * y + (-sin(ry) * z)) * scale + tx
    ys = ((sin(rx) * sin(ry) * cos(rz) - cos(rx) * sin(rz)) * x
          + (sin(rx) * sin(ry) * sin(rz) + cos(rx) * cos(rz)) * y
          + (sin(rx) * cos(ry)) * z) * scale + ty
    zs = ((cos(rx) * sin(ry) * cos(rz) + sin(rx) * sin(rz)) * x
          + (cos(rx) * sin(ry) * sin(rz) - sin(rx) * cos(rz)) * y
          + (cos(rx) * cos(ry)) * z) * scale + tz

    # Convert Cartesian coordinates to Geodetic coordinates
    p = sqrt(xs * xs + ys * ys)
    r = sqrt(p * p + zs * zs)
    u = atan((zs / p) * ((1 - f) + (e2 * a) / r))
    lat_tl = zs * (1 - f) + e2 * a * sin(u) * sin(u) * sin(u)
    lat_bl = (1 - f) * (p - e2 * a * cos(u) * cos(u) * cos(u))
    long = atan(ys / xs)
    lat = atan(lat_tl / lat_bl)
    if long < 0:
        long = pi + long
    output_latitude = (lat / pi) * 180
    output_longitude = (long / pi) * 180
    output_height = p * cos(lat) + zs * sin(lat) - a * sqrt(1 - e2 * sin(lat) * sin(lat))
    return output_latitude, output_longitude, output_height


print(gda94to2020(-23.6701238941, 133.88551329, 603.3466))
