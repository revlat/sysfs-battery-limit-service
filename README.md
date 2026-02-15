# sysfs-battery-limit-service

A minimal systemd service with a Python script that sets laptop battery charge thresholds via the kernel sysfs interface at boot (e.g. start charging at 70 %, stop at 80 %). Extends battery lifespan without any background process running.

## Why a custom service?

Many Linux distributions ship their own power management tools -- e.g. `tuned` and `power-profiles-daemon` on openSUSE Tumbleweed. The popular [TLP](https://linrunner.de/tlp/) does support battery charge thresholds, but often conflicts with these pre-installed packages: installing TLP typically requires removing `power-profiles-daemon` or `tuned`, breaking the distribution's default power profiles.

I originally ran into this on openSUSE Tumbleweed, but the same issue can occur on other distributions with a similar setup (e.g. Fedora with `power-profiles-daemon`).

This solution is intentionally simple:

- **No package conflicts** -- pre-installed power management tools stay untouched.
- **No background process** -- the script runs once at boot, then the kernel takes over.
- **Minimal dependencies** -- just Python 3 and systemd, available on virtually every modern Linux distribution.
- **Easy to adjust** -- charge thresholds can be changed directly in the script, no package manager or config files needed.

## How it works

The script writes the desired thresholds once into the kernel's sysfs files:

```
/sys/class/power_supply/BAT0/charge_control_start_threshold  → charging starts below this value
/sys/class/power_supply/BAT0/charge_control_end_threshold    → charging stops at this value
```

After that, the firmware/kernel handles charging automatically. Since sysfs values are reset on every reboot, the systemd service ensures they are rewritten at boot.

## Prerequisites

- **Compatible hardware**: The laptop must expose the sysfs files `charge_control_start_threshold` and `charge_control_end_threshold` under `/sys/class/power_supply/BAT0/`. This is the case on many modern laptops (e.g. Lenovo ThinkPad, some ASUS models), but not all vendors support it.
- **Python 3**
- **systemd**

Check if your hardware is compatible:

```bash
ls /sys/class/power_supply/BAT0/charge_control_*_threshold
```

If the files exist, this solution will work.

## Installation

1. Copy the script:

```bash
sudo cp set_battery_limits.py /usr/local/bin/set_battery_limits.py
sudo chmod 755 /usr/local/bin/set_battery_limits.py
```

2. Install and enable the service:

```bash
sudo cp set_battery_limits.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now set_battery_limits.service
```

3. Verify:

```bash
systemctl status set_battery_limits.service
```

## Adjusting charge thresholds

Edit the values in `/usr/local/bin/set_battery_limits.py`:

```python
MIN_BATTERY = 70  # charging starts below 70 %
MAX_BATTERY = 80  # charging stops at 80 %
```

Then restart the service:

```bash
sudo systemctl restart set_battery_limits.service
```
