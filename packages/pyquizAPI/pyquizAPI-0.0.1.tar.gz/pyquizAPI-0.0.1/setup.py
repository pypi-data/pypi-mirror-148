from setuptools import setup, find_packages
setup(
    name=  "pyquizAPI",
    version = "0.0.1",
    author="msherburne",
    license="MIT",
    description="API Client Wrapper for QuizAPI.io",
    packages= find_packages(include=['pyquizAPI','pyquizAPI.*']),
    install_requires=[
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8'
)