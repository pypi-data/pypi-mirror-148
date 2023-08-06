from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="libtesthello",
    version="0.0.3",
    author="fr",
    author_email='testsayhellofr@gmail.com',
    description='Biblioteca que diz Hello',
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/faustoroger/dio-desafio-github-primeiro-repositorio/tree/main/Python/Desafios/03-Desafios.Descomplicando.a.Cria%C3%A7%C3%A3o.de.Pacotes/libtesthello",
    packages=find_packages(),
    install_requires=requirements,
    license='MIT'
)
