# coding: utf-8

# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = vio_from_dict(json.loads(json_string))

from datetime import datetime
import dateutil.parser


def from_str(x):
    assert isinstance(x, (str, unicode))
    return x


def from_none(x):
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_datetime(x):
    return dateutil.parser.parse(x)


def from_bool(x):
    assert isinstance(x, bool)
    return x

def from_int(x):
    assert (isinstance(x, int) or isinstance(x, float)) and not isinstance(x, bool)
    return x


def to_class(c, x):
    assert isinstance(x, c)
    return x.to_dict()


def from_list(f, x):
    assert isinstance(x, list)
    return [f(y) for y in x]


class Address:
    def __init__(self, street, number, city, province, zip_code, phone_number):
        self.street = street
        self.number = number
        self.city = city
        self.province = province
        self.zip_code = zip_code
        self.phone_number = phone_number

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        street = from_union([from_str, from_none], obj.get(u"street"))
        number = from_union([from_str, from_none], obj.get(u"number"))
        city = from_union([from_str, from_none], obj.get(u"city"))
        province = from_union([from_str, from_none], obj.get(u"province"))
        zip_code = from_union([from_str, from_none], obj.get(u"zipCode"))
        phone_number = from_union([from_str, from_none], obj.get(u"phoneNumber"))
        return Address(street, number, city, province, zip_code, phone_number)

    def to_dict(self):
        result = {}
        result[u"street"] = from_union([from_str, from_none], self.street)
        result[u"number"] = from_union([from_str, from_none], self.number)
        result[u"city"] = from_union([from_str, from_none], self.city)
        result[u"province"] = from_union([from_str, from_none], self.province)
        result[u"zipCode"] = from_union([from_str, from_none], self.zip_code)
        result[u"phoneNumber"] = from_union([from_str, from_none], self.phone_number)
        return result


class Afip:
    def __init__(self, birthday):
        self.birthday = birthday

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        birthday = from_union([from_datetime, from_none], obj.get(u"birthday"))
        return Afip(birthday)

    def to_dict(self):
        result = {}
        result[u"birthday"] = from_union([lambda x: x.isoformat(), from_none], self.birthday)
        return result


class Beard:
    def __init__(self, value, confidence):
        self.value = value
        self.confidence = confidence

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        value = from_union([from_bool, from_none], obj.get(u"value"))
        confidence = from_union([from_int, from_none], obj.get(u"confidence"))
        return Beard(value, confidence)

    def to_dict(self):
        result = {}
        result[u"value"] = from_union([from_bool, from_none], self.value)
        result[u"confidence"] = from_union([from_int, from_none], self.confidence)
        return result


class Emotion:
    def __init__(self, value, confidence):
        self.value = value
        self.confidence = confidence

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        value = from_union([from_str, from_none], obj.get(u"value"))
        confidence = from_union([from_int, from_none], obj.get(u"confidence"))
        return Emotion(value, confidence)

    def to_dict(self):
        result = {}
        result[u"value"] = from_union([from_str, from_none], self.value)
        result[u"confidence"] = from_union([from_int, from_none], self.confidence)
        return result


class FaceAnalysis:
    def __init__(self, age_min, age_max, sex, smile, eyeglasses, sunglasses, beard, mustache, eyes_open, mouth_open, emotion, confidence):
        self.age_min = age_min
        self.age_max = age_max
        self.sex = sex
        self.smile = smile
        self.eyeglasses = eyeglasses
        self.sunglasses = sunglasses
        self.beard = beard
        self.mustache = mustache
        self.eyes_open = eyes_open
        self.mouth_open = mouth_open
        self.emotion = emotion
        self.confidence = confidence

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        age_min = from_union([from_int, from_none], obj.get(u"ageMin"))
        age_max = from_union([from_int, from_none], obj.get(u"ageMax"))
        sex = from_union([Emotion.from_dict, from_none], obj.get(u"sex"))
        smile = from_union([Beard.from_dict, from_none], obj.get(u"smile"))
        eyeglasses = from_union([Beard.from_dict, from_none], obj.get(u"eyeglasses"))
        sunglasses = from_union([Beard.from_dict, from_none], obj.get(u"sunglasses"))
        beard = from_union([Beard.from_dict, from_none], obj.get(u"beard"))
        mustache = from_union([Beard.from_dict, from_none], obj.get(u"mustache"))
        eyes_open = from_union([Beard.from_dict, from_none], obj.get(u"eyesOpen"))
        mouth_open = from_union([Beard.from_dict, from_none], obj.get(u"mouthOpen"))
        emotion = from_union([Emotion.from_dict, from_none], obj.get(u"emotion"))
        confidence = from_union([from_int, from_none], obj.get(u"confidence"))
        return FaceAnalysis(age_min, age_max, sex, smile, eyeglasses, sunglasses, beard, mustache, eyes_open, mouth_open, emotion, confidence)

    def to_dict(self):
        result = {}
        result[u"ageMin"] = from_union([from_int, from_none], self.age_min)
        result[u"ageMax"] = from_union([from_int, from_none], self.age_max)
        result[u"sex"] = from_union([lambda x: to_class(Emotion, x), from_none], self.sex)
        result[u"smile"] = from_union([lambda x: to_class(Beard, x), from_none], self.smile)
        result[u"eyeglasses"] = from_union([lambda x: to_class(Beard, x), from_none], self.eyeglasses)
        result[u"sunglasses"] = from_union([lambda x: to_class(Beard, x), from_none], self.sunglasses)
        result[u"beard"] = from_union([lambda x: to_class(Beard, x), from_none], self.beard)
        result[u"mustache"] = from_union([lambda x: to_class(Beard, x), from_none], self.mustache)
        result[u"eyesOpen"] = from_union([lambda x: to_class(Beard, x), from_none], self.eyes_open)
        result[u"mouthOpen"] = from_union([lambda x: to_class(Beard, x), from_none], self.mouth_open)
        result[u"emotion"] = from_union([lambda x: to_class(Emotion, x), from_none], self.emotion)
        result[u"confidence"] = from_union([from_int, from_none], self.confidence)
        return result


class Location:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        latitude = from_union([from_int, from_none], obj.get(u"latitude"))
        longitude = from_union([from_int, from_none], obj.get(u"longitude"))
        return Location(latitude, longitude)

    def to_dict(self):
        result = {}
        result[u"latitude"] = from_union([from_int, from_none], self.latitude)
        result[u"longitude"] = from_union([from_int, from_none], self.longitude)
        return result


class RenaperAddress:
    def __init__(self, street, number, city, province, zip_code, floor, department, municipality, country):
        self.street = street
        self.number = number
        self.city = city
        self.province = province
        self.zip_code = zip_code
        self.floor = floor
        self.department = department
        self.municipality = municipality
        self.country = country

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        street = from_union([from_str, from_none], obj.get(u"street"))
        number = from_union([from_str, from_none], obj.get(u"number"))
        city = from_union([from_str, from_none], obj.get(u"city"))
        province = from_union([from_str, from_none], obj.get(u"province"))
        zip_code = from_union([from_str, from_none], obj.get(u"zipCode"))
        floor = from_union([from_str, from_none], obj.get(u"floor"))
        department = from_union([from_str, from_none], obj.get(u"department"))
        municipality = from_union([from_str, from_none], obj.get(u"municipality"))
        country = from_union([from_str, from_none], obj.get(u"country"))
        return RenaperAddress(street, number, city, province, zip_code, floor, department, municipality, country)

    def to_dict(self):
        result = {}
        result[u"street"] = from_union([from_str, from_none], self.street)
        result[u"number"] = from_union([from_str, from_none], self.number)
        result[u"city"] = from_union([from_str, from_none], self.city)
        result[u"province"] = from_union([from_str, from_none], self.province)
        result[u"zipCode"] = from_union([from_str, from_none], self.zip_code)
        result[u"floor"] = from_union([from_str, from_none], self.floor)
        result[u"department"] = from_union([from_str, from_none], self.department)
        result[u"municipality"] = from_union([from_str, from_none], self.municipality)
        result[u"country"] = from_union([from_str, from_none], self.country)
        return result


class ID:
    def __init__(self, first_name, last_name, id_number, pdf5417, mrz_code, id_version, text_found, valid_id, valid_renaper, death_renaper, id_creation_date, id_expiration_date, renaper_address, nationality, country_birth):
        self.first_name = first_name
        self.last_name = last_name
        self.id_number = id_number
        self.pdf5417 = pdf5417
        self.mrz_code = mrz_code
        self.id_version = id_version
        self.text_found = text_found
        self.valid_id = valid_id
        self.valid_renaper = valid_renaper
        self.death_renaper = death_renaper
        self.id_creation_date = id_creation_date
        self.id_expiration_date = id_expiration_date
        self.renaper_address = renaper_address
        self.nationality = nationality
        self.country_birth = country_birth

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        first_name = from_union([from_str, from_none], obj.get(u"firstName"))
        last_name = from_union([from_str, from_none], obj.get(u"lastName"))
        id_number = from_union([from_str, from_none], obj.get(u"idNumber"))
        pdf5417 = from_union([from_str, from_none], obj.get(u"pdf5417"))
        mrz_code = from_union([from_str, from_none], obj.get(u"mrzCode"))
        id_version = from_union([from_str, from_none], obj.get(u"idVersion"))
        text_found = from_union([from_bool, from_none], obj.get(u"textFound"))
        valid_id = from_union([from_bool, from_none], obj.get(u"validId"))
        valid_renaper = from_union([from_bool, from_none], obj.get(u"validRenaper"))
        death_renaper = from_union([from_bool, from_none], obj.get(u"deathRenaper"))
        id_creation_date = from_union([from_datetime, from_none], obj.get(u"idCreationDate"))
        id_expiration_date = from_union([from_datetime, from_none], obj.get(u"idExpirationDate"))
        renaper_address = from_union([RenaperAddress.from_dict, from_none], obj.get(u"renaperAddress"))
        nationality = from_union([from_str, from_none], obj.get(u"nationality"))
        country_birth = from_union([from_str, from_none], obj.get(u"countryBirth"))
        return ID(first_name, last_name, id_number, pdf5417, mrz_code, id_version, text_found, valid_id, valid_renaper, death_renaper, id_creation_date, id_expiration_date, renaper_address, nationality, country_birth)

    def to_dict(self):
        result = {}
        result[u"firstName"] = from_union([from_str, from_none], self.first_name)
        result[u"lastName"] = from_union([from_str, from_none], self.last_name)
        result[u"idNumber"] = from_union([from_str, from_none], self.id_number)
        result[u"pdf5417"] = from_union([from_str, from_none], self.pdf5417)
        result[u"mrzCode"] = from_union([from_str, from_none], self.mrz_code)
        result[u"idVersion"] = from_union([from_str, from_none], self.id_version)
        result[u"textFound"] = from_union([from_bool, from_none], self.text_found)
        result[u"validId"] = from_union([from_bool, from_none], self.valid_id)
        result[u"validRenaper"] = from_union([from_bool, from_none], self.valid_renaper)
        result[u"deathRenaper"] = from_union([from_bool, from_none], self.death_renaper)
        result[u"idCreationDate"] = from_union([lambda x: x.isoformat(), from_none], self.id_creation_date)
        result[u"idExpirationDate"] = from_union([lambda x: x.isoformat(), from_none], self.id_expiration_date)
        result[u"renaperAddress"] = from_union([lambda x: to_class(RenaperAddress, x), from_none], self.renaper_address)
        result[u"nationality"] = from_union([from_str, from_none], self.nationality)
        result[u"countryBirth"] = from_union([from_str, from_none], self.country_birth)
        return result


class Media:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get(u"name"))
        url = from_union([from_str, from_none], obj.get(u"url"))
        return Media(name, url)

    def to_dict(self):
        result = {}
        result[u"name"] = from_union([from_str, from_none], self.name)
        result[u"url"] = from_union([from_str, from_none], self.url)
        return result


class Personal:
    def __init__(self, first_name, last_name, dni, birthday, age, sex, phone_number):
        self.first_name = first_name
        self.last_name = last_name
        self.dni = dni
        self.birthday = birthday
        self.age = age
        self.sex = sex
        self.phone_number = phone_number

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        first_name = from_union([from_str, from_none], obj.get(u"firstName"))
        last_name = from_union([from_str, from_none], obj.get(u"lastName"))
        dni = from_union([from_str, from_none], obj.get(u"dni"))
        birthday = from_union([from_datetime, from_none], obj.get(u"birthday"))
        age = from_union([from_int, from_none], obj.get(u"age"))
        sex = from_union([from_str, from_none], obj.get(u"sex"))
        phone_number = from_union([from_str, from_none], obj.get(u"phoneNumber"))
        return Personal(first_name, last_name, dni, birthday, age, sex, phone_number)

    def to_dict(self):
        result = {}
        result[u"firstName"] = from_union([from_str, from_none], self.first_name)
        result[u"lastName"] = from_union([from_str, from_none], self.last_name)
        result[u"dni"] = from_union([from_str, from_none], self.dni)
        result[u"birthday"] = from_union([lambda x: x.isoformat(), from_none], self.birthday)
        result[u"age"] = from_union([from_int, from_none], self.age)
        result[u"sex"] = from_union([from_str, from_none], self.sex)
        result[u"phoneNumber"] = from_union([from_str, from_none], self.phone_number)
        return result


class TotalByCategory:
    def __init__(self, category_name, total_apps):
        self.category_name = category_name
        self.total_apps = total_apps

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        category_name = from_union([from_str, from_none], obj.get(u"categoryName"))
        total_apps = from_union([from_int, from_none], obj.get(u"totalApps"))
        return TotalByCategory(category_name, total_apps)

    def to_dict(self):
        result = {}
        result[u"categoryName"] = from_union([from_str, from_none], self.category_name)
        result[u"totalApps"] = from_union([from_int, from_none], self.total_apps)
        return result


class AppRank:
    def __init__(self, total_installed_apps, total_by_category):
        self.total_installed_apps = total_installed_apps
        self.total_by_category = total_by_category

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        total_installed_apps = from_union([from_int, from_none], obj.get(u"totalInstalledApps"))
        total_by_category = from_union([lambda x: from_list(TotalByCategory.from_dict, x), from_none], obj.get(u"totalByCategory"))
        return AppRank(total_installed_apps, total_by_category)

    def to_dict(self):
        result = {}
        result[u"totalInstalledApps"] = from_union([from_int, from_none], self.total_installed_apps)
        result[u"totalByCategory"] = from_union([lambda x: from_list(lambda x: to_class(TotalByCategory, x), x), from_none], self.total_by_category)
        return result


class WorstLast:
    def __init__(self, situation, month, debt):
        self.situation = situation
        self.month = month
        self.debt = debt

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        situation = from_union([from_int, from_none], obj.get(u"situation"))
        month = from_union([from_str, from_none], obj.get(u"month"))
        debt = from_union([from_int, from_none], obj.get(u"debt"))
        return WorstLast(situation, month, debt)

    def to_dict(self):
        result = {}
        result[u"situation"] = from_union([from_int, from_none], self.situation)
        result[u"month"] = from_union([from_str, from_none], self.month)
        result[u"debt"] = from_union([from_int, from_none], self.debt)
        return result


class Cendeu:
    def __init__(self, with_debts, worst_last_month, worst_last3_months, worst_last6_months, worst_last12_months):
        self.with_debts = with_debts
        self.worst_last_month = worst_last_month
        self.worst_last3_months = worst_last3_months
        self.worst_last6_months = worst_last6_months
        self.worst_last12_months = worst_last12_months

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        with_debts = from_union([from_bool, from_none], obj.get(u"withDebts"))
        worst_last_month = from_union([WorstLast.from_dict, from_none], obj.get(u"worstLastMonth"))
        worst_last3_months = from_union([WorstLast.from_dict, from_none], obj.get(u"worstLast3Months"))
        worst_last6_months = from_union([WorstLast.from_dict, from_none], obj.get(u"worstLast6Months"))
        worst_last12_months = from_union([WorstLast.from_dict, from_none], obj.get(u"worstLast12Months"))
        return Cendeu(with_debts, worst_last_month, worst_last3_months, worst_last6_months, worst_last12_months)

    def to_dict(self):
        result = {}
        result[u"withDebts"] = from_union([from_bool, from_none], self.with_debts)
        result[u"worstLastMonth"] = from_union([lambda x: to_class(WorstLast, x), from_none], self.worst_last_month)
        result[u"worstLast3Months"] = from_union([lambda x: to_class(WorstLast, x), from_none], self.worst_last3_months)
        result[u"worstLast6Months"] = from_union([lambda x: to_class(WorstLast, x), from_none], self.worst_last6_months)
        result[u"worstLast12Months"] = from_union([lambda x: to_class(WorstLast, x), from_none], self.worst_last12_months)
        return result


class ContactRank:
    def __init__(self, total_contacts):
        self.total_contacts = total_contacts

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        total_contacts = from_union([from_int, from_none], obj.get(u"totalContacts"))
        return ContactRank(total_contacts)

    def to_dict(self):
        result = {}
        result[u"totalContacts"] = from_union([from_int, from_none], self.total_contacts)
        return result


class GISRank:
    def __init__(self, address_location, address_geolocation, nse_gis):
        self.address_location = address_location
        self.address_geolocation = address_geolocation
        self.nse_gis = nse_gis

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        address_location = from_union([Location.from_dict, from_none], obj.get(u"addressLocation"))
        address_geolocation = from_union([Location.from_dict, from_none], obj.get(u"addressGeolocation"))
        nse_gis = from_union([from_str, from_none], obj.get(u"nseGIS"))
        return GISRank(address_location, address_geolocation, nse_gis)

    def to_dict(self):
        result = {}
        result[u"addressLocation"] = from_union([lambda x: to_class(Location, x), from_none], self.address_location)
        result[u"addressGeolocation"] = from_union([lambda x: to_class(Location, x), from_none], self.address_geolocation)
        result[u"nseGIS"] = from_union([from_str, from_none], self.nse_gis)
        return result


class IncomeRank:
    def __init__(self, declared_personal_income, couple_income, other_income, total_income, housing_property, housing_age, mobility, studies_level, predicted_nse):
        self.declared_personal_income = declared_personal_income
        self.couple_income = couple_income
        self.other_income = other_income
        self.total_income = total_income
        self.housing_property = housing_property
        self.housing_age = housing_age
        self.mobility = mobility
        self.studies_level = studies_level
        self.predicted_nse = predicted_nse

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        declared_personal_income = from_union([from_int, from_none], obj.get(u"declaredPersonalIncome"))
        couple_income = from_union([from_int, from_none], obj.get(u"coupleIncome"))
        other_income = from_union([from_int, from_none], obj.get(u"otherIncome"))
        total_income = from_union([from_int, from_none], obj.get(u"totalIncome"))
        housing_property = from_union([from_str, from_none], obj.get(u"housingProperty"))
        housing_age = from_union([from_str, from_none], obj.get(u"housingAge"))
        mobility = from_union([from_str, from_none], obj.get(u"mobility"))
        studies_level = from_union([from_str, from_none], obj.get(u"studiesLevel"))
        predicted_nse = from_union([from_str, from_none], obj.get(u"predictedNSE"))
        return IncomeRank(declared_personal_income, couple_income, other_income, total_income, housing_property, housing_age, mobility, studies_level, predicted_nse)

    def to_dict(self):
        result = {}
        result[u"declaredPersonalIncome"] = from_union([from_int, from_none], self.declared_personal_income)
        result[u"coupleIncome"] = from_union([from_int, from_none], self.couple_income)
        result[u"otherIncome"] = from_union([from_int, from_none], self.other_income)
        result[u"totalIncome"] = from_union([from_int, from_none], self.total_income)
        result[u"housingProperty"] = from_union([from_str, from_none], self.housing_property)
        result[u"housingAge"] = from_union([from_str, from_none], self.housing_age)
        result[u"mobility"] = from_union([from_str, from_none], self.mobility)
        result[u"studiesLevel"] = from_union([from_str, from_none], self.studies_level)
        result[u"predictedNSE"] = from_union([from_str, from_none], self.predicted_nse)
        return result


class Risk:
    def __init__(self, findo_score, gis_rank, contact_rank, app_rank, income_rank, cendeu):
        self.findo_score = findo_score
        self.gis_rank = gis_rank
        self.contact_rank = contact_rank
        self.app_rank = app_rank
        self.income_rank = income_rank
        self.cendeu = cendeu

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        findo_score = from_union([from_int, from_none], obj.get(u"findoScore"))
        gis_rank = from_union([GISRank.from_dict, from_none], obj.get(u"gisRank"))
        contact_rank = from_union([ContactRank.from_dict, from_none], obj.get(u"contactRank"))
        app_rank = from_union([AppRank.from_dict, from_none], obj.get(u"appRank"))
        income_rank = from_union([IncomeRank.from_dict, from_none], obj.get(u"incomeRank"))
        cendeu = from_union([Cendeu.from_dict, from_none], obj.get(u"cendeu"))
        return Risk(findo_score, gis_rank, contact_rank, app_rank, income_rank, cendeu)

    def to_dict(self):
        result = {}
        result[u"findoScore"] = from_union([from_int, from_none], self.findo_score)
        result[u"gisRank"] = from_union([lambda x: to_class(GISRank, x), from_none], self.gis_rank)
        result[u"contactRank"] = from_union([lambda x: to_class(ContactRank, x), from_none], self.contact_rank)
        result[u"appRank"] = from_union([lambda x: to_class(AppRank, x), from_none], self.app_rank)
        result[u"incomeRank"] = from_union([lambda x: to_class(IncomeRank, x), from_none], self.income_rank)
        result[u"cendeu"] = from_union([lambda x: to_class(Cendeu, x), from_none], self.cendeu)
        return result


class Security:
    def __init__(self, questions_right, questions_wrong, first_public_ip, last_public_ip):
        self.questions_right = questions_right
        self.questions_wrong = questions_wrong
        self.first_public_ip = first_public_ip
        self.last_public_ip = last_public_ip

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        questions_right = from_union([from_int, from_none], obj.get(u"questionsRight"))
        questions_wrong = from_union([from_int, from_none], obj.get(u"questionsWrong"))
        first_public_ip = from_union([from_str, from_none], obj.get(u"firstPublicIP"))
        last_public_ip = from_union([from_str, from_none], obj.get(u"lastPublicIP"))
        return Security(questions_right, questions_wrong, first_public_ip, last_public_ip)

    def to_dict(self):
        result = {}
        result[u"questionsRight"] = from_union([from_int, from_none], self.questions_right)
        result[u"questionsWrong"] = from_union([from_int, from_none], self.questions_wrong)
        result[u"firstPublicIP"] = from_union([from_str, from_none], self.first_public_ip)
        result[u"lastPublicIP"] = from_union([from_str, from_none], self.last_public_ip)
        return result


class SignIn:
    def __init__(self, provider, display_name, email, verified):
        self.provider = provider
        self.display_name = display_name
        self.email = email
        self.verified = verified

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        provider = from_union([from_str, from_none], obj.get(u"provider"))
        display_name = from_union([from_str, from_none], obj.get(u"displayName"))
        email = from_union([from_str, from_none], obj.get(u"email"))
        verified = from_union([from_bool, from_none], obj.get(u"verified"))
        return SignIn(provider, display_name, email, verified)

    def to_dict(self):
        result = {}
        result[u"provider"] = from_union([from_str, from_none], self.provider)
        result[u"displayName"] = from_union([from_str, from_none], self.display_name)
        result[u"email"] = from_union([from_str, from_none], self.email)
        result[u"verified"] = from_union([from_bool, from_none], self.verified)
        return result


class Smartphone:
    def __init__(self, device_name, sim_operator_name, valid_operator, os_version, list_of_emails, device_cell_phone_number, sim_state):
        self.device_name = device_name
        self.sim_operator_name = sim_operator_name
        self.valid_operator = valid_operator
        self.os_version = os_version
        self.list_of_emails = list_of_emails
        self.device_cell_phone_number = device_cell_phone_number
        self.sim_state = sim_state

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        device_name = from_union([from_str, from_none], obj.get(u"deviceName"))
        sim_operator_name = from_union([from_str, from_none], obj.get(u"simOperatorName"))
        valid_operator = from_union([from_bool, from_none], obj.get(u"validOperator"))
        os_version = from_union([from_str, from_none], obj.get(u"osVersion"))
        list_of_emails = from_union([lambda x: from_list(from_str, x), from_none], obj.get(u"listOfEmails"))
        device_cell_phone_number = from_union([from_str, from_none], obj.get(u"deviceCellPhoneNumber"))
        sim_state = from_union([from_str, from_none], obj.get(u"simState"))
        return Smartphone(device_name, sim_operator_name, valid_operator, os_version, list_of_emails, device_cell_phone_number, sim_state)

    def to_dict(self):
        result = {}
        result[u"deviceName"] = from_union([from_str, from_none], self.device_name)
        result[u"simOperatorName"] = from_union([from_str, from_none], self.sim_operator_name)
        result[u"validOperator"] = from_union([from_bool, from_none], self.valid_operator)
        result[u"osVersion"] = from_union([from_str, from_none], self.os_version)
        result[u"listOfEmails"] = from_union([lambda x: from_list(from_str, x), from_none], self.list_of_emails)
        result[u"deviceCellPhoneNumber"] = from_union([from_str, from_none], self.device_cell_phone_number)
        result[u"simState"] = from_union([from_str, from_none], self.sim_state)
        return result


class WorkInformation:
    def __init__(self, work_relationship, job, employeer, position, address, phone_number):
        self.work_relationship = work_relationship
        self.job = job
        self.employeer = employeer
        self.position = position
        self.address = address
        self.phone_number = phone_number

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        work_relationship = from_union([from_str, from_none], obj.get(u"workRelationship"))
        job = from_union([from_str, from_none], obj.get(u"job"))
        employeer = from_union([from_str, from_none], obj.get(u"employeer"))
        position = from_union([from_str, from_none], obj.get(u"position"))
        address = from_union([Address.from_dict, from_none], obj.get(u"address"))
        phone_number = from_union([from_str, from_none], obj.get(u"phoneNumber"))
        return WorkInformation(work_relationship, job, employeer, position, address, phone_number)

    def to_dict(self):
        result = {}
        result[u"workRelationship"] = from_union([from_str, from_none], self.work_relationship)
        result[u"job"] = from_union([from_str, from_none], self.job)
        result[u"employeer"] = from_union([from_str, from_none], self.employeer)
        result[u"position"] = from_union([from_str, from_none], self.position)
        result[u"address"] = from_union([lambda x: to_class(Address, x), from_none], self.address)
        result[u"phoneNumber"] = from_union([from_str, from_none], self.phone_number)
        return result


class Vio:
    def __init__(self, personal, sign_in, address, address_validated, geolocation, face_analysis, face_comparison, afip, work_information, smartphone, id, security, risk, media, request_time_stamp):
        self.personal = personal
        self.sign_in = sign_in
        self.address = address
        self.address_validated = address_validated
        self.geolocation = geolocation
        self.face_analysis = face_analysis
        self.face_comparison = face_comparison
        self.afip = afip
        self.work_information = work_information
        self.smartphone = smartphone
        self.id = id
        self.security = security
        self.risk = risk
        self.media = media
        self.request_time_stamp = request_time_stamp

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        personal = from_union([Personal.from_dict, from_none], obj.get(u"personal"))
        sign_in = from_union([SignIn.from_dict, from_none], obj.get(u"signIn"))
        address = from_union([Address.from_dict, from_none], obj.get(u"address"))
        address_validated = from_union([from_str, from_none], obj.get(u"addressValidated"))
        geolocation = from_union([Location.from_dict, from_none], obj.get(u"geolocation"))
        face_analysis = from_union([FaceAnalysis.from_dict, from_none], obj.get(u"faceAnalysis"))
        face_comparison = from_union([from_int, from_none], obj.get(u"faceComparison"))
        afip = from_union([Afip.from_dict, from_none], obj.get(u"afip"))
        work_information = from_union([WorkInformation.from_dict, from_none], obj.get(u"workInformation"))
        smartphone = from_union([Smartphone.from_dict, from_none], obj.get(u"smartphone"))
        id = from_union([ID.from_dict, from_none], obj.get(u"id"))
        security = from_union([Security.from_dict, from_none], obj.get(u"security"))
        risk = from_union([Risk.from_dict, from_none], obj.get(u"risk"))
        media = from_union([lambda x: from_list(Media.from_dict, x), from_none], obj.get(u"media"))
        request_time_stamp = from_union([from_datetime, from_none], obj.get(u"requestTimeStamp"))
        return Vio(personal, sign_in, address, address_validated, geolocation, face_analysis, face_comparison, afip, work_information, smartphone, id, security, risk, media, request_time_stamp)

    def to_dict(self):
        result = {}
        result[u"personal"] = from_union([lambda x: to_class(Personal, x), from_none], self.personal)
        result[u"signIn"] = from_union([lambda x: to_class(SignIn, x), from_none], self.sign_in)
        result[u"address"] = from_union([lambda x: to_class(Address, x), from_none], self.address)
        result[u"addressValidated"] = from_union([from_str, from_none], self.address_validated)
        result[u"geolocation"] = from_union([lambda x: to_class(Location, x), from_none], self.geolocation)
        result[u"faceAnalysis"] = from_union([lambda x: to_class(FaceAnalysis, x), from_none], self.face_analysis)
        result[u"faceComparison"] = from_union([from_int, from_none], self.face_comparison)
        result[u"afip"] = from_union([lambda x: to_class(Afip, x), from_none], self.afip)
        result[u"workInformation"] = from_union([lambda x: to_class(WorkInformation, x), from_none], self.work_information)
        result[u"smartphone"] = from_union([lambda x: to_class(Smartphone, x), from_none], self.smartphone)
        result[u"id"] = from_union([lambda x: to_class(ID, x), from_none], self.id)
        result[u"security"] = from_union([lambda x: to_class(Security, x), from_none], self.security)
        result[u"risk"] = from_union([lambda x: to_class(Risk, x), from_none], self.risk)
        result[u"media"] = from_union([lambda x: from_list(lambda x: to_class(Media, x), x), from_none], self.media)
        result[u"requestTimeStamp"] = from_union([lambda x: x.isoformat(), from_none], self.request_time_stamp)
        return result


def vio_from_dict(s):
    return Vio.from_dict(s)


def vio_to_dict(x):
    return to_class(Vio, x)
