PradaQ: Multi-Asset Probability & Risk Engine
Author: Adwaita Tulsyan Focus: Multivariate Statistics, Stochastic Volatility Modeling, and 3D Risk Geometry.

Nexus is a quantitative framework designed to move beyond 2D price analysis. It models the Joint Probability Density of non-correlated assets to identify "Safe Havens" and "Risk Clusters" using 3D visualization of the Black-Scholes and Student-t surfaces.

1. The 3D Joint Probability Surface (The "Mountain")
What it represents: The likelihood of two assets hitting specific price targets simultaneously.

Z-Axis (Height): Probability Density. The higher the peak, the more "certain" the model is.

Shape Interpretation: * The Cigar: High correlation. Assets move in lockstep (High Systemic Risk).

The Dome: Low correlation. Assets are independent (High Diversification).

2. The Black-Scholes Volatility Surface (The "Time Tunnel")
What it represents: The cost of market insurance (options) over time.

Z-Axis (Value): Option Premium.

The "Melt" Factor: As time passes (Y-axis), the surface "decays" toward zero. In a crash scenario, this surface "warps" upward, representing a spike in market fear (Vega).

3. The Clustermap (Sector Interaction)
Method: Hierarchical Clustering.

Interpretation: It groups stocks not by name, but by behavior. If Adani and Tata Steel are in the same dark-colored block, they share the same risk DNA.