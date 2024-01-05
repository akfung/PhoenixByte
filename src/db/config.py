
from dotenv import load_dotenv
import os
load_dotenv()

conn_s = "postgresql://{user}:{password}@{host}:{port}/{db_name}".format(user=os.environ.get('DB_USER'),
                                                                         password=os.environ.get('DB_PASSWORD'),
                                                                         host=os.environ.get('DB_HOST'),  
                                                                         port=os.environ.get('DB_PORT'), 
                                                                         db_name=os.environ.get('DB_NAME'),
                                                                         )

justice_names = {'Alito',
    'Barrett',
    'Breyer',
    'Ginsburg',
    'Gorsuch',
    'Jackson',
    'Kagan',
    'Kavanaugh',
    'Kennedy',
    'Roberts',
    'Scalia',
    'Sotomayor',
    'Thomas',}