import subprocess

COMMANDS = [
    ["python", "scripts/download_futures.py"],
    ["python", "scripts/download_macro_fred.py"],
    ["python", "scripts/download_climate_disaster.py"],
    ["python", "scripts/build_monthly_panel.py"],
]


if __name__ == "__main__":
    for cmd in COMMANDS:
        print(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
