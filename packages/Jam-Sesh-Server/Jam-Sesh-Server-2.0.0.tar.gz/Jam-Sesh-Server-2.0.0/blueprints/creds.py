import dotenv
import os
from celery import Celery

dotenv.load_dotenv()

celery_link = Celery('task',
                     broker=os.getenv("BROKER_URL"),
                     backend='db+postgresql+psycopg2://' + os.getenv("DATABASE_URL"))

