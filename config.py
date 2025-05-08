import dotenv
import os
import logging


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(module)s - %(message)s")

dotenv.load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]