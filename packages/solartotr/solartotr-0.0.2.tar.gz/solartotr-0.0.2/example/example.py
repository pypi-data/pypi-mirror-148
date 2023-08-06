import solartotr


t = solartotr.get_hour_angle()
print(t)
sun_angle = solartotr.get_sun_angle()
print("Sun angle:", sun_angle)
b = solartotr.get_h(t=t, latitude=40, sun_angle=sun_angle)
print(b)
i_dir = solartotr.get_i_dir(b=0, height=800)
tr = solartotr.solar_to_tr(i_dir=i_dir, ta=30, b=0, sharp=120)
print(tr)
