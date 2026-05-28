from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, BigInteger, JSON, Index
from sqlalchemy.orm import relationship
from app.database import Base
class Portfolio(Base):
    __tablename__ = 'portfolios'
    id = Column(BigInteger, primary_key=True, index=True)
    owner = Column(String(100), nullable=False, index=True)
    name = Column(String(100), nullable=False, index=True)
    trades = relationship('Trade', back_populates='portfolio', cascade="all, delete-orphan")

class Trade(Base):
    __tablename__ = 'trades'
    __table_args__={
        Index(
            "idx_trade_portfolio_time",
            "portfolio_id",
            "trade_time"
        )
    }
    id = Column(BigInteger, primary_key=True, index=True)
    portfolio_id = Column(BigInteger, ForeignKey('portfolios.id'))
    ticker = Column(String(16), nullable=False)
    side = Column(String(8), nullable=False)
    amount = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    trade_time = Column(DateTime, nullable=False)
    status = Column(String(16))
    portfolio = relationship('Portfolio', back_populates='trades')
    audit_logs = relationship('AuditLog', back_populates='trade',  cascade="all, delete-orphan")


class MarketData(Base):
    __tablename__ = 'market_data'
    __table_args__= Index(
        "idx_market_ticker_time",
        "ticker",
        "trade_time"
    )
    id = Column(BigInteger, primary_key=True, index=True)
    ticker = Column(String(16), nullable=False, index=True)
    trade_time = Column(DateTime, nullable=False,  index=True)
    price = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    extra_json = Column(JSON)

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    __table_args__=( Index(
        "idx_audit_trade_time",
        "trade_id",
        "log_timestamp"
    ),
    Index(
        "idx_audit_event_type_time",
        "event_type",
        "log_timestamp"
    ))
    id = Column(BigInteger, primary_key=True, index=True)
    trade_id = Column(BigInteger, ForeignKey('trades.id', ondelete = "CASCADE" ), nullable=True,  index=True)
    event_type = Column(String(32), nullable=False,  index=True)
    event_data = Column(JSON, nullable=False)
    log_timestamp = Column(DateTime, nullable=False)
    trade = relationship('Trade', back_populates='audit_logs')

# Deliberately sub-optimal / missing indexes for performance troubleshooting:
# (No composite indexes, missing timestamp/ticker indexes, no partial indexes, and nullable foreign keys)