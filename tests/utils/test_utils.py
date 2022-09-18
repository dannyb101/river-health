import pandas as pd
import app.utils.data_utils as data_utils

def test_ninetey_nine_percentile():
    df = pd.read_excel('./tests/files/Example-UPM-output.xlsx')
    df.drop(index=0, inplace=True)
    df.rename(columns={"Unnamed: 12": "mix_bod_mg/l", 
                        "Unnamed: 13": "mix_nh3_mg/l",
                        "Unnamed: 9": "upstream_bod_mg/l",
                        "Unnamed: 10": "upstream_nh3_mg/l"}, inplace=True)

    ninety_nine_percentile_dict = data_utils.ninety_ninth_percentile(df)
    print("printing dict")
    print(ninety_nine_percentile_dict)
    assert ninety_nine_percentile_dict['pre_spill_bod_99_percentile'] ==  19.13010000000003
    assert ninety_nine_percentile_dict['pre_spill_nh3_99_percentile'] ==  4.540400000000009
    assert ninety_nine_percentile_dict['post_spill_bod_99_percentile'] == 110.91870000000002
    assert ninety_nine_percentile_dict['post_spill_nh3_99_percentile'] ==  7.324700000000003

def test_mixed_output_mean_sd():
    data = [[30000, 10, 0.2], [20000, 15, 0.3], [40000, 20, 0.4]]
  
    # Create the pandas DataFrame
    dataframe = pd.DataFrame(data, columns=['mix_flow_l/s', 'mix_bod_mg/l', 'mix_nh3_mg/l'])

    mean_mixed_flow, sd_mixed_flow, mean_mixed_bod, sd_mixed_bod, mean_mixed_nh3, sd_mixed_nh3 = data_utils.calculate_mixed_mean_sd(dataframe)

    assert mean_mixed_flow ==  30000
    assert round(sd_mixed_flow) == 10000
