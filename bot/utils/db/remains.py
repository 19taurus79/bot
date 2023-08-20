import re
from typing import List
from piccolo.query import Sum
from pic.tables import Remains


async def get_remains_series(val) -> List:
    ans = await Remains.select(
        Remains.product.product,
        Remains.nomenclature_series,
        Remains.buh,
        Remains.skl,
    ).where(
        (Remains.line_of_business != "Загальні витрати/доходи")
        & (Remains.product.product.ilike(f"%{val}%"))
        & (Remains.buh > 0)
        & (Remains.warehouse == 'Харківський підрозділ  ТОВ "Фірма Ерідон" с.Коротич')
    )

    return ans


async def get_summary_remains(val) -> List:
    summary_buh = (
        await Remains.select(
            Remains.product.product,
            Sum(Remains.buh).as_alias("buh"),
            Sum(Remains.skl).as_alias("skl"),
        )
        .where(
            (Remains.line_of_business != "Загальні витрати/доходи")
            & (Remains.product.product.ilike(f"%{val}%"))
            & (Remains.buh > 0)
            & (
                Remains.warehouse
                == 'Харківський підрозділ  ТОВ "Фірма Ерідон" с.Коротич'
            ),
        )
        .group_by(Remains.product.product)
    )
    return summary_buh


async def get_remains_series_seeds(val) -> List:
    ans = await Remains.select(
        Remains.product.product,
        Remains.nomenclature_series,
        Remains.buh,
        Remains.skl,
        Remains.crop_year,
        Remains.germination,
        Remains.mtn,
        Remains.origin_country,
        Remains.weight,
    ).where(
        (Remains.line_of_business == "Насіння")
        & (Remains.product.product.ilike(f"%{val}%"))
        & (Remains.buh > 0)
        & (Remains.warehouse == 'Харківський підрозділ  ТОВ "Фірма Ерідон" с.Коротич')
    )

    return ans


async def get_remains_analog_nomenclature_in_our_warehouse_product(val) -> List:
    active_ingredient = await Remains.select(Remains.active_substance).where(
        Remains.product.product.ilike(f"%{val}%")
    )
    try:
        first_word = active_ingredient[0]["active_substance"].split()[0]
    except Exception:
        ans = []
        return ans
    ans = (
        await Remains.select(
            Remains.product.product,
            Sum(Remains.buh).as_alias("buh"),
            Sum(Remains.skl).as_alias("skl"),
            Remains.active_substance,
        )
        .where(
            (Remains.active_substance.ilike(f"%{first_word}%"))
            & (Remains.buh > 0)
            & (
                Remains.warehouse
                == 'Харківський підрозділ  ТОВ "Фірма Ерідон" с.Коротич'
            )
        )
        .group_by(Remains.product.product, Remains.active_substance)
    )

    return ans


async def get_remains_analog_nomenclature_in_our_warehouse_substance(val) -> List:
    ans = (
        await Remains.select(
            Remains.product.product,
            Sum(Remains.buh).as_alias("buh"),
            Sum(Remains.skl).as_alias("skl"),
            Remains.active_substance,
        )
        .where(
            (Remains.active_substance.ilike(f"%{val}%"))
            & (Remains.buh > 0)
            & (
                Remains.warehouse
                == 'Харківський підрозділ  ТОВ "Фірма Ерідон" с.Коротич'
            )
        )
        .group_by(Remains.product.product, Remains.active_substance)
    )

    return ans
