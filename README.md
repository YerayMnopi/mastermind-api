# Mastermind api
## Run wit docker-compose
`make run` or `docker-compose up --build`
The server would run on 0.0.0.0:8000/search.

## Open api
`0.0.0.0:8000/docs` or `0.0.0.0:8000/redoc`

## Codebase
This repo uses [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)

This repo follows [githubflow](https://docs.github.com/en/get-started/quickstart/github-flow).

This service follows the [twelve-factors methodology](https://12factor.net/). A .env file containing enviroment variables could be provided.

This projects is structured following [Domain Driven Design](https://www.amazon.es/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215) and [cosmic python](https://www.cosmicpython.com/) guidelines. The src folder contains all the app code. You can find inside three folders:
- Domain, where the business rules and important logic is contained.
- Application, where all the use cases of the app are listed.
- Infrastructure, where all the entrypoints and communications of the app are implemented.


## Assumptions
Maybe there should be nice to have some kind of authentication and authorization, but since is not specified on the requirements and for the sake of time, I assume these not to be required.


## Architecture
The proposed architecture is based on two critical components:
- A database to store all games.
- The api server, responsable for reading games from the db.


## Packege manager pdm
This project is handled with [pdm](https://pdm.fming.dev/latest/#installation)

You can run the following scripts:
```
pdm run server
pdm run cli
pdm run make_migration
pdm run migrate
pdm run test
pdm run test_coverage
pdm run test_coverage_html
pdm run test_e2e (Needs a db server up)
```

## Code quality
Install pre-commit with `pdm run pre-commit install` to lint, format code and order imports on every commit.

## Questionnaire
### What is your favorite package manager and why?
PDM, because it supports the latest PEP standards. The most significant benefit is it installs and manages packages in a similar way to npm that doesn't need to create a virtualenv at all.

### What architecture did you follow for this project?
The proposed architecture is based on two critical components:
- A database to store all games.
- The api server, responsable for reading games from the db.

This projects is structured following [Domain Driven Design](https://www.amazon.es/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215) and [cosmic python](https://www.cosmicpython.com/) guidelines. The src folder contains all the app code. You can find inside three folders:
- Domain, where the business rules and important logic is contained.
- Application, where all the use cases of the app are listed.
- Infrastructure, where all the entrypoints and communications of the app are implemented.


### Do you know and understand UML? What would the class diagram of the domain exposed in the mastermind game be like for you?
I don't usually use UML on my day to day work. I use diagrams, of course, but I don't follow an strict format or convention.

### What tools are you aware of to handle things like code styling and consistency, formatting, typing…?
I personally use pylint for linting, autopep8 for formatting and isort for consistency across imports.

### Is there anything you would like to comment about the project, this small exercise,etc?
It was fun to code it.

I did not have time for everything, In order to improve my excercise, I would add logging, a seperate db for integration test, and a little more of documentation.