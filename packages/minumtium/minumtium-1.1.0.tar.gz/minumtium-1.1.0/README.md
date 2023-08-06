# Minumtium

A minimal blogging library.

### What can I use it for?

The purpose of _minumtium_ is to be embedded inside simple projects like landing pages or personal portfolio pages where
it is not needed to have a lot of features. The objective is to:

- Provide a simple way to add and list posts inside a page
- Provide a summary of the most recent posts
- Provide (very) basic user management

It is not meant to provide a full-fledged blogging platform. Features like comments, profiles, view counters,
social-network integrations and even configuration files are **out of scope**.

## Why minimal?

The idea behind _minumtium_ is that it should do the bare minimum: provide you the code to create posts, as well as
provide a way to control who can post. That's it:

- There are no user profiles, it accepts whatever value you pass as an author
- There is no UI, you have to create your own or use a library that provides it
- There are no endpoints, but there are implementations for fastapi

It is just a library that creates and lists blog posts, you can add other features by using external libraries, like
building lego (a very minimal lego, though).

## Why embedable?

_Minumtium_ has been created so that it can be a library inside a bigger project. By default, it won't even provide you
a UI or even REST API endpoints. The user should encapsulate _minumtium_ inside its own code and integrate it inside its
project. It is expected that you implement your own authentication adapters to allow it to integrate to your auth system
and so on.

## Why extensible?

Being so bare minimal would mean that _minumtium_ is almost useless, as it is quite simple to implement its core
functionality. _Minumtium_ has been built from ground up to be extensible with custom adapters and extension libraries.
Those can:

- Provide you alternative authentication methods
- Provide integration with different databases
- Provide you API endpoints using libraries like Flask or FastAPI
- Provide you Front-End endpoints using Jinja or Mako rendering

# Usage

Install it using pip, or you favorite _venv_ manager:

```commandline
# Using pip
pip install minumtium
```

```commandline
# Using pipenv
pipenv install minumtium
```

```commandline
# Using poetry
poetry install minumtium
```

Always interact with the service by providing its dependencies:

```python
from modules.posts import PostRepository, PostService
from minumtium.infra.implementations.sqlalchemy_database import SqlAlchemyAdapter

db_adapter = SqlAlchemyAdapter({'engine': 'sqlite_memory'}, 'posts')
post_repository = PostRepository(db_adapter)
post_service = PostService(post_repository)

summary = post_service.get_latest_posts_summary(count=10)
```

# Extensions and Adapters

You may not want to write a bunch of code, and for that reason you will very likely want to use plugins. Here are some
of the standard plugins:

- [FastAPI REST API]() - REST Endpoints using FaskAPI. Includes authenticated endpoints.
- [Simple JWT Authentication Adapter]() - Allows to authenticate _minumtium_ using simple JWT tokens
- [SqlAlchemy Database Adapter]() - Stores data using relational databases and _SqlAlchemy_

You can refer to their repositories for more information on how to use them.

# Integrating with other things

There are two things you will want to integrate:

- The `posts` service at `minumtium.modules.posts.PostService`
- The `idm` service at `minumtium.modules.idm.IdmService`

Integrating those services mean you will need to inject a few dependencies into them:

- The `posts` service depends on the `PostRepository`.
- The `PostRepository` depends on a `DatabaseAdapter` implementation.

Having a dependency injection system definitely helps out. You can take a look at the [FastAPI Plugin]() code that is
very simple and shows how this integration can be done.

### Creating your own adapters

Adding support for other kinds of databases or authentication methods will consist on implementing the adapter
interfaces:

- `minumtium.infra.database.adapter.DatabaseAdapter`
- `minumtium.infra.authentication.adapter.AuthenticationAdapter`

Those custom adapters are provided as dependencies when creating the services and the repositories.

### Creating your own application

Applications are the _actual_ implementation of something usable. An example is the [Fast API REST API]() application.
Applications are supposed to provide you a way to _actually_ use _minumtium_ without having to reinvent the wheel.

Applications are provided as extension libraries, that will encapsulate minumtium something like FastAPI, for example.
It is up to the user to register the minumtium client inside your main client so that you have all of its routes
available.

You can create your own application and distribute it as a library. Those extension libraries are supposed to wrap
minumtium into something else.

# Rationale

I have created this while working on my [personal portfolio page](https://danodic.dev). It was supposed to be _much more
minimal_, like a single python file. As I started developing it I have decided to use it to practice both TDD and
layered architectures. It is mostly a crud, so it was a good exercise and it is easy to read the source code.

Maybe it will not be so minimal as I wanted, but I learned some nice stuff along the way 😁.