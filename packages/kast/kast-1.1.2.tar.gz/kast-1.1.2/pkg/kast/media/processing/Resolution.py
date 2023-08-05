#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from __future__ import annotations  # TODO: Remove when support dropped for: Python < 3.10

from dataclasses import dataclass
from functools import total_ordering


@total_ordering
@dataclass(frozen=True)
class Resolution:
    width: int
    height: int

    def __str__(self) -> str:
        return f"{self.width}x{self.height}"

    def __lt__(self, other: Resolution) -> bool:
        if not isinstance(other, Resolution):
            raise ValueError(f"Cannot compare {Resolution.__name__} with {other.__class__.__name__}!")

        return self.width < other.width or \
            self.height < other.height

    def shrinkToFit(self, boundingSize: Resolution) -> Resolution:
        def adjustDimension(dimToAdjust: int, dimOther: int, dimOtherBound: int) -> int:
            return int(dimToAdjust * (dimOtherBound / dimOther))

        def adjustWidth(resolution: Resolution) -> Resolution:
            if resolution.width < boundingSize.width:
                return resolution
            return Resolution(
                width=boundingSize.width,
                height=adjustDimension(
                    dimToAdjust=resolution.height,
                    dimOther=resolution.width,
                    dimOtherBound=boundingSize.width
                )
            )

        def adjustHeight(resolution: Resolution) -> Resolution:
            if resolution.height < boundingSize.height:
                return resolution
            return Resolution(
                width=adjustDimension(
                    dimToAdjust=resolution.width,
                    dimOther=resolution.height,
                    dimOtherBound=boundingSize.height
                ),
                height=boundingSize.height
            )

        return adjustHeight(adjustWidth(self))


FULL_HD = Resolution(1920, 1080)
ULTRA_HD = Resolution(3840, 2160)
