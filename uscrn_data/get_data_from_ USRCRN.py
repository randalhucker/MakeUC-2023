import requests
import pandas
import re
from typing import List, Tuple

headers = [
    "WBANNO",
    "UTC_DATE",
    "UTC_TIME",
    "LST_DATE",
    "LST_TIME",
    "CRX_VN",
    "LONGITUDE",
    "LATITUDE",
    "T_CALC",
    "T_HR_AVG",
    "T_MAX",
    "T_MIN",
    "P_CALC",
    "SOLARAD",
    "SOLARAD_FLAG",
    "SOLARAD_MAX",
    "SOLARAD_MAX_FLAG",
    "SOLARAD_MIN",
    "SOLARAD_MIN_FLAG",
    "SUR_TEMP_TYPE",
    "SUR_TEMP",
    "SUR_TEMP_FLAG",
    "SUR_TEMP_MAX",
    "SUR_TEMP_MAX_FLAG",
    "SUR_TEMP_MIN",
    "SUR_TEMP_MIN_FLAG",
    "RH_HR_AVG",
    "RH_HR_AVG_FLAG",
    "SOIL_MOISTURE_5",
    "SOIL_MOISTURE_10",
    "SOIL_MOISTURE_20",
    "SOIL_MOISTURE_50",
    "SOIL_MOISTURE_100",
    "SOIL_TEMP_5",
    "SOIL_TEMP_10",
    "SOIL_TEMP_20",
    "SOIL_TEMP_50",
    "SOIL_TEMP_100"
]

urls: List[Tuple[str,str]] = [
    ['2022','https://www.ncei.noaa.gov/pub/data/uscrn/products/hourly02/2022/CRNH0203-2022-OH_Wooster_3_SSE.txt'],
    ['2021','https://www.ncei.noaa.gov/pub/data/uscrn/products/hourly02/2021/CRNH0203-2021-OH_Wooster_3_SSE.txt'],
    ['2020','https://www.ncei.noaa.gov/pub/data/uscrn/products/hourly02/2020/CRNH0203-2020-OH_Wooster_3_SSE.txt'],
    ['2019','https://www.ncei.noaa.gov/pub/data/uscrn/products/hourly02/2019/CRNH0203-2019-OH_Wooster_3_SSE.txt'],
    ['2018','https://www.ncei.noaa.gov/pub/data/uscrn/products/hourly02/2018/CRNH0203-2018-OH_Wooster_3_SSE.txt'],
]
for (year, url) in urls:
    # Send a GET request to the URL and get the content
    response = requests.get(url)

    if response.status_code == 200:
        # The request was successful, so you can access the contentUSRCRN
        content = response.text

        # Split the content into lines
        lines = content.split('\n')

        # Create an empty list to store the data
        data = []

        # Iterate through the lines and split values
        for line in lines:
            values = re.split(r'\s+', line.strip())  # Split by one or more whitespace characters
            data.append(values)

        # Create a DataFrame from the data and headers
        df = pandas.DataFrame(data, columns=headers)

        # Create a new DataFrame with only the specified columns
        selected_columns = [
            "LST_DATE", # The Local Standard Time (LST) date of the observation.
            "LST_TIME", # The Local Standard Time (LST) time of the observation. Time is the end of the observed hour (see UTC_TIME description).
            "T_HR_AVG", # The average temperature for the past hour in degrees Celsius (°C).
            "P_CALC", # Total amount of precipitation, in mm, recorded during the hour.
        ]

        new_df = df[selected_columns]

        # Save the new DataFrame to a CSV file
        new_df.to_csv(f"{year}.csv", index=False)  # Adjust the file name as needed
        
    else:
        print(f"Failed to retrieve content. Status code: {response.status_code}")
