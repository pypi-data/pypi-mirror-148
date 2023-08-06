from setuptools import setup, Extension

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='ZabbixPyAPI',
    packages=['ZabbixPyAPI'],
    version='1.0',
    license='MIT',
    description='Simple zabbix api using python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Ewerton Henrique Marschalk',
    author_email='sis-ewertonmarschalk@uniguacu.edu.br',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/ewertonhm/ZabbixPyAPI',
    # I explain this later on
    download_url='https://github.com/ewertonhm/ZabbixPyAPI/archive/refs/tags/1.0.tar.gz',
    # Keywords that define your package best
    keywords=['ZABBIX', 'API'],
    install_requires=[            # I get to this in a second
        'requests'
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
