from pic.tables import MovedData, MovedNot, Submissions


async def get_manager_sub(manager):
    value = await Submissions.select(
        Submissions.client, Submissions.contract_supplement
    ).where((Submissions.manager == manager) & (Submissions.different > 0))
    return value


async def get_products_from_number(order):
    value = await MovedData.select().where(MovedData.contract == order)
    return value


async def get_line_of_business_sub(client):
    value = (
        await Submissions.select(Submissions.line_of_business)
        .where(Submissions.client.ilike(f"%{client}%"))
        .group_by(Submissions.line_of_business)
        .order_by(Submissions.line_of_business)
    )
    return value
