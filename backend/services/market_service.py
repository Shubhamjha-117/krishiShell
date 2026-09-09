from sqlalchemy import func

from models.market_price import MarketPrice


def get_latest_prices_for_crop(crop_id):

    latest_dates = (
        MarketPrice.query
        .with_entities(
            MarketPrice.market_id,
            func.max(MarketPrice.arrival_date).label("latest_date")
        )
        .filter(
            MarketPrice.crop_id == crop_id
        )
        .group_by(
            MarketPrice.market_id
        )
        .subquery()
    )

    prices = (
        MarketPrice.query
        .join(
            latest_dates,
            (
                MarketPrice.market_id == latest_dates.c.market_id
            )
            &
            (
                MarketPrice.arrival_date == latest_dates.c.latest_date
            )
        )
        .filter(
            MarketPrice.crop_id == crop_id
        )
        .all()
    )

    return prices