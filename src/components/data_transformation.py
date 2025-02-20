import os
import sys
from src.logger import logging
from src.exception import CustomException
from src.utils import save_object
import pandas as pd
import numpy as np

from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.compose import ColumnTransformer
from dataclasses import dataclass


@dataclass
class DataTransformationconfig:
    preprocessor_obj_file_path = os.path.join('Artifacts', 'preprocessor_obj.pkl')

class DataTransformation():
    def __init__(self):
        self.data_transformer_config = DataTransformationconfig()
    
    def get_datatransformer_object(self):
        try:
            num_columns =  ['reading_score', 'writing_score']
            cat_columns =  ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']
            logging.info("Numerical and Categorical features Encoding in pipeline has started")
            num_pipeline = Pipeline(
                steps=[('imputer', SimpleImputer(strategy='median')),
                       ('Scaler', StandardScaler())])
            
            
            cat_pipeline = Pipeline(
                steps=[('imputer', SimpleImputer(strategy='most_frequent')),
                       ('Onehotencoder', OneHotEncoder()),
                       ('Scaler', StandardScaler(with_mean=False))]
            )

            logging.info("Numerical and Categorical features are encoded in pipeline")
            
            preprocessor = ColumnTransformer(
                [('num_tranformer', num_pipeline, num_columns),
                ('cat_transformer', cat_pipeline, cat_columns)]
            )
            
            logging.info("Numerical and Categorical features transformation is done")

            return preprocessor
            
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object")
            preprocessing_obj = self.get_datatransformer_object()

            target_column_name="math_score"
            numerical_columns = ["writing_score", "reading_score"]

            input_feature_train_df = train_df.drop(columns=target_column_name,axis=1)
            target_feature_train_df = train_df[target_column_name]
            input_feature_test_df = test_df.drop(columns=target_column_name,axis=1)
            target_feature_test_df = test_df[target_column_name]
            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            save_object(filepath=self.data_transformer_config.preprocessor_obj_file_path, obj=preprocessing_obj)

            return (
                train_arr,
                test_arr,
                self.data_transformer_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e,sys)
