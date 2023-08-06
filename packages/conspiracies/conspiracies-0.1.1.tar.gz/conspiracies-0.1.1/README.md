
# 👁‍🗨 Conspiracies
[![python versions](https://img.shields.io/badge/Python-%3E=3.7-blue)](https://github.com/centre-for-humanities-computing/conspiracies)
[![Code style: black](https://img.shields.io/badge/Code%20Style-Black-black)](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html)
[![github actions pytest](https://github.com/centre-for-humanities-computing/conspiracies/actions/workflows/pytest.yml/badge.svg)](https://github.com/centre-for-humanities-computing/conspiracies/actions)
[![spacy](https://img.shields.io/badge/built%20with-spaCy-09a3d5.svg)](https://spacy.io)


<!-- [![release version](https://img.shields.io/badge/belief_graph%20Version-0.0.1-green)](https://github.com/centre-for-humanities-computing/conspiracies) -->

Discovering and examining conspiracies using NLP.



## 🔧 Installation
Installation using pip:
```bash
pip install pip --upgrade
pip install conspiracies
```

Note that this package is dependent on AllenNLP and thus does not support Windows.

## 👩‍💻 Usage

### Coreference model
A small use case of the coreference component in spaCy.

```python
import spacy
from spacy.tokens import Span
from conspiracies.coref import CoreferenceComponent 

nlp = spacy.blank("da")
nlp.add_pipe("allennlp_coref")
doc = nlp("Do you see Julie over there? She is really into programming!")

assert isinstance(doc._.coref_clusters, list)

for sent in doc.sents:
    assert isinstance(sent._.coref_cluster, list)
    assert isinstance(sent._.coref_cluster[0], tuple)
    assert isinstance(sent._.coref_cluster[0][0], int)
    assert isinstance(sent._.coref_cluster[0][1], Span)
```


<details>
  <summary>Details on output </summary>

Examining the output a bit further:

```python
print("DOC LEVEL (Coref clusters)")
print(doc._.coref_clusters)
print("-----\n\nSPAN LEVEL (sentences)")
for sent in doc.sents:
    print(sent._.coref_cluster)
print("-----\n\nSPAN LEVEL (entities)\n")
for sent in doc.sents:
    for i, coref_entity in sent._.coref_cluster:
        print(f"Coref Entity: {coref_entity} \nAntecedent: {coref_entity._.antecedent}")
        print("\n")
```

This should produce the following output

```python
DOC LEVEL (Coref clusters)
[(0, [Julie, She])]
-----

SPAN LEVEL (sentences)
[(0, Julie)]
[(0, She)]
-----

SPAN LEVEL (entities)

Coref Entity: Julie 
Antecedent: Julie


Coref Entity: She 
Antecedent: Julie
```

</details>


### Headword Extraction
A small use case of how to use the headword extraction component to extract headwords.

```python
import spacy
from conspiracies.HeadWordExtractionComponent import contains_ents

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("heads_extraction")

doc = nlp("Mette Frederiksen is the Danish politician.")
heads_spans = []

for sent in doc:
    sent._.most_common_ancestor  # extract the most common ancestor i.e. span head
```

### Wordpiece length normalization Extraction
A small use case of how to use word piece length normalization to normalize the length of
your texts in case you are applying transformer-based pipelines.

```python
import spacy
from transformers import AutoTokenizer

# load nlp (we don't recommend a trf based spacy model as it is too slow)
nlp = spacy.load("da_core_news_lg")
# load huggingface tokenizer - should be the same as the model you wish to apply later
tokenizer_name = "DaNLP/da-bert-tone-subjective-objective"
tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

# An example with a very long text
from conspiracies import wordpiece_length_normalization
long_text = ["Hej mit navn er Kenneth. " * 200]
normalized_text = wordpiece_length_normalization(long_text, nlp, tokenizer, max_length=500)
assert len(norm_text) > 1, "a long text should be split into multiple texts"
```



## FAQ

### How do I run the tests?
To run the test, you will need to install the package in editable mode. This is
intentional as it ensures that you always run the package installation before running
the tests, which ensures that the installation process works as intended.

To run the test you can use the following code:
```
# download repo
git clone https://github.com/centre-for-humanities-computing/conspiracies
cd conspiracies

# install package
pip install --editable .

# run tests
python -m  pytest
```

## Contact
Please use the [GitHub Issue Tracker](https://github.com/centre-for-humanities-computing/conspiracies/issues) to contact us on this project.
