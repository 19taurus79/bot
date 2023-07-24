import pandas as pd
import sqlalchemy
from sqlalchemy import text

from connection import engine


def get_template_submissions():
    submissions_xls = pd.read_excel("tables/Заявки.xlsx", header=None)
    step1 = submissions_xls.drop(submissions_xls.columns[[0, 1, 2, 3, 4, 5]])
    step2 = step1.rename(columns=step1.iloc[0])
    step3 = step2.dropna(axis="columns", how="all")
    step4 = step3.drop(step3.index[[0, 1, 2]], axis=0)
    step5 = step4.drop(step4.tail(1).index, axis=0)
    names = [
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
    step5.columns = names
    step5.reset_index(drop=True, inplace=True)
    step5["buying_season"].fillna(" ", inplace=True)
    step5.loc[(step5["party_sign"] == "Закупівля поточного сезону"), "party_sign"] = " "
    step5["product"] = step5.apply(
        lambda row: str(row["nomenclature"])
        + " "
        + str(row["party_sign"])
        + " "
        + str(row["buying_season"]),
        axis=1,
    )
    step5["fact"].fillna(0, inplace=True)
    step5["different"].fillna(0, inplace=True)
    step5["plan"].fillna(0, inplace=True)
    step5.to_excel("tables/submissions.xlsx")

    prod_sql = pd.read_sql_table(table_name="product_guide", con=engine)
    val = step5.merge(prod_sql, on="product", how="left")
    val.drop(columns=["line_of_business_y", "product"], axis=1, inplace=True)
    val.rename(
        columns={"line_of_business_x": "line_of_business", "id": "product"},
        inplace=True,
    )
    val.to_excel("tables/submissions_uuids.xlsx")
    return val


def get_template_remains():
    remains_xls = pd.read_excel("tables/Остатки.xlsx", header=None)
    step1 = remains_xls.drop(remains_xls.columns[[0, 1, 2, 4]])
    step2 = step1.rename(columns=step1.iloc[0])
    step3 = step2.dropna(axis="columns", how="all")
    step4 = step3.drop(step3.index[[0, 1]], axis=0)
    step5 = step4.drop(step4.tail(1).index, axis=0)
    step5.columns = [
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
        "weight",
    ]
    step5.reset_index(drop=True, inplace=True)
    step5["buying_season"].fillna(" ", inplace=True)
    step5["party_sign"].fillna(" ", inplace=True)
    step5["product"] = step5.apply(
        lambda row: str(row["nomenclature"])
        + " "
        + str(row["party_sign"])
        + " "
        + str(row["buying_season"]),
        axis=1,
    )
    step5["buh"].fillna(0, inplace=True)
    step5["skl"].fillna(0, inplace=True)
    step5.to_excel("tables/remains.xlsx")

    prod_sql = pd.read_sql_table(table_name="product_guide", con=engine)
    val = step5.merge(prod_sql, on="product", how="left")
    val.drop(columns=["line_of_business_y", "product"], axis=1, inplace=True)
    val.rename(
        columns={"line_of_business_x": "line_of_business", "id": "product"},
        inplace=True,
    )
    val.to_excel("tables/remains_uuids.xlsx")
    return val


def get_template_avstock():
    available_stock_xls = pd.read_excel(
        "tables/Доступность товара подразделения.xlsx", header=None
    )
    step1 = available_stock_xls.drop(
        available_stock_xls.columns[[0, 1, 2, 3, 4, 5, 6, 7]]
    )
    step2 = step1.rename(columns=step1.iloc[0])
    step3 = step2.dropna(axis="columns", how="all")
    step4 = step3.drop(step3.index[[1, 4]], axis=0)
    step5 = step4.drop(step4.tail(1).index, axis=0)
    names = [
        "nomenclature",
        "party_sign",
        "buying_season",
        "division",
        "line_of_business",
        "available",
    ]
    step5.columns = names
    step5.reset_index(drop=True, inplace=True)
    step5["buying_season"].fillna(" ", inplace=True)
    step5["party_sign"].fillna(" ", inplace=True)
    step5["product"] = step5.apply(
        lambda row: str(row["nomenclature"])
        + " "
        + str(row["party_sign"])
        + " "
        + str(row["buying_season"]),
        axis=1,
    )
    step5["available"].fillna(0, inplace=True)
    step5.to_excel("tables/available_stock.xlsx")

    prod_sql = pd.read_sql_table(table_name="product_guide", con=engine)
    val = step5.merge(prod_sql, on="product", how="left")
    val.drop(columns=["line_of_business_y", "product"], axis=1, inplace=True)
    val.rename(
        columns={"line_of_business_x": "line_of_business", "id": "product"},
        inplace=True,
    )
    val.to_excel("tables/available_stock_uuids.xlsx")
    return val


def get_submission():
    val = get_template_submissions()
    data_type = {
        "plan": sqlalchemy.types.BIGINT,
        "fact": sqlalchemy.types.BIGINT,
        "different": sqlalchemy.types.BIGINT,
        "product": sqlalchemy.types.UUID,
    }
    val.to_sql(
        con=engine,
        if_exists="replace",
        name="submissions_tmp",
        index=False,
        dtype=data_type,
    )
    clean_table_sql = """
                   TRUNCATE submissions
                   """
    update_sql = """
                   INSERT INTO submissions(division,manager,company_group,client,contract_supplement,parent_element,
                   manufacturer,active_ingredient,nomenclature,party_sign,buying_season,line_of_business,period,
                   shipping_warehouse,document_status,delivery_status,shipping_address,transport,plan,fact,different,product)
                   SELECT division,manager,company_group,client,contract_supplement,parent_element,
                   manufacturer,active_ingredient,nomenclature,party_sign,buying_season,line_of_business,period,
                   shipping_warehouse,document_status,delivery_status,shipping_address,transport,plan,fact,different,product
                    FROM submissions_tmp
                   """
    with engine.connect() as conn:
        conn.execute(text(clean_table_sql))
        conn.execute(text(update_sql))
        conn.commit()
    # clean_table_sql = """
    #                    TRUNCATE product_under_submissions
    #                    """
    # update_sql = """
    #                 INSERT INTO product_under_submissions(product, SUM(different))
    #                 SELECT product
    #                 FROM submissions
    #                 GROUP BY product
    # """
    # with engine.connect() as conn:
    #     conn.execute(text(clean_table_sql))
    #     conn.execute(text(update_sql))
    #     conn.commit()
    return print("Файл с заявками обработан")


def product_guide():
    remains = pd.read_excel("tables/remains.xlsx")
    submissions = pd.read_excel("tables/submissions.xlsx")
    aval_stocks = pd.read_excel("tables/available_stock.xlsx")
    a = remains.merge(submissions, left_on="product", right_on="product", how="outer")
    b = a.merge(aval_stocks, left_on="product", right_on="product", how="outer")
    c = b.drop_duplicates(subset=["product"])
    d = c["product"]
    d.to_sql(con=engine, if_exists="replace", name="product_guide_temp", index=False)

    clean_table_sql = """
    TRUNCATE product_guide CASCADE
    """
    update_sql = """
    INSERT INTO product_guide(product)
    SELECT product FROM product_guide_temp
    """
    with engine.connect() as conn:
        conn.execute(text(clean_table_sql))
        conn.execute(text(update_sql))
        conn.commit()
    prod_sql = pd.read_sql_table(table_name="product_guide", con=engine)
    submissions_uuids = submissions.merge(prod_sql, on="product", how="left")
    submissions_uuids.drop(
        columns=["line_of_business_y", "product"], axis=1, inplace=True
    )
    submissions_uuids.rename(
        columns={"line_of_business_x": "line_of_business", "id": "product"},
        inplace=True,
    )
    submissions_uuids.to_excel("tables/submissions_uuids.xlsx")
    d.to_excel("tables/product.xlsx")
    return print("Справочник товаров получен")


def client_guide():
    data = pd.read_excel("submissions.xlsx")
    client = data[["client", "company_group"]]
    client.drop_duplicates(
        subset=["client", "company_group"], keep="first", inplace=True
    )
    client.reset_index(drop=True, inplace=True)
    client.to_sql(con=engine, if_exists="replace", name="client_guide_tmp", index=False)
    client.to_excel("client.xlsx")
    clean_table_sql = """
        TRUNCATE client_guide
        """
    update_sql = """
        INSERT INTO client_guide(client, company_group)
        SELECT client, company_group FROM client_guide_tmp
        """
    with engine.connect() as conn:
        conn.execute(text(clean_table_sql))
        conn.execute(text(update_sql))
        conn.commit()
    return print("Справочник клиентов получен")


def manager_guide():
    data = pd.read_excel("tables/submissions.xlsx")
    manager = data["manager"]
    manager.drop_duplicates(keep="first", inplace=True)
    manager.reset_index(drop=True, inplace=True)
    manager.to_sql(
        con=engine, if_exists="replace", name="manager_guide_tmp", index=False
    )
    manager.to_excel("manager.xlsx")
    clean_table_sql = """
            TRUNCATE manager_guide
            """
    update_sql = """
            INSERT INTO manager_guide(manager)
            SELECT manager FROM manager_guide_tmp
            """
    with engine.connect() as conn:
        conn.execute(text(clean_table_sql))
        conn.execute(text(update_sql))
        conn.commit()
    return print("Справочник менеджеров получен")


def get_remains():
    val = get_template_remains()
    data_type = {
        "buh": sqlalchemy.types.BIGINT,
        "skl": sqlalchemy.types.BIGINT,
        "product": sqlalchemy.types.UUID,
    }
    val.to_sql(
        con=engine,
        if_exists="replace",
        name="remains_tmp",
        index=False,
        dtype=data_type,
    )
    clean_table_sql = """
               TRUNCATE remains
               """
    update_sql = """
               INSERT INTO remains(line_of_business, warehouse, 
               parent_element, nomenclature, party_sign, buying_season,
               nomenclature_series,mtn,origin_country,germination,
               crop_year,quantity_per_pallet,active_substance,certificate,
               certificate_start_date,certificate_end_date,buh,skl,weight,product)
               SELECT line_of_business,warehouse,
               parent_element,nomenclature,party_sign,buying_season,
               nomenclature_series,mtn,origin_country,germination,
               crop_year,quantity_per_pallet,active_substance,certificate,
               certificate_start_date,certificate_end_date,buh,skl,weight,product
                FROM remains_tmp
               """
    with engine.connect() as conn:
        conn.execute(text(clean_table_sql))
        conn.execute(text(update_sql))
        conn.commit()
    return print("Файл с остатками обработан")


def get_available_stock():
    val = get_template_avstock()
    data_type = {"available": sqlalchemy.types.BIGINT, "product": sqlalchemy.types.UUID}
    val.to_sql(
        con=engine,
        if_exists="replace",
        name="available_stock_tmp",
        index=False,
        dtype=data_type,
    )
    clean_table_sql = """
                       TRUNCATE available_stock 
                       """
    update_sql = """
                       INSERT INTO available_stock(nomenclature,party_sign,buying_season,division,
                       line_of_business,available,product)
                       SELECT nomenclature,party_sign,buying_season,division,
                       line_of_business,available,product
                        FROM available_stock_tmp
                       """
    with engine.connect() as conn:
        conn.execute(text(clean_table_sql))
        conn.execute(text(update_sql))
        conn.commit()
    return print("Файл со свободными остатками обработан")


if __name__ == "__main__":
    product_guide()
    get_submission()
    get_remains()
    get_available_stock()
    # client_guide()
    # manager_guide()
