# PROCEDURE FOR CALCULATING COMFORT IMPACT OF SOLAR GAIN ON OCCUPANTS BY ASHRAE 55-2020

Convert a solar gain on human to radiant temperature.


## Install

    pip install solartotr
## Usage

    import solartotr
    # 自动计算时角
    t = solartotr.get_hour_angle()
    # 自动计算太阳赤纬角
    sun_angle = solartotr.get_sun_angle()
    print("Sun angle:", sun_angle)
    # 根据时角、地理纬度和太阳赤纬角计算太阳高度角
    b = solartotr.get_h(t=t, latitude=40, sun_angle=sun_angle)
    print(b)
    # 根据太阳高度角和海拔高度计算直射太阳辐射
    i_dir = solartotr.get_i_dir(b=0, height=800)
    # 根据直射太阳辐射、环境温度、太阳高度角和太阳相对于人正面的夹角计算辐射温度
    tr = solartotr.solar_to_tr(i_dir=i_dir, ta=30, b=0, sharp=120)
    print(tr)

## Parameters

- `t`: 时角，单位为度，正午为0度，取值-180度到180度
- `latitude`: 地理纬度，单位为度，北纬为正，南纬为负
- `sun_angle`: 太阳赤纬角，单位为度，北纬为正，南纬为负
- `b`: 太阳高度角，单位为度，0-90
- `i_dir`: 直射太阳辐射，单位为W/m2
- `ta`: 环境温度，单位为摄氏度
- `b`: 太阳高度角，单位为度
- `sharp`: 太阳相对于人正面的夹角，单位为度
- `tr`: 辐射温度，单位为摄氏度


## References

    ASHRAE 55-2020, Thermal Environmental Conditions for Human Occupancy.
