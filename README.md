# Adaptive Solar MPPT Emergency Backup Power System
This project aims to enhance the reliability and output of residential emergency backup power systems by implementing an adaptive solar energy management approach. Traditional PWM-based solar charge controllers often fail to operate efficiently under fluctuating environmental conditions due to their static nature. To address this, the proposed system integrates Maximum Power Point Tracking (MPPT) techniques capable of dynamically adjusting voltage and current to maximize solar panel output. The design incorporates relay-based switching mechanisms and inverter load balancing strategies to manage power distribution effectively. By continuously adapting to changes in temperature and load conditions, the system ensures optimal energy conversion and provides a more dependable backup power solution for households.

<img src="https://github.com/user-attachments/assets/12c970ca-7c3a-432c-b8d8-61af132cfaa1" width="500x500">

## Problem Statement
PWM (Pulse Width Modulation) controllers are widely used in solar charge regulation but are limited by their inability to effectively handle variations in environmental conditions, such as temperature and sunlight. Some use current limiting resistors or filters to induce a delay, although a cheap method it is highly dangerous to do so for long term use thus, these limitations result in lower efficiency, leading to insufficient power generation. A more dynamic, adaptive system is required to overcome these inefficiencies and make the most of solar energy and DC power available from a Lead ACID or Lithium based battery.

<img src="https://github.com/user-attachments/assets/8c8f58a1-ef3d-4705-903d-b33cf700037f" width="250x250">

## Solution Approach
The project proposes a holistic approach by integrating relay switches, adjustable timers, and simple inverter load balancing strategies into the solar power system. This setup enables more precise control over power distribution, improving energy harvesting and optimizing the performance of the solar panel across different environmental conditions.

<img src="https://github.com/user-attachments/assets/476539eb-109e-4ece-8a4c-8cc67e06327b" width="250x250">

<img src="https://github.com/user-attachments/assets/15ab3425-139a-4740-82d0-79c46bf402bc" width="250x250">

<img src="https://github.com/user-attachments/assets/a4736272-e1c5-4386-93a6-69d724b7f950" width="250x250">

## Features
- **MPPT Optimization**: Real-time tracking of maximum power point for efficient energy conversion.
- **Relay Switch Integration**: Adjusts the load based on real-time system requirements.
- **Inverter Load Balancing**: Dynamically balances the inverter’s load to enhance power output.
- **Increased Efficiency**: Boosts overall system efficiency by 10% compared to traditional PWM systems (Cabling and Wiring Matters too I2R losses).

## System Architecture
- **Solar Panel**: Captures solar energy and converts it to electrical power.
- **MPPT Controller**: Maximizes the energy harvested from the solar panel.
- **Relay Switches**: Dynamically manage the load to optimize energy distribution.
- **Inverter**: Converts DC to AC and balances the load to ensure stability.
- **Delay Timer**: To enable a delay (Logical state) during low sunlight or unstable sunlight conditions for maximum power delivery without sudden or unforseen dropouts.

```plaintext
                          +----------------------+
                          |     Solar Panel      |
                          +----------------------+
                                    |
                                    v
                          +----------------------+
                          |   MPPT Controller    |
                          +----------------------+
                                    |
                                    v
                          +----------------------+
                          |   Battery Storage    |
                          +----------------------+
                                    |
                                    v
                          +----------------------+
                          |       Inverter       |
                          |   (DC to AC Power)   |
                          +----------------------+
                                    |                                               
                                    v                                               
                          +----------------------+
                          |  Relay Switch +      |
                          |    Delay Timer       |
                          | (Switches Load       |                        
                          |  Between Inverter AC |  
                          |  and Mains AC)       |
                          +----------------------+
                                    |
                                    v
                          +----------------------+
                          |   AC Load Output     |
                          +----------------------+
```
## Usage
1. Once the hardware is set up properly, the system will begin tracking the maximum power point of the solar panel.
2. Relay switches will automatically adjust switching from battery powered DC-AC to Mains AC load using an adjustable timer, this should ensure a stable inverter AC output especially within unstable conditions (Can cause Arcing on Relay if not careful).
3. The system will dynamically respond to temperature variations and other environmental factors to optimize power generation.

## Lead-Acid vs. Lithium Batteries

Switching from lead-acid to lithium batteries significantly enhances the overall performance and reliability of the backup power system. The following improvements are observed:

| Feature                      | Lead-Acid Battery                  | Lithium Battery                       | Improvement Impact                                       |
|-----------------------------|------------------------------------|----------------------------------------|----------------------------------------------------------|
| **Energy Density**          | Low                                | High                                   | Enables smaller, lighter systems                         |
| **Charging Speed**          | Slow (limited charge current)      | Fast (handles higher charge current)   | Quicker recharge times from solar or DC input            |
| **Cycle Life**              | ~300–500 cycles                    | 2000+ cycles                           | Longer battery lifespan and reduced maintenance          |
| **Depth of Discharge (DoD)**| ~50% usable capacity               | 80–90% usable capacity                 | More usable energy per cycle                             |
| **Voltage Stability**       | Drops as battery discharges        | Stable throughout discharge            | Consistent inverter performance, better AC output        |
| **Self-Discharge Rate**     | Higher                             | Lower                                  | Better for intermittent solar harvesting/storage         |

Integrating lithium batteries enhances system efficiency, reliability, and compatibility with adaptive MPPT and inverter balancing strategies.

![image](https://github.com/user-attachments/assets/8d7b104b-66da-4a77-b261-5116ba7d4c70)

## Potential Future Upgrades
1. Power monitoring and automation control via an IoT Edge based Microcontroller with ML integration.
2. Mitigation of capacitive and inductive loads at higher currents to prevent spikes or conditions that may damage components in the chain like DC-AC Inverters not rated at higher current limits.
3. Integration of robust embedded tools and electronics to guarantee stability and reliability for long term use.
4. Design of custom circuitry for maximum performance and remote operation.
