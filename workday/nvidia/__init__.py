"""NVIDIA Workday job application automation package."""

from .nvidia import nvidia_application_workflow
from .upload_resume import upload_resume
from .personal_info import fill_personal_info
from .how_you_heard import how_you_heard_about_us
from .phone_number import fill_phone_number
from .save_and_continue import save_and_continue
from .add_work_experience import click_add_work_experience, click_add_another_work_experience, fill_work_experience
from .add_education import click_add_education, click_add_another_education, fill_education
from .add_url import add_urls

__all__ = [
    "nvidia_application_workflow",
    "upload_resume",
    "fill_personal_info",
    "how_you_heard_about_us",
    "fill_phone_number",
    "save_and_continue",
    "click_add_work_experience",
    "click_add_another_work_experience",
    "fill_work_experience",
    "click_add_education",
    "click_add_another_education",
    "fill_education",
    "add_urls",
]
