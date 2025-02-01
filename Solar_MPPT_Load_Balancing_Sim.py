import numpy as np
import matplotlib.pyplot as plt

# Time Simulation (10 seconds, 100 steps)
time = np.linspace(0, 10, 100)

# Simulating a cloudy day: sunlight fluctuates unpredictably
solar_power = 50 + 30 * np.sin(time) + 20 * np.random.randn(100)  # 20% random noise

# MPPT Controller (dynamic efficiency ~98%)
mppt_efficiency = 0.98
mppt_output = np.clip(solar_power * mppt_efficiency, 0, 100)

# PWM Controller (~75% efficiency)
pwm_efficiency = 0.75
pwm_output = np.clip(solar_power * pwm_efficiency, 0, 100)

# Relay switching WITHOUT PWM Timer (erratic switching)
relay_switch_no_timer = np.where(solar_power > 40, 1, 0)  # Abrupt ON/OFF if power > 40W

# Relay switching WITH PWM Timer (smoother transitions)
relay_switch_with_timer = np.zeros_like(relay_switch_no_timer)
switch_state = 0
for i in range(1, len(time)):
    if relay_switch_no_timer[i] != switch_state:
        if np.random.rand() > 0.7:  # Introduce delay (simulate PWM Timer)
            switch_state = relay_switch_no_timer[i]
    relay_switch_with_timer[i] = switch_state

# Visualizing Power and Relay Behavior
plt.figure(figsize=(12, 6))

plt.plot(time, solar_power, label="Solar Power Input (W)", linestyle="dashed", color="gray")
plt.plot(time, mppt_output, label="MPPT Output (W)", color="green", linewidth=2)
plt.plot(time, pwm_output, label="PWM Output (W)", color="red", linewidth=2)
plt.plot(time, relay_switch_no_timer * 100, label="Relay Switching (No PWM Timer)", color="purple", linestyle="dashdot")
plt.plot(time, relay_switch_with_timer * 100, label="Relay Switching (With PWM Timer)", color="blue", linestyle="dotted")

plt.xlabel("Time (seconds)")
plt.ylabel("Power (Watts) / Relay State")
plt.title("MPPT vs PWM Controller & Relay Stability")
plt.legend()
plt.grid()
plt.show()
