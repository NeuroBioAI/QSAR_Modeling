# QSAR Modeling for pIC50 Prediction

## Overview

QSAR (Quantitative Structure–Activity Relationship) modeling is a computational approach used to predict the biological activity of compounds based on their molecular structures. It can be used for virtual screening of molecular libraries to identify promising compounds that may serve as potential drug candidates.

In this project, a QSAR pipeline was developed to predict the **pIC50** values of molecules from their molecular representations. The workflow includes molecular descriptor calculation, molecular fingerprint generation, data preprocessing, feature selection, regression modeling, and model evaluation.

The main goal of the project was to investigate how different molecular representations perform in predicting pIC50 and to compare several regression algorithms to identify the best-performing model.

---

## Project Workflow

This project consists of three main stages:

1. Molecular descriptor and fingerprint calculation
2. Data preprocessing and feature selection
3. Regression modeling and pIC50 prediction

```text
Molecular Structures (SMILES)
          │
          ▼
Descriptor & Fingerprint Calculation
          │
          ▼
Data Preprocessing
          │
          ▼
Feature Selection
          │
          ▼
20 Selected Molecular Descriptors
          │
          ├───────────────┐
          │               │
          ▼               ▼
   Morgan Fingerprint   Combined Features
          │               │
          └───────┬───────┘
                  ▼
          Regression Models
                  │
                  ▼
             Predictions
                  │
                  ▼
              Evaluation
                  │
                  ▼
          Model Comparison
```

---

## Dataset

The dataset contains **180 molecules** with available SMILES representations and experimentally measured IC50 values.

The IC50 values were converted to **pIC50** values and used as the target variable for regression modeling.

The molecular SMILES were used to calculate molecular descriptors and Morgan fingerprints.

---

# 1. Molecular Descriptors and Fingerprints

In the first stage, molecular representations were generated from the SMILES structures.

### Extended Molecular Descriptors

An extended descriptor function was developed to calculate a large set of molecular descriptors using RDKit.

The resulting dataset initially contained **217 molecular descriptors**, which were later used for preprocessing and feature selection.

### Morgan Fingerprints

Morgan fingerprints were generated to represent molecular structural features and substructures.

The fingerprint configuration used in this project was:

* **Radius:** 2
* **Number of bits:** 2048

The fingerprints were later used as an alternative molecular representation for regression modeling.

---

# 2. Data Preprocessing and Feature Selection

The second stage focused on improving the quality of the molecular descriptor dataset and reducing redundant features.

The preprocessing workflow included:

### Missing Value Analysis

The descriptor dataset was examined for missing values before applying feature selection techniques.

### Constant Feature Removal

Descriptors with constant values across the dataset were identified and removed because they do not provide useful information for regression modeling.

### Correlation Analysis

A correlation matrix was generated to identify highly correlated molecular descriptors.

Highly correlated features were filtered to reduce redundancy and improve the quality of the feature set.

Through these preprocessing steps, the number of descriptors was reduced from:

**217 → 118 descriptors**

### Random Forest Feature Importance

Random Forest feature importance was then used to rank the remaining descriptors according to their contribution to the regression model.

The **top 30 descriptors** were selected based on their feature importance scores.

### Recursive Feature Elimination (RFE)

Finally, Recursive Feature Elimination (RFE) was applied to further reduce the feature set and select the final molecular descriptors.

The final selected feature set contained:

**20 molecular descriptors**

These 20 descriptors were used as the final descriptor-based representation in the regression stage.

---

# 3. Regression Modeling for pIC50 Prediction

The final stage of the project focused on developing regression models to predict the pIC50 values of the molecules.

Three machine learning algorithms were evaluated:

* **Linear Regression**
* **Random Forest Regressor**
* **Support Vector Regression (SVR)**

To investigate the effect of different molecular representations, three separate feature sets were evaluated.

### 3.1 Selected Molecular Descriptors

The final **20 selected molecular descriptors** were used as input features.

Three regression models were trained:

* Linear Regression
* Random Forest Regressor
* SVR

Predictions were generated on the test set and evaluated using R², RMSE, and MAE.

For the SVR model, the descriptor features were standardized before model training.

### 3.2 Morgan Fingerprints

The **2048-bit Morgan fingerprints** generated with a radius of 2 were used as the second molecular representation.

The same three regression algorithms were trained using the fingerprint representation.

For SVR, the fingerprint features were standardized before training.

### 3.3 Combined Descriptors and Fingerprints

In the third approach, the final 20 molecular descriptors were combined with the Morgan fingerprints to create a combined molecular representation.

The same three regression algorithms were then trained and evaluated using this combined feature set.

In total:

**3 feature representations × 3 regression algorithms = 9 regression models**

were trained and evaluated.

---

# 4. Model Evaluation

The trained models were evaluated on their test sets using three regression metrics:

### R² (R-squared)

R² measures how well the model explains the variance in the target variable.

Higher values indicate better performance.

### RMSE (Root Mean Squared Error)

RMSE measures the magnitude of prediction errors while giving greater weight to larger errors.

Lower values indicate better performance.

### MAE (Mean Absolute Error)

MAE measures the average absolute difference between the predicted and experimentally measured pIC50 values.

Lower values indicate better performance.

A reusable evaluation function was developed to calculate all three metrics consistently across the nine models.

---

# 5. Results and Model Comparison

The performance of all nine models is summarized below.

| Model             | Data Representation |        R² |      RMSE |       MAE |
| ----------------- | ------------------- | --------: | --------: | --------: |
| Linear Regression | Descriptors         |    -0.618 |     0.899 |     0.683 |
| **Random Forest** | **Descriptors**     | **0.542** | **0.478** | **0.405** |
| SVR               | Descriptors         |     0.423 |     0.537 |     0.458 |
| Linear Regression | Morgan Fingerprint  |    -0.133 |     0.752 |     0.578 |
| Random Forest     | Morgan Fingerprint  |     0.533 |     0.483 | **0.397** |
| SVR               | Morgan Fingerprint  |     0.508 |     0.496 |     0.414 |
| Linear Regression | Combined            |    -0.618 |     0.899 |     0.683 |
| **Random Forest** | **Combined**        | **0.556** | **0.471** | **0.394** |
| SVR               | Combined            |     0.448 |     0.525 |     0.438 |

Among the evaluated models, the **Random Forest Regressor using the combined molecular descriptors and Morgan fingerprints** achieved the best overall performance:

* **R² = 0.556**
* **RMSE = 0.471**
* **MAE = 0.394**

The Random Forest model using the 20 selected descriptors alone also performed well, with an R² of 0.542.

The results indicate that the Random Forest models generally outperformed Linear Regression and SVR for this dataset.

Linear Regression produced negative R² values for the descriptor and combined representations, indicating poor predictive performance on the test set.

---

# 6. Visualization

Several visualizations were generated to analyze the modeling results.

### Feature Importance

Random Forest feature importance was visualized to examine the relative contribution of the selected molecular descriptors.

### Predicted vs. True pIC50

A scatter plot of experimentally measured versus predicted pIC50 values was generated for the selected model.

In an ideal prediction model, the points should be distributed close to the diagonal line, indicating good agreement between predicted and experimental values.

---

# 7. Project Structure

```text
QSAR_MODELING/
│
├── data/
│   ├── input/
│   │   └── IC50LiBA.csv
│   │
│   └── output/
│       ├── basic_descriptors.csv
│       ├── extended_descriptors.csv
│       ├── fingerprint.csv
│       ├── pIC50LiBA.csv
│       ├── descriptors_top30features.csv
│       ├── UnCorrelated_descriptors.csv
│       └── QSAR_descriptors.csv
│
├── notebooks/
│   ├── 01_Data_Curation.ipynb
│   ├── 02_Descriptors.ipynb
│   ├── 03_Preprocessing.ipynb
│   ├── 04_Feature_selection.ipynb
│   └── 05_Regression_models.ipynb
│
├── src/
│   ├── descriptors.py
│   └── fingerprint.py
│
├── README.md
└── requirements.txt
```

The notebooks represent the main stages of the workflow, while reusable molecular descriptor and fingerprint calculation functions are stored separately in the `src` directory.

---

# 8. Libraries and Tools

The project was developed using Python and the following main libraries:

* **RDKit** — molecular structure processing and descriptor/fingerprint calculation
* **Pandas** — data manipulation and analysis
* **NumPy** — numerical computation
* **Scikit-learn** — preprocessing, feature selection, regression models, and evaluation metrics
* **Matplotlib** — data visualization
* **Seaborn** — statistical visualization
* **Jupyter Notebook** — development and experimentation
* **VS Code** — development environment

---

# 9. Conclusion

This project demonstrates the development of a complete QSAR modeling workflow for pIC50 prediction, starting from molecular SMILES and experimentally measured IC50 values and progressing through molecular representation, preprocessing, feature selection, machine learning, prediction, and evaluation.

A total of nine regression models were developed using three different molecular representations and three regression algorithms.

Among the tested approaches, the **Random Forest Regressor using the combined molecular descriptors and Morgan fingerprints** achieved the best overall performance, with an R² of **0.556**, RMSE of **0.471**, and MAE of **0.394**.

The project also demonstrates the importance of molecular representation and feature selection in QSAR modeling. Reducing the descriptor space from 217 initial descriptors to a final set of 20 selected descriptors allowed the regression models to work with a more focused and less redundant feature set.

---

# 10. Future Work

Several improvements can be considered for future development of the project:

* Hyperparameter optimization for the regression models
* Cross-validation for more robust model evaluation
* Testing additional regression algorithms
* Further optimization of the Random Forest model
* External validation using an independent molecular dataset
* Applying the trained model to a new molecular library for pIC50 prediction
* Expanding the workflow toward virtual screening of candidate molecules

---

## Project Status

**Completed:** Core QSAR modeling pipeline

The current pipeline includes:

* Data curation
* pIC50 calculation
* Molecular descriptor calculation
* Morgan fingerprint generation
* Descriptor preprocessing
* Feature selection
* Regression model training
* Prediction
* Model evaluation
* Model comparison
* Visualization
