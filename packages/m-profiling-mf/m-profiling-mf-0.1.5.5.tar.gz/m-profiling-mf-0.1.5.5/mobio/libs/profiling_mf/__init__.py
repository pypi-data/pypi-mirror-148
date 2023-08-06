import os

from mobio.libs.caching import LruCache, StoreType


class CommonMerchant:
    MERGE_WHEN = 0.95
    PREFIX_DYNAMIC_FIELD = "_dyn"
    PREFIX_CRITERIA = "cri"
    ADMIN_HOST = os.environ.get("ADMIN_HOST")
    MOBIO_TOKEN = "Basic " + os.environ.get("YEK_REWOP", "f38b67fa-22f3-4680-9d01-c36b23bd0cad")


class ProfileStructure:
    THIRD_PARTY_INFO = "third_party_info"
    PROFILE_GROUP = "profile_group"
    BUSINESS_CASE_ID = "business_case_id"
    SOURCE_ID = "source_id"
    SOURCE_TYPE = "source_type"
    MERCHANT_ID = "merchant_id"
    PROFILE_ID = "profile_id"
    CREATED_TIME = "created_time"
    UPDATED_TIME = "updated_time"
    EMAIL = "email"
    EMAIL_1 = "email_1"
    EMAIL_2 = "email_2"
    PHONE_NUMBER = "phone_number"
    PHONE_NUMBER_1 = "phone_number_1"
    PHONE_NUMBER_2 = "phone_number_2"
    SOCIAL_USER = "social_user"
    SOCIAL_NAME = "social_name"
    SOCIAL_ID = "social_id"
    ID_SOCIAL = "id_social"
    SOCIAL_TYPE = "social_type"
    SOCIAL_ID_TYPE = "social_id_type"
    PEOPLE_ID = "people_id"
    IDENTIFY_CODE = "identify_code"
    DRIVER_LICENSE = "driver_license"
    PASSPORT = "passport"
    IS_COMPANY = "is_company"
    TAX_CODE = "tax_code"
    TAX_NAME = "tax_name"
    TAX_ADDRESS = "tax_address"
    LAT = "lat"
    LON = "lon"
    CREATED_ACCOUNT_TYPE = "created_account_type"
    BANK_ACC = "bank_acc"
    GENDER = "gender"
    BIRTHDAY = "birthday"
    BIRTH_YEAR = "birth_year"
    BIRTH_DATE = "birth_date"
    BIRTH_MONTH = "birth_month"
    BIRTH_MONTH_DATE = "birth_month_date"
    MARITAL_STATUS = "marital_status"
    NAME = "name"
    DISPLAY_NAME = "display_name"
    PASSWORD = "password"
    ADDRESS = "address"
    PROFILE_ADDRESS = "profile_address"
    PROVINCE_CODE = "province_code"
    DISTRICT_CODE = "district_code"
    WARD_CODE = "ward_code"
    FAX = "fax"
    OPERATION = "operation"
    JOB = "job"
    HOBBY = "hobby"
    TAGS = "tags"
    TAGS_SEARCH = "tags_search"
    PROFILE_TAGS = "profile_tags"
    RELIGIOUSNESS = "religiousness"
    NATION = "nation"
    AVATAR = "avatar"
    COMPANY = "company"
    FACE_ID = "face_id"
    INCOME_LOW_THRESHOLD = "income_low_threshold"
    INCOME_HIGH_THRESHOLD = "income_high_threshold"
    INCOME_TYPE = "income_type"
    BUDGET_LOW_THRESHOLD = "budget_low_threshold"
    BUDGET_HIGH_THRESHOLD = "budget_high_threshold"
    FREQUENTLY_DEMANDS = "frequently_demands"
    LST_PHONE_DELETED = "lst_phone_deleted"
    LST_EMAIL_DELETED = "lst_email_deleted"
    DEGREE = "DEGREE".lower()
    INCOME_FAMILY = "income_family"
    RELATIONSHIP_DATA = "relationship_data"
    RELATION_WITH_CHILDS = "relation_with_childs"
    CHILDS = "CHILDS".lower()
    NUMBER_CHILDS = "number_childs"
    CHILD_ID = "child_id"
    NTH = "nth"
    CUSTOMER_ID = "customer_id"
    CUSTOMER_CREATED_TIME = "customer_created_time"
    PARTNER_POINT = "partner_point"
    IS_STAFF_UPDATE = "is_staff_update"
    SOCIAL_TAGS = "social_tags"
    LENDING_LIMIT = "lending_limit"
    SOURCE = "source"
    PRIMARY_EMAIL = "primary_email"
    SECONDARY_EMAILS = "secondary_emails"
    PRIMARY_PHONE = "primary_phone"
    SECONDARY_PHONES = "secondary_phones"
    PREDICT = "predict"
    IS_NON_PROFILE = "is_non_profile"
    CARD = "card"
    CARDS = "cards"
    PUSH_ID = "push_id"
    POINT = "point"
    RANK_POINT = "rank_point"
    AGE = "age"
    DEVICES = "devices"
    TAGS_INTERACTIVE = "tags_interactive"
    SALARY = "salary"
    CIF_CODE = "cif"
    CLV = "clv"
    NUMBER_TRANSACTION = "number_transactions"
    PROFILE_IDENTIFY = "profile_identify"
    LAST_PAYMENT = "last_payment"
    MERGEABLE = "mergeable"
    DEVICE_TYPES = "device_types"
    ISP = 'isp'
    HIDDEN_AUDIENCE = "hidden_audience"


class ProfileByIdentifyStructure:
    MERCHANT_ID = "merchant_id"
    PROFILE_ID = "profile_id"
    IDENTIFY_VALUE = "identify_value"
    IDENTIFY_TYPE = "identify_type"
    IS_VERIFY = "is_verify"
    DATE_VERIFY = "date_verify"


class Device:
    DEVICE_ID = "device_id"
    SOURCE = "source"
    DEVICE_NAME = "device_name"


class DeviceTypeStructure:
    DEVICE_TYPE = "device_type"
    DEVICE_NAME = "device_name"


class ProfileTagsStructure:
    ID = "id"
    TAG = "tag"
    TAG_TYPE = "tag_type"
    MERCHANT_ID = "merchant_id"


class TagInteractiveStructure:
    TAG_ID = "tag_id"
    INTERACTIVE_TOTAL = "interactive_total"
    INTERACTIVE_3_DAYS = "interactive_3_day"
    INTERACTIVE_7_DAYS = "interactive_7_day"
    INTERACTIVE_30_DAYS = "interactive_30_day"
    LAST_ACTION_TIME = "last_action_time"


class Environment:
    HOST = 'HOST'
    ADMIN_HOST = 'ADMIN_HOST'
    REDIS_URI = 'REDIS_URI'
    REDIS_HOST = 'REDIS_HOST'
    REDIS_PORT = 'REDIS_PORT'
    KAFKA_BROKER = 'KAFKA_BROKER'


lru_cache = LruCache(
    store_type=StoreType.REDIS,
    # config_file_name=APP_CONFIG_FILE_PATH,
    cache_prefix="profiling_mf",
    redis_uri=os.getenv(Environment.REDIS_URI),
)
