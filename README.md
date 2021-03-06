<img src="https://raw.githubusercontent.com/mikesaurio/refinadora_static/master/img/logo.png" alt="Refinadora" height="auto" width="200"/>
# Refinadora ([español](/LEEME.md))

Refinadora is a project that allows the analysis of data sets and the identification of possible structure, format or standard problems.

This is done through an API that allows the creation of asynchronous validations to consult their state either through the validator ID or defining the URL where to be notified when the validation is done.


## Install

Refinadora has 2 ways of installation, the first one is a Python package and the other as a container.

Either option you choose you need to clone the repo:

```console
git clone  git@github.com:civica-digital/refinadora.git
```

### Python package

We recommend the use of `virtualenvs` for the installation and specially if you want to contribute to the project.

```console
python setup.py install
```

### Additional

 We also provide `playbooks` and a `Vagrantafile` to create an test enviroment
Please consult the wiki

### Container

You need to install Docker, in Mac or Windows use `boot2docker` to build the container.

```console
docker build -t civicadigital/refinadora
```

## Use

If you choose the option of the Python package you can run an instance of the aplication with:

```console
python bin/run.py
```

If you choose Docker, you need to connect your temporary folder so we can share your datasets with the validators.

```console
docker run -v /tmp:/datasets -p 5000:5000 civicadigital/refinadora
```

## Demo
<img src="https://raw.githubusercontent.com/mikesaurio/refinadora_static/master/img/landing.png" alt="Civica-digital" height="auto" width="100%"/>

**We are setting up one for you, which will be available soon.**

## ¿FAQs?

You can follow the conversation for this project in our Github [issues](https://github.com/civica-digital/refinadora/issues), if you have any other questions you can contact us at equipo@civica.digital.

## Contribute

We want this project to be the result of a community effort, please contribute with code, debugs or ideas.

## Licence

Available under the license: GNU GPL License, Version 2.0. Read the document [LICENSE](./LICENSE) for more information.
