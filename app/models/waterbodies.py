from ..utils import data_utils, monte_carlo
import pandas as pd
from functools import reduce

class Cso:

    def __init__(self, df, cso_id, bod_conc_mgl=None, nh3_conc_mgl=None, multi=False):
        """
        create final dataframe on instantiation
        """
        self.cso_id = cso_id
        self.bod_conc_mgl = bod_conc_mgl
        self.nh3_conc_mgl = nh3_conc_mgl
        if not multi:
            df.rename(columns={'cso_vol_l_1': 'cso_vol_l'}, inplace=True)
            df[['cso_bod_kg', 'cso_nh3_kg']] = df.apply(lambda row: self.calculate_pollutant_mass(row['cso_vol_l']), axis=1, result_type='expand')
        self.data_frame = df
        
    def calculate_pollutant_mass(self, cso_vol_l):
        """
        mass balance - round results to 4dp to prevent overflow from float
        list returned to create multiple df columns with pd.apply(result_type='expand') 
        """
        # mass = concentration x vol
        
        cso_bod_mass_kg = data_utils.convert_mg_to_kg(self.bod_conc_mgl * cso_vol_l)
        cso_nh3_mass_kg = data_utils.convert_mg_to_kg(self.nh3_conc_mgl * cso_vol_l)

        return [round(cso_bod_mass_kg, 4), round(cso_nh3_mass_kg, 4)]

class River:
    
    def __init__(
        self,
        river_stretch_name,
        river_flow_ls,
        river_flow_ls_sd,
        river_bod_mgl,
        river_bod_mgl_sd,
        river_nh3_mgl,
        river_nh3_mgl_sd,
        river_do_conc_mgl=0,
        river_do_conc_mgl_sd=0,
        river_temp_celcius=0,
        river_temp_celcius_sd=0,
        river_ph=0,
        river_ph_sd=0):

        self.river_stretch_name = river_stretch_name
        self.river_flow_ls = river_flow_ls
        self.river_flow_ls_sd = river_flow_ls_sd
        self.river_bod_mgl = river_bod_mgl
        self.river_bod_mgl_sd = river_bod_mgl_sd
        self.river_nh3_mgl = river_nh3_mgl
        self.river_nh3_mgl_sd = river_nh3_mgl_sd
        self.river_do_conc_mgl = river_do_conc_mgl
        self.river_do_conc_mgl_sd = river_do_conc_mgl_sd
        self.river_temp_celcius = river_temp_celcius
        self.river_temp_celcius_sd = river_temp_celcius_sd
        self.river_ph = river_ph
        self.river_ph_sd = river_ph_sd
    

    """
    Function uses a Cso object to create a dataframe with cso, upstream and downstream data
    for flow rate, bod conc and nh3 conc
    """
    def add_cso_spill(self, cso: Cso):
        cso_df = cso.data_frame
        upstream_river_flow = monte_carlo.log_normal_dist(self.river_flow_ls, self.river_flow_ls_sd,len(cso_df.index))
        upstream_river_bod = monte_carlo.log_normal_dist(self.river_bod_mgl, self.river_bod_mgl_sd,len(cso_df.index))
        upsream_river_nh3 = monte_carlo.log_normal_dist(self.river_nh3_mgl, self.river_nh3_mgl_sd,len(cso_df.index))
        
        # zip lists together makes a list of tuples which can be used to iterate over all lists at the same time for dataframe creation
        zipped_upstream_river_data = list(zip(upstream_river_flow, upstream_river_bod, upsream_river_nh3))
        upstream_df = pd.DataFrame(
            zipped_upstream_river_data,
            columns=['upstream_flow_l/s','upstream_bod_mg/l', 'upstream_nh3_mg/l'],
            index=cso_df.index
        )
        output_df = pd.concat([cso_df, upstream_df], axis=1)
        num_seconds_in_hour = 3600
        output_df['mix_flow_l/s'] = output_df['upstream_flow_l/s'] + (output_df['cso_vol_l'] /num_seconds_in_hour)
        output_df[['mix_bod_mg/l', 'mix_nh3_mg/l']] = output_df.apply(
            lambda row: self.calculate_mixture_pollutant_concentrations(
                row['upstream_flow_l/s'],
                row['cso_vol_l'],
                row['cso_bod_kg'],
                row['cso_nh3_kg'],
                row['upstream_bod_mg/l'],
                row['upstream_nh3_mg/l']
            ),
            axis=1,
            result_type='expand'
        )
        return output_df


    def calculate_mixture_pollutant_concentrations(self,river_flow_ls, cso_vol_l, cso_bod_mass_kg, cso_nh3_mass_kg,  river_bod_conc_mgl, river_nh3_conc_mgl):
        """
        volume = flow rate x time
        mass = volume x concentraion
        """
        num_seconds_in_hour = 3600
        river_vol_l = river_flow_ls * num_seconds_in_hour
        river_bod_mass_kg = data_utils.convert_mg_to_kg(river_vol_l * river_bod_conc_mgl)
        river_nh3_mass_kg = data_utils.convert_mg_to_kg(river_vol_l * river_nh3_conc_mgl)
  
        mix_flow_ls = river_flow_ls + (cso_vol_l / num_seconds_in_hour)
        mix_bod_mass_kg = cso_bod_mass_kg + river_bod_mass_kg
        mix_nh3_mass_kg = cso_nh3_mass_kg + river_nh3_mass_kg

        mix_vol_l = mix_flow_ls * num_seconds_in_hour

        # concentration = mass / vol
        mix_bod_conc_mgl = data_utils.convert_kg_to_mg(mix_bod_mass_kg) / mix_vol_l
        mix_nh3_conc_mgl = data_utils.convert_kg_to_mg(mix_nh3_mass_kg) / mix_vol_l
        
        # round results to 4dp to prevent overflow from float
        # return as list for use with pd.apply(result_type=) 
        return [round(mix_bod_conc_mgl, 4), round(mix_nh3_conc_mgl, 4)]

    def run_simulations(self, cso: Cso, num_simulations: int, simulation_id: str):
        """
        Runs the number of simulations specified by the user, and returns the average values of the 99th percentile of the bod and nh3 values as well as the combined dataframe
        """
        df_array = []
        percentiles = []
        pre_spill_sum_bod_values = 0
        pre_spill_sum_nh3_values = 0    
        post_spill_sum_bod_values = 0
        post_spill_sum_nh3_values = 0

        for i in range(num_simulations):
            df = self.add_cso_spill(cso)
            percentiles.append(data_utils.ninety_ninth_percentile(df))
            num = "_0" + str(i+1) if i < 9 else "_" + str(i+1)
            sim_id = simulation_id + num
            df.insert(0, 'sim_id', sim_id)
            df_array.append(df)

        all_dfs = pd.concat(df_array)

        for item in percentiles:
            pre_spill_sum_bod_values += item["pre_spill_bod_99_percentile"]
            pre_spill_sum_nh3_values += item["pre_spill_nh3_99_percentile"]
            post_spill_sum_bod_values += item["post_spill_bod_99_percentile"]
            post_spill_sum_nh3_values += item["post_spill_nh3_99_percentile"]

        pre_spill_avg_bod_value = round(pre_spill_sum_bod_values / num_simulations, 2)
        pre_spill_avg_nh3_value = round(pre_spill_sum_nh3_values / num_simulations, 2)
            
        post_spill_avg_bod_value = round(post_spill_sum_bod_values / num_simulations, 2)
        post_spill_avg_nh3_value = round(post_spill_sum_nh3_values / num_simulations, 2)
        
        return pre_spill_avg_bod_value, pre_spill_avg_nh3_value, post_spill_avg_bod_value, post_spill_avg_nh3_value, all_dfs

def create_multi_cso(csv_file, cso_dict, trunc_unique_id):
    # Create multi-cso dataframe
    multi_cso_df = data_utils.convert_cso_csv_to_df(csv_file)
    summed_multi_cso_df = data_utils.sum_df_over_hour(multi_cso_df)

    # create list of cso objects for each cso in the multi-cso dataframe
    list_of_cso_objects = []
    columns = summed_multi_cso_df.columns
    for index, (key, val_dict) in enumerate(cso_dict.items()):
        cso_df = summed_multi_cso_df[[columns[index]]]
        cso_df.set_axis(['cso_vol_l'], axis='columns', inplace=True)
        list_of_cso_objects.append(Cso(cso_df, key, val_dict['bod_conc'], val_dict['nh3_conc']))
    list_of_cso_dfs = [cso.data_frame for cso in list_of_cso_objects]

    # return multi-cso object - reduce used to sum the cso dataframes
    return Cso(reduce(lambda a, b: a.add(b, fill_value=0), list_of_cso_dfs), trunc_unique_id, multi=True)
     