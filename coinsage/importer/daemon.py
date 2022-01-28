from datetime import timedelta, datetime

from sqlmodel import select, Session

from coinsage.database import engine
from coinsage.importer.binance import BinanceImporter
from coinsage.models import Exchange
from coinsage.constants import ExchangeType
from coinsage.security import decrypt_data


def start_importer_daemon():
    with Session(engine) as session:
        while True:
            current_date = datetime.utcnow()

            stmt = select(Exchange).where(
                Exchange.exchange_type == ExchangeType.BINANCE
            )
            for exchange in session.exec(stmt).fetchall():
                importer = BinanceImporter(
                    session=session,
                    portfolio_id=exchange.portfolio_id,
                    api_key=decrypt_data(exchange.api_key),
                    secret_key=decrypt_data(exchange.secret_key),
                    start_date=current_date - timedelta(days=40),
                    end_date=current_date,
                )
                importer.run()