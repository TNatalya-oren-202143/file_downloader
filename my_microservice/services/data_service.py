import pandas as pd
from my_microservice.data_loader.loader_factory import DataLoaderFactory

class DataService:
    def __init__(self):
        self.factory = DataLoaderFactory()

    def process_data(self, file_path: str) -> pd.DataFrame:
        loader = self.factory.create_loader(file_path)
        data = loader.load_data(file_path)
        return data
