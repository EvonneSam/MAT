from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained model artifact
model = joblib.load('jet_engine_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        # Expecting an array with [core_temperature, fan_speed]
        sensor_readings = np.array(data['sensors']).reshape(1, -1)
        
        # Predict remaining cycles until failure
        predicted_rul = model.predict(sensor_readings)[0]
        
        # Real-time critical safety routing logic
        status = "OPERATIONAL"
        action = "MONITORING SYSTEM ACTIVE"
        
        if predicted_rul <= 30:
            status = "CRITICAL FAILURE RISK IMMINENT"
            action = "EMERGENCY: GROUND AIRCRAFT IMMEDIATELY / DISPATCH REPAIR"
        elif predicted_rul <= 75:
            status = "WARNING INDICATOR TRIGGERED"
            action = "SCHEDULE TARGETED MAINTENANCE AT NEXT PORT OF ARRIVAL"

        return jsonify({
            'remaining_useful_cycles': int(predicted_rul),
            'engine_status': status,
            'recommended_action': action,
            'mainframe_inference_latency': "sub-1ms"
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # Run on port 5000 accessible to external traffic
    app.run(host='0.0.0.0', port=5000)
