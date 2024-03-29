# datasette-haversine-point-path
[![PyPI](https://img.shields.io/pypi/v/datasette-haversine-point-path.svg)](https://pypi.org/project/datasette-haversine-point-path/)
[![Changelog](https://img.shields.io/github/v/release/hcarter333/datasette-haversine-point-path?include_prereleases&label=changelog)](https://github.com/hcarter333/datasette-haversine-point-path/releases)
[![Tests](https://github.com/hcarter333/datasette-haversine-point-path/workflows/Test/badge.svg)](https://github.com/hcarter333/datasette-haversine-point-path/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/hcarter333/datasette-haversine-point-path/blob/main/LICENSE)

Datasette plugin that adds a custom SQL function that returns the shortest haversine distances between a point and a path on a sphere. The base assumption is that the sphere is the Earth.

If a perpendicular line can be drawn from the point to the path, then the distance along that line is the shortest distance between the point and the path and is the value that is returned. The following Google Earth image illustrates this case. It shows perpendicular white lines between two different points, (blue markers), and a path, (yellow line). The white lines denote the shorest distance and intersect with the path at the locations shown by the green markers. 

![image](https://github.com/hcarter333/datasette-haversine-point-path/assets/363004/f9b28929-28c0-41f8-aff6-61e5df788070)


In cases where the perpendicular distance from the point to the path intersects with a point on the path's great circle, but the intersectino is not between the endpoints of the path itself, the distance from the point to the nearest endpoint of the path is returned. In the example below the pink line is the perpendicular distance from the point to the great circle containing the path of interest, but since it doesn't intersect the path of interest, it does not represent the shortest distance between the point and the path. In this special case, the distance along the green line, shown in the Google Earth image below, connecting the point and the nearest endpoint of the path is the shortest distance, and is returned by haversine_point_path. 

![image](https://github.com/hcarter333/datasette-haversine-point-path/assets/363004/7237d7e0-150f-412a-bf5f-8ba6ac1c84f9)



Install this plugin in the same environment as Datasette to enable the `haversine_point_path()` SQL function.
```bash
datasette install datasette-haversine-point-path
```
The plugin is built on top of the [haversine](https://github.com/mapado/haversine) library.

## haversine_point_path() to calculate distances

```sql
select haversine_point_path(lat1, lon1, lat2, lon2, lat3, lon3);
```

This will return the distance in kilometers between the path defined by `(lat1, lon1)`, `(lat2, lon2)`, and the point defined by `(lat3, lon3)`.

## Demo
No demo yet

## Custom units

By default `haversine_point_path()` returns results in km. You can pass an optional third argument to get results in a different unit:

- `ft` for feet
- `m` for meters
- `in` for inches
- `mi` for miles
- `nmi` for nautical miles
- `km` for kilometers (the default)

```sql
select haversine_point_path(lat1, lon1, lat2, lon2, 'mi');
```
