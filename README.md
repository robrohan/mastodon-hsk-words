# Mastodon HSK Words Bot

This bot is used to toot words from the [HSK](https://en.wikipedia.org/wiki/Hanyu_Shuiping_Kaoshi) test to help people study.

- https://github.com/robrohan/HSKWords
- https://github.com/Destaq/chinese-sentence-miner


## Audio

- https://pypi.org/project/zhtts/

Requires tensorflow (inference done on the CPU)

## Images

- https://github.com/robrohan/stable-diffusion-tensorflow

Requires tensorflow and stable diffusion (inference can done on the CPU)

## Video

Requires the above, and FFMPG to be installed

## Database

```
cat data/simple_hsk1_sentences.txt data/simple_hsk2_sentences.txt data/simple_hsk3_sentences.txt > data/sample_sentences.txt
```

```
sqlite> .mode tabs
sqlite> .import ./data/sample_sentences.txt sentences
```