# Dansk Gigaword Corpus

Version: 1.0 – 2021-06-01

[gigaword.dk](https://gigaword.dk)

PI: Leon Derczynski, IT University of Copenhagen (ITU)
Co-I: Manuel R Ciosici, IT University of Copenhagen (ITU) / University of Southern California Information Sciences Institute (ISI)

## Instructions for use

The Danish Gigaword corpus (DAGW) is split into sections, stored under the `sektioner` directory. Each section has a license, a .jsonl manifest, and a series of raw text files.

Some sections contain social media data. This must be "rehydrated" manually by you; we do not distribute that data directly as part of the corpus, but we do give you the tools to do that. See the `dokumentation` directory for a guide to rehydrating tweets.

Information on the file format, the paper describing the dataset, and and other information is in the `dokumentation` directory.

## License & Reference

If you use the data, you MUST acknowledge it. The license is CC-BY 4.0, Creative Commons with Attribution. 

### Sample attributions:

In a press release:

> Modellen er præ-trænet på et datasæt fra The Danish Gigaword Project ([https://gigaword.dk](https://gigaword.dk)), der er udviklet af forskere fra IT-Universitetet i København

> The model is pre-trained using the Danish Gigaword Corpus ([https://gigaword.dk](https://gigaword.dk)), developed at the IT University of Copenhagen

In academic writing:

> Derczynski, L., Ciosici, M. R., et al. (2021). The Danish Gigaword Corpus. In *Proceedings of the 23rd Nordic Conference on Computational Linguistics (NoDaLiDa 2021)*.

>```bibtex
>@inproceedings{derczynski-ciosici-etal-2021-dagw,
>    title = "The {{Danish Gigaword Project}}",
>    author = "Strømberg-Derczynski, Leon and Ciosici, Manuel R. and Baglini, Rebekah and Christiansen, Morten H. and Dalsgaard, Jacob Aarup and Fusaroli, Riccardo and Henrichsen, Peter Juel and Hvingelby, Rasmus and Kirkedal, Andreas and Kjeldsen, Alex Speed and Ladefoged, Claus and Nielsen, Finn Årup and Petersen, Malte Lau and Rystrøm, Jonathan Hvithamar and Varab, Daniel",
>    booktitle = "Proceedings of the 23nd Nordic Conference on Computational Linguistics",
>    month = jun,
>    year = "2021",
>    address = "Reykjavík, Iceland",
>    publisher = {Link{\"o}ping University Electronic Press},
>}
>```

In a software product, tool, or service:

> Danish Gigaword Corpus: [license](https://creativecommons.org/licenses/by/4.0/) - [homepage](https://gigaword.dk/)

> Denne service er lavede med data fra [The Danish Gigaword Corpus](https://gigaword.dk/)

That's all we ask in return for our work; no money, no signed agreement, no royalties - just acknowledgment. We hope you think that's fair.

If you cannot acknowledge the project like this, you are not licensed to use the data.

## GDPR note

The Danish Gigaword project involves the obtaining of personal data regarding around 1.6 million tweets in Danish. The tweets were publicly available at the time of indexing. The data subjects (Twitter users) remain fully in control of altering and deleting the tweets. Due to the significant amount of tweets, and since Twitter only allows the contacting of a user where the user in question is either following or being followed by the data collector, it has been assessed that the duty to inform data subjects cf. Article 14, para 1-4 of the GDPR does not apply. The provision of such information would involve a disproportionate effort concerning a scientific research purpose and the provision in Article 14(5) thus exempts ITU as data collector from the information duty.