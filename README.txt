# optimal-connect-points

```text
┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
┃   │ ┏━━━━━━━3 │   │   │   ┃
┣───┼─┃─┼───┼───┼───┼───┼───┫
┃   │ ┃ │ ┏━━━━━━━━━━━━━━━┓ ┃
┣───┼─┃─┼─┃─┼───┼───┼───┼─┃─┫
┃   │ ┃ │ ┃ │ ┏━━━━━━━┓ │ ┃ ┃
┣───┼─┃─┼─┃─┼─┃─┼───┼─┃─┼─┃─┫
┃ 1 │ ┃ │ 2 │ ┃ │ 1 │ ┃ │ 2 ┃
┣─┃─┼─┃─┼───┼─┃─┼─┃─┼─┃─┼───┫
┃ ┃ │ ┗━━━━━━━┛ │ ┃ │ ┃ │   ┃
┣─┃─┼───┼───┼───┼─┃─┼─┃─┼───┫
┃ ┗━━━━━━━━━━━━━━━┛ │ ┃ │   ┃
┣───┼───┼───┼───┼───┼─┃─┼───┫
┃   │   │   │ 3━━━━━━━┛ │   ┃
┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
```

## Integer Programming formulation

| element    | formulation                                                                                     | meaning                                                                          |
| :--------- | :---------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------- |
| constant   | $I$                                                                                             | row length of a board                                                            |
| constant   | $J$                                                                                             | column length of a board                                                         |
| constant   | $N$                                                                                             | number of start/end points                                                       |
| index      | $i \in [0..I+1]$                                                                                | $1,...,I$ are row indices on a borad, $0,I+1$ are row indices at sentinels       |
| index      | $j \in [0..J+1]$                                                                                | $1,...,J$ are column indices on a borad, $0,J+1$ are column indices at sentinels |
| index      | $n$                                                                                             | number of start/end points                                                       |
| variable   | $x_{i,j,n}\in\{0,1\}$                                                                           | if point at $(i,j)$ is filled with $n$, $x_{i,j,n}=1$, otherwise $x_{i,j,n}=0$.  |
| constraint | $\forall i,j\quad\Sigma_n x_{i,j,n}=1$                                                          | $x_{i,j,n}$ are distinct for $n$.                                                |
| constraint | if a point $(i,j)$ is a start/end point, $x_{i,j,n}=1$                                          | define start/end points.                                                         |
| constraint | if a point $(i,j)$ is a start/end point, $x_{i-1,j,n}+x_{i+1,j,n}+x_{i,j-1,n}+x_{i-1,j+1,n}=1$  | consistent path for each $n$ at start/end points.                                |
| constraint | $\forall i,j,n\quad x_{i,j,n}=1\Rightarrow x_{i-1,j,n}+x_{i+1,j,n}+x_{i,j-1,n}+x_{i-1,j+1,n}=2$ | consistent path for each $n$ not at start/end points.                            |
| objective  | $\Sigma x_{i,j,n}$                                                                              | optimize total path length                                                       |