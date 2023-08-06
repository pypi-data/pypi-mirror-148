from typing import List, Optional, Union
from xmlrpc.client import boolean
from model.common.address import Address
from model.common.educationbase import EducationBase
from model.common.phone import Phone
from model.common.commonmodel import CommonModel
from model.common.employmentbase import EmploymentBase
from model.common.id import ID
from model.common.person import Person
from datetime import date, datetime
from pydantic import BaseModel, EmailStr, root_validator, validator
from model.common.utils import normalize
from webform.prportal.data.country_residence import country_residence


class PersonId(ID):
    pass


class Employment(EmploymentBase):
    bcpnp_qualified: bool


class Marriage(BaseModel):
    marital_status: str
    married_date: Optional[date]
    sp_last_name: Optional[str]
    sp_first_name: Optional[str]
    previous_married: bool
    pre_sp_last_name: Optional[str]
    pre_sp_first_name: Optional[str]
    pre_sp_dob: Optional[date]
    pre_relationship_type: Optional[str]
    pre_start_date: Optional[date]
    pre_end_date: Optional[date]


class Personal(Person):
    email: EmailStr

    used_last_name: Optional[str]
    used_first_name: Optional[str]
    place_of_birth: str
    country_of_birth: str
    did_eca: bool
    eca_supplier: Optional[str]
    eca_number: Optional[str]
    ita_assessed: bool
    ita_assess_number: Optional[str]

    _normalize_used_first_name = validator(
        "used_first_name", allow_reuse=True, check_fields=False
    )(normalize)
    _normalize_used_last_name = validator(
        "used_last_name", allow_reuse=True, check_fields=False
    )(normalize)

    @property
    def user_id(self):
        dob = self.dob.strftime(("%Y-%m-%d"))
        return (
            self.last_name[0].upper()
            + self.first_name[0]
            + dob.split("-")[0]
            + dob.split("-")[1]
            + dob.split("-")[2]
        )

    @property
    def password(self):
        return "Super" + str(datetime.today().year) + "!"


class Education(EducationBase):
    city: Optional[str]
    country: Optional[str]
    is_trade: Optional[bool]


class Family(BaseModel):
    relationship: Optional[str]
    last_name: Optional[str]
    first_name: Optional[str]
    native_last_name: Optional[str]
    native_first_name: Optional[str]
    date_of_birth: Optional[date]
    date_of_death: Optional[date]
    place_of_birth: Optional[str]
    birth_country: Optional[str]
    marital_status: Optional[str]
    email: Optional[EmailStr]
    address: Optional[str]


class Bcpnp(BaseModel):
    # account:str
    # password:str #TODO: 根据person做出来。
    has_current_app: bool
    has_applied_before: bool
    pre_file_no: Optional[str]
    submission_date: Optional[date]
    case_stream: Optional[str]
    q1: bool
    q1_explaination: Optional[str]
    q2: bool
    q2_explaination: Optional[str]
    q3: bool
    q3_explaination: Optional[str]
    q4: bool
    q4_file_number: Optional[str]
    q4_explaination: Optional[str]
    q5: bool
    q5_explaination: Optional[str]
    q6: bool
    q6_explaination: Optional[str]
    q7: bool
    q7_explaination: Optional[str]


class BcpnpModel(CommonModel):
    personal: Personal
    # marriage: Marriage
    address: List[Address]
    phone: List[Phone]
    personid: List[PersonId]
    # family: List[Family]
    bcpnp: Bcpnp
    education: List[Education]
    employment: List[Employment]

    # initialize the model with a list of excels, which includes all nececcery information the model required. if outpuot_excel_file is not None, it will make an excel file.
    def __init__(self, excels=None, output_excel_file=None):
        if output_excel_file:
            import os

            path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), os.path.pardir)
            )
            excels = [
                path + "/template/excel/bcpnp.xlsx",
                path + "/template/excel/pa.xlsx",
            ]
        else:
            if excels is None and len(excels) == 0:
                raise ValueError(
                    "You must input excel file list as source data for validation"
                )
        super().__init__(excels, output_excel_file, globals())
