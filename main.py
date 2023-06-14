import cantera as ct
import numpy as np
import matplotlib.pyplot as plt

# chemical mechanism
gas = ct.Solution('gri30.yaml')

# initial conditions
initial_temperature = 1200  # in Kelvin
initial_pressure = 1.0 * ct.one_atm  # in Pascals

# equivalence ratios to consider
equivalence_ratios = np.linspace(0.1, 10.0, 50)

# lists to store the highest pressure, temperature, N2O, NO, NO2, and CO results
highest_temperatures = []
highest_pressures = []
n2o_concentrations = []
no_concentrations = []
no2_concentrations = []
co_concentrations = []

for equivalence_ratio in equivalence_ratios:
    # Initial state of the gas
    gas.TP = initial_temperature, initial_pressure
    gas.set_equivalence_ratio(equivalence_ratio, 'H2', 'O2:1, N2:3.76')

    # Create a reactor
    reactor = ct.IdealGasReactor(gas)
    simulator = ct.ReactorNet([reactor])

    # Time stepping
    time_step = 1e-6  # Time step size in seconds
    end_time = 0.00135  # Total simulation time in seconds
    n_steps = int(end_time / time_step)

    # Create arrays to store the simulation results
    time = np.zeros(n_steps)
    temperature = np.zeros(n_steps)
    pressure = np.zeros(n_steps)
    n2o = np.zeros(n_steps)
    no = np.zeros(n_steps)
    no2 = np.zeros(n_steps)
    co = np.zeros(n_steps)

    # Perform the simulation
    for i in range(n_steps):
        time[i] = simulator.time
        temperature[i] = reactor.T
        pressure[i] = reactor.thermo.P
        n2o[i] = reactor.thermo['N2O'].X[0]
        no[i] = reactor.thermo['NO'].X[0]
        no2[i] = reactor.thermo['NO2'].X[0]
        co[i] = reactor.thermo['CO'].X[0]
        simulator.step()

    # Find the highest pressure, temperature, N2O, NO, NO2, and CO
    highest_temperature = np.max(temperature)
    highest_pressure = np.max(pressure)
    highest_n2o_concentration = np.max(n2o)
    highest_no_concentration = np.max(no)
    highest_no2_concentration = np.max(no2)
    highest_co_concentration = np.max(co)

    # Store the results
    highest_temperatures.append(highest_temperature)
    highest_pressures.append(highest_pressure)
    n2o_concentrations.append(highest_n2o_concentration)
    no_concentrations.append(highest_no_concentration)
    no2_concentrations.append(highest_no2_concentration)
    co_concentrations.append(highest_co_concentration)

# Plots of the highest temperature, pressure, N2O, NO, NO2, and CO results
plt.figure()
plt.plot(equivalence_ratios, highest_temperatures, marker='o')
plt.xlabel('Equivalence Ratio')
plt.ylabel('Highest Temperature (K)')
plt.title('Highest Temperature vs. Equivalence Ratio')

plt.figure()
plt.plot(equivalence_ratios, highest_pressures, marker='o')
plt.xlabel('Equivalence Ratio')
plt.ylabel('Highest Pressure (Pa)')
plt.title('Highest Pressure vs. Equivalence Ratio')

plt.figure()
plt.plot(equivalence_ratios, n2o_concentrations, marker='o')
plt.xlabel('Equivalence Ratio')
plt.ylabel('N2O Concentration')
plt.title('N2O Concentration vs. Equivalence Ratio')

plt.figure()
plt.plot(equivalence_ratios, no_concentrations, marker='o')
plt.xlabel('Equivalence Ratio')
plt.ylabel('NO Concentration')
plt.title('NO Concentration vs. Equivalence Ratio')

plt.figure()
plt.plot(equivalence_ratios, no2_concentrations, marker='o')
plt.xlabel('Equivalence Ratio')
plt.ylabel('NO2 Concentration')
plt.title('NO2 Concentration vs. Equivalence Ratio')

plt.figure()
plt.plot(equivalence_ratios, co_concentrations, marker='o')
plt.xlabel('Equivalence Ratio')
plt.ylabel('CO Concentration')
plt.title('CO Concentration vs. Equivalence Ratio')

plt.show()