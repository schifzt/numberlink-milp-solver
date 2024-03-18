# optimal-connect-points
minimize or maximize a path lengh which connect points with same number

```text
minimize path length              maximize path length
┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓     ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
┃   │ ┏━━━━━━━3 │   │   │   ┃     ┃ ┏━━━━━━━┓ │ 3━━━━━━━━━━━┓ ┃
┣───┼─┃─┼───┼───┼───┼───┼───┫     ┣─┃─┼───┼─┃─┼───┼───┼───┼─┃─┫
┃   │ ┃ │ ┏━━━━━━━━━━━━━━━┓ ┃     ┃ ┃ │   │ ┗━━━━━━━┓ │   │ ┃ ┃
┣───┼─┃─┼─┃─┼───┼───┼───┼─┃─┫     ┣─┃─┼───┼───┼───┼─┃─┼───┼─┃─┫
┃   │ ┃ │ ┃ │ ┏━━━━━━━┓ │ ┃ ┃     ┃ ┃ │ ┏━━━━━━━┓ │ ┃ │ ┏━━━┛ ┃
┣───┼─┃─┼─┃─┼─┃─┼───┼─┃─┼─┃─┫     ┣─┃─┼─┃─┼───┼─┃─┼─┃─┼─┃─┼───┫
┃ 1 │ ┃ │ 2 │ ┃ │ 1 │ ┃ │ 2 ┃     ┃ 1 │ ┃ │ 2 │ ┃ │ 1 │ ┃ │ 2 ┃
┣─┃─┼─┃─┼───┼─┃─┼─┃─┼─┃─┼───┫     ┣───┼─┃─┼─┃─┼─┃─┼───┼─┃─┼─┃─┫
┃ ┃ │ ┗━━━━━━━┛ │ ┃ │ ┃ │   ┃     ┃ ┏━━━┛ │ ┃ │ ┗━━━━━━━┛ │ ┃ ┃
┣─┃─┼───┼───┼───┼─┃─┼─┃─┼───┫     ┣─┃─┼───┼─┃─┼───┼───┼───┼─┃─┫
┃ ┗━━━━━━━━━━━━━━━┛ │ ┃ │   ┃     ┃ ┃ │   │ ┗━━━━━━━┓ │   │ ┃ ┃
┣───┼───┼───┼───┼───┼─┃─┼───┫     ┣─┃─┼───┼───┼───┼─┃─┼───┼─┃─┫
┃   │   │   │ 3━━━━━━━┛ │   ┃     ┃ ┗━━━━━━━━━━━3 │ ┗━━━━━━━┛ ┃
┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛     ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
```

## Integer Programming formulation

| element          | formulation                                                                                                  | meaning                                                                                                                    |
| :--------------- | :----------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------- |
| constant         | $I$                                                                                                          | row length of a board                                                                                                      |
| constant         | $J$                                                                                                          | column length of a board                                                                                                   |
| constant         | $N$                                                                                                          | number of paths                                                                                                            |
| index            | $i \in \lbrace 0,\ldots,I+1 \rbrace$                                                                         | $\lbrace 1,\ldots,I \rbrace$ are row indices on a borad, $\lbrace 0,I+1 \rbrace$ are row indices at sentinel points.       |
| index            | $j \in \lbrace 0,\ldots,J+1 \rbrace$                                                                         | $\lbrace 1,\ldots,J \rbrace$ are column indices on a borad, $\lbrace 0,J+1 \rbrace$ are column indices at sentinel points. |
| index            | $n \in \lbrace 1,\ldots,N \rbrace$                                                                           | index of paths                                                                                                             |
| variable         | $x_{i,j,n}\in\lbrace0,1\rbrace$                                                                              | if a point at $(i,j)$ is filled with $n$, $x_{i,j,n}=1$, otherwise $x_{i,j,n}=0$.                                          |
| variable         | $a_{i,j,n} \in \mathbb{Z}_{\geq 0}$                                                                          | number of adjacent along to a $n$-th path at a point $(i,j)$.                                                              |
| constraint $C_1$ | if a point $(i,j)$ is a sentinel point, $x_{i,j,n}=0$                                                        | define sentinel points.                                                                                                    |
| constraint $C_2$ | For all paths and points $(i,j)$ on a board, $a_{i,j,n} = x_{i-1,j,n}+x_{i+1,j,n}+x_{i,j-1,n}+x_{i-1,j+1,n}$ | define $a_{i,j,n}$.                                                                                                        |
| constraint $C_3$ | For all points $(i,j)$ on a board, $\sum_n x_{i,j,n} \leq 1$                                                 | $x_{i,j,n}$ are distinct for $n$.                                                                                          |
| constraint $C_4$ | if a point $(i,j)$ is a start/end point of a $n$-th path, $x_{i,j,n}=1$                                      | define start/end points.                                                                                                   |
| constraint $C_5$ | if a point $(i,j)$ is a start/end point of a $n$-th path, $a_{i,j,n}=1$                                      | consistent path for each $n$ at start/end points.                                                                          |
| constraint $C_6$ | For all paths and points $(i,j)$ on a candidate points, $x_{i,j,n}=1\Rightarrow a_{i,j,n}=2$                 | consistent path for each $n$ at path candidate points.                                                                     |
| objective $E_1$  | $\sum_{i,j,n} x_{i,j,n}$                                                                                     | minimize/maximize total path length.                                                                                       |

## Licenese
Distributed under MIT license