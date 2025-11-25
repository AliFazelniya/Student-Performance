from pathlib import Path
from typing import List, Tuple

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


def load_datasets() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load the math and Portuguese datasets from the raw data directory."""
    mat_path = RAW_DATA_DIR / "student-mat.csv"
    por_path = RAW_DATA_DIR / "student-por.csv"
    mat_df = pd.read_csv(mat_path, sep=";")
    por_df = pd.read_csv(por_path, sep=";")
    return mat_df, por_df


def build_preprocessor(feature_columns: List[str]) -> ColumnTransformer:
    binary_cols = [
        "sex",
        "address",
        "famsize",
        "Pstatus",
        "schoolsup",
        "famsup",
        "paid",
        "activities",
        "nursery",
        "higher",
        "internet",
        "romantic",
    ]
    categorical_cols = ["school", "Mjob", "Fjob", "reason", "guardian"]
    numeric_cols = [col for col in feature_columns if col not in binary_cols + categorical_cols]

    # OneHotEncode categoricals and scale numerics; drop one level for binary flags.
    return ColumnTransformer(
        transformers=[
            ("bin", OneHotEncoder(drop="if_binary"), binary_cols),
            ("cat", OneHotEncoder(), categorical_cols),
            ("num", StandardScaler(), numeric_cols),
        ]
    )


def save_processed(df_mat: pd.DataFrame, df_por: pd.DataFrame) -> None:
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    df_mat.to_csv(PROCESSED_DATA_DIR / "processed_mat.csv", index=False)
    df_por.to_csv(PROCESSED_DATA_DIR / "processed_por.csv", index=False)


def main() -> None:
    mat, por = load_datasets()
    preprocessor = build_preprocessor(mat.columns.tolist())

    processed_mat = preprocessor.fit_transform(mat)
    processed_por = preprocessor.transform(por)

    bin_enc = preprocessor.named_transformers_["bin"]
    cat_enc = preprocessor.named_transformers_["cat"]

    bin_feature_names = bin_enc.get_feature_names_out(bin_enc.feature_names_in_)
    cat_feature_names = cat_enc.get_feature_names_out(cat_enc.feature_names_in_)
    num_feature_names = preprocessor.transformers_[2][2]

    all_feature_names = list(bin_feature_names) + list(cat_feature_names) + list(num_feature_names)

    df_mat = pd.DataFrame(processed_mat, columns=all_feature_names)
    df_por = pd.DataFrame(processed_por, columns=all_feature_names)

    save_processed(df_mat, df_por)
    print("DONE! CSV files saved successfully!")


if __name__ == "__main__":
    main()
