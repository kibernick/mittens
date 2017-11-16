import MySQLdb
import click

from mittens.settings import DevConfig


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
    if click.confirm("Create DB on: %s" % DevConfig.SQLALCHEMY_DATABASE_URI):
        init_from_config(DevConfig)


if __name__ == '__main__':
    init_db()
