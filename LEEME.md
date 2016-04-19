<img src="https://raw.githubusercontent.com/mikesaurio/refinadora_static/master/img/logo.png" alt="Refinadora" height="auto" width="200"/>
# Refinadora ([english](/README.md))

La refinadora es un proyecto que permite el análisis de recursos de datos y la identificaciones de posibles problemas de estructura, formato o estandarización.
Todo esto a través de un API que permiten crear validaciones asíncronas y consultar su estado ya sea por medio del identificador de la validación o definiendo URL a donde será notificado cuando termine la validaciones.


## Instalación

La refinadora tiene dos formas de instalación, una es como un paquete normal de Python y la otra como contenedor.

En cualquier opción que desees seguir, necesitaras clonar el repositorio:

```console
git clone  git@github.com:civica-digital/refinadora.git
```

### Paquete de Python

Se recomienda el uso de `virtualenvs` para la instalación y en especial si se desea contribuir al proyecto.

```console
python setup.py install
```

### Adicional

 También proveemos `playbooks` y un `Vagrantafile` para crear un ambiente de pruebas.
 Consultalo en la wiki.

### Contenedor

Necesitaras instalar Docker, en el caso de Mac o Windows hacer uso de `boot2docker` para poder construir el contenedor.

```console
docker build -t civicadigital/refinadora
```

## Uso

Si has elegido la opción del paquete de Python puedes levantar una instancia de la aplicación con:

```console
python bin/run.py
```

Pero si tu opción fue Docker, necesitas enlazar tu carpeta temporal a manera que podemos compartir los datasets entre los validadores.

```console
docker run -v /tmp:/datasets -p 5000:5000 civicadigital/refinadora
```

## Demo
<img src="https://raw.githubusercontent.com/mikesaurio/refinadora_static/master/img/landing.png" alt="Civica-digital" height="auto" width="100%"/>

**Estamos preparando un sitio para pruebas, esperalo proximamente.**

## ¿Preguntas o problemas?

Mantenemos la conversación del proyecto en nuestra página de problemas [issues](https://github.com/civica-digital/refinadora/issues). Si usted tiene cualquier otra pregunta, nos puede contactar por correo a equipo@civica.digital.

## Contribuye

Queremos que este proyecto sea el resultado de un esfuerzo de la comunidad. Usted puede colaborar con código, ideas y bugs.

## Licencia

Available under the license: GNU GPL License, Version 2.0. Read the document [LICENSE](./LICENSE) for more information.
