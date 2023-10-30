import os

from google.cloud.sql.connector import Connector, IPTypes
import pymysql

import sqlalchemy

from dotenv import load_dotenv
load_dotenv()

def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    """
    Initializes a connection pool for a Cloud SQL instance of MySQL.

    Uses the Cloud SQL Python Connector package.
    """
    
    project_id = os.environ["PROJECT_ID"]
    region = os.environ["REGION"]
    instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]
    instance_connection_name = f"{project_id}:{region}:{instance_connection_name}"
    db_user = os.environ["DB_USER"]  # e.g. 'my-db-user'
    db_pass = os.environ["DB_PASS"]  # e.g. 'my-db-password'
    db_name = os.environ["DB_NAME"]  # e.g. 'my-database'

    ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC

    connector = Connector(ip_type)

    def getconn() -> pymysql.connections.Connection:
        conn: pymysql.connections.Connection = connector.connect(
            instance_connection_name,
            "pymysql",
            user=db_user,
            password=db_pass,
            db=db_name,
        )
        return conn

    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn
    )
    return pool

# TESTING
pool = connect_with_connector()
describe_stmt = sqlalchemy.text("DESCRIBE failed_request")

with pool.connect() as db_conn:
    result = db_conn.execute(describe_stmt)
    print(result.fetchall())