import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

# Create dummy columns to simulate the NASA dataset structure smoothly
columns = ['engine_id', 'cycle', 'setting1', 'setting2', 'setting3'] + [f'sensor{i}' for i in range(1, 22)]

print("Simulating clean sensor stream data tracking...")
# Create mock time-series data to represent engine cycles decaying over time
np.random.seed(42)
rows = []
for engine in range(1, 11): # 10 engines
    max_life = np.random.randint(120, 200) # Each engine runs until failure
    for cycle in range(1, max_life + 1):
        # Calculate a decaying health factor as cycles approach max_life
        health_factor = (max_life - cycle) / max_life
        
        # Core temperature and fan speeds increase as health degrades
        core_temp = 500 + (100 * (1 - health_factor)) + np.random.normal(0, 5)
        fan_speed = 1200 + (300 * (1 - health_factor)) + np.random.normal(0, 10)
        
        # Generate stable dummy values for remaining sensors
        row = [engine, cycle, 0.0, 0.0, 0.0] + [core_temp, fan_speed] + [np.random.normal(10, 1) for _ in range(19)]
        rows.append(row)

train_df = pd.DataFrame(rows, columns=columns)

# Calculate Target Variable: Remaining Useful Life (RUL)
max_cycles = train_df.groupby('engine_id')['cycle'].max().reset_index()
max_cycles.columns = ['engine_id', 'max_cycle']
train_df = train_df.merge(max_cycles, on='engine_id')
train_df['RUL'] = train_df['max_cycle'] - train_df['cycle']

# Train on our 2 main critical indicator features (Core Temp and Fan Speed)
features = ['sensor1', 'sensor2']
X = train_df[features]
y = train_df['RUL']

print("Training predictive model on critical patterns...")
model = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1)
model.fit(X, y)

# Save the trained model binary artifact
joblib.dump(model, 'jet_engine_model.pkl')
print("Success! 'jet_engine_model.pkl' created and saved.")
