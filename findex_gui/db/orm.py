import sqlalchemy as sql
import sqlalchemy.pool as sql_pool
from pyramid_sqlalchemy import BaseObject as Base, init_sqlalchemy
from sqlalchemy import create_engine, Column, Index
from sqlalchemy.dialects.postgresql import INET
import random
import psycopg2


def initialize_pyramid_sqlalchemy(config):
    engine_configs = config.registry.settings['findex.db_hosts'].split(',')

    def get_connection():
        random.shuffle(engine_configs)
        for engine_config in engine_configs:
            try:
                return psycopg2.connect(engine_config)
            except psycopg2.OperationalError as e:
                print 'Failed to connect to %s: %s' % (engine_config, e)
        print 'Panic! No servers left.'
        return None

    pool = sql_pool.QueuePool(get_connection, max_overflow=1, pool_size=2)
    engine = create_engine('postgresql+psycopg2://', pool=pool)
    init_sqlalchemy(engine)


class Files(Base):
    __tablename__ = 'files'
 
    id = Column(sql.Integer, primary_key=True)

    host_id = Column(sql.Integer())

    file_name = Column(sql.String())
    file_path = Column(sql.String())
    file_ext = Column(sql.String(8))
    file_format = Column(sql.Integer())
    file_isdir = Column(sql.Boolean())
    file_size = Column(sql.BigInteger())

    file_modified = Column(sql.DateTime())

    file_perm = Column(sql.Integer())

    searchable = Column(sql.String(23))

    def __init__(self, file_name, file_path, file_ext, file_format, file_isdir, file_modified, file_perm, searchable, file_size, host, img_icon=None):
        self.host = host
        self.file_name = file_name
        self.file_path = file_path
        self.file_ext = file_ext
        self.file_format = file_format
        self.file_size = file_size
        self.file_isdir = file_isdir
        self.file_modified = file_modified
        self.file_perm = file_perm
        self.searchable = searchable
        self.img_icon = None

    # regular indexes
    ix_file_ext = Index('ix_file_ext', file_ext)
    ix_file_size = Index('ix_file_size', file_size)

    # multi column indexes
    ix_host_id_file_path = Index('ix_host_id_file_path', host_id, file_path)
    ix_file_format_searchable = Index('ix_file_format_searchable', file_format, searchable)

    # partial text search LIKE 'needle%'
    ix_file_searchable_text = Index('ix_file_searchable_text', searchable, postgresql_ops={
        'searchable': 'text_pattern_ops'
    })

    # full text search LIKE '%needle%'
    ix_file_searchable_gin = Index('ix_file_searchable_gin', searchable, postgresql_using='gin', postgresql_ops={
        'searchable': 'gin_trgm_ops'
    })


class Hosts(Base):
    __tablename__ = 'hosts'

    id = Column(sql.Integer, primary_key=True)

    address = Column(INET())
    date_crawled = Column(sql.DateTime())
    file_count = Column(sql.Integer())
    protocol = Column(sql.Integer())

    # regular indexes
    ix_address = Index('ix_address', address)

    def __init__(self, address, date_crawled, file_count, protocol):
        self.address = address
        self.date_crawled = date_crawled
        self.file_count = file_count
        self.protocol = protocol


class Options(Base):
    __tablename__ = 'options'

    id = Column(sql.Integer, primary_key=True)

    key = Column(sql.String())
    val = Column(sql.String())

    def __init__(self, key, val):
        self.key = key
        self.val = val