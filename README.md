# Solar-MPPT-Emergency-AC-Load-Balancing
This project focuses on enhancing household power output and reliability of a DC-AC solar panel MPPT (Maximum Power Point Tracking) system. Traditional PWM-based solar charge controllers often struggle to produce sufficient power, especially under varying temperature conditions, due to their inability to dynamically adjust voltage and current for optimal efficiency. The solution presented here utilizes relay switches and inverter load balancing techniques to improve energy output and maximize solar panel efficiency.

## Problem Statement
PWM (Pulse Width Modulation) controllers are widely used in solar charge regulation but are limited by their inability to effectively handle variations in environmental conditions, such as temperature and sunlight. Some use current limiting resistors or filters to induce a delay, although a cheap method it is highly dangerous to do so for long term use thus, these limitations result in lower efficiency, leading to insufficient power generation. A more dynamic, adaptive system is required to overcome these inefficiencies and make the most of solar energy and DC power available from a Lead ACID or Lithium based battery.

## Solution Approach
The project proposes a low cost approach by integrating relay switches, pwm timers, and inverter load balancing into the solar power system. This setup enables more precise control over power distribution, improving energy harvesting and optimizing the performance of the solar panel across different environmental conditions.

## Features
- **MPPT Optimization**: Real-time tracking of maximum power point for efficient energy conversion.
- **Relay Switch Integration**: Adjusts the load based on real-time system requirements.
- **Inverter Load Balancing**: Dynamically balances the inverter’s load to enhance power output.
- **Increased Efficiency**: Boosts overall system efficiency by 10% compared to traditional systems.

## System Architecture
- **Solar Panel**: Captures solar energy and converts it to electrical power.
- **MPPT Controller**: Maximizes the energy harvested from the solar panel.
- **Relay Switches**: Dynamically manage the load to optimize energy distribution.
- **Inverter**: Converts DC to AC and balances the load to ensure stability.
- **PWM Timer**: To enable a delay (Logical state) during low sunlight or unstable sunlight conditions for maximum power delivery without sudden or unforseen dropouts.

## Usage
1. Once the hardware is set up and setup properly, the system will begin tracking the maximum power point of the solar panel.
2. Relay switches will automatically adjust the load using an adjustable timer, and the inverter will ensure stable AC output especially within unstable conditions.
3. The system will dynamically respond to temperature variations and other environmental factors to optimize power generation.

## Potential Future Upgrades
1. Power monitoring and automation control via an IoT Edge based Microcontroller with ML integration.
2. Mitigation of capacitive and inductive loads at higher currents to prevent spikes or conditions that may damage components in the chain like DC-AC Inverters not rated at higher current limits.
3. Integration of robust embedded tools and electronics to garauntee stability and reliability for long term use.
4. Design of custom circuitry for maximum performance and remote operation.
