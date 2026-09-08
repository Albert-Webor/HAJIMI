"""Database connection test suite for db_tool.
Tests connectivity for configured databases in config.toml with colored log outputs.
"""

import os
import sys
import unittest
from pathlib import Path

# Add project root to sys.path to allow importing from common
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common import print_green, print_red, print_cyan, Color

def print_success(msg: str):
    print_green(msg)

def print_error(msg: str):
    print_red(msg)

def print_info(msg: str):
    print_cyan(f"{Color.BOLD}{msg}")


# Python 3.11+ built-in TOML parser
try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        import toml as tomllib


def get_config_path() -> Path:
    """Return the path to config.toml relative to this test file."""
    base_dir = Path(__file__).resolve().parent.parent
    return base_dir / "config.toml"


def load_db_config(db_name: str) -> dict:
    """Load configuration for a specific database from config.toml."""
    config_file = get_config_path()
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_file}")

    with open(config_file, "rb") as f:
        data = tomllib.load(f)

    db_configs = data.get("db", {})
    if db_name not in db_configs:
        raise KeyError(
            f"Database '{db_name}' not found in {config_file}. Available: {list(db_configs.keys())}"
        )

    return db_configs[db_name]


class TestDBConnect(unittest.TestCase):
    """Test suite for validating database connections."""

    def test_01_connect_local_pgsql(self):
        """Test PostgreSQL connection for local_pgsql."""
        config = load_db_config("local_pgsql")
        print_info(f"\n[Testing PostgreSQL] {config.get('host')}:{config.get('port')}/{config.get('database')}...")

        try:
            import psycopg2
        except ImportError:
            err_msg = "psycopg2 is not installed. Run: pip install psycopg2-binary"
            print_error(f"  ✗ {err_msg}")
            self.fail(err_msg)

        conn = None
        try:
            conn = psycopg2.connect(
                host=config.get("host", "localhost"),
                port=config.get("port", 5432),
                user=config.get("user", "postgres"),
                password=config.get("password", ""),
                dbname=config.get("database", "postgres"),
                connect_timeout=5,
            )
            with conn.cursor() as cursor:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()[0]
                print_success("  ✓ PostgreSQL connected successfully!")
                print_success(f"  ✓ Version: {version.split(',')[0]}")

                # If schema is specified, test schema search_path
                schema = config.get("schema")
                if schema:
                    cursor.execute(f"SET search_path TO {schema}, public;")
                    print_success(f"  ✓ Search path set to schema: '{schema}'")

            self.assertFalse(conn.closed, "PostgreSQL connection should be active")
        except Exception as e:
            print_error(f"  ✗ PostgreSQL connection failed: {e}")
            self.fail(f"PostgreSQL connection failed: {e}")
        finally:
            if conn and not conn.closed:
                conn.close()

    def test_02_connect_local_mysql(self):
        """Test MySQL connection for local_mysql."""
        config = load_db_config("local_mysql")
        print_info(f"\n[Testing MySQL] {config.get('host')}:{config.get('port')}/{config.get('database')}...")

        try:
            import pymysql
        except ImportError:
            err_msg = "pymysql is not installed. Run: pip install pymysql"
            print_error(f"  ✗ {err_msg}")
            self.fail(err_msg)

        conn = None
        try:
            conn = pymysql.connect(
                host=config.get("host", "localhost"),
                port=int(config.get("port", 3306)),
                user=config.get("user", "root"),
                password=config.get("password", ""),
                database=config.get("database") or None,
                connect_timeout=5,
            )
            with conn.cursor() as cursor:
                cursor.execute("SELECT VERSION();")
                version = cursor.fetchone()[0]
                print_success("  ✓ MySQL connected successfully!")
                print_success(f"  ✓ Version: {version}")

            self.assertTrue(conn.open)
        except Exception as e:
            print_error(f"  ✗ MySQL connection failed: {e}")
            self.fail(f"MySQL connection failed: {e}")
        finally:
            if conn and conn.open:
                conn.close()

    def test_03_connect_local_mssql(self):
        """Test SQL Server connection for local_mssql."""
        config = load_db_config("local_mssql")
        print_info(f"\n[Testing SQL Server] {config.get('host')}:{config.get('port')}/{config.get('database')}...")

        driver_found = False
        conn = None

        # 1. Try pymssql
        try:
            import pymssql
            driver_found = True
            try:
                conn = pymssql.connect(
                    server=config.get("host", "localhost"),
                    port=int(config.get("port", 1433)),
                    user=config.get("user", "sa"),
                    password=config.get("password", ""),
                    database=config.get("database", "master"),
                    login_timeout=5,
                )
                with conn.cursor() as cursor:
                    cursor.execute("SELECT @@VERSION;")
                    version = cursor.fetchone()[0]
                    print_success("  ✓ SQL Server (pymssql) connected successfully!")
                    print_success(f"  ✓ Version: {version.splitlines()[0]}")
            except Exception as e:
                print_error(f"  ✗ SQL Server connection failed (pymssql): {e}")
                self.fail(f"SQL Server connection failed (pymssql): {e}")
            finally:
                if conn:
                    conn.close()
            return
        except ImportError:
            pass

        # 2. Try pyodbc
        try:
            import pyodbc
            driver_found = True
            driver = config.get("driver", "ODBC Driver 18 for SQL Server")
            trust_cert = (
                "yes"
                if config.get("trust_server_certificate", False) in (True, "yes", "true", "True")
                else "no"
            )
            conn_str = (
                f"DRIVER={{{driver}}};"
                f"SERVER={config.get('host')},{config.get('port', 1433)};"
                f"DATABASE={config.get('database', 'master')};"
                f"UID={config.get('user', 'sa')};"
                f"PWD={config.get('password', '')};"
                f"TrustServerCertificate={trust_cert};"
                f"Timeout=5;"
            )
            try:
                conn = pyodbc.connect(conn_str)
                with conn.cursor() as cursor:
                    cursor.execute("SELECT @@VERSION;")
                    version = cursor.fetchone()[0]
                    print_success("  ✓ SQL Server (pyodbc) connected successfully!")
                    print_success(f"  ✓ Version: {version.splitlines()[0]}")
            except Exception as e:
                print_error(f"  ✗ SQL Server connection failed (pyodbc): {e}")
                self.fail(f"SQL Server connection failed (pyodbc): {e}")
            finally:
                if conn:
                    conn.close()
            return
        except ImportError:
            pass

        if not driver_found:
            err_msg = (
                "Neither 'pymssql' nor 'pyodbc' is installed. "
                "Please run: pip install pymssql (or: pip install pyodbc)"
            )
            print_error(f"  ✗ {err_msg}")
            self.fail(err_msg)


class ColoredTestResult(unittest.TextTestResult):
    """Unittest result formatter with colored status output."""

    def addSuccess(self, test):
        unittest.TestResult.addSuccess(self, test)
        if self.showAll:
            self.stream.writeln(f"{Color.GREEN}PASS (OK){Color.RESET}")
        elif self.dots:
            self.stream.write(f"{Color.GREEN}.{Color.RESET}")
            self.stream.flush()

    def addFailure(self, test, err):
        unittest.TestResult.addFailure(self, test, err)
        if self.showAll:
            self.stream.writeln(f"{Color.RED}FAIL{Color.RESET}")
        elif self.dots:
            self.stream.write(f"{Color.RED}F{Color.RESET}")
            self.stream.flush()

    def addError(self, test, err):
        unittest.TestResult.addError(self, test, err)
        if self.showAll:
            self.stream.writeln(f"{Color.RED}ERROR{Color.RESET}")
        elif self.dots:
            self.stream.write(f"{Color.RED}E{Color.RESET}")
            self.stream.flush()


class ColoredTestRunner(unittest.TextTestRunner):
    """Unittest runner that uses ColoredTestResult."""
    resultclass = ColoredTestResult


if __name__ == "__main__":
    unittest.main(testRunner=ColoredTestRunner(verbosity=2))
