# core/utils.py

import json
import re
import logging

# Configure logger
logger = logging.getLogger(__name__)

def escape_latex_special_chars(text):
    """
    Escapes special LaTeX characters in the provided text.

    Args:
        text (str): The text to escape.

    Returns:
        str: The escaped text.
    """
    if not text:
        return ""
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\^{}",
    }
    pattern = re.compile("|".join(re.escape(key) for key in replacements.keys()))
    return pattern.sub(lambda m: replacements[m.group()], text)


# core/utils.py


def format_user_education(education_queryset):
    """
    Formats the user's education data into a list suitable for inclusion in the prompt.

    Args:
        education_queryset (QuerySet): The queryset of Education objects.

    Returns:
        list: A list of formatted education dictionaries.
    """
    formatted_education = []
    for edu in education_queryset:
        edu_details = {
            "education_level": escape_latex_special_chars(edu.education_level),
            "university": escape_latex_special_chars(edu.university),
            "specialization": escape_latex_special_chars(edu.specialization or ""),
            "start_date": escape_latex_special_chars(
                edu.start_date.strftime("%B %Y") if edu.start_date else ""
            ),
            "end_date": escape_latex_special_chars(
                edu.end_date.strftime("%B %Y") if edu.end_date else "Present"
            ),
            "thesis": escape_latex_special_chars(edu.thesis or ""),
            "relevant_subjects": escape_latex_special_chars(
                edu.relevant_subjects or ""
            ),
        }
        formatted_education.append(edu_details)
    return formatted_education


# core/utils.py

def format_user_experience(experience_queryset):
    """
    Formats the user's experience data into a list suitable for inclusion in the prompt.

    Args:
        experience_queryset (QuerySet): The queryset of Experience objects.

    Returns:
        list: A list of formatted experience dictionaries.
    """
    formatted_experience = []
    for exp in experience_queryset:
        exp_details = {
            'company': escape_latex_special_chars(exp.company),
            'title': escape_latex_special_chars(exp.title),
            'city': escape_latex_special_chars(exp.city),
            'start_date': escape_latex_special_chars(
                exp.start_date.strftime('%B %Y') if exp.start_date else ''
            ),
            'end_date': escape_latex_special_chars(
                exp.end_date.strftime('%B %Y') if exp.end_date else 'Present'
            ),
            'description': [
                escape_latex_special_chars(detail)
                for detail in exp.description.split('\n') if detail
            ] if exp.description else [],
        }
        formatted_experience.append(exp_details)
    return formatted_experience

def format_user_list_field(field_data):
    """
    Escapes special LaTeX characters in a list of strings.

    Args:
        field_data (str or list): The data, either as a JSON string, comma-separated string, or list.

    Returns:
        list: A list of escaped strings.
    """
    if isinstance(field_data, str):
        # Try parsing as JSON
        try:
            field_list = json.loads(field_data)
        except json.JSONDecodeError:
            # Split by commas
            field_list = [item.strip() for item in field_data.split(",")]
    else:
        field_list = field_data or []

    return [escape_latex_special_chars(item) for item in field_list]


def user_info_to_prompt_format(user_info):
    """
    Formats the user_info dictionary into a JSON-formatted string for inclusion in the prompt.

    Args:
        user_info (dict): The user information.

    Returns:
        str: The formatted user information as a JSON string.
    """
    return json.dumps(user_info, indent=2)

def clean_latex(latex_escaped):
    """
    Cleans the LaTeX code by handling escaped newlines and ensuring proper backslashes.

    Parameters:
    - latex_escaped (str): The raw LaTeX string extracted from JSON.

    Returns:
    - str: The cleaned LaTeX string.
    """
    try:
        # Replace escaped newline characters with actual newlines
        latex_unescaped = latex_escaped.replace('\\n', '\n')
        logger.debug("Replaced '\\n' with actual newline characters.")

        # At this point, backslashes are correctly represented as single backslashes
        # If there are double backslashes intended for LaTeX (e.g., line breaks), they should remain as is

        return latex_unescaped

    except Exception as e:
        logger.error(f"Unexpected error during LaTeX cleaning: {e}")
        raise


from pydantic import BaseModel

class LatexOutput(BaseModel):
    latex_code: str

