# -*- coding: utf-8 -*-
"""DelhiHousePrices.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xt_OzcdyeGaVpP5OSNwvE1cSJfoEfP_Y
"""

#import all the necessary libraries import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# mount file on drive in colab
from google.colab import drive
drive.mount('/content/drive')
path='/content/drive/My Drive/House price prediction model/MagicBricks.csv'

#access the file
df=pd.read_csv(path)

#gather information about the data
df.head()
df.info()
df.describe()

df.columns

#Data Cleaning
#missing values
print(df.isnull().sum())

# Drop rows with missing target values
df.dropna(subset=['Price'], inplace=True)

#Finding outliers
sns.countplot(x='BHK', data=df)

df['BHK'].value_counts()

#identified rows to drop
df.drop([721,345,163,164,261,352,353,585],inplace=True)

#Finding outliers
sns.countplot(x='Bathroom', data=df)

df.drop([225,495,527,659,676,681,1211,248,1029],inplace=True)

df.Parking.fillna(0,inplace=True)

#Finding outliers
sns.countplot(x='Parking', data=df)

df['Parking'].replace([39,114],1,inplace=True)
df['Parking'].replace([5,9,10],4,inplace=True)

#area and price related so per sq ft not needed
df.drop('Per_Sqft',axis=1,inplace=True)

df.isnull().sum()

#null imputations reqd
df.Bathroom.fillna(df.Bathroom.median(),inplace=True)
df.Type.fillna('Apartment',inplace=True)
df.Furnishing.fillna('Semi-Furnished',inplace=True)

df.drop('Locality',axis=1,inplace=True)

#onehotencoding
df = pd.get_dummies(df)

df.columns

df = df.astype(float)

for col in df.columns:
    m = max(df[col])
    df[col] = df[col]/m

X = df.drop('Price', axis=1)
y = df['Price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

from sklearn.metrics import r2_score

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'\nMean Squared Error: {mse}')
print(f'R-squared: {r2}')

plt.scatter(y_test, y_pred, marker='o', label='Actual vs Predicted Prices')
plt.plot(y_test, y_test, color='r', label='Ideal Predictions')  # plot the ideal line where actual = predicted
plt.xlabel('Actual Prices')
plt.ylabel('Predicted Prices')
plt.title('Actual vs Predicted Prices')
plt.legend()
plt.show()