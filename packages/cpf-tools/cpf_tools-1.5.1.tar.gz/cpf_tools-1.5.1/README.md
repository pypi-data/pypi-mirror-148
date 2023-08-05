# cpf_tools

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg?style=flat-square)](https://www.python.org/)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/BrunoASNascimento/cpf_tools/Run%20Python%20Tests?style=flat-square)](https://github.com/BrunoASNascimento/cpf_tools/actions/workflows/python-app.yml)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/BrunoASNascimento/cpf_tools.svg?logo=lgtm&logoWidth=18&style=flat-square)](https://lgtm.com/projects/g/BrunoASNascimento/cpf_tools/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/BrunoASNascimento/cpf_tools.svg?logo=lgtm&logoWidth=18&style=flat-square)](https://lgtm.com/projects/g/BrunoASNascimento/cpf_tools/context:python)
[![PyPi](https://anaconda.org/brunoasnascimento/cpf-tools/badges/installer/PyPi.svg?style=flat-square)](https://pypi.org/project/cpf-tools/)
[![Anaconda](https://anaconda.org/brunoasnascimento/cpf-tools/badges/installer/Anaconda.svg?style=flat-square)](https://anaconda.org/BrunoASNascimento/cpf-tools)

Biblioteca com ferramentas para auxiliar na checagem, formatação etc. de CPFs.

## Instalação:

` $ pip install cpf-tools`

## Funções:

- _cpf-tools.**cpf_int_validation**(cpf: int) -> bool_:

Essa função recebe um valor inteiro e verifica se o digito verificador do CPF é verdadeiro (True) ou falso (False).

- _cpf-tools.**cpf_str_validation**(cpf: str) -> bool_:

Essa função recebe um valor string e verifica se o digito verificador do CPF é verdadeiro (True) ou falso (False).

- _cpf-tools.**cpf_format**(cpf: Union[int, str, float]) -> str_:

Essa função recebe um valor integer, string ou float de um CPF e retorna uma string formatada.
(Exemplo: "00000000000" -> "000.000.000-00")

## Usando com Pandas:

Para utilizar com a biblioteca Pandas, utilize o seguinte comando:

`df['your-cpf-field'].apply(cpf-tools.cpf_int_validation)` ou

`df['your-cpf-field'].apply(cpf-tools.cpf_str_validation)` ou

`df['your-cpf-field'].apply(cpf-tools.cpf_format)`
