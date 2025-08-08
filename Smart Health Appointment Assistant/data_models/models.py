import re
from pydantic import BaseModel, Field, field_validator


class AppointmentDateTime(BaseModel):
    """
    Validates date and time in 'DD-MM-YYYY HH:MM' format.
    Example: '05-08-2024 14:30'
    """
    datetime_str: str = Field(
        description="Date and time in 'DD-MM-YYYY HH:MM' format",
        pattern=r'^\d{2}-\d{2}-\d{4} \d{2}:\d{2}$'
    )

    @field_validator("datetime_str")
    def validate_datetime_format(cls, value: str) -> str:
        if not re.match(r'^\d{2}-\d{2}-\d{4} \d{2}:\d{2}$', value):
            raise ValueError("Datetime must be in format 'DD-MM-YYYY HH:MM'")
        return value


class AppointmentDate(BaseModel):
    """
    Validates date in 'DD-MM-YYYY' format.
    Example: '05-08-2024'
    """
    date_str: str = Field(
        description="Date in 'DD-MM-YYYY' format",
        pattern=r'^\d{2}-\d{2}-\d{4}$'
    )

    @field_validator("date_str")
    def validate_date_format(cls, value: str) -> str:
        if not re.match(r'^\d{2}-\d{2}-\d{4}$', value):
            raise ValueError("Date must be in format 'DD-MM-YYYY'")
        return value


class PatientID(BaseModel):
    """
    Validates patient ID as a 7 or 8-digit numeric identifier.
    Example: 1000097
    """
    id_number: int = Field(description="7 or 8-digit patient ID number")

    @field_validator("id_number")
    def validate_id_format(cls, value: int) -> int:
        if not re.match(r'^\d{7,8}$', str(value)):
            raise ValueError("ID number must be a 7 or 8-digit numeric value")
        return value



