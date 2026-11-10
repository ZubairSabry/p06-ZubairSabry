# -*- coding: utf-8 -*-

from PIL import Image
from tornado.testing import gen_test

from tests.base import FilterTestCase


class RoundCornerTransparentEdgeTestCase(FilterTestCase):
    @gen_test
    async def test_transparent_edge_keeps_color_and_fades_through_alpha(self):
        source = Image.open(self.get_fixture_path("source.jpg")).convert("RGB")
        result = await self.get_filtered(
            "source.jpg",
            "thumbor.filters.round_corner",
            "round_corner(50,255,255,255,1)",
            mode="RGBA",
        )

        edge = []
        for x in range(50):
            for y in range(50):
                red, green, blue, alpha = result.getpixel((x, y))
                if 0 < alpha < 255:
                    edge.append(((red, green, blue), source.getpixel((x, y))))

        assert edge, "the curve has no partly transparent pixels"
        for color, original in edge:
            assert all(
                abs(got - want) <= 2 for got, want in zip(color, original)
            ), f"edge pixel {color} is not the original color {original}"
