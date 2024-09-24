import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import joblib
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_saved_models():
    """
    Load the pre-saved models and parameters from disk.

    Returns:
    - dict: Dictionary containing encoder, imputer, categorical_cols, all_features, selected_features, and classifier.
    """
    paths = {
        'encoder': './model/encoder.joblib',
        'imputer': './model/imputer.joblib',
        'categorical_cols': './model/categorical_cols.joblib',
        'all_features': './model/all_features.joblib',
        'classifier': './model/xgboost_model.joblib'
    }
    
    models = {}
    for key, path in paths.items():
        try:
            models[key] = joblib.load(path)
        except Exception as e:
            logging.error(f"Failed to load {key}: {e}")
            return None

    # Manually provide the list of selected features
    models['selected_features'] = ['dur', 'spkts', ...]  # continue with the rest of the features
    
    return models

def preprocess_data(new_data, models):
    """
    Preprocess the input data.

    Parameters:
    - new_data (DataFrame): The data to be preprocessed.
    - models (dict): Dictionary containing pre-saved models and parameters.

    Returns:
    - DataFrame: Preprocessed data.
    """
    X_new = new_data.drop(['id'], axis=1)
    categorical_cols = X_new.select_dtypes(include=['object']).columns.tolist()
    
    # One-hot encoding
    encoded_cat_new = models['encoder'].transform(X_new[categorical_cols])
    encoded_cat_df_new = pd.DataFrame(encoded_cat_new, columns=models['encoder'].get_feature_names_out(categorical_cols))
    
    # Combine encoded data
    X_encoded_new = pd.concat([X_new.drop(categorical_cols, axis=1).reset_index(drop=True), encoded_cat_df_new.reset_index(drop=True)], axis=1)
    
    # Missing Value Imputation
    X_imputed_new = models['imputer'].transform(X_encoded_new)
    
    # Feature selection
    selected_features= ['dur', 'spkts', 'dpkts', 'sbytes', 'dbytes', 'rate', 'sttl', 'dttl', 'sload', 'dload', 'sloss', 'dloss', 'sinpkt', 'dinpkt', 'sjit', 'djit', 'swin', 'stcpb', 'dtcpb', 'dwin', 'tcprtt', 'synack', 'ackdat', 'smean', 'dmean', 'ct_srv_src', 'ct_state_ttl', 'ct_dst_ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'ct_src_ltm', 'ct_srv_dst', 'proto_tcp', 'state_INT']
    X_selected_new = pd.DataFrame(X_imputed_new, columns=X_encoded_new.columns.tolist())[selected_features]

    return X_selected_new

def make_predictions(X, classifier):
    """
    Use the provided classifier to make predictions on the data.

    Parameters:
    - X (DataFrame): The data on which predictions should be made.
    - classifier: Pre-trained classifier.

    Returns:
    - array: Array of predictions.
    """
    return classifier.predict(X)

def predict(path,logger):
    # Load the data
    new_data = pd.read_csv(path)
    logger.info(f"Data loaded with shape: {new_data.shape}")
    
    # Load saved models and parameters
    models = load_saved_models()
    if not models:
        logger.error("Failed to load models. Exiting!")
        return

    # Preprocess the data
    X = preprocess_data(new_data, models)
    logger.info(f"Data preprocessed with shape: {X.shape}")
    
    # Predict using the loaded classifier
    predictions = make_predictions(X, models['classifier'])
    new_data['predicted_label'] = predictions
    logger.info(f"Predictions made with shape: {predictions.shape}")

    # Count and display the number of predictions where label is 1
    count_predicted_label_1 = len(new_data[new_data["predicted_label"] == 1])
    logger.info(f"Number of rows with predicted_label equal to 1: {count_predicted_label_1}")

    # Save predictions with label 1 to CSV
    attacks = new_data[new_data["predicted_label"] == 1]
    attacks.to_csv('./csv_files/attacks.csv', index=False)
    logger.info(f"Saved attacks to 'attacks.csv'")

if __name__ == "__main__":
    predict()
