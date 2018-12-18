# Space v0.3.1-alpha

[![Build Status](https://travis-ci.org/ruslanosipov/space.png?branch=develop)](https://travis-ci.org/ruslanosipov/space)
[![Code Coverage](https://coveralls.io/repos/ruslanosipov/space/badge.png?branch=develop)](https://coveralls.io/r/ruslanosipov/space)

Space is a multiplayer roguelike game with ship vs ship and crew vs crew
battles. **I abandoned work on this project a few years ago. Picking it up
and continuing would be somewhat difficult, in part due to using a number
ofoutdated packages, and not being ready for a Python 2 -> 3 migration.**

## Key bindings

### Player and spaceship

| Key     | Player      | Spaceship    |
| :------ | ----------- | -----------: |
| `h`     | move West   | rotate left  |
| `j`     | move South  | decelerate   |
| `k`     | move North  | accelerate   |
| `l`     | move East   | rotate right |
| `y`     | move NW     | -            |
| `u`     | move NE     | -            |
| `b`     | move SW     | -            |
| `n`     | move SE     | -            |
| `t`     | set target  | -            |
| `>`     | next target | -            |
| `<`     | prev target | -            |
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

The game uses virtualenv and pip bundle, but `pygame` module needs to be
installed separately (this dependency is to be removed in the future).

Mac OS X, via `homebrew`:

    brew tap homebrew/python
    brew update
    brew install pygame

Linux, via `apt-get`:

    sudo apt-get install python-pygame

After `pygame` is installed, run:

    virtualenv env
    . env/bin/activate
    pip install -r requirements.txt
