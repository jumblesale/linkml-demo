# linkml-demo

This repository contains a demonstration of generating a REST API from an abstract LinkML schema.

## Features

- Produces domain models, sql-alchemy entities, and read/write DTOs from the LinkML schema
- Supports POSTing a new entity, GETing an entity by ID, and GETing all entities
- Validates model invariants defined in the LinkML schema when creating entities
- Supports uniqueness constraints and responds with a 409 response if they are not unique

## Setup

- Install the dependencies from `uv`
- Run the app with `just run`
- Navigate to [http://127.0.0.1:8000/docs#/](http://127.0.0.1:8000/docs) to see the Swagger documentation


## Structure

- [schema/bookstore.md](schema/bookstore.md) - contains a natural language description of a fictional bookstore domain
- [schema/bookstore.yaml](schema/bookstore.yaml) - a LinkML schema produced from the markdown file
- [generate/](generate/) - a Python module containing scripts to generate the domain models, sqlalchemy entities and DTOs based on the LinkML schema
- [bookstore/](bookstore/) - a Python module containing the generated artifacts from the generate step
- [app/](app/) - a Python module containing the application consisting of a FastAPI instance, an EntityService and a EntityRepository