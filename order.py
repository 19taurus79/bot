import asyncio
from bot import piccolo_conf
from bot.pic.tables import Submissions
from piccolo.query import Sum


async def product_needs():
    ans = await Submissions.select(Submissions.product, Sum(Submissions.different))
    return ans


if __name__ == "__main__":
    asyncio.run(product_needs())
