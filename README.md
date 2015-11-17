# Gisela
<img src="https://github.com/toirl/gisela/blob/master/gisela.png" width="100" border="0">

Gisela is a simple time tracking and tagging service. Gisela provides a REST api which allows creating, and modifying timelogs and tags.
Gisela is meant to be used as microservice.

## License
Gisela is licensed under the [MIT license](https://github.com/toirl/gisela/blob/master/LICENSE)

## Source
Gisela is available via github: https://github.com/toirl/gisela

## Status
Gisela is currently in Alpha status. Contribution on the project is very welcome!

[![Build Status](https://travis-ci.org/toirl/gisela.svg?branch=master)](https://travis-ci.org/toirl/gisela)

## Service
### Tags
List all available tags:

    curl -i -H "Accept: application/json"  -X GET \
    "http://localhost:8080/tags"
    {"status": "success", "data": [{"description": "Foo Description", "id": 1, "name": "Foo"}, ...]}
    
Create a new tag:

    curl -i -H "Accept: application/json" -X POST \
    -d "name=Quey&description=Quex Description" \
    "http://localhost:8080/tags"
    {"status": "success", "data": {"description": "Quex Description", "id": 4, "name": "Quey"}}
    
Get a specific tag:

    curl -i -H "Accept: application/json" -X GET \
    "http://localhost:8080/tags/1"
    {"status": "success", "data": {"description": "Foo Description", "id": 1, "name": "Foo"}}
    
Update a specific tag:

    curl -i -H "Accept: application/json" -X PUT \
    -d "name=Foo2" \
    "http://localhost:8080/tags/1"
    {"status": "success", "data": {"description": "Foo Description", "id": 1, "name": "Foo2"}}

    
Delete a speficic tag:

    curl -i -H "Accept: application/json" -X DELETE \
    "http://localhost:8080/tags/1"
    {"status": "success", "data": null}
