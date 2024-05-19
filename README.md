# AuNP seed-mediated growth recipes

### For the publication "Data-driven analysis of text-mined seed-meidated growth AuNP recipes*" by Sanghoon Lee, Kevin Cruse, Samuel Gleason, A. Paul Alivisatos,  Gerbrand Ceder, and Anubhav Jain.

[AuNP_seedmed_dataset.json](AuNP_seedmed_dataset.json) is the dataset consisting of 492 seed-mediated recipes of AuNPs with complete precursor amounts, and [AuNP_seedmed_dataset_binary.json](AuNP_seedmed_dataset_binary.json) is the dataset of 519 recipes with precursors used but not with amounts.

[llama2weights](llama2weights) contains LoRA weights obtained from fine-tuning 8-bit quantized [Llama-2-13b-hf](https://huggingface.co/meta-llama/Llama-2-13b-hf). The code base for fine-tuning to obtain this and also for inference using this fine-tuned model can be found in [NERRE-Llama repo](https://github.com/lbnlp/nerre-llama/tree/main).

For search-based parser, [AuNP_searchbasedparser.ipynb](AuNP_searchbasedparser.ipynb) is a jupyter notebook tutorial on how to use each step of the regex-based parser.
Although this tutorial uses dummy paper (list of paragraphs) as an example, you can easily adapt this search-based parser to your own tasks, for instance by changing `Prec_Dict_regex` to expand/modify precursor regular expressions to extract, or `morphdicts` to extract additional morphologies of interest in in [regex_patterns.py](regex_patterns.py) .

Prepare your environment using [requirements.txt](requirements.txt) (confirmed working with python=3.6.13)
```bash
pip install -r requirements.txt
```
Please note that chemdataextractor is only used for sentence tokenization.
