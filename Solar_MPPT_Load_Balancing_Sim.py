
# Solar Power System Relay Control Simulation with Controller Comparison
# Author: Arshia Keshvari
# Date: May 10, 2025
#
# Description:
# This simulation compares MPPT and PWM charge controllers in a solar power system with intelligent relay control.
# It implements hysteresis and time delays to prevent relay wear under fluctuating solar conditions.
# The visualization demonstrates controller efficiency differences and shows how controlled switching
# prevents rapid relay toggling.

import numpy as np
import matplotlib.pyplot as plt

# Control Parameters
on_threshold = 45  # Watts - relay activates above this power level
off_threshold = 35  # Watts - relay deactivates below this power level
on_delay = 0.5     # Seconds - time above threshold before switching ON
off_delay = 1.0    # Seconds - time below threshold before switching OFF

# Simulation Setup (10 seconds, 100 steps)
time = np.linspace(0, 10, 100)
dt = time[1] - time[0]

# Solar Input with Weather Variability (cloudy day simulation)
np.random.seed(42)  # For reproducible results
solar_power = 50 + 30 * np.sin(time) + 20 * np.random.randn(100)

# MPPT Controller Output
mppt_efficiency = 0.95  # Typical efficiency for MPPT controllers
mppt_output = np.clip(solar_power * mppt_efficiency, 0, 100)

# PWM Controller Output
# PWM is less efficient, especially in variable conditions
# PWM efficiency changes with the ratio of panel voltage to battery voltage
pwm_base_efficiency = 0.75
# PWM efficiency drops more in lower light conditions
pwm_efficiency = pwm_base_efficiency * (0.9 + 0.1 * (solar_power / 100))
pwm_output = np.clip(solar_power * pwm_efficiency, 0, 100)

# Simple Relay Control (Direct threshold comparison without delays)
mppt_relay_simple = np.where(mppt_output > 40, 1, 0)
pwm_relay_simple = np.where(pwm_output > 40, 1, 0)

# Advanced Relay Control (With hysteresis and delays)
mppt_relay_advanced = np.zeros_like(mppt_relay_simple)
pwm_relay_advanced = np.zeros_like(pwm_relay_simple)

# Advanced Relay Control Logic for MPPT
relay_state_mppt = 0
on_timer_mppt = 0
off_timer_mppt = 0
on_delay_steps = int(on_delay / dt)
off_delay_steps = int(off_delay / dt)

for i in range(1, len(time)):
    if relay_state_mppt == 0:  # Currently OFF
        if mppt_output[i] >= on_threshold:
            on_timer_mppt += 1
            if on_timer_mppt >= on_delay_steps:
                relay_state_mppt = 1  # Turn ON after delay
                on_timer_mppt = 0
        else:
            on_timer_mppt = 0
    elif relay_state_mppt == 1:  # Currently ON
        if mppt_output[i] <= off_threshold:
            off_timer_mppt += 1
            if off_timer_mppt >= off_delay_steps:
                relay_state_mppt = 0  # Turn OFF after delay
                off_timer_mppt = 0
        else:
            off_timer_mppt = 0
    
    mppt_relay_advanced[i] = relay_state_mppt

# Advanced Relay Control Logic for PWM
relay_state_pwm = 0
on_timer_pwm = 0
off_timer_pwm = 0

for i in range(1, len(time)):
    if relay_state_pwm == 0:  # Currently OFF
        if pwm_output[i] >= on_threshold:
            on_timer_pwm += 1
            if on_timer_pwm >= on_delay_steps:
                relay_state_pwm = 1  # Turn ON after delay
                on_timer_pwm = 0
        else:
            on_timer_pwm = 0
    elif relay_state_pwm == 1:  # Currently ON
        if pwm_output[i] <= off_threshold:
            off_timer_pwm += 1
            if off_timer_pwm >= off_delay_steps:
                relay_state_pwm = 0  # Turn OFF after delay
                off_timer_pwm = 0
        else:
            off_timer_pwm = 0
    
    pwm_relay_advanced[i] = relay_state_pwm

# Create subplots for better organization
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

# Plot 1: Power Curves and Thresholds
ax1.plot(time, solar_power, label="Solar Power Input (W)", linestyle="dashed", color="gray")
ax1.plot(time, mppt_output, label="MPPT Output (W)", color="green", linewidth=2)
ax1.plot(time, pwm_output, label="PWM Output (W)", color="orange", linewidth=2)
ax1.axhline(on_threshold, color="green", linestyle=":", label="ON Threshold (45W)")
ax1.axhline(off_threshold, color="red", linestyle=":", label="OFF Threshold (35W)")
ax1.set_ylabel("Power (Watts)")
ax1.set_title("Solar Controller Output Comparison: MPPT vs PWM")
ax1.legend(loc="best")
ax1.grid(True)

# Plot 2: Relay States - Using offset for clarity
# Adding small vertical offsets to make multiple states visible
ax2.plot(time, mppt_relay_simple*0.2 + 0.0, label="MPPT Simple Relay (ON/OFF immediate)", 
         drawstyle='steps-post', color="lightgreen", linewidth=2)
ax2.plot(time, mppt_relay_advanced*0.2 + 0.4, label="MPPT Advanced Relay (with delays)", 
         drawstyle='steps-post', color="darkgreen", linewidth=2)
ax2.plot(time, pwm_relay_simple*0.2 + 0.8, label="PWM Simple Relay (ON/OFF immediate)", 
         drawstyle='steps-post', color="moccasin", linewidth=2)
ax2.plot(time, pwm_relay_advanced*0.2 + 1.2, label="PWM Advanced Relay (with delays)", 
         drawstyle='steps-post', color="darkorange", linewidth=2)

# Add relay state labels
ax2.set_yticks([0.3, 0.7, 1.1, 1.5])
ax2.set_yticklabels(['1', '2', '3', '4'])
ax2.set_ylim(-0.1, 1.5)

ax2.set_xlabel("Time (seconds)")
ax2.set_ylabel("Relay States")
ax2.set_title("Relay State Comparison: Simple vs Advanced Control")
ax2.legend(loc="best")
ax2.grid(True)

plt.tight_layout()
plt.show()

# Calculate switching statistics
mppt_simple_switches = np.sum(np.abs(np.diff(mppt_relay_simple)))
mppt_advanced_switches = np.sum(np.abs(np.diff(mppt_relay_advanced)))
pwm_simple_switches = np.sum(np.abs(np.diff(pwm_relay_simple)))
pwm_advanced_switches = np.sum(np.abs(np.diff(pwm_relay_advanced)))

# Calculate relay wear reduction
if mppt_simple_switches > 0:
    mppt_reduction = ((mppt_simple_switches - mppt_advanced_switches) / mppt_simple_switches * 100)
else:
    mppt_reduction = 0  # Prevent division by zero

if pwm_simple_switches > 0:
    pwm_reduction = ((pwm_simple_switches - pwm_advanced_switches) / pwm_simple_switches * 100)
else:
    pwm_reduction = 0  # Prevent division by zero
    
# Print results
print("==== CONTROLLER EFFICIENCY COMPARISON ====")
print(f"MPPT average power output: {np.mean(mppt_output):.2f}W")
print(f"PWM average power output: {np.mean(pwm_output):.2f}W")
print(f"Efficiency difference: {(np.mean(mppt_output) - np.mean(pwm_output)):.2f}W ({(np.mean(mppt_output)/np.mean(pwm_output)-1)*100:.1f}% MPPT advantage)")

print("\n==== RELAY SWITCHING STATISTICS ====")
print(f"MPPT Simple Control: {mppt_simple_switches} switches (no delays)")
print(f"MPPT Advanced Control: {mppt_advanced_switches} switches (with hysteresis & delays)")
print(f"PWM Simple Control: {pwm_simple_switches} switches (no delays)")
print(f"PWM Advanced Control: {pwm_advanced_switches} switches (with hysteresis & delays)")

# Calculate relay wear reduction
mppt_reduction = ((mppt_simple_switches - mppt_advanced_switches) / mppt_simple_switches * 100) if mppt_simple_switches > 0 else 0
pwm_reduction = ((pwm_simple_switches - pwm_advanced_switches) / pwm_simple_switches * 100) if pwm_simple_switches > 0 else 0

print(f"\nAdvanced control reduces relay switching by {mppt_reduction:.1f}% with MPPT and {pwm_reduction:.1f}% with PWM")
