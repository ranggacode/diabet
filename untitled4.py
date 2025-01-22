# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1G5gTRtQApeL3QmKFTu_TOGTcUSMOyZ30
"""

pip install streamlit tensorflow pandas scikit-learn

import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Concatenate
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load the dataset
def load_data():
    url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
    column_names = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age", "Outcome"]
    data = pd.read_csv(url, names=column_names)
    return data

# Preprocess the data
def preprocess_data(data):
    X = data.drop("Outcome", axis=1)
    y = data["Outcome"]

    # Standardize the data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y

# Build the Wide & Deep model
def build_model(input_shape):
    # Wide part (linear)
    wide_input = Input(shape=(input_shape,), name="wide_input")
    wide_output = Dense(1, activation='sigmoid', name="wide_output")(wide_input)

    # Deep part (non-linear)
    deep_input = Input(shape=(input_shape,), name="deep_input")
    deep_layer_1 = Dense(64, activation='relu')(deep_input)
    deep_layer_2 = Dense(32, activation='relu')(deep_layer_1)
    deep_output = Dense(1, activation='sigmoid', name="deep_output")(deep_layer_2)

    # Concatenate wide and deep outputs
    merged_output = Concatenate()([wide_output, deep_output])
    final_output = Dense(1, activation='sigmoid', name="final_output")(merged_output)

    # Create model
    model = Model(inputs=[wide_input, deep_input], outputs=final_output)
    model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])

    return model

# Train the model
def train_model(X, y):
    # Split data into training and testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Build and train the model
    model = build_model(X.shape[1])
    model.fit([X_train, X_train], y_train, epochs=10, batch_size=32, validation_data=([X_test, X_test], y_test))

    return model

# Streamlit user interface
def main():
    st.title("Prediksi Penyakit Diabetes")

    # Load and preprocess data
    data = load_data()
    X, y = preprocess_data(data)

    # Sidebar input for prediction
    st.sidebar.header("Masukkan Data Pengguna")
    pregnancies = st.sidebar.number_input("Jumlah Kehamilan", min_value=0, max_value=20, value=1)
    glucose = st.sidebar.number_input("Kadar Glukosa", min_value=0, max_value=250, value=100)
    blood_pressure = st.sidebar.number_input("Tekanan Darah", min_value=0, max_value=200, value=70)
    skin_thickness = st.sidebar.number_input("Ketebalan Kulit", min_value=0, max_value=100, value=20)
    insulin = st.sidebar.number_input("Kadar Insulin", min_value=0, max_value=1000, value=50)
    bmi = st.sidebar.number_input("BMI", min_value=0.0, max_value=50.0, value=25.0)
    diabetes_pedigree = st.sidebar.number_input("Fungsi Pedigree Diabetes", min_value=0.0, max_value=2.0, value=0.5)
    age = st.sidebar.number_input("Usia", min_value=0, max_value=120, value=30)

    user_input = np.array([[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree, age]])

    # Train the model only once (you can save and load a trained model for production)
    model = train_model(X, y)

    # Standardize the user input
    scaler = StandardScaler()
    user_input_scaled = scaler.fit_transform(user_input)

    # Make prediction
    prediction = model.predict([user_input_scaled, user_input_scaled])

    if prediction >= 0.5:
        st.write("Prediksi: Diabetes Positif")
    else:
        st.write("Prediksi: Diabetes Negatif")

if __name__ == "__main__":
    main()

!streamlit run Untitled4.ipynb