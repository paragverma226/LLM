from setuptools import find_packages, setup
from typing import List


def load_requirements() -> List[str]:
    """
    Load project dependencies from requirements.txt,
    excluding editable installs.
    """
    try:
        with open("requirements.txt", "r") as req_file:
            requirements = [
                line.strip()
                for line in req_file.readlines()
                if line.strip() and line.strip() != "-e ."
            ]
        return requirements
    except FileNotFoundError:
        print("⚠️ 'requirements.txt' not found. Please ensure it exists in the project root.")
        return []


setup(
    name="smart-health-assistant",
    version="0.0.1",
    author="Parag Verma",
    author_email="paragverma226@gmail.com",
    packages=find_packages(),
    install_requires=load_requirements(),
    python_requires=">=3.10",
)
