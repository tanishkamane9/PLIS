from collections import Counter, defaultdict
from datetime import datetime


def read_log_file(file_path: str):
    with open(file_path, "r") as file:
        return file.readlines()


def analyze_logs(log_lines):
    total_logs = 0
    level_counter = Counter()
    error_messages = Counter()
    hourly_errors = defaultdict(int)

    for line in log_lines:
        line = line.strip()
        if not line:
            continue

        parts = line.split()

        # Basic structure validation
        if len(parts) < 3:
            continue

        try:
            timestamp_str = parts[0] + " " + parts[1]
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            # Skip lines that don't match expected format
            continue

        level = parts[2]
        message = " ".join(parts[3:])

        total_logs += 1
        level_counter[level] += 1

        if level == "ERROR":
            error_messages[message] += 1
            hour_key = timestamp.strftime("%Y-%m-%d %H")
            hourly_errors[hour_key] += 1

    top_error_message = (
        error_messages.most_common(1)[0][0]
        if error_messages
        else None
    )

    peak_error_hour = (
        max(hourly_errors, key=hourly_errors.get)
        if hourly_errors
        else None
    )

    return {
        "total_logs": total_logs,
        "info_count": level_counter.get("INFO", 0),
        "warning_count": level_counter.get("WARNING", 0),
        "error_count": level_counter.get("ERROR", 0),
        "top_error_message": top_error_message,
        "peak_error_hour": peak_error_hour,
    }