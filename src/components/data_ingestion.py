import os
import sys
from src.logger import logging
from src.exception import CustomException
from src.components.data_transformation import DataTransformationconfig, DataTransformation
from src.components.model_trainer import ModelTrainer,ModelTrainerConfig


import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    train_data_path = os.path.join('Artifacts', 'train_data.csv')
    test_data_path = os.path.join('Artifacts', 'test_data.csv')
    raw_data_path = os.path.join('Artifacts', 'data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        try:

            logging.info("Initiating the Data Ingestion process")
            
            logging.info("Reading the data")
            df = pd.read_csv('notebook\data\stud_perf.csv')

            logging.info("Creating Artifacts folder")
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)

            logging.info("Writing raw data to Artifacts")
            df.to_csv(self.ingestion_config.raw_data_path,index=False)

            logging.info("Initiating train test split of data")
            train_set, test_set = train_test_split(df,test_size=0.2,random_state=42)

            logging.info("Writing training data to Artifacts")
            train_set.to_csv(self.ingestion_config.train_data_path,index=False)

            logging.info("Writing testing data to Artifacts")
            test_set.to_csv(self.ingestion_config.test_data_path,index=False)

            logging.info("Data Ingestion is completed successfully")

            return (self.ingestion_config.train_data_path, self.ingestion_config.test_data_path)

        except Exception as e:
            raise CustomException(e,sys)
        
if __name__ == "__main__":
    obj = DataIngestion()
    train_path ,test_path = obj.initiate_data_ingestion()

    data_transformation=DataTransformation()
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_path ,test_path)

    model_trainer = ModelTrainer()
    print(model_trainer.initiate_model_trainer(train_arr, test_arr))
        



