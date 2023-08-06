# python-template

<div align="center">

[![Build status](https://github.com/ingwersen-erik/python-template/workflows/build/badge.svg?branch=master&event=push)](https://github.com/ingwersen-erik/python-template/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/python-template.svg)](https://pypi.org/project/python-template/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/ingwersen-erik/python-template/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/ingwersen-erik/python-template/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/ingwersen-erik/python-template/releases)
[![License](https://img.shields.io/github/license/ingwersen-erik/python-template)](https://github.com/ingwersen-erik/python-template/blob/master/LICENSE)
![Coverage Report](assets/images/coverage.svg)

Repositório template para criação de projetos em Python.

</div>

## Primeiros Passos

### Inicializando o repositório

1. Comece configurando a ferramenta de versionamento de código (VCS).
   Para inicializar um repositório, utilizando o [GitHub](https://github.com),
   execute o comando `git`, na linha de comando:

```bash
cd python-template && git init
```

**Onde:**

- `cd`: comando é a abreviação de "change directory". Você pode usar esse comando para mudar
  o diretório da linha de comando.
- `git init`: inicializa um novo repositório no [GitHub](https://github.com).
  Vale ressaltar que este comando apenas cria os arquivos necessários para inicializar o repositório, mas não 
  realiza upload dos arquivos para o [GitHub](https://github.com). De certo modo, estamos apenas **"preparando o terreno"** neste momento.
- `&&`: permite a execução de mais de um comando, de uma só vez. No caso acima, mudamos o diretório do nosso 
  terminal e criamos os arquivos que o [GitHub](https://github.com) precisa.

2. Em seguida, instale o [Poetry](https://tinyurl.com/python-poetry-docs), 
   executando o seguinte comando:

Ignorar esta etapa, caso você já tenha o [Poetry](https://tinyurl.com/python-poetry-docs)
instalado na sua maquina.

```bash
make poetry-download
```

> Nunca ouviu falar do [Poetry](https://tinyurl.com/python-poetry-docs)? 
> Clique [aqui](LINK) para uma breve contextualização.

3. Depois de instalar o Poetry, execute o comando abaixo, para instalar as dependências 
   necessárias do pacote:Initialize poetry and install 
   `pre-commit` hooks:

```bash
make install

```

**Opcional:** você também pode habilitar uma feature chamada `pre-commit` hooks, executando o seguinte comando:

```bash
make pre-commit-install
```

`pre-commit` hooks são basicamente verificações, que são executadas automaticamente, toda vez que você realiza um 
commit no seu repositório. Essas verificações variam desde formatar o código fonte, usando ferramentas, como o 
[Black](https://tinyurl.com/black-psf), até execuções de testes unitários. Estes hooks são normalmente utilizados,
de modo que o commit só é realizado, quando o seu código passa por todas as verificações sem erros. **Caso você não 
tenha muita familiaridade com ferramentas, como [MyPy](https://mypy.readthedocs.io/en/stable/getting_started.html),
[Pytest](https://pytest.org), [Isort](https://pycqa.github.io/isort/) e [Black](https://tinyurl.com/black-psf), 
recomendo que não habilite essa opção.**

4. Executando codestyle:

O comando a seguir formatando o seu código fonte, conforme as configurações especificadas dentro do arquivo
[pyproject.toml](pyproject.toml).

```bash
make codestyle
```

5. Fazendo upload do repositório para o [GitHub](https://github.com):

```bash
git add .
git commit -m ":tada: Initial commit"
git branch -M main
git remote add origin https://github.com/ingwersen-erik/python-template.git
git push -u origin main
```

Os comandos acima realizam as seguintes operações:

- `git add .`: Adiciona quaisquer arquivos que você tenha criado/adicionado na pasta do repositório,
  para serem enviados para o repositório no GitHub.
- `git commit -m ":tada: Initial commit"`: cria o commit destes arquivos adicionados. Basicamente, um commit
  especifica as mudanças que pretendemos subir no repositório. A flag `-m` é utilizada para especificar a mensagem
  do commit e, é obrigatória. Caso você não especifique uma mensagem, o commit nao será feito.
- `git branch -M main`: cria a branch que iremos utilizar para subir os arquivos. Como estamos criando agora o 
  repositório e, subindo os arquivos do projeto pela primeira vez, estamos criando/utilizando a branch "padrão",
  que é a branch "main" (alguns projetos preferem utilizar o nome "master", ao invés de "main", muito embora não seja 
  o mais usual).
- `git remote add origin https://github.com/ingwersen-erik/python-template.git`: esse comando especifica a URL do 
  repositório no Github.
- `git push -u origin main`: realiza o upload dos arquivos especificados pelo comando `git add .`, utilizando o commit
  que criamos utilizando o segundo comando (`git commit -m ":tada: Initial commit"`).

### (Opcional) Configurando os bots

Acesse os links abaixo, para instruções de como habilitar o **GitHub Dependabot** e o **Stale bot**.

- Set up [Dependabot](https://docs.github.com/en/github/administering-a-repository/enabling-and-disabling-version-updates#enabling-github-dependabot-version-updates) verifica as dependências do seu projeto e, sugere a 
  atualização de pacotes identificados que possuem algum problema de segurança.
- Set up [Stale bot](https://github.com/apps/stale) realiza o fechamento automático de GitHub issues estagnados.

### Poetry

Want to know more about Poetry? Check [its documentation](https://python-poetry.org/docs/).

<details>
<summary>Details about Poetry</summary>
<p>

Poetry's [commands](https://python-poetry.org/docs/cli/#commands) are very intuitive and easy to learn, like:

- `poetry add numpy@latest`
- `poetry run pytest`
- `poetry publish --build`

etc
</p>
</details>

### Building and releasing your package

Building a new version of the application contains steps:

- Bump the version of your package `poetry version <version>`.
  You can pass the new version explicitly, or a rule such as `major`, `minor`, or `patch`.
  For more details, refer to the [Semantic Versions](https://semver.org/) standard.
- Make a commit to `GitHub`.
- Create a `GitHub release`.
- And... publish 🙂 `poetry publish --build`

## 🎯 What's next

### Packages and Articles

Helpful packages and articles:

- [`Typer`](https://github.com/tiangolo/typer) is great for creating CLI applications.
- [`Rich`](https://github.com/willmcgugan/rich) makes it easy to add beautiful formatting in the terminal.
- [`Pydantic`](https://github.com/samuelcolvin/pydantic/) – data validation and settings management using Python type hinting.
- [`Loguru`](https://github.com/Delgan/loguru) makes logging (stupidly) simple.
- [`tqdm`](https://github.com/tqdm/tqdm) – fast, extensible progress bar for Python and CLI.
- [`IceCream`](https://github.com/gruns/icecream) is a little library for sweet and creamy debugging.
- [`orjson`](https://github.com/ijl/orjson) – ultra fast JSON parsing library.
- [`Returns`](https://github.com/dry-python/returns) makes you function's output meaningful, typed, and safe!
- [`Hydra`](https://github.com/facebookresearch/hydra) is a framework for elegantly configuring complex applications.
- [`FastAPI`](https://github.com/tiangolo/fastapi) is a type-driven asynchronous web framework.

### Artigos:

- [Open Source Guides](https://opensource.guide/).
- [A handy guide to financial support for open source](https://github.com/nayafia/lemonade-stand)
- [GitHub Actions Documentation](https://help.github.com/en/actions).
- Maybe you would like to add [gitmoji](https://gitmoji.carloscuesta.me/) to commit names. This is really funny. 😄

## 🚀 Features

### Development features

- Supports for `Python 3.9` and higher.
- [`Poetry`](https://python-poetry.org/) as the dependencies manager. See configuration in [`pyproject.toml`](https://github.com/ingwersen-erik/python-template/blob/master/pyproject.toml) and [`setup.cfg`](https://github.com/ingwersen-erik/python-template/blob/master/setup.cfg).
- Automatic codestyle with [`black`](https://github.com/psf/black), [`isort`](https://github.com/timothycrosley/isort) and [`pyupgrade`](https://github.com/asottile/pyupgrade).
- Ready-to-use [`pre-commit`](https://pre-commit.com/) hooks with code-formatting.
- Type checks with [`mypy`](https://mypy.readthedocs.io); docstring checks with [`darglint`](https://github.com/terrencepreilly/darglint); security checks with [`safety`](https://github.com/pyupio/safety) and [`bandit`](https://github.com/PyCQA/bandit)
- Testing with [`pytest`](https://docs.pytest.org/en/latest/).
- Ready-to-use [`.editorconfig`](https://github.com/ingwersen-erik/python-template/blob/master/.editorconfig), [`.dockerignore`](https://github.com/ingwersen-erik/python-template/blob/master/.dockerignore), and [`.gitignore`](https://github.com/ingwersen-erik/python-template/blob/master/.gitignore). You don't have to worry about those things.

### Deployment features

- `GitHub` integration: issue and pr templates.
- `Github Actions` with predefined [build workflow](https://github.com/ingwersen-erik/python-template/blob/master/.github/workflows/build.yml) as the default CI/CD.
- Everything is already set up for security checks, codestyle checks, code formatting, testing, linting, docker builds, etc with [`Makefile`](https://github.com/ingwersen-erik/python-template/blob/master/Makefile#L89). More details in [makefile-usage](#makefile-usage).
- [Dockerfile](https://github.com/ingwersen-erik/python-template/blob/master/docker/Dockerfile) for your package.
- Always up-to-date dependencies with [`@dependabot`](https://dependabot.com/). You will only [enable it](https://docs.github.com/en/github/administering-a-repository/enabling-and-disabling-version-updates#enabling-github-dependabot-version-updates).
- Automatic drafts of new releases with [`Release Drafter`](https://github.com/marketplace/actions/release-drafter). You may see the list of labels in [`release-drafter.yml`](https://github.com/ingwersen-erik/python-template/blob/master/.github/release-drafter.yml). Works perfectly with [Semantic Versions](https://semver.org/) specification.

### Open source community features

- Ready-to-use [Pull Requests templates](https://github.com/ingwersen-erik/python-template/blob/master/.github/PULL_REQUEST_TEMPLATE.md) and several [Issue templates](https://github.com/ingwersen-erik/python-template/tree/master/.github/ISSUE_TEMPLATE).
- Files such as: `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and `SECURITY.md` are generated automatically.
- [`Stale bot`](https://github.com/apps/stale) that closes abandoned issues after a period of inactivity. (You will only [need to setup free plan](https://github.com/marketplace/stale)). Configuration is [here](https://github.com/ingwersen-erik/python-template/blob/master/.github/.stale.yml).
- [Semantic Versions](https://semver.org/) specification with [`Release Drafter`](https://github.com/marketplace/actions/release-drafter).

## Installation

```bash
pip install -U python-template
```

or install with `Poetry`

```bash
poetry add python-template
```


### Makefile usage

[`Makefile`](https://github.com/ingwersen-erik/python-template/blob/master/Makefile)
contains a lot of functions for faster development.

<details>
<summary>1. Download and remove Poetry</summary>
<p>

To download and install Poetry run:

```bash
make poetry-download
```

To uninstall

```bash
make poetry-remove
```

</p>
</details>

<details>
<summary>2. Install all dependencies and pre-commit hooks</summary>
<p>

Install requirements:

```bash
make install
```

Pre-commit hooks could be installed after `git init` via:

```bash
make pre-commit-install
```

</p>
</details>

<details>
<summary>3. Codestyle</summary>
<p>

Automatic formatting uses `pyupgrade`, `isort` and `black`.

```bash
make codestyle

# ou use o sinônimo do comando acima
make formatting
```

Codestyle checks only, without rewriting files:

```bash
make check-codestyle
```

> Observação: `check-codestyle` utiliza as seguintes ferramentas: `isort`, `black` e `darglint`.

Executando o próximo comando, o Poetry atualiza as dependência do seu projeto,
buscando a versão mais atualizada de cada biblioteca, caso não existam erros de 
compatibilidade entre os requerimentos de cada biblioteca.

```bash
make update-dev-deps
```

<details>
<summary>4. Code security</summary>
<p>

```bash
make check-safety
```

This command launches `Poetry` integrity checks as well as identifies security issues with `Safety` and `Bandit`.

```bash
make check-safety
```

</p>
</details>

</details>

<details>
<summary>5. Type checks</summary>
<p>

Run `mypy` static type checker

```bash
make mypy
```

</p>
</details>

<details>
<summary>6. Tests with coverage badges</summary>
<p>

Run `pytest`

```bash
make test
```

</p>
</details>

<details>
<summary>7. All linters</summary>
<p>

Of course there is a command to ~~rule~~ run all linters in one:

```bash
make lint
```

the same as:

```bash
make test && make check-codestyle && make mypy && make check-safety
```

</p>
</details>

<details>
<summary>8. Docker</summary>
<p>

```bash
make docker-build
```

which is equivalent to:

```bash
make docker-build VERSION=latest
```

Remove docker image with

```bash
make docker-remove
```

More information [about docker](https://github.com/ingwersen-erik/python-template/tree/master/docker).

</p>
</details>

<details>
<summary>9. Cleanup</summary>
<p>
Delete pycache files

```bash
make pycache-remove
```

Remove package build

```bash
make build-remove
```

Delete .DS_STORE files

```bash
make dsstore-remove
```

Remove .mypycache

```bash
make mypycache-remove
```

Or to remove all above run:

```bash
make cleanup
```

</p>
</details>

## 📈 Releases

You can see the list of available releases on the [GitHub Releases](https://github.com/ingwersen-erik/python-template/releases) page.

We follow [Semantic Versions](https://semver.org/) specification.

We use [`Release Drafter`](https://github.com/marketplace/actions/release-drafter). As pull requests are merged, a draft release is kept up-to-date listing the changes, ready to publish when you’re ready. With the categories option, you can categorize pull requests in release notes using labels.

### List of labels and corresponding titles

|               **Label**               |  **Title in Releases**  |
|:-------------------------------------:|:-----------------------:|
|       `enhancement`, `feature`        |       🚀 Features       |
| `bug`, `refactoring`, `bugfix`, `fix` | 🔧 Fixes & Refactoring  |
|       `build`, `ci`, `testing`        | 📦 Build System & CI/CD |
|              `breaking`               |   💥 Breaking Changes   |
|            `documentation`            |    📝 Documentation     |
|            `dependencies`             | ⬆️ Dependencies updates |

You can update it in [`release-drafter.yml`](https://github.com/ingwersen-erik/python-template/blob/master/.github/release-drafter.yml).

GitHub creates the `bug`, `enhancement`, and `documentation` labels for you. Dependabot creates the `dependencies` label. Create the remaining labels on the Issues tab of your GitHub repository, when you need them.

## 🛡 License

[![License](https://img.shields.io/github/license/ingwersen-erik/python-template)](https://github.com/ingwersen-erik/python-template/blob/master/LICENSE)

This project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/ingwersen-erik/python-template/blob/master/LICENSE) for more details.

## 📃 Citation

```bibtex
@misc{python-template,
  author = {ingwersen-erik},
  title = {Repositorio template para criacao de projetos em Python.},
  year = {2022},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/ingwersen-erik/python-template}}
}
```

