import os
import pandas as pd
from sqlalchemy import create_engine, text


# PostgreSQL connection details
user = os.getenv("PGUSER", "postgres")
password = os.getenv("PGPASSWORD", 5432)
host = os.getenv("PGHOST", "localhost")
port = os.getenv("PGPORT", "5432")
database = os.getenv("PGDATABASE", "product_feedback_db")


# Create connection to PostgreSQL
engine = create_engine(
    f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
)


def get_feedback():
    """
    Get all feedback records from PostgreSQL.
    """

    query = """
        SELECT *
        FROM feedback
        ORDER BY timestamp DESC;
    """

    return pd.read_sql(query, engine)


def get_category_summary():
    """
    Count feedback by category.
    """

    query = """
        SELECT
            category,
            COUNT(*) AS feedback_count
        FROM feedback
        GROUP BY category
        ORDER BY feedback_count DESC;
    """

    return pd.read_sql(query, engine)


def get_product_area_summary():
    """
    Count feedback by product area.
    """

    query = """
        SELECT
            product_area,
            COUNT(*) AS feedback_count
        FROM feedback
        GROUP BY product_area
        ORDER BY feedback_count DESC;
    """

    return pd.read_sql(query, engine)


def get_sentiment_summary():
    """
    Count feedback by sentiment.
    """

    query = """
        SELECT
            sentiment,
            COUNT(*) AS feedback_count
        FROM feedback
        GROUP BY sentiment
        ORDER BY feedback_count DESC;
    """

    return pd.read_sql(query, engine)


def get_severity_summary():
    """
    Count feedback by severity bucket.
    """

    query = """
        SELECT
            severity_bucket,
            COUNT(*) AS feedback_count
        FROM feedback
        GROUP BY severity_bucket
        ORDER BY feedback_count DESC;
    """

    return pd.read_sql(query, engine)


def get_total_feedback():
    """
    Get total number of feedback records.
    """

    query = """
        SELECT COUNT(*) AS total
        FROM feedback;
    """

    result = pd.read_sql(query, engine)

    return int(result.iloc[0]["total"])


def get_critical_feedback():
    """
    Get number of critical issues.
    """

    query = """
        SELECT COUNT(*) AS total
        FROM feedback
        WHERE severity = 'Critical';
    """

    result = pd.read_sql(query, engine)

    return int(result.iloc[0]["total"])

def get_top_categories():
    query = """
        SELECT
            category,
            COUNT(*) AS feedback_count
        FROM feedback
        GROUP BY category
        ORDER BY feedback_count DESC;
    """

    return pd.read_sql(query, engine)

def get_top_product_areas():
    query = """
        SELECT
            product_area,
            COUNT(*) AS feedback_count
        FROM feedback
        GROUP BY product_area
        ORDER BY feedback_count DESC;
    """

    return pd.read_sql(query, engine)

def get_severity_summary():
    query = """
        SELECT
            severity,
            COUNT(*) AS issue_count
        FROM feedback
        GROUP BY severity
        ORDER BY
            CASE
                WHEN severity = 'Critical' THEN 1
                WHEN severity = 'High' THEN 2
                WHEN severity = 'Medium' THEN 3
                WHEN severity = 'Low' THEN 4
                ELSE 5
            END;
    """

    return pd.read_sql(query, engine)

def get_critical_feedback():
    query = """
        SELECT
            feedback_id,
            product_area,
            category,
            severity,
            feedback_text
        FROM feedback
        WHERE severity = 'Critical'
        ORDER BY feedback_id;
    """

    return pd.read_sql(query, engine)

def get_unhappy_features():
    query = """
        SELECT
            product_area,
            category,

            COUNT(*) AS total_feedback,

            SUM(
                CASE
                    WHEN sentiment = 'Negative' THEN 1
                    ELSE 0
                END
            ) AS negative_feedback,

            ROUND(
                100.0 * SUM(
                    CASE
                        WHEN sentiment = 'Negative' THEN 1
                        ELSE 0
                    END
                ) / COUNT(*),
                1
            ) AS negative_percentage

        FROM feedback

        GROUP BY product_area, category

        HAVING COUNT(*) >= 5

        ORDER BY negative_percentage DESC;
    """

    return pd.read_sql(query, engine)
    