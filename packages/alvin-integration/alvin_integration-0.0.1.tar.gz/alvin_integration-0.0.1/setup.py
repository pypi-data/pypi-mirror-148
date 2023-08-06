import setuptools

requirements = [
    "gorilla==0.4.0",
    "openlineage-airflow==0.6.1"
]

setuptools.setup(
    name="alvin_integration",
    version="0.0.1",
    author="Alvin",
    author_email="tech@alvin.ai",
    description="Alvin lineage python library for integrations",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    python_requires=">=3.7",
)
