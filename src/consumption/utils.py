from datetime import datetime

def heating_consumption_calculator(heating_type,current_temp,target_temp,room_volume,starting_time):
    #Does not take into account the insulation of the room and the outside temperature 
    now = datetime.now()
    heating_time = now - starting_time
    heating_time = heating_time.total_seconds()/3600 #in hours

    if heating_type == 'oil':
        mean_lower_heating_volume = 9.96 #in kWh for 1L of oil
    
    #calculate the power needed to heat the room
    air_volumetric_eat_capacity = 1256 #in J/(m3⋅°C)
    heating_power_needed = (target_temp - current_temp) * air_volumetric_eat_capacity * room_volume # in J
    heating_power_needed = heating_power_needed / 3600000 #in kilowatts

    #calculate the consumption
    print(heating_time, heating_power_needed)
    consumption = (heating_power_needed * heating_time) / mean_lower_heating_volume #in L

    return consumption



