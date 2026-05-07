from database import add_incident, get_rules

LOG_FILE = "logs/system.log"
processed_lines = set()


def detect():
    active_rules = get_rules()
    global processed_lines

    with open(LOG_FILE, "r") as f:
        logs = f.readlines()

    failed_login_count = 0

    for line in logs:
        line = line.strip()

        if line in processed_lines:
            continue

        processed_lines.add(line)

        if "FAILED_LOGIN" in line and "Brute Force" in active_rules:
            failed_login_count += 1

            if failed_login_count >= 5:
                add_incident("Brute Force",
                        "Multiple failed login attempts",
                        "High")
                failed_login_count = 0

        elif "PORT_SCAN" in line and "Port Scan" in active_rules:
            ip = line.split("ip=")[-1]
            
            add_incident(
                            "Port Scan",
                            "Port scanning detected",
                            "Medium",
                            source_ip=ip
                        )

        elif "FILE_ACCESS" in line and "File Access" in active_rules:
            add_incident("File Access",
                    "Sensitive file accessed",
                    "Medium")

        elif "UNKNOWN_IP" in line and "Unknown IP" in active_rules:
            ip = line.split("ip=")[-1]
            
            add_incident(
                        "Unknown IP",
                        "Connection from unknown IP",
                        "Low",
                        source_ip=ip
                    )