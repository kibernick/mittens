import MySQLdb
import click

from mittens.settings import DevConfig, TestConfig


def init_from_config(cfg):
    conn = MySQLdb.connect(user='root')
    with conn.cursor() as cur:
        cur.execute('create database if not exists `%s`;' % cfg.SQLALCHEMY_DB)
        cur.execute('create user if not exists `%s`;' % cfg.SQLALCHEMY_USER)
        cur.execute("grant all on {db}.* to '{user}'@'{host}' identified by '{pwd}';".format(
            user=cfg.SQLALCHEMY_USER, pwd=cfg.SQLALCHEMY_PASS,
            host=cfg.SQLALCHEMY_HOST, db=cfg.SQLALCHEMY_DB
        ))
    conn.close()


def init_db():
    """Initialize a local DB."""
    for cfg in [DevConfig, TestConfig]:
        msg = "Create {} DB on: {}".format(cfg.ENV, cfg.SQLALCHEMY_DATABASE_URI)
        if click.confirm(msg):
            init_from_config(cfg)


if __name__ == '__main__':
    init_db()
