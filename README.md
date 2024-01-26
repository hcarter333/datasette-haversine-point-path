# datasette-haversine-point-path
[![PyPI](https://img.shields.io/pypi/v/datasette-haversine-point-path.svg)](https://pypi.org/project/datasette-haversine-point-path/)
[![Changelog](https://img.shields.io/github/v/release/hcarter333/datasette-haversine-point-path?include_prereleases&label=changelog)](https://github.com/hcarter333/datasette-haversine-point-path/releases)
[![Tests](https://github.com/hcarter333/datasette-haversine-point-path/workflows/Test/badge.svg)](https://github.com/hcarter333/datasette-haversine-point-path/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/hcarter333/datasette-haversine-point-path/blob/main/LICENSE)

Datasette plugin that adds a custom SQL function for shortest haversine distances between a point and a path on a sphere. The base assumption is that the sphere is the Earth.

If there's a perpendicular distance from the point to the path, then that distance is returned. See the example below illustrating the shortest distances between two different points and a path traced along the Earth shown in yellow. The shortest distance between each of the points and the path form perpendicular lines to the path (in this case) that intersect at the blue markers on the path that traces from the bottom-left of the image towards the top-right in the Googel Earth image. 
![image](https://github.com/hcarter333/datasette-haversine-point-path/assets/363004/0507a3a4-f6c4-4d4e-8352-4e7e37b3f066)

In cases where the perpendicular distance to the path intersects with the path's great circle rather than the path itself, the distance form the point to the nearest endpoint of the path is returned, in the example below, the pink line is the perpendicular distance from the point to the great circle that contains the path of interest, but since it doesn't intersect the path of interest, it's does not represent the shortest distance between the point and the path (the yellow line denotes the path of interest.) In this special case, the green line between the point and the nearest endpoint of the path is the correct anser. It is that distance that is returned by haversine_point_path. 

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
