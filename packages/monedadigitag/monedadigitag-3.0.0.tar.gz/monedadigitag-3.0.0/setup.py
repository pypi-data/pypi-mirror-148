from setuptools import setup

with open('README.md') as f:
  readme = f.read().replace('```', '')

setup(
    name='monedadigitag',
    version='3.0.0',
    packages=['monedadigitag'],
    url='https://github.com/jvergnol/TSGemini',
    license='GNU GPL',
    author='Julien Vergnol',
    author_email='jvergnol@gmail.com',
    zip_safe=False,
    long_description=readme,
    description='API client for Gemini',
)
