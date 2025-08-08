import pandas as pd
from typing import Literal
from langchain_core.tools import tool
from data_models.models import DateModel, DateTimeModel, IdentificationNumberModel
from datetime import datetime

CSV_FILE = "../data/doctor_availability.csv"
OUTPUT_CSV_FILE = "availability.csv"


@tool
def check_availability_by_doctor(
    desired_date: DateModel,
    doctor_name: Literal[
        'kevin anderson', 'robert martinez', 'susan davis', 'daniel miller',
        'sarah wilson', 'michael green', 'lisa brown', 'jane smith',
        'emily johnson', 'john doe'
    ]
):
    """
    Check availability for a specific doctor on a given date.
    """
    df = pd.read_csv(CSV_FILE)
    df['date_slot_time'] = df['date_slot'].apply(lambda x: x.split(' ')[-1])
    
    available_slots = df[
        (df['date_slot'].str.split(' ').str[0] == desired_date.date) &
        (df['doctor_name'] == doctor_name) &
        (df['is_available'] == True)
    ]['date_slot_time'].tolist()
    
    if not available_slots:
        return "No availability in the entire day"
    
    return (
        f"Doctor availability for {desired_date.date}\n"
        f"Available slots: {', '.join(available_slots)}"
    )


@tool
def check_availability_by_specialization(
    desired_date: DateModel,
    specialization: Literal[
        "general_dentist", "cosmetic_dentist", "prosthodontist",
        "pediatric_dentist", "emergency_dentist", "oral_surgeon", "orthodontist"
    ]
):
    """
    Check availability for doctors by specialization on a given date.
    """
    df = pd.read_csv(CSV_FILE)
    df['date_slot_time'] = df['date_slot'].apply(lambda x: x.split(' ')[-1])

    filtered = df[
        (df['date_slot'].str.split(' ').str[0] == desired_date.date) &
        (df['specialization'] == specialization) &
        (df['is_available'] == True)
    ]
    
    grouped = filtered.groupby(['specialization', 'doctor_name'])['date_slot_time'].apply(list).reset_index(name='available_slots')
    
    if grouped.empty:
        return "No availability in the entire day"
    
    def convert_to_am_pm(time_str: str) -> str:
        hours, minutes = map(int, str(time_str).split(":"))
        period = "AM" if hours < 12 else "PM"
        hours = hours % 12 or 12
        return f"{hours}:{minutes:02d} {period}"
    
    output = f"Doctor availability for {desired_date.date}\n"
    for _, doctor, slots in grouped.itertuples(index=False):
        slot_str = ', \n'.join([convert_to_am_pm(slot) for slot in slots])
        output += f"{doctor}. Available slots:\n{slot_str}\n"
    
    return output


@tool
def set_appointment(
    desired_date: DateTimeModel,
    id_number: IdentificationNumberModel,
    doctor_name: Literal[
        'kevin anderson', 'robert martinez', 'susan davis', 'daniel miller',
        'sarah wilson', 'michael green', 'lisa brown', 'jane smith',
        'emily johnson', 'john doe'
    ]
):
    """
    Set an appointment for a patient with a doctor at a specific datetime.
    """
    df = pd.read_csv(CSV_FILE)
    
    def convert_datetime_format(dt_str: str) -> str:
        dt = datetime.strptime(dt_str, "%d-%m-%Y %H:%M")
        return dt.strftime("%d-%m-%Y %#H.%M")  # Windows-specific, use %-H on Linux/macOS
    
    formatted_dt = convert_datetime_format(desired_date.date)
    
    match = df[
        (df['date_slot'] == formatted_dt) &
        (df['doctor_name'] == doctor_name) &
        (df['is_available'] == True)
    ]
    
    if match.empty:
        return "No available appointments for that particular case"
    
    df.loc[
        (df['date_slot'] == formatted_dt) &
        (df['doctor_name'] == doctor_name),
        ['is_available', 'patient_to_attend']
    ] = [False, id_number.id]
    
    df.to_csv(OUTPUT_CSV_FILE, index=False)
    return "Appointment successfully set"


@tool
def cancel_appointment(
    date: DateTimeModel,
    id_number: IdentificationNumberModel,
    doctor_name: Literal[
        'kevin anderson', 'robert martinez', 'susan davis', 'daniel miller',
        'sarah wilson', 'michael green', 'lisa brown', 'jane smith',
        'emily johnson', 'john doe'
    ]
):
    """
    Cancel an existing appointment.
    """
    df = pd.read_csv(CSV_FILE)
    
    match = df[
        (df['date_slot'] == date.date) &
        (df['patient_to_attend'] == id_number.id) &
        (df['doctor_name'] == doctor_name)
    ]
    
    if match.empty:
        return "You don’t have any appointment matching those specifications"
    
    df.loc[
        (df['date_slot'] == date.date) &
        (df['patient_to_attend'] == id_number.id) &
        (df['doctor_name'] == doctor_name),
        ['is_available', 'patient_to_attend']
    ] = [True, None]
    
    df.to_csv(OUTPUT_CSV_FILE, index=False)
    return "Appointment successfully cancelled"


@tool
def reschedule_appointment(
    old_date: DateTimeModel,
    new_date: DateTimeModel,
    id_number: IdentificationNumberModel,
    doctor_name: Literal[
        'kevin anderson', 'robert martinez', 'susan davis', 'daniel miller',
        'sarah wilson', 'michael green', 'lisa brown', 'jane smith',
        'emily johnson', 'john doe'
    ]
):
    """
    Reschedule an existing appointment to a new datetime.
    """
    df = pd.read_csv(CSV_FILE)
    
    available = df[
        (df['date_slot'] == new_date.date) &
        (df['is_available'] == True) &
        (df['doctor_name'] == doctor_name)
    ]
    
    if available.empty:
        return "No available slots at the desired time"
    
    cancel_appointment.invoke({
        'date': old_date,
        'id_number': id_number,
        'doctor_name': doctor_name
    })
    
    set_appointment.invoke({
        'desired_date': new_date,
        'id_number': id_number,
        'doctor_name': doctor_name
    })
    
    return "Appointment successfully rescheduled"
