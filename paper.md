```

title: 'Design and Development of a Smart Energy Management System for UNILAG, Akoka Campus'
tags:

* Smart Grid
* Artificial Intelligence
* IoT
* LSTM
* Energy Forecasting
* Sustainable Development
authors:
* name: Ajibade, Ibrahim Adebowale
corresponding: true
affiliation: 1
* name: Prof. P. O. Oluseyi
affiliation: 1
affiliations:
* name: Department of Electrical and Electronics Engineering, University of Lagos, Nigeria
index: 1
date: 31 January 2026
bibliography: paper.bib

```

# Summary

The University of Lagos (UNILAG) Akoka campus faces significant challenges stemming from inefficient energy management and exorbitant utility costs. These high bills strain institutional finances, limiting funds for research and infrastructure. This project addresses these issues through the development of a Smart Energy Management System (SEMS) leveraging Artificial Intelligence (AI) and the Internet of Things (IoT).

By utilizing a year-long dataset of hourly energy consumption (June 2024–June 2025) from the UNILAG Service Station, the research implements a Long Short-Term Memory (LSTM) neural network to forecast energy demand. The project culminates in an interactive, web-based dashboard that translates complex data into actionable insights for energy managers, providing a scalable blueprint for reducing waste and enhancing grid reliability in tertiary institutions.

# Statement of Need

Public universities in Nigeria are often burdened by unreliable electricity services and high Band A tariffs. Without a centralized management system, UNILAG experiences energy waste and an over-reliance on the national grid. There is a pressing need for data-driven frameworks that can predict demand and optimize consumption patterns.

The SEMS developed in this work fills this gap by providing a prototype capable of processing and forecasting energy data. While existing literature often relies on simulations from developed regions, this project uses local, empirical data to account for specific grid instabilities and academic schedules.

# Research Methodology

The system is grounded in the integration of Smart Grids, AI, and IoT.

* 
**Data Collection**: Hourly load profile data was obtained from the UNILAG Service Station, totaling 8,784 data points per feeder.


* 
**Software Stack**: Python was the primary language, using `Pandas` for wrangling, `TensorFlow/Keras` for deep learning, and `Streamlit` for dashboard deployment.


* 
**Model Architecture**: A stacked LSTM network was designed to capture long-term temporal dependencies in the time-series data.



# Performance Evaluation

The LSTM model was evaluated using standard error metrics to ensure reliability:

* 
**Mean Absolute Error (MAE)**: Measures the average magnitude of errors.


* 
**Root Mean Squared Error (RMSE)**: Penalizes larger errors, useful for grid stability.


* 
**Mean Absolute Percentage Error (MAPE)**: Provides a percentage-based accuracy assessment.



The model demonstrated robust performance across different feeders, such as Feeder 5, which achieved an MAE of 2.68 MW and an RMSE of 3.53 MW.

# Visualization and Insights

The deployed dashboard (Figure 4.15) allows managers to filter data by day, week, or month to visualize energy predictions and estimated costs. Analysis revealed that demand is heavily influenced by academic cycles, with reduced loads during semester breaks and peaks during examination periods.

# Mathematical Framework

The LSTM gates—Input (), Forget (), and Output ()—are governed by the following sigmoid () functions:

The final evaluation for accuracy is calculated as:

# Conclusion

The project successfully demonstrates that AI-powered forecasting can form the bedrock of a strategic energy management policy for UNILAG. The system provides a replicable model for other Nigerian institutions to promote sustainability (SDG 7) and innovation (SDG 9).

# Acknowledgements

The author expresses gratitude to Almighty Allah and appreciates the guidance of Prof. Peter O. Oluseyi and the support of the Electrical and Electronics Engineering Department at UNILAG. Special thanks to MSSN UNILAG and family for their encouragement.

# References

The project references 30 primary sources, including:

* Fouad et al. (2020) on Machine Learning and IoT for Smart Grids.


* Zhakiyev et al. (2024) regarding Energy Management for Campus Microgrids.


* Ohanu et al. (2024) on renewable energy integration in smart grids.


* The Guardian Nigeria on the energy crisis in tertiary institutions.

