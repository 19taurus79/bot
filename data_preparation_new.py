!pip install aiogram

valid_line_of_business = [

    "Власне виробництво насіння",

    "Демо-продукція",

    "ЗЗР",

    "Міндобрива (основні)",

    "Насіння",

    "Позакореневi добрива",

]

valid_warehouse = [

    'Харківський підрозділ  ТОВ "Фірма Ерідон" с.Коротич',

    'Харківський підрозділ  ТОВ "Фірма Ерідон" м.Балаклія',

]



from sqlalchemy import create_engine

engine=create_engine("postgresql+psycopg2://admin:root@195.189.226.96:5432/eridon_kharkiv_db")

managers_id = {

    "Онищенко": 548019148,

    "Скирда Дмитро Юрійович": 392207160,

    "Цовма Віктор Станіславович": 979678923,

    "Гаража Денис Олександрович": 5072996747,

    "Полівода Антон Сергійович": 811507369,

    "Шпак Дмитро Юрійович": 1779116530,

    # "Гуржій Віктор Миколайович": 7385862387,

    "Онищенко рабочий": 1060393824,

    "Чех Олександр Вікторович": 1600296306,

    "Повар Денис Олексійович": 651394664,

    "Грязнов Сергей Алексеевич": 919756698,

    "Шевцов Микола Петрович": 6968050615,

    # "Гуржій Віктор Миколайович": 688741543,

}

managers = managers_id.values()



import pandas as pd

import uuid

import sqlalchemy

from sqlalchemy import text

import datetime

from aiogram import Bot

import asyncio



bot = Bot("6102159293:AAFm5j2vn38f1NcRcxGmni7L6o3Wt9K5DJY")

def get_submissions():



    submissions = pd.read_excel("drive/MyDrive/1CData/Заявки.xlsx")

    submissions.drop(axis=0, labels=[0, 1, 2, 3, 4, 5, 6, 7], inplace=True)

    submissions.drop(axis=0, labels=submissions.tail(1).index, inplace=True)

    submissions.drop(

        axis=1, labels=["Unnamed: 1", "Unnamed: 2", "Unnamed: 6"], inplace=True

    )

    submissions_col_names = [

        "division",

        "manager",

        "company_group",

        "client",

        "contract_supplement",

        "parent_element",

        "manufacturer",

        "active_ingredient",

        "nomenclature",

        "party_sign",

        "buying_season",

        "line_of_business",

        "period",

        "shipping_warehouse",

        "document_status",

        "delivery_status",

        "shipping_address",

        "transport",

        "plan",

        "fact",

        "different",

    ]

    submissions.columns = submissions_col_names

    submissions["plan"]=submissions["plan"].fillna(0)

    submissions["fact"]=submissions["fact"].fillna(0)

    submissions["different"]=submissions["different"].fillna(0)

    submissions.fillna("", inplace=True)

    submissions.loc[

        (submissions["party_sign"] == "Закупівля поточного сезону"), "party_sign"

    ] = " "

    submissions["product"] = submissions.apply(

        lambda row: str(row["nomenclature"]).rstrip()

                    + " "

                    + str(row["party_sign"]).rstrip()

                    + " "

                    + str(row["buying_season"]).rstrip(),

        axis=1,

    )

    submissions["contract_supplement"] = submissions["contract_supplement"].str.slice(

        23, 34

    )



    return submissions



def get_av_stock():



    av_stock = pd.read_excel("drive/MyDrive/1CData/Доступность товара подразделения.xlsx")

    av_stock.drop(axis=0, labels=[0, 1, 2, 3, 4, 5, 6], inplace=True)

    av_stock.drop(

        axis=1, labels=["Unnamed: 1", "Unnamed: 2", "Unnamed: 4"], inplace=True

    )

    av_col_names = [

        "nomenclature",

        "party_sign",

        "buying_season",

        "division",

        "line_of_business",

        "active_substance",

        "available",

    ]

    av_stock.columns = av_col_names



    av_stock.fillna("", inplace=True)

    av_stock["product"] = av_stock.apply(

        lambda row: str(row["nomenclature"]).rstrip()

                    + " "

                    + str(row["party_sign"]).rstrip()

                    + " "

                    + str(row["buying_season"]).rstrip(),

        axis=1,

    )

    return av_stock



def get_remains_reg():



    remains = pd.read_excel("drive/MyDrive/1CData/Остатки.xlsx")

    remains.drop(axis=0, labels=[0, 1, 2, 3, 4], inplace=True)

    remains.drop(

        axis=1, labels=["Unnamed: 1", "Unnamed: 2", "Unnamed: 4"], inplace=True

    )

    remains.drop(axis=0, labels=remains.tail(1).index, inplace=True)

    remains_col_name = [

        "line_of_business",

        "warehouse",

        "parent_element",

        "nomenclature",

        "party_sign",

        "buying_season",

        "nomenclature_series",

        "mtn",

        "origin_country",

        "germination",

        "crop_year",

        "quantity_per_pallet",

        "active_substance",

        "certificate",

        "certificate_start_date",

        "certificate_end_date",

        "buh",

        "skl",

        "weight","storage",

    ]

    remains.columns = remains_col_name

    remains["buh"]=remains["buh"].fillna(0)

    remains["skl"]=remains["skl"].fillna(0)

    remains.fillna("", inplace=True)

    remains["product"] = remains.apply(

        lambda row: str(row["nomenclature"]).rstrip()

                    + " "

                    + str(row["party_sign"]).rstrip()

                    + " "

                    + str(row["buying_season"]).rstrip(),

        axis=1,

    )

    remains = remains.loc[remains["line_of_business"].isin(valid_line_of_business)]

    remains = remains.loc[remains["warehouse"].isin(valid_warehouse)]

    return remains



def get_payment():



    payment = pd.read_excel("drive/MyDrive/1CData/оплата.xlsx")

    payment.drop(axis=0, labels=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], inplace=True)

    payment.drop(

        axis=1, labels=["Unnamed: 1", "Unnamed: 2", "Unnamed: 7"], inplace=True

    )

    payment.drop(axis=0, labels=payment.tail(1).index, inplace=True)

    payment_col_name = [

        "contract_supplement",

        "contract_type",

        "prepayment_amount",

        "amount_of_credit",

        "prepayment_percentage",

        "loan_percentage",

        "planned_amount",

        "planned_amount_excluding_vat",

        "actual_sale_amount",

        "actual_payment_amount",

    ]

    payment.columns = payment_col_name

    payment.fillna(0, inplace=True)

    return payment



def get_moved_data():



    moved = pd.read_excel("drive/MyDrive/1CData/Заказано_Перемещено.xlsx", sheet_name="Данные")

    moved_col_names = [

        "order",

        "date",

        "line_of_business",

        "product",

        "qt_order",

        "qt_moved",

        "party_sign",

        "period",

        "contract",

    ]

    moved.columns = moved_col_names

    return moved

def run_async(coro):

    try:

        loop = asyncio.get_running_loop()

    except RuntimeError:

        return asyncio.run(coro)

    else:

        return loop.create_task(coro)



from datetime import timedelta

async def send_message():

    user_tg_id = managers_id.values()

    now = datetime.datetime.now()+timedelta(hours=2)

    time_format = "%d-%m-%Y %H:%M:%S"

    for i in user_tg_id:

        await bot.send_message(

            chat_id=i,

            text=f"Данные в боте обновлены{chr(10)}"

                 f"И они актуальны на {now:{time_format}}",

        )



from contextlib import contextmanager

import pandas as pd

import sqlalchemy

from sqlalchemy import text

import uuid



@contextmanager

def get_connection():

    connection = engine.connect()

    try:

        yield connection

        connection.commit()

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()



def save_to_db_sync():

    av_stock = get_av_stock()

    remains = get_remains_reg()

    submissions = get_submissions()

    payment = get_payment()

    moved = get_moved_data()



    av_stock_tmp = av_stock[["product", "line_of_business", "active_substance"]]

    remains_tmp = remains[["product", "line_of_business", "active_substance"]]

    submissions_tmp = submissions[["product", "line_of_business", "active_ingredient"]].rename(columns={"active_ingredient": "active_substance"})



    pr = pd.concat([av_stock_tmp, submissions_tmp, remains_tmp], ignore_index=True)

    product_guide = pr.drop_duplicates(["product"]).reset_index(drop=True)

    product_guide.insert(0, "id", product_guide.apply(lambda _: uuid.uuid4(), axis=1))



    with get_connection() as conn:

        conn.execute(text("TRUNCATE product_guide CASCADE"))

        product_guide["product"] = product_guide["product"].str.rstrip()

        product_guide.to_sql("product_guide", con=conn, if_exists="append", index=False)



    remains_sql = pd.merge(remains, product_guide, on="product", suffixes=("", "_guide"))

    remains_sql = remains_sql[[

        "line_of_business", "warehouse", "parent_element", "nomenclature", "party_sign",

        "buying_season", "nomenclature_series", "mtn", "origin_country", "germination",

        "crop_year", "quantity_per_pallet", "active_substance", "certificate",

        "certificate_start_date", "certificate_end_date", "buh", "skl", "weight", "id"]]

    remains_sql.rename(columns={"id": "product"}, inplace=True)

    remains_sql.insert(0, "id", remains_sql.apply(lambda _: uuid.uuid4(), axis=1))



    remains_data_type = {

        "buh": sqlalchemy.types.FLOAT,

        "skl": sqlalchemy.types.FLOAT,

        "product": sqlalchemy.types.UUID

    }



    with get_connection() as conn:

        conn.execute(text("TRUNCATE remains CASCADE"))

        remains_sql.to_sql("remains", con=conn, if_exists="append", index=False, dtype=remains_data_type)



    available_stock_sql = pd.merge(av_stock, product_guide, on="product", suffixes=("", "_guide"))

    available_stock_sql = available_stock_sql[[

        "nomenclature", "party_sign", "buying_season", "division",

        "line_of_business", "active_substance", "available", "id"]]

    available_stock_sql.rename(columns={"id": "product"}, inplace=True)

    available_stock_sql.drop(columns=["active_substance"], inplace=True)



    av_stock_data_type = {

        "product": sqlalchemy.types.UUID,

        "available": sqlalchemy.types.FLOAT

    }



    with get_connection() as conn:

        conn.execute(text("TRUNCATE available_stock CASCADE"))

        available_stock_sql.to_sql("available_stock", con=conn, if_exists="append", index=False, dtype=av_stock_data_type)



    submissions_sql = pd.merge(submissions, product_guide, on="product", suffixes=("", "_guide"))

    submissions_sql = submissions_sql[[

        "division", "manager", "company_group", "client", "contract_supplement",

        "parent_element", "manufacturer", "active_ingredient", "nomenclature",

        "party_sign", "buying_season", "line_of_business", "period",

        "shipping_warehouse", "document_status", "delivery_status",

        "shipping_address", "transport", "plan", "fact", "different", "id"]]

    submissions_sql.rename(columns={"id": "product"}, inplace=True)



    sub_data_type = {

        "plan": sqlalchemy.types.FLOAT,

        "fact": sqlalchemy.types.FLOAT,

        "different": sqlalchemy.types.FLOAT,

        "product": sqlalchemy.types.UUID

    }



    with get_connection() as conn:

        conn.execute(text("TRUNCATE submissions CASCADE"))

        submissions_sql.to_sql("submissions", con=conn, if_exists="append", index=False, dtype=sub_data_type)



    with get_connection() as conn:

        conn.execute(text("TRUNCATE payment CASCADE"))

        payment.to_sql("payment", con=conn, if_exists="append", index=False)



    with get_connection() as conn:

        conn.execute(text("TRUNCATE moved_data CASCADE"))

        moved.to_sql("moved_data", con=conn, if_exists="append", index=False)

        # run_async(send_message())



    print("Done!")