"""Module containing the base OSM class."""

from __future__ import annotations

import pathlib
import random

from lxml import objectify
import colorsys


class OSM:
    def __init__(self, file: str | pathlib.Path):
        self._file = pathlib.Path(file)
        self._root = objectify.parse(str(self._file))

        self._nodes = self._get_nodes()
        self._ways = self._get_ways()

    @property
    def way_lat_lons(self):
        output = {}
        for way_id, node_ids in self._ways.items():
            output[way_id] = {
                "color": f"#{self.get_color(random.random())}",
                "lon_lats": [
                    [self._nodes[node_id]["lat"], self._nodes[node_id]["lon"]]
                    for node_id in node_ids
                ],
            }

        return output

    def _get_nodes(self):
        output = {}
        for node in self._root.xpath("//osm/node"):
            output[node.get("id")] = {
                "lat": float(node.get("lat")),
                "lon": float(node.get("lon")),
            }

        return output

    @staticmethod
    def get_color(red_to_green):
        assert 0 <= red_to_green <= 1
        # in HSV, red is 0 deg and green is 120 deg (out of 360);
        # divide red_to_green with 3 to map [0, 1] to [0, 1./3.]
        hue = red_to_green / 3.0
        r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
        r, g, b = list(map(lambda x: int(255 * x), (r, g, b)))
        return ("{:02x}{:02x}{:02x}").format(r, g, b)

    def _get_ways(self):
        output = {}
        for way in self._root.xpath("//osm/way"):
            is_highway = any(
                [
                    "highway" in tag.get("k")
                    for tag in way.iterchildren(tag="tag")
                ]
            )

            # Ignore non-highway ways
            if not is_highway:
                continue

            output[way.get("id")] = [
                node.get("ref") for node in way.iterchildren(tag="nd")
            ]

        return output

    @property
    def nodes(self):
        return self._nodes

    @property
    def ways(self):
        return self._ways
