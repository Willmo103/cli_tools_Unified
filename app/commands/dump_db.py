import os
import click
import sqlalchemy as sa
from sqlalchemy import create_engine, MetaData, Table
from urllib.parse import urlparse

@click.command()
@click.option('--source', help='Source database connection string')
@click.option('--destination', default=None, help='Destination database connection string (optional)')
def transfer_data(source, destination):
    if not destination:
        parsed_url = urlparse(source)
        db_name = os.path.basename(parsed_url.path).split('.')[0]
        destination = f'sqlite:///{db_name}.sqlite3'

    src_engine = create_engine(source)
    dest_engine = create_engine(destination)

    # Retrieve the metadata (table information) from the source database
    metadata = MetaData()
    metadata.reflect(bind=src_engine)

    # Create a new destination database with the same schema as the source database
    metadata.create_all(bind=dest_engine)

    # Transfer data from the source to the destination database for each table
    with src_engine.connect() as src_conn, dest_engine.connect() as dest_conn:
        for table_name in metadata.tables:
            # Fetch data from the source database
            src_data = src_conn.execute(sa.select([metadata.tables[table_name]])).fetchall()

            # Insert data into the destination database
            if src_data:
                dest_conn.execute(metadata.tables[table_name].insert(), src_data)

    # Close the connections
    src_engine.dispose()
    dest_engine.dispose()

if __name__ == '__main__':
    transfer_data()
