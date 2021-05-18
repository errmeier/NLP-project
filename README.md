# Chess Commentary Generation

A neural network for generating commentary for chess moves.

## Results

| Model | BLEU Score | RIBES |
| ----- | ---------- | ----- |
| Boilerplate | 0.0015413505199354763 | 0.120584 |
| Score Data Transformer | 0.012592180853612005 | 0.310440 | 
| Attack Data Transformer | 0.01119994363770219 | 0.297493 |
| Simple Data Transformer | 0.008931533685728885 | 0.304716 |
| Classifier Transformer | 0.009690130971129089 | 308305 |

### Related Work/References
- https://www.cs.cmu.edu/~hovy/papers/18ACL-chess-commentary.pdf
- https://arxiv.org/pdf/1909.10413.pdf
- https://www.aclweb.org/anthology/D10-1092.pdf (RIBES)
