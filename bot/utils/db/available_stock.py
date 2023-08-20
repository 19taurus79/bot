from typing import List

from pic.tables import AvailableStock
from piccolo.query import Sum


async def get_available_stock(val) -> List:
    aval = await AvailableStock.select(
        AvailableStock.product.product,
        AvailableStock.buying_season,
        AvailableStock.division,
        AvailableStock.available,
    ).where(
        (AvailableStock.product.product.ilike(f"%{val}%"))
        & (AvailableStock.available > 0)
        & (AvailableStock.line_of_business != "Загальні витрати/доходи")
    )
    return aval


async def get_available_stock_analog_nomenclature_product(val) -> List:
    active_ingredient = await AvailableStock.select(
        AvailableStock.product.active_substance
    ).where(AvailableStock.product.product.ilike(f"%{val}%"))
    try:
        first_word = active_ingredient[0]["product.active_substance"].split()[0]
    except Exception:
        ans = []
        return ans
    ans = (
        await AvailableStock.select(
            AvailableStock.product.product,
            Sum(AvailableStock.available).as_alias("available"),
            AvailableStock.product.active_substance,
            AvailableStock.division,
        )
        .where(
            (AvailableStock.product.active_substance.ilike(f"%{first_word}%"))
            & (AvailableStock.available > 0)
        )
        .group_by(
            AvailableStock.product.product,
            AvailableStock.product.active_substance,
            AvailableStock.division,
        )
    )

    return ans


async def get_available_stock_analog_nomenclature_substance(val) -> List:
    ans = (
        await AvailableStock.select(
            AvailableStock.product.product,
            Sum(AvailableStock.available).as_alias("available"),
            AvailableStock.product.active_substance,
            AvailableStock.division,
        )
        .where(
            (AvailableStock.product.active_substance.ilike(f"%{val}%"))
            & (AvailableStock.available > 0)
        )
        .group_by(
            AvailableStock.product.product,
            AvailableStock.product.active_substance,
            AvailableStock.division,
        )
    )

    return ans
