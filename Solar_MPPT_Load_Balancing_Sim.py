# The above below simulates a solar power system with relay control using hysteresis and timer delays.
# It visualizes the solar power input, MPPT output, PWM output, and relay switching behavior.
# The relay switching is controlled by hysteresis and delays to prevent rapid toggling.
# The plot shows the effect of these controls on the relay state, providing a clear view of how the system behaves under varying solar conditions.
# The simulation includes a cloudy day effect with random noise in solar power input.
# The relay control logic ensures that the relay does not switch on and off too quickly, which could cause wear and tear on the relay contacts.
# The use of hysteresis and delays helps to stabilize the system and improve reliability.

import numpy as np
import matplotlib.pyplot as plt

# Adjustable Hysteresis & Delay Parameters
on_threshold = 45  # W
off_threshold = 35  # W
on_delay = 0.5  # seconds
off_delay = 1.0  # seconds

# Time Simulation (10 seconds, 100 steps)
time = np.linspace(0, 10, 100)
dt = time[1] - time[0]  # time step size

# Simulating a cloudy day: sunlight fluctuates unpredictably
solar_power = 50 + 30 * np.sin(time) + 20 * np.random.randn(100)  # 20% random noise

# MPPT Controller (dynamic efficiency ~98%)
mppt_efficiency = 0.98
mppt_output = np.clip(solar_power * mppt_efficiency, 0, 100)

# PWM Controller (~75% efficiency)
pwm_efficiency = 0.75
pwm_output = np.clip(mppt_output * pwm_efficiency, 0, 100)  # Fixed: Apply PWM to MPPT output

# Relay switching WITHOUT control logic (raw comparison)
relay_switch_no_timer = np.where(pwm_output > 40, 1, 0)  # Fixed: Compare PWM output, not solar_power

# Relay switching WITH hysteresis and ON/OFF delays
relay_switch_with_control = np.zeros_like(relay_switch_no_timer)
switch_state = 0
on_timer_counter = 0
off_timer_counter = 0
on_delay_steps = int(on_delay / dt)
off_delay_steps = int(off_delay / dt)

for i in range(1, len(time)):
    # Check if we should turn ON (only count when consistently above threshold)
    if switch_state == 0:
        if pwm_output[i] >= on_threshold:  # Fixed: Compare PWM output
            on_timer_counter += 1
            if on_timer_counter >= on_delay_steps:
                switch_state = 1
                on_timer_counter = 0
        else:
            on_timer_counter = 0  # Reset counter if drops below threshold
    
    # Check if we should turn OFF (only count when consistently below threshold)
    elif switch_state == 1:
        if pwm_output[i] <= off_threshold:  # Fixed: Compare PWM output
            off_timer_counter += 1
            if off_timer_counter >= off_delay_steps:
                switch_state = 0
                off_timer_counter = 0
        else:
            off_timer_counter = 0  # Reset counter if rises above threshold
    
    relay_switch_with_control[i] = switch_state

# Visualizing Power and Relay Behavior
plt.figure(figsize=(12, 6))
plt.plot(time, solar_power, label="Solar Power Input (W)", linestyle="dashed", color="gray")
plt.plot(time, mppt_output, label="MPPT Output (W)", color="green", linewidth=2)
plt.plot(time, pwm_output, label="PWM Output (W)", color="red", linewidth=2)
plt.plot(time, relay_switch_no_timer * 100, label="Relay Switching (No Control)", color="purple", linestyle="dashdot")
plt.plot(time, relay_switch_with_control * 100, label="Relay Switching (Hysteresis + Delays)", color="blue", linewidth=2)
plt.axhline(on_threshold, color="green", linestyle=":", label="ON Threshold")
plt.axhline(off_threshold, color="red", linestyle=":", label="OFF Threshold")
plt.xlabel("Time (seconds)")
plt.ylabel("Power (Watts) / Relay State")
plt.title("Relay Behavior with Hysteresis and ON/OFF Delay")
plt.legend()
plt.grid(True)
plt.show()
