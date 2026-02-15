#!/usr/bin/env python3
import os

# Pfad zur Batterie
BATTERY_PATH = "/sys/class/power_supply/BAT0"
CHARGE_END_THRESHOLD_FILE = os.path.join(BATTERY_PATH, "charge_control_end_threshold")
CHARGE_START_THRESHOLD_FILE = os.path.join(BATTERY_PATH, "charge_control_start_threshold")

# Ladegrenzen
MIN_BATTERY = 70  # Ladebeginn bei 70%
MAX_BATTERY = 80  # Ladeende bei 80%

def set_charge_limits(start_limit, end_limit):
    """Setzt die Ladegrenzen auf den angegebenen Wert."""
    try:
        if os.path.exists(CHARGE_END_THRESHOLD_FILE) and os.path.exists(CHARGE_START_THRESHOLD_FILE):
            with open(CHARGE_END_THRESHOLD_FILE, "w") as f_end, open(CHARGE_START_THRESHOLD_FILE, "w") as f_start:
                f_end.write(str(end_limit))
                f_start.write(str(start_limit))
            print(f"[INFO] Ladelimit auf {start_limit}% (Start) und {end_limit}% (Ende) gesetzt.")
        else:
            print(f"[WARNUNG] Ladegrenzen-Dateien existieren nicht. Ladebegrenzung kann nicht gesetzt werden.")
    except PermissionError:
        print("[ERROR] Root-Rechte benötigt, um Ladegrenze zu setzen.")
    except OSError as e:
        print(f"[ERROR] Fehler beim Schreiben in Ladegrenzen-Dateien: {e}")
    except Exception as e:
        print(f"[ERROR] Unbekannter Fehler beim Setzen der Ladegrenzen: {e}")

# Einmaliges Setzen der Ladegrenzen
set_charge_limits(MIN_BATTERY, MAX_BATTERY)

