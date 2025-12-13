"""
General utility functions for Workday job application automation.
These functions work across different Workday implementations (NVIDIA, Expedia, etc.)
"""

from .utils import (
    clear_chip_in_container,
    clear_chip_field_by_input_id,
    clear_and_fill_input,
)

from .add_education import (
    click_add_education,
    click_add_another_education,
    fill_education,
)

from .add_skills import add_skills

from .add_url import (
    click_add_url,
    click_add_another_url,
    fill_url,
    add_urls,
)

from .add_work_experience import (
    click_add_work_experience,
    click_add_another_work_experience,
    fill_work_experience,
)

from .phone_number import fill_phone_number

from .save_and_continue import save_and_continue

from .upload_resume import open_job_application_url, upload_resume, apply_with_resume

__all__ = [
    # Utils
    "clear_chip_in_container",
    "clear_chip_field_by_input_id",
    "clear_and_fill_input",
    # Education
    "click_add_education",
    "click_add_another_education",
    "fill_education",
    # Skills
    "add_skills",
    # URLs
    "click_add_url",
    "click_add_another_url",
    "fill_url",
    "add_urls",
    # Work Experience
    "click_add_work_experience",
    "click_add_another_work_experience",
    "fill_work_experience",
    # Phone
    "fill_phone_number",
    # Save
    "save_and_continue",
    # Resume
    "open_job_application_url",
    "upload_resume",
    "apply_with_resume",
]
