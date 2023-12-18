from bot.pic.tables import MovedData, MovedNot, Submissions


async def get_manager_sub(manager):
    value = await Submissions.select(
        Submissions.client, Submissions.contract_supplement
    ).where(Submissions.manager == manager)
    return value
