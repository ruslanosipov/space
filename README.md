# Space v0.3.1-alpha

[![Build Status](https://travis-ci.org/ruslanosipov/space.png?branch=develop)]
(https://travis-ci.org/ruslanosipov/space)
[![Code Coverage]
(https://coveralls.io/repos/ruslanosipov/space/badge.png?branch=develop)]
(https://coveralls.io/r/ruslanosipov/space)

Space is a multiplayer roguelike game with ship vs ship and crew vs crew
battles. 

## Key bindings

### Player and spaceship

| Key     | Player      | Spaceship    |
| :------ | ----------- | -----------: |
| `h`     | move left   | rotate left  |
| `j`     | move down   | decelerate   |
| `k`     | move up     | accelerate   |
| `l`     | move right  | rotate right |
| `t`     | set target  | -            |
| `f`     | fire        | fire missile |
| `v`     | look        | -            |
| `a`     | activate    | -            |
| `,`     | pick up     | -            |
| `Q`     | quit game   | quit flight  |
| `/`     | say         | -            |
| `i`     | inventory   | -            |
| `E`     | equipment   | -            |

### Equipment screen

| Key     | Description |
| :------ | ----------: |
| `i`     | inventory   |
| `u`     | unequip     |
| `Q`     | quit screen |

### Inventory screen

| Key     | Description |
| :------ | ----------: |
| `d`     | drop        |
| `e`     | equip       |
| `E`     | equipment   |
| `Q`     | quit screen |

## Contribution

You are free to contribute, please keep in mind following things:
* Code should comply with PEP 8 standards.
* Tests: I use `unittest` module. `fab test` should pass. Everything
except for UI elements is reasonably tested. New code should not be
submitted without unit tests.
* Project uses nvie's branching guidelines, main branches are develop and
master (for details see
[nvie.com](http://nvie.com/posts/a-successful-git-branching-model)).
* Please keep your commit messages descriptive and grammatically correct. I
use tpope's commit message guidelines (for details see
[tpope.com](http://www.tpope.net/node/106)).

## Dependencies

Currently the game does not require a lot to run, and I would prefer to keep
it that way. It uses virtualenv and pip bundle, so you can set up the
environment as follows:

    virtualenv env
    . env/bin/activate
    pip install -r requirements.txt

There might be an issue with installing pygame package via pip - don't forget
to install the dependencies in this case.
