# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021, earthobservations developers.
# Distributed under the MIT License. See LICENSE for more info.
from enum import Enum

from wetterdienst.util.parameter import DatasetTreeCore


class DwdMosmixParameter(DatasetTreeCore):
    # https://opendata.dwd.de/weather/lib/MetElementDefinition.xml
    class SMALL(Enum):
        TEMPERATURE_AIR_MEAN_200 = "ttt"
        TEMPERATURE_DEW_POINT_MEAN_200 = "td"
        TEMPERATURE_AIR_MAX_200 = "tx"
        TEMPERATURE_AIR_MIN_200 = "tn"
        WIND_DIRECTION = "dd"
        WIND_SPEED = "ff"
        WIND_GUST_MAX_LAST_1H = "fx1"
        WIND_GUST_MAX_LAST_3H = "fx3"
        WIND_GUST_MAX_LAST_12H = "fxh"
        PRECIPITATION_HEIGHT_SIGNIFICANT_WEATHER_LAST_1H = "rr1c"
        PRECIPITATION_HEIGHT_SIGNIFICANT_WEATHER_LAST_3H = "rr3c"
        WATER_EQUIVALENT_SNOW_DEPTH_NEW_LAST_1H = "rrs1c"
        WATER_EQUIVALENT_SNOW_DEPTH_NEW_LAST_3H = "rrs3c"
        WEATHER_SIGNIFICANT = "ww"
        WEATHER_LAST_6H = "w1w2"
        CLOUD_COVER_TOTAL = "n"
        CLOUD_COVER_EFFECTIVE = "neff"
        CLOUD_COVER_BELOW_500_FT = "n05"
        CLOUD_COVER_BELOW_1000_FT = "nl"
        CLOUD_COVER_BETWEEN_2_TO_7_KM = "nm"
        CLOUD_COVER_ABOVE_7_KM = "nh"
        PRESSURE_AIR_SITE_REDUCED = "pppp"
        TEMPERATURE_AIR_MEAN_005 = "t5cm"
        RADIATION_GLOBAL = "rad1h"
        VISIBILITY_RANGE = "vv"
        SUNSHINE_DURATION = "sund1"
        PROBABILITY_WIND_GUST_GE_25_KN_LAST_12H = "fxh25"
        PROBABILITY_WIND_GUST_GE_40_KN_LAST_12H = "fxh40"
        PROBABILITY_WIND_GUST_GE_55_KN_LAST_12H = "fxh55"
        PROBABILITY_FOG_LAST_1H = "wwm"
        PROBABILITY_FOG_LAST_6H = "wwm6"
        PROBABILITY_FOG_LAST_12H = "wwmh"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_0_0_MM_LAST_12H = "rh00"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_0_2_MM_LAST_6H = "r602"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_0_2_MM_LAST_12H = "rh02"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_0_2_MM_LAST_24H = "rd02"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_1_0_MM_LAST_12H = "rh10"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_5_0_MM_LAST_6H = "r650"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_5_0_MM_LAST_12H = "rh50"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_5_0_MM_LAST_24H = "rd50"

    class LARGE(Enum):
        TEMPERATURE_AIR_MEAN_200 = "ttt"
        TEMPERATURE_DEW_POINT_MEAN_200 = "td"
        TEMPERATURE_AIR_MAX_200 = "tx"
        TEMPERATURE_AIR_MIN_200 = "tn"
        WIND_DIRECTION = "dd"
        WIND_SPEED = "ff"
        WIND_GUST_MAX_LAST_1H = "fx1"
        WIND_GUST_MAX_LAST_3H = "fx3"
        WIND_GUST_MAX_LAST_12H = "fxh"
        PRECIPITATION_HEIGHT_SIGNIFICANT_WEATHER_LAST_1H = "rr1c"
        PRECIPITATION_HEIGHT_LAST_1H = "rr1"
        PRECIPITATION_HEIGHT_SIGNIFICANT_WEATHER_LAST_3H = "rr3c"
        PRECIPITATION_HEIGHT_LAST_3H = "rr3"
        WATER_EQUIVALENT_SNOW_DEPTH_NEW_LAST_1H = "rrs1c"
        WATER_EQUIVALENT_SNOW_DEPTH_NEW_LAST_3H = "rrs3c"
        WEATHER_SIGNIFICANT = "ww"
        WEATHER_LAST_6H = "w1w2"
        CLOUD_COVER_TOTAL = "n"
        CLOUD_COVER_EFFECTIVE = "neff"
        CLOUD_COVER_BELOW_500_FT = "n05"
        CLOUD_COVER_BELOW_1000_FT = "nl"
        CLOUD_COVER_BETWEEN_2_TO_7_KM = "nm"
        CLOUD_COVER_ABOVE_7_KM = "nh"
        PRESSURE_AIR_SITE_REDUCED = "pppp"
        TEMPERATURE_AIR_MEAN_005 = "t5cm"
        RADIATION_GLOBAL_LAST_3H = "rads3"
        RADIATION_GLOBAL = "rad1h"
        RADIATION_SKY_LONG_WAVE_LAST_3H = "radl3"
        VISIBILITY_RANGE = "vv"
        SUNSHINE_DURATION = "sund1"
        PROBABILITY_WIND_GUST_GE_25_KN_LAST_12H = "fxh25"
        PROBABILITY_WIND_GUST_GE_40_KN_LAST_12H = "fxh40"
        PROBABILITY_WIND_GUST_GE_55_KN_LAST_12H = "fxh55"
        PROBABILITY_FOG_LAST_1H = "wwm"
        PROBABILITY_FOG_LAST_6H = "wwm6"
        PROBABILITY_FOG_LAST_12H = "wwmh"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_0_0_MM_LAST_12H = "rh00"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_0_2_MM_LAST_6H = "r602"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_0_2_MM_LAST_12H = "rh02"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_0_2_MM_LAST_24H = "rd02"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_1_0_MM_LAST_12H = "rh10"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_5_0_MM_LAST_6H = "r650"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_5_0_MM_LAST_12H = "rh50"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_5_0_MM_LAST_24H = "rd50"
        TEMPERATURE_AIR_MIN_005_LAST_12H = "tg"
        TEMPERATURE_AIR_MEAN_200_LAST_24H = "tm"
        PRECIPITATION_DURATION = "drr1"
        PROBABILITY_DRIZZLE_LAST_1H = "wwz"
        PROBABILITY_PRECIPITATION_STRATIFORM_LAST_1H = "wwd"
        PROBABILITY_PRECIPITATION_CONVECTIVE_LAST_1H = "wwc"
        PROBABILITY_THUNDER_LAST_1H = "wwt"
        PROBABILITY_PRECIPITATION_LIQUID_LAST_1H = "wwl"
        PROBABILITY_PRECIPITATION_SOLID_LAST_1H = "wws"
        PROBABILITY_PRECIPITATION_FREEZING_LAST_1H = "wwf"
        PROBABILITY_PRECIPITATION_LAST_1H = "wwp"
        PROBABILITY_VISIBILITY_BELOW_1000_M = "vv10"
        ERROR_ABSOLUTE_TEMPERATURE_AIR_MEAN_200 = "e_ttt"
        ERROR_ABSOLUTE_WIND_SPEED = "e_ff"
        ERROR_ABSOLUTE_WIND_DIRECTION = "e_dd"
        ERROR_ABSOLUTE_TEMPERATURE_DEW_POINT_MEAN_200 = "e_td"
        PRECIPITATION_HEIGHT_LAST_6H = "rr6"
        PRECIPITATION_HEIGHT_SIGNIFICANT_WEATHER_LAST_6H = "rr6c"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_0_0_MM_LAST_6H = "r600"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_0_1_MM_LAST_1H = "r101"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_0_2_MM_LAST_1H = "r102"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_0_3_MM_LAST_1H = "r103"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_0_5_MM_LAST_1H = "r105"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_0_7_MM_LAST_1H = "r107"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_1_0_MM_LAST_1H = "r110"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_2_0_MM_LAST_1H = "r120"
        SUNSHINE_DURATION_YESTERDAY = "sund"
        SUNSHINE_DURATION_RELATIVE_LAST_24H = "rsund"
        PROBABILITY_SUNSHINE_DURATION_RELATIVE_GT_0_PCT_LAST_24H = "psd00"
        PROBABILITY_SUNSHINE_DURATION_RELATIVE_GT_30_PCT_LAST_24H = "psd30"
        PROBABILITY_SUNSHINE_DURATION_RELATIVE_GT_60_PCT_LAST_24H = "psd60"
        PROBABILITY_RADIATION_GLOBAL_LAST_1H = "rrad1"
        EVAPOTRANSPIRATION_POTENTIAL_LAST_24H = "pevap"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_3_0_MM_LAST_1H = "r130"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_5_0_MM_LAST_1H = "r150"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_10_0_MM_LAST_1H = "rr1o1"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_15_0_MM_LAST_1H = "rr1w1"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_25_0_MM_LAST_1H = "rr1u1"
        PROBABILITY_PRECIPITATION_STRATIFORM_LAST_6H = "wwd6"
        PROBABILITY_PRECIPITATION_CONVECTIVE_LAST_6H = "wwc6"
        PROBABILITY_THUNDER_LAST_6H = "wwt6"
        PROBABILITY_PRECIPITATION_LAST_6H = "wwp6"
        PROBABILITY_PRECIPITATION_LIQUID_LAST_6H = "wwl6"
        PROBABILITY_PRECIPITATION_FREEZING_LAST_6H = "wwf6"
        PROBABILITY_PRECIPITATION_SOLID_LAST_6H = "wws6"
        PROBABILITY_DRIZZLE_LAST_6H = "wwz6"
        PROBABILITY_FOG_LAST_24H = "wwmd"
        PROBABILITY_WIND_GUST_GE_25_KN_LAST_6H = "fx625"
        PROBABILITY_WIND_GUST_GE_40_KN_LAST_6H = "fx640"
        PROBABILITY_WIND_GUST_GE_55_KN_LAST_6H = "fx655"
        PROBABILITY_PRECIPITATION_STRATIFORM_LAST_12H = "wwdh"
        PROBABILITY_PRECIPITATION_CONVECTIVE_LAST_12H = "wwch"
        PROBABILITY_THUNDER_LAST_12H = "wwth"
        PROBABILITY_PRECIPITATION_LAST_12H = "wwph"
        PROBABILITY_PRECIPITATION_LIQUID_LAST_12H = "wwlh"
        PROBABILITY_PRECIPITATION_FREEZING_LAST_12H = "wwfh"
        PROBABILITY_PRECIPITATION_SOLID_LAST_12H = "wwsh"
        PROBABILITY_DRIZZLE_LAST_12H = "wwzh"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_1_0_MM_LAST_6H = "r610"
        PRECIPITATION_HEIGHT_LAST_12H = "rrh"
        PRECIPITATION_HEIGHT_SIGNIFICANT_WEATHER_LAST_12H = "rrhc"
        WEATHER_SIGNIFICANT_LAST_3H = "ww3"
        PRECIPITATION_HEIGHT_LIQUID_SIGNIFICANT_WEATHER_LAST_1H = "rrl1c"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_0_0_MM_LAST_24H = "rd00"
        PROBABILITY_PRECIPITATION_HEIGHT_GT_1_0_MM_LAST_24H = "rd10"
        PRECIPITATION_HEIGHT_LAST_24H = "rrd"
        PRECIPITATION_HEIGHT_SIGNIFICANT_WEATHER_LAST_24H = "rrdc"
        CLOUD_COVER_BELOW_7_KM = "nlm"
        PROBABILITY_PRECIPITATION_LAST_24H = "wwpd"
        CLOUD_BASE_CONVECTIVE = "h_bsc"
        PROBABILITY_THUNDER_LAST_24H = "wwtd"
        ERROR_ABSOLUTE_PRESSURE_AIR_SITE = "e_ppp"
        SUNSHINE_DURATION_LAST_3H = "sund3"
        WEATHER_SIGNIFICANT_OPTIONAL_LAST_1H = "wpc11"
        WEATHER_SIGNIFICANT_OPTIONAL_LAST_3H = "wpc31"
        WEATHER_SIGNIFICANT_OPTIONAL_LAST_6H = "wpc61"
        WEATHER_SIGNIFICANT_OPTIONAL_LAST_12H = "wpch1"
        WEATHER_SIGNIFICANT_OPTIONAL_LAST_24H = "wpcd1"
