import MySQLdb
import click

from mittens.settings import DevConfig, TestConfig


def init_from_config(cfg):
    conn = MySQLdb.connect(user="root")
    sql_commands = [
        f"create database if not exists {cfg.SQLALCHEMY_DB};",
        f"create user if not exists '{cfg.SQLALCHEMY_USER}'@'{cfg.SQLALCHEMY_HOST}' identified by '{cfg.SQLALCHEMY_PASS}';",
        f"grant all on {cfg.SQLALCHEMY_DB}.* to '{cfg.SQLALCHEMY_USER}'@'{cfg.SQLALCHEMY_HOST}';",
    ]
    with conn.cursor() as cur:
        for sql_cmd in sql_commands:
            cur.execute(sql_cmd)
    conn.close()


def init_db():
    """Initialize a local DB."""
    for cfg in [DevConfig, TestConfig]:
        msg = "Create {} DB on: {}".format(cfg.ENV, cfg.SQLALCHEMY_DATABASE_URI)
        if click.confirm(msg):
            init_from_config(cfg)


if __name__ == "__main__":
    init_db()
