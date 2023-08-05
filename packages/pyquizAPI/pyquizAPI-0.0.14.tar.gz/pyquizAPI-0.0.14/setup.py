from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme:
    description = readme.read()

setup(
    name=  "pyquizAPI",
    version = "0.0.14",
    author="Mathieu Sherburne",
    license="MIT",
    description="API Client Wrapper for QuizAPI.io",
    long_description=description,
    long_description_content_type="text/markdown",
    packages= find_packages(include=['pyquizAPI', 'pyquizAPI.*']),
    install_requires=[
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    url="https://github.com/msherburne/pyquizAPI"
)