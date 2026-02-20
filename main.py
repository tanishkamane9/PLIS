import argparse
import os
import json
from datetime import date
from storage.db import initialize_database
from storage.models import get_or_create_application, insert_daily_log_summary
from analyzer.analysis import read_log_file, analyze_logs

def parse_arguments():
    parser = argparse.ArgumentParser(description="PLIS - Production Log Insight System")

    parser.add_argument(
        "--file",
        required=True,
        help="Path to the log file"
    )

    parser.add_argument(
        "--env",
        default="production",
        help="Environment of the logs (default: production)"
    )

    parser.add_argument(
        "--app",
        default="default_app",
        help="Application name"
    )

    return parser.parse_args()

def main():
    args = parse_arguments()

    # Validate file exists
    if not os.path.exists(args.file):
        print(f"❌ Log file not found: {args.file}")
        return
    
    initialize_database()

    log_lines = read_log_file(args.file)
    analysis_result = analyze_logs(log_lines)

    app_id = get_or_create_application(args.app, args.env)

    today = date.today().isoformat()

    error_rate = (
        analysis_result["error_count"] / analysis_result["total_logs"]
        if analysis_result["total_logs"] > 0
        else 0
    )

    warning_rate = (
        analysis_result["warning_count"] / analysis_result["total_logs"]
        if analysis_result["total_logs"] > 0
        else 0
    )

    ALERT_THRESHOLD = 0.20

    if error_rate > ALERT_THRESHOLD:
        print("\n🚨 ALERT: High error rate detected!")

        from storage.models import insert_alert

        insert_alert(
            application_id=app_id,
            date=today,
            metric_name="error_rate",
            metric_value=error_rate,
            threshold=ALERT_THRESHOLD,
            alert_message="Error rate exceeded 20%"
        )


    insert_daily_log_summary(
        application_id=app_id,
        total_logs=analysis_result["total_logs"],
        info_count=analysis_result["info_count"],
        warning_count=analysis_result["warning_count"],
        error_count=analysis_result["error_count"],
        top_error_message=analysis_result["top_error_message"],
        peak_error_hour=analysis_result["peak_error_hour"]
    )

    print("\n" + "=" * 45)
    print("PLIS Analysis Summary")
    print("=" * 45)

    print(f"Application : {args.app}")
    print(f"Environment : {args.env}")
    print(f"Date        : {today}")
    print("-" * 45)

    print(f"Total Logs  : {analysis_result['total_logs']}")
    print(f"INFO        : {analysis_result['info_count']}")
    print(f"WARNING     : {analysis_result['warning_count']}")
    print(f"ERROR       : {analysis_result['error_count']}")
    print("-" * 45)

    print(f"Top Error   : {analysis_result['top_error_message']}")
    print(f"Peak Hour   : {analysis_result['peak_error_hour']}")
    print("-" * 45)

    print(f"Error Rate  : {error_rate:.2%}")
    print(f"Warn Rate   : {warning_rate:.2%}")

    if error_rate > ALERT_THRESHOLD:
        print("\n🚨 ALERT: High error rate detected!")

    print("=" * 45)
    print("Analysis stored successfully ✅")
    print("=" * 45)

    os.makedirs("output", exist_ok=True)

    output_data = {
        "application": args.app,
        "environment": args.env,
        "date": today,
        "total_logs": analysis_result["total_logs"],
        "info_count": analysis_result["info_count"],
        "warning_count": analysis_result["warning_count"],
        "error_count": analysis_result["error_count"],
        "top_error_message": analysis_result["top_error_message"],
        "peak_error_hour": analysis_result["peak_error_hour"],
        "error_rate": error_rate,
        "warning_rate": warning_rate,
    }

    output_path = f"output/{args.app}_{today}.json"

    with open(output_path, "w") as json_file:
        json.dump(output_data, json_file, indent=4)

if __name__ == "__main__":
    main()
 


