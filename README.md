# Chess Commentary Generation

A Natural Language Processing project with the goal of automatically generating commentary for chess moves.

## Code

`transformer.py` is the code used for each of the transformers, `neural_classifier.py` is the classifier network, and `category_transformer.py` is the script to combine the trained classifier and trained category models. Each of the models were trained for 10-15 epochs, with the model with the best dev loss being saved as the final model.  
`transformer.py` and `layers.py` were taken from the homeworks for CSE 40657, with some modifications of my own in the transformer (mainly adding the copy mechanism).  
The other python programs were written by me, with the exception of the `bleu.py` and `RIBES.py`

The output of the different models is saved in the format `out.[model_type].en`

## Results

The best classifier accuracy I was able to achieve after working through several iterations of different types of classifiers was 82%

| Model | BLEU Score | RIBES |
| ----- | ---------- | ----- |
| Boilerplate | 0.0015413505199354763 | 0.120584 |
| Score Data Transformer | 0.012592180853612005 | 0.310440 | 
| Attack Data Transformer | 0.01119994363770219 | 0.297493 |
| Simple Data Transformer | 0.008931533685728885 | 0.304716 |
| Classifier Transformer | 0.009690130971129089 | 0.308305 |

### Related Work/References
- https://www.cs.cmu.edu/~hovy/papers/18ACL-chess-commentary.pdf  
- https://arxiv.org/pdf/1909.10413.pdf  
- https://www.aclweb.org/anthology/D10-1092.pdf  
- https://github.com/nttcslab-nlp/RIBES  
