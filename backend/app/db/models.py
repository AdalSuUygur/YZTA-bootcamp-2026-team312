"""
Task 2.1 — SQLAlchemy ORM modeli.

Tablo adı bilinçli olarak `yok_atlas_data`: Task 2.2'nin teknik detaylarında
verilen `SELECT * FROM yok_atlas_data WHERE department_code = :code` sorgusuyla
birebir eşleşsin diye.
"""

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class YokAtlasData(Base):
    __tablename__ = "yok_atlas_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # LLM'in department_codes.py'deki kapalı listeden ürettiği kodla eşleşir.
    department_code: Mapped[str] = mapped_column(String, index=True, nullable=False)
    department_name: Mapped[str] = mapped_column(String, nullable=False)

    university_name: Mapped[str] = mapped_column(String, nullable=False)
    quota: Mapped[int] = mapped_column(Integer, nullable=False)
    last_min_score: Mapped[float] = mapped_column(Float, nullable=False)
    last_min_rank: Mapped[int] = mapped_column(Integer, nullable=False)
