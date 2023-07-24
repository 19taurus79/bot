from piccolo.table import Table
from piccolo.columns import Varchar, UUID, ForeignKey, Date, Integer


# class Agent(Table):
#     id = UUID(primary_key=True)
#     name = Varchar(length=50, null=False, unique=True)
#
#
# class Client(Table):
#     id = UUID(primary_key=True)
#     name = Varchar(length=50, null=False, unique=True)
#     agent = ForeignKey(references=Agent)


class ProductGuide(Table):
    id = UUID(primary_key=True)
    product = Varchar(null=False, unique=True)
    line_of_business = Varchar(null=False)


# class ManagerGuide(Table):
#     id = UUID(primary_key=True)
#     manager = Varchar(null=False, unique=True)


# class ClientGuide(Table):
#     id = UUID(primary_key=True)
#     client = Varchar(null=False, unique=True)
#     company_group = Varchar(null=True)


class Remains(Table):
    id = UUID(primary_key=True)
    line_of_business = Varchar(null=False)
    warehouse = Varchar(null=True)
    parent_element = Varchar(null=True)
    nomenclature = Varchar(null=True)
    party_sign = Varchar(null=True)
    buying_season = Varchar(null=True)
    nomenclature_series = Varchar(null=True)
    mtn = Varchar(null=True)
    origin_country = Varchar(null=True)
    germination = Varchar(null=True)
    crop_year = Varchar(null=True)
    quantity_per_pallet = Varchar(null=True)
    active_substance = Varchar(null=True)
    certificate = Varchar(null=True)
    certificate_start_date = Varchar(null=True)
    certificate_end_date = Varchar(null=True)
    buh = Integer()
    skl = Integer()
    weight = Varchar(null=True)
    product = ForeignKey(references=ProductGuide)


class Submissions(Table):
    id = UUID(primary_key=True)
    division = Varchar(null=True)
    manager = Varchar(null=True)
    company_group = Varchar(null=True)
    client = Varchar(null=True)
    contract_supplement = Varchar(null=True)
    parent_element = Varchar(null=True)
    manufacturer = Varchar(null=True)
    active_ingredient = Varchar(null=True)
    nomenclature = Varchar(null=True)
    party_sign = Varchar(null=True)
    buying_season = Varchar(null=True)
    line_of_business = Varchar(null=True)
    period = Varchar(null=True)
    shipping_warehouse = Varchar(null=True)
    document_status = Varchar(null=True)
    delivery_status = Varchar(null=True)
    shipping_address = Varchar(null=True)
    transport = Varchar(null=True)
    plan = Integer()
    fact = Integer()
    different = Integer()
    product = ForeignKey(references=ProductGuide)


class AvailableStock(Table):
    id = UUID(primary_key=True)
    nomenclature = Varchar(null=True)
    party_sign = Varchar(null=True)
    buying_season = Varchar(null=True)
    division = Varchar(null=True)
    line_of_business = Varchar(null=True)
    available = Integer()
    product = ForeignKey(references=ProductGuide)


class ProductUnderSubmissions(Table):
    id = UUID(primary_key=True)
    product = ForeignKey(references=ProductGuide)
    quantity = Integer()
