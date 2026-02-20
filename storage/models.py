from storage.db import get_db_connection
from datetime import date

def get_or_create_application(name: str, environment:str):
    """
    fetch application if it exists, otherwise crrete it 
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    #check if application already exists 
    cursor.execute(
        """
        SELECT id from applications
        WHERE name = ? AND environment = ?
        """,
        (name, environment)
    )
    
    row = cursor.fetchone()

    if row:
        app_id = row["id"]
    else:
        cursor.execute(
            """
            INSERT INTO applications(name, environment)
            VALUES (?, ?)
            """,
            (name, environment))
        conn.commit()
        app_id = cursor.lastrowid               


    conn.close()
    return app_id


def insert_daily_log_summary(
        application_id: int,
        total_logs: int,
        info_count: int,
        warning_count: int,
        error_count: int,
        top_error_message: str,
        peak_error_hour: str
    ):
    """
    Insert a daily log summary for today
    """
    conn = get_db_connection()  
    cursor = conn.cursor()  

    today = date.today().isoformat()

    cursor.execute(
        """
        INSERT OR REPLACE INTO daily_log_summary(
            application_id,
            date,
            total_logs,
            info_count,
            warning_count,
            error_count,
            top_error_message,
            peak_error_hour
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            application_id,
            today,
            total_logs,
            info_count,
            warning_count,
            error_count,
            top_error_message,
            peak_error_hour
        )
    )

    conn.commit()
    conn.close()

def insert_metrics(application_id, date, error_rate, warning_rate):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO metrics_daily (
            application_id,
            date,
            error_rate,
            warning_rate
        )
        VALUES (?, ?, ?, ?)
        """,
        (application_id, date, error_rate, warning_rate)
    )

    conn.commit()
    conn.close()

def insert_alert(application_id, date, metric_name, metric_value, threshold, alert_message):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO alerts (
            application_id,
            date,
            metric_name,
            metric_value,
            threshold,
            alert_message
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (application_id, date, metric_name, metric_value, threshold, alert_message)
    )

    conn.commit()
    conn.close()