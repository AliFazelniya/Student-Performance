import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# 1) Load datasets
mat = pd.read_csv("student-mat.csv", sep=';')
por = pd.read_csv("student-por.csv", sep=';')

# 2) Define columns
binary_cols = [
    "sex", "address", "famsize", "Pstatus",
    "schoolsup", "famsup", "paid", "activities",
    "nursery", "higher", "internet", "romantic"
]

categorical_cols = ["school", "Mjob", "Fjob", "reason", "guardian"]

numeric_cols = [col for col in mat.columns if col not in binary_cols + categorical_cols]

# 3) Build preprocessors
preprocessor = ColumnTransformer(transformers=[
    ("bin", OneHotEncoder(drop="if_binary"), binary_cols),
    ("cat", OneHotEncoder(), categorical_cols),
    ("num", StandardScaler(), numeric_cols)
])

# 4) Fit on mat dataset
processed_mat = preprocessor.fit_transform(mat)
processed_por = preprocessor.transform(por)

# 5) Extract fitted encoders
bin_enc = preprocessor.named_transformers_["bin"]
cat_enc = preprocessor.named_transformers_["cat"]

# 6) Build final column names
bin_feature_names = bin_enc.get_feature_names_out(binary_cols)
cat_feature_names = cat_enc.get_feature_names_out(categorical_cols)
num_feature_names = numeric_cols

all_feature_names = list(bin_feature_names) + list(cat_feature_names) + num_feature_names

# 7) Convert to DataFrame
df_mat = pd.DataFrame(processed_mat, columns=all_feature_names)
df_por = pd.DataFrame(processed_por, columns=all_feature_names)

# 8) Save CSV
df_mat.to_csv("processed_mat.csv", index=False)
df_por.to_csv("processed_por.csv", index=False)

print("DONE! CSV files saved successfully!")
