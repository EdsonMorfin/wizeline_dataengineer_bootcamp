import pandas as pd
import numpy as np
from scipy import stats
import unittest
answer_dict =  {"Q1" : None,
                "Q2" : None,
                "Q3" : None,
                "Q4" : None,
                "Q5" : None,
                "Q6" : None,
                "Q7" : None}


url='https://drive.google.com/file/d/1PCJ7ltluquoXKi6MYTPMfwZQNI_-MIFP/view?usp=sharing'
url='https://drive.google.com/uc?id=' + url.split('/')[-2]
df = pd.read_csv(url)

"""
 #   Column                   Non-Null Count  Dtype  
---  ------                   --------------  -----  
 0   Make                     35952 non-null  object 
 1   Model                    35952 non-null  object 
 2   Year                     35952 non-null  int64  
 3   Engine Displacement      35952 non-null  float64
 4   Cylinders                35952 non-null  float64
 5   Transmission             35952 non-null  object 
 6   Drivetrain               35952 non-null  object 
 7   Vehicle Class            35952 non-null  object 
 8   Fuel Type                35952 non-null  object 
 9   Fuel Barrels/Year        35952 non-null  float64
 10  City MPG                 35952 non-null  int64  
 11  Highway MPG              35952 non-null  int64  
 12  Combined MPG             35952 non-null  int64  
 13  CO2 Emission Grams/Mile  35952 non-null  float64
 14  Fuel Cost/Year           35952 non-null  int64 
 """


def average_CO2():
    """Q1. What is the average CO2 emmission per gram/mile of all Volkswagen cars? 

    Returns:
        C02 Mean: float
    """
    Co2 = df['Fuel Cost/Year']
    return Co2.mean()

def most_unique_brands() -> list:
    """Q2. Calculate the top 5 brands(Make) with the most unique models, order your answer in descending order with respect to the number of unique models.

    Returns:
        values_unique: list
    """
    unique = df.groupby('Make')['Model'].nunique().sort_values(ascending=False).head(5)
    index_unique = unique.index
    values_unique = unique.values
    unique_models = []
    for i in range(5):
        temp = []
        temp.append(index_unique[i])
        temp.append(int(values_unique[i]))
        unique_models.append(temp)
    return list(unique_models)

def types_of_fuel():
    """Q3. What are all the different types of fuels in the dataset sorted alphabetically?
    Returns:
        fuels: list
    """
    fuels = list(dict.fromkeys(df['Fuel Type']))
    return sorted(fuels)

def fuel_per_year():
    """Q4. Show the 9 Toyota cars with the most extreme Fuel Barrels/Year in abosolute terms within all Toyota cars.
        Show the car Model, Year and their Fuel Barrels/Year in standard deviation units(Z-score)
        sorted in descending order by their Fuel Barrels/Year in absolute terms first and
        then by year in descending order BUT without modifying the negative values."""
    toyota_vehicles = df.query('Make=="Toyota"')
    toyota_vehicles['Fuel Barrels/Year'] = stats.zscore(toyota_vehicles['Fuel Barrels/Year'])
    toyota_vehicles= toyota_vehicles.sort_values(by=['Fuel Barrels/Year','Year'], ascending=False)
    galons_per_year=toyota_vehicles.reindex(toyota_vehicles['Fuel Barrels/Year'].abs().sort_values(ascending=False).index).head(9)
    toyota_gpy = []
    for i in range(9):
        temp = []
        temp.append(galons_per_year['Model'].values[i])
        temp.append(int(galons_per_year['Year'].values[i]))
        temp.append(float(galons_per_year['Fuel Barrels/Year'].values[i]))
        toyota_gpy.append(temp)
    return toyota_gpy

def golf_changes():
    """
    Q5. Calculate the changes in Combined MPG with their previous model
     of all Golf cars with Manual 5-spd transmission and Regular Fuel Type.
     Show the Year, the Combined MPG and the calculated difference of MPG in a list sorted by Year in ascending order.
    """
    golf_vehicles = df.query('Model=="Golf" & Transmission=="Manual 5-spd" & `Fuel Type`=="Regular"')
    golf_vehicles = golf_vehicles.sort_values(by=['Year'],ascending=True)
    golf_MPG = []
    for i in range(19):
        temp = []
        temp.append(int(golf_vehicles['Year'].values[i]))
        temp.append(int(golf_vehicles['Combined MPG'].values[i]))
        if i==0:
            temp.append(float(0))
        else:
            temp.append(float(golf_vehicles['Combined MPG'].values[i] - golf_vehicles['Combined MPG'].values[i-1]))
        golf_MPG.append(temp)
    return golf_MPG

def low_co2():
    """
    Q6. What are the top 5 lowest CO2 Emission Grams/Mile emmisions of cars for each of the following brands: 
    Toyota, Ford, Volkswagen, Nissan, Honda
    """
    #CO2 Emission Grams/Mile
    cars_brand = ['Toyota','Ford','Volkswagen','Nissan','Honda']
    low_co2_brands = []
    for i in cars_brand:
        temp = []
        vehicles = df.query('Make == "%s"' %(i))
        vehicles = vehicles.sort_values(by=['CO2 Emission Grams/Mile']).head(5)
        temp.append(i)
        temp.extend(list(map(float,vehicles['CO2 Emission Grams/Mile'].values)))
        low_co2_brands.append(temp)
    return low_co2_brands

def median_mpg():
    """ 
    
    """
    year_range = [(1984,1988),(1989,1993),(1994,1998),(1999,2003),(2004,2008),(2009,2013),(2014,2018)]
    median_mpg = []
    for i in year_range:
        temp = []
        vehicles_range = df.query('Year >=%s & Year <= %s'%(str(i[0]),str(i[1])))
        vehicles_range = vehicles_range['Combined MPG'].median()
        temp.append(i)
        temp.append(float(vehicles_range))
        median_mpg.append(temp)
    return median_mpg



class TestAnswers(unittest.TestCase):
    def test_if_dict(self):
        self.assertIsInstance(answer_dict, dict)

    def test_keys(self):
        self.assertEqual(list(answer_dict.keys()), ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7'])

    def test_answers_types(self):
        types_values = [type(k) for k in answer_dict.values()]
        answer_types = [float, list, list, list, list, list, list]
        self.assertEqual(types_values, answer_types)

    def test_Q1(self):
        self.assertEqual(type(answer_dict['Q1']), float)

    def test_Q2_dim(self):
        self.assertEqual(np.array(answer_dict['Q2']).shape, (5,2))

    def test_Q2_types(self):
        dtype1 = type(answer_dict['Q2'][0][0])
        dtype2 = type(answer_dict['Q2'][0][1])
        self.assertEqual([dtype1, dtype2], [str, int])

    def test_Q3_types(self):
        q3_types = set([type(item) for item in answer_dict['Q3']])
        self.assertEqual(q3_types, {str})

    def test_Q4_dim(self):
        self.assertEqual(np.array(answer_dict['Q4']).shape, (9,3))

    def test_Q4_types(self):
        dtype1 = type(answer_dict['Q4'][0][0])
        dtype2 = type(answer_dict['Q4'][0][1])
        dtype3 = type(answer_dict['Q4'][0][2])
        self.assertEqual([dtype1, dtype2, dtype3], [str, int, float])

    def test_Q5_dim(self):
        self.assertEqual(np.array(answer_dict['Q5']).shape, (19,3))

    def test_Q5_types(self):
        dtype1 = type(answer_dict['Q5'][0][0])
        dtype2 = type(answer_dict['Q5'][0][1])
        dtype3 = type(answer_dict['Q5'][0][2])
        self.assertEqual([dtype1, dtype2, dtype3], [int, int, float])

    def test_Q5_first_zero(self):
        self.assertEqual(answer_dict['Q5'][0][2], 0)


    def test_Q6_dim(self):
        self.assertEqual(np.array(answer_dict['Q6']).shape, (5,6))

    def test_Q5_types(self):
        dtype1 = type(answer_dict['Q6'][0][0])
        dtype2 = type(answer_dict['Q6'][0][1])
        dtype3 = type(answer_dict['Q6'][0][2])
        dtype4 = type(answer_dict['Q6'][0][3])
        dtype5 = type(answer_dict['Q6'][0][4])
        dtype6 = type(answer_dict['Q6'][0][5])
        self.assertEqual([dtype1, dtype2, dtype3, dtype4, dtype5, dtype6], [str, float, float, float, float, float])

    def test_Q6_check_first_and_last_brand(self):
        first_brand = answer_dict['Q6'][0][0]
        last_brand = answer_dict['Q6'][4][0]

        self.assertEqual([first_brand, last_brand], ["Toyota", "Honda"])

    def test_Q7_dim(self):
        self.assertEqual(np.array(answer_dict['Q7'], dtype=object).shape, (7,2))

    def test_Q7_types(self):
        dtype1 = type(answer_dict['Q7'][0][0])
        dtype2 = type(answer_dict['Q7'][0][1])
        self.assertEqual([dtype1, dtype2], [tuple, float])




def main():
    answer_dict["Q1"] =float(average_CO2())
    answer_dict["Q2"] = most_unique_brands()
    answer_dict["Q3"] = types_of_fuel()
    answer_dict["Q4"] = fuel_per_year()
    answer_dict["Q5"] = golf_changes()
    answer_dict["Q6"] = low_co2()
    answer_dict["Q7"] = median_mpg()
    unittest.main(argv=[''], verbosity=2, exit=False)

main()
