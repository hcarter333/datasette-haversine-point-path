from datasette import hookimpl
from haversine import haversine
import math


def cartesian_x(f,l):
    #f = latitude, l = longitude
    return (math.cos(f*deg2rad)*math.cos(l*deg2rad))

def cartesian_y(f,l):
    #f = latitude, l = longitude
    return (math.cos(f*deg2rad)*math.sin(l*deg2rad))

def cartesian_z(f,l):
    #f = latitude, l = longitude
    return (math.sin(f*deg2rad))

def cross_x(x, y, z, i,j,k):
    return ((y*k)-(z*j))
def cross_y(x, y, z, i,j,k):
    return ((z*i)-(x*k))
def cross_z(x, y, z, i,j,k):
    return ((x*j)-(y*i))

def spherical_lat(x,y,z):
    r = math.sqrt(x*x + y*y)
    #Omitting the special cases because points will always
    #be separated for this application
    return (math.atan2(z, r)*rad2deg) # return degrees

def spherical_lng(x,y,z):
    #Omitting the special cases because points will always
    #be separated for this application
    return (math.atan2(y, x)*rad2deg) # return degrees
  
def haversine_point_path_sql(lat1, lon1, lat2, lon2, lat3, lon3, unit="km"):
    tx_x = cartesian_x(lat1,lon1)
    tx_y = cartesian_y(lat1,lon1)
    tx_z = cartesian_z(lat1,lon1)
    rx_x = cartesian_x(lat2,lon2)
    rx_y = cartesian_y(lat2,lon2)
    rx_z = cartesian_z(lat2,lon2)
    c_x = cartesian_x(lat3,lon3)
    c_y = cartesian_y(lat3,lon3)
    c_z = cartesian_z(lat3,lon3)

    #The plane containing the path
    g_x = cross_x(tx_x, tx_y, tx_z, rx_x, rx_y, rx_z)
    g_y = cross_y(tx_x, tx_y, tx_z, rx_x, rx_y, rx_z)
    g_z = cross_z(tx_x, tx_y, tx_z, rx_x, rx_y, rx_z)
    #The plane containing the ionosonde and perpendicular to the path?
    f_x = cross_x(c_x, c_y, c_z, g_x, g_y, g_z)
    f_y = cross_y(c_x, c_y, c_z, g_x, g_y, g_z)
    f_z = cross_z(c_x, c_y, c_z, g_x, g_y, g_z)
    t_x = cross_x(g_x, g_y, g_z, f_x, f_y, f_z)
    t_y = cross_y(g_x, g_y, g_z, f_x, f_y, f_z)
    t_z = cross_z(g_x, g_y, g_z, f_x, f_y, f_z)

    t_mag = math.sqrt(t_x**2 + t_y**2 + t_z**2)

    tp_x = t_x/t_mag
    tp_y = t_y/t_mag
    tp_z = t_z/t_mag
    
    intersection_lat = spherical_lat(tp_x,tp_y,tp_z)
    intersection_lon = spherical_lng(tp_x,tp_y,tp_z)
  
    return haversine((float(lat3), float(lon3)), (float(intersection_lat), float(intersection_lon)), unit=unit)


@hookimpl
def prepare_connection(conn):
    conn.create_function("haversine_point_path", 6, haversine_point_path_sql)
    conn.create_function("haversine_point_path", 7, haversine_point_path_sql)
