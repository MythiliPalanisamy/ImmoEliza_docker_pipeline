import pandas as pd

def clean():

    AIRFLOW_HOME = "/home/mythili/becode/Immo_airflow/airflow"
    cleaned_csv_path = AIRFLOW_HOME + "/dags/data/cleaned.csv"
    df = pd.read_csv(AIRFLOW_HOME + "/dags/data/scraped_data.csv")

    df = df.drop_duplicates()

    df['Energy class']=df['Energy class'].replace('Not specified', 'NS')

    df['Primary energy consumption']=df['Primary energy consumption'].replace('Not specified', '0')
    df['Primary energy consumption'] = pd.to_numeric(df['Primary energy consumption'], errors='coerce')
  
    df['Terrace']=df['Terrace'].replace('Yes',int(1))
    df['Terrace']=pd.to_numeric(df['Terrace'], errors='coerce')

    df['Furnished']=df['Furnished'].replace('Yes',int(1))
    df['Furnished']=df['Furnished'].replace('No',int(0))
    df['Furnished']=pd.to_numeric(df['Furnished'], errors='coerce')

    df['Office']=df['Office'].replace('Yes',int(1))
    df['Office']=df['Office'].replace('No',int(0))
    df['Office']=pd.to_numeric(df['Office'], errors='coerce')

    df['Price']=df['Price'].str.replace('€', '')
    df['Price'] = df['Price'].str.split('.').str[0]
    df['Price']=df['Price'].str.replace('.', '')
    df = df.drop(df[df['Price'] == str(0)].index)
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df = df.dropna(subset=['Price'])
        
    df.rename(columns=({'Type_of_property' : 'type_of_property','Shower rooms':'shower_rooms','Office':'office','Construction year': 'construction_year','Outdoor parking space': 'outdoor_parking_space','Furnished':'furnished','Terrace':'terrace', 'Terrace surface':'terrace_surface', 'Price':'price', 'Address':'address', 'Primary energy consumption':'primary_energy_consumption', 'Location':'location','postal code': 'postal_code','immo code':'immo_code', 'Energy class' : 'energy_class', 'Bedrooms' : 'bedrooms', 'Bathrooms': 'bathrooms' , 'Toilets': 'toilets', 'Number of frontages': 'number_of_frontages','Kitchen type': 'kitchen_type','Heating type': 'heating_type', 'Surface of the plot': 'surface_of_the_plot',  'Living room surface': 'living_room_surface', 'province':'province' , 'Building condition':'building_condition'}),inplace=True)
    df = df[df['price'] < 7.1e5]

    df['number_of_frontages'] = pd.to_numeric(df['number_of_frontages'], errors='coerce')
    df = df.drop(df[df['number_of_frontages'] > 10].index) # after romving,min = 6

    df['toilets'] = pd.to_numeric(df['toilets'], errors='coerce')
    df = df.drop(df[df['toilets'] > 9].index)

    # since bathrooms and shower rooms are same adding it and removing >10 and (-1) values considering it as outliers 
    df['bathrooms'] = pd.to_numeric(df['bathrooms'], errors='coerce')
    df['shower_rooms'] = pd.to_numeric(df['shower_rooms'], errors='coerce')
    
    df['bathrooms']=df['bathrooms']+df['shower_rooms'] 
    df = df.drop(df[df['bathrooms'] > 10].index)
    df = df.drop(df[df['bathrooms'] == -1].index)
    df = df.drop(columns=[ 'postal_code', 'furnished', 'construction_year','terrace', 'office' ,'primary_energy_consumption','terrace_surface','outdoor_parking_space','shower_rooms'], axis=1)
    
    df.to_csv(cleaned_csv_path,index=False)
    return df
print('starting cleaning')
clean()
print('cleaned the scraped data')
