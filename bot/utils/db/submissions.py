from typing import List

from piccolo.query import Sum

from pic.tables import Submissions


async def get_submissions(val) -> List:
    sub = (
        await Submissions.select(
            Submissions.manager,
            Submissions.client,
            Submissions.different,
            Submissions.product.product,
        )
        .where(
            (Submissions.line_of_business != "Загальні витрати/доходи")
            & (Submissions.product.product.ilike(f"%{val}%"))
            & (
                Submissions.shipping_warehouse
                == 'Харківський підрозділ  ТОВ "Фірма Ерідон" с.Коротич'
            )
            & (Submissions.different > 0)
            & (Submissions.document_status == "затверджено")
        )
        .order_by("product.product")
    )
    return sub


async def get_submissions_delivery_status(manager) -> List:
    sub = (
        await Submissions.select(
            Submissions.manager,
            Submissions.client,
            Submissions.different,
            Submissions.product.product,
            Submissions.delivery_status,
        )
        .where(
            (Submissions.line_of_business.ilike(f"%насіння%"))
            & (Submissions.manager == manager)
            & (
                Submissions.shipping_warehouse
                == 'Харківський підрозділ  ТОВ "Фірма Ерідон" с.Коротич'
            )
            & (Submissions.different > 0)
            & (Submissions.document_status == "затверджено")
            & (Submissions.delivery_status.ilike(f"%ні%"))
        )
        .order_by("client")
    )
    return sub


async def quantity_under_orders(nom) -> List:
    under_orders = (
        await Submissions.select(
            Submissions.product.product, Sum(Submissions.different)
        )
        .where(
            (Submissions.product.product.ilike(f"%{nom}%")),
            (Submissions.document_status == "затверджено")
            & (Submissions.different > 0)
            & (
                Submissions.shipping_warehouse
                == 'Харківський підрозділ  ТОВ "Фірма Ерідон" с.Коротич'
            ),
        )
        .group_by(Submissions.product.product)
    )
    return under_orders


async def all_product_under_orders():
    all_under_orders = (
        Submissions.select(Submissions.product, Sum(Submissions.different))
        .where(
            (Submissions.document_status == "затверджено")
            & (Submissions.different > 0)
            & (
                Submissions.shipping_warehouse
                == 'Харківський підрозділ  ТОВ "Фірма Ерідон" с.Коротич'
            ),
        )
        .group_by(Submissions.product)
    )
    return all_under_orders


async def get_my_submissions(manager):
    sub = (
        await Submissions.select(Submissions.client)
        .where((Submissions.manager == manager) & (Submissions.different > 0))
        .group_by(Submissions.client)
        .order_by(Submissions.client)
    )
    return sub


async def get_contract(manager, client, l_o_b):
    result = (
        await Submissions.select(Submissions.contract_supplement)
        .where(
            (Submissions.manager == manager)
            & (Submissions.different > 0)
            & (Submissions.line_of_business == l_o_b)
            & (Submissions.client.ilike(f"%{client}%"))
        )
        .group_by(Submissions.contract_supplement)
        .order_by(Submissions.contract_supplement)
    )
    return result
