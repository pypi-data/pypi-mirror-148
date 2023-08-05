from setuptools import setup

with open("README.md", 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='cpf_tools',
    version='1.5.1',
    author='Bruno Nascimento',
    author_email='bruno-asn@outlook.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['cpf_tools'],
    url='https://github.com/BrunoASNascimento/cpf_tools',
    project_urls={
        'Código fonte': 'https://github.com/BrunoASNascimento/cpf_tools',
        'Download': 'https://github.com/BrunoASNascimento/cpf_tools/archive/master.zip'
    },
    license='MIT',
    keywords=['format', 'cpf', 'validation'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Internationalization'
    ],
    python_requires='>=3.6'
)
