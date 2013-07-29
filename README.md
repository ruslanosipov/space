# Space v0.2.1-alpha

Space is a multiplayer roguelike game with ship vs ship and crew vs crew
battles. 

## Key bindings

| Key     | Player      | Spaceship    |
| :------ | ----------- | -----------: |
| `left`  | move left   | rotate left  |
| `down`  | move down   | decelerate   |
| `up`    | move up     | accelerate   |
| `right` | move right  | rotate right |
| `t`     | set target  | -            |
| `f`     | fire        | fire missile |
| `v`     | look        | -            |
| `a`     | activate    | -            |
| `,`     | pick up     | -            |
| `Q`     | quit game   | quit flight  |
| `/`     | say         | -            |
| `i`     | inventory   | -            |

## Contribution

You are free to contribute, please keep in mind following things:
* Code should comply with PEP 8 standards.
* Tests: I use `doctest` and `unittest` modules in a bundle. `runtests.py`
should pass. Everything except for UI elements is reasonably tested.
* Project uses nvie's branching guidelines, main branches are develop and
master (for details see
[nvie.com](http://nvie.com/posts/a-successful-git-branching-model)).
* Please keep your commit messages descriptive and grammatically correct. I
use tpope's commit message guidelines (for details see
[tpope.com](http://www.tpope.net/node/106)).

## Dependencies

Currently the game does not require a lot to run, and I would prefer to keep
it that way. Required packages:

* Client:
    * `python2.7`
    * `python-pygame`
* Server:
    * `python2.7`
