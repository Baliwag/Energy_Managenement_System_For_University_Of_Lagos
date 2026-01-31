# UNILAG Energy Management and Forecasting System

## Overview

The UNILAG Energy Management and Forecasting System is a comprehensive machine learning-based solution for predicting hourly energy consumption across multiple feeders in a university campus environment. This system leverages Long Short-Term Memory (LSTM) neural networks to generate accurate 8760-hour (one-year) forecasts of energy usage patterns, accounting for academic calendar variations and seasonal effects.

## Key Features

- **Multi-feeder forecasting**: Predicts energy consumption for individual feeders (Feeder1-9 and Service Area)
- **Academic calendar integration**: Automatically adjusts predictions based on academic sessions and holidays
- **Relationship-aware calculations**: Properly models the relationships between feeders and PHCN components
- **8760-hour forecasting**: Generates complete one-year forecasts at hourly resolution
- **Comprehensive visualization**: Provides multiple plots for analysis and validation
- **Historical data validation**: Compares forecasts against actual historical data

## Installation

### Prerequisites

```bash
# Required Python packages
pip install pandas numpy matplotlib scikit-learn tensorflow
```

### Dependencies

- Python 3.8+
- pandas >= 1.4.0
- numpy >= 1.21.0
- matplotlib >= 3.5.0
- scikit-learn >= 1.0.0
- tensorflow >= 2.10.0

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/baliwag/Energy_Managenement_System_For_University_Of_Lagos.git
cd Energy_Managenement_System_For_University_Of_Lagos
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Prepare your data file:
   - Ensure you have `unilag_profile_load_Jun2024_Jun2025.xlsx` in the project directory
   - The file should contain hourly energy readings for all feeders

## Usage

### Basic Usage

Run the main forecasting script:

```bash
python unilag_lstm_forecast_multi_feeder_v2.py
```

### Expected Input Data Format

The system expects an Excel file with the following columns:
- `Timestamp`: DateTime index
- `Feeder1` to `Feeder9`: Individual feeder energy readings (in appropriate units)
- `Service_Area`: Service area energy reading
- `PHCN_A_amps`: Sum of Feeder1,9,4,3,2 (automatically calculated if missing)
- `PHCN_B_amps`: Sum of Feeder8,7,6,5,Service_Area (automatically calculated if missing)
- `Total_MW`: Total energy in MW ((PHCN_A + PHCN_B)/60)

### Output Files

The system generates:
- `unilag_LSTM_8760h_forecast_Jun2025_Jun2026.csv`: Complete hourly forecasts for all feeders and derived metrics
- `lstm_forecast_plots.png`: Visualization of forecast results

### Configuration Options

Key configuration parameters in the script:

```python
LOOKBACK = 24           # Hours of historical data to use for prediction
FORECAST_H = 8760      # Hours to forecast (one year)
EPOCHS = 50            # Training epochs for LSTM
BATCH = 64             # Batch size for training
START_FCST = "2025-06-02 00:00"  # Start date for forecast
```

## Methodology

### Data Processing Pipeline

1. **Data Loading and Cleaning**: Loads historical energy data and handles missing values
2. **Academic Calendar Integration**: Applies scaling factors based on university schedule
3. **Feature Engineering**: Adds temporal features (month, weekday, hour, cyclic features)
4. **Model Training**: Trains individual LSTM models for each feeder
5. **Forecast Generation**: Rolls forward predictions for 8760 hours
6. **Derived Calculations**: Computes PHCN_A, PHCN_B, and Total_MW based on feeder relationships

### Model Architecture

Each feeder uses an LSTM neural network with:
- Input: 24 hours of historical data + calendar features
- LSTM layer: 64 units
- Dense layers: 32 units (ReLU activation) + 1 output unit
- Loss function: Mean Squared Error
- Optimizer: Adam

### Academic Calendar Scaling

The system accounts for university schedule variations:
- **Regular session**: Full load (scale factor = 1.0)
- **May/late semester**: Reduced load (scale factor = 0.8)
- **Long vacation (Sep-Nov)**: Significant reduction (scale factor = 0.6)
- **Christmas break**: Reduced load (scale factor = 0.6)

## Example Usage

```python
# Customize the forecast start date
START_FCST = pd.Timestamp("2025-07-01 00:00")

# Adjust academic calendar if needed
def custom_academic_scale(ts):
    # Add custom scaling rules
    if ts.month in [6, 7]:  # Summer break
        return 0.5
    return academic_scale(ts)  # Use default otherwise
```

## Testing

The system includes validation through:
- Train/test split (80/20)
- Performance metrics (MAE, RMSE, MAPE)
- Comparison with historical data
- Visualization of test set performance

Run the basic test:
```bash
python -c "import pandas as pd; print('Testing import...'); print('All imports successful!')"
```

## Community Guidelines

### Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

### Reporting Issues

Use the GitHub Issues tab to report:
- Bugs or unexpected behavior
- Feature requests
- Documentation improvements

### Support

For questions about using the system:
- Check the documentation
- Review example usage
- Open an issue for specific questions

## Citation

If you use this system in your research, please cite:

```
@software{unilag_energy_forecasting_2025,
  author = {Ibrahim Ajibade},
  title = {UNILAG Energy Management Prediction System},
  year = {2025},
  url = {https://github.com/baliwag/Energy_Managenement_System_For_University_Of_Lagos}
}
```

## License

This project is licensed under the Apache License - see the LICENSE file for details.

## Acknowledgments

- University of Lagos for providing the energy data
- TensorFlow and scikit-learn communities for machine learning tools
- Contributors and testers who helped improve the system

## Contact

For questions about the project, please contact:
- Project maintainer: [Ibrahim Ajibade]
- Email: [ajibadeia@gmail.com]
- Department: Electrical and Electronics Engineering, University of Lagos

---

*Note: This system is designed for research and educational purposes. Always validate forecasts against actual measurements before making operational decisions.*
