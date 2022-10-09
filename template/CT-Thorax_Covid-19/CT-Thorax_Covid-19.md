|    | NL   | Rel with Parent | VT        | Concept Name                                                                                   | VM | Req Type | Condition | Value Set Constraint |
|----|------|-----------------|-----------|------------------------------------------------------------------------------------------------|----|----------|-----------|----------------------|
| 1  |      |                 | Container | EV(1, 99_HS-KL, CT-Thorax Covid-19)                                                            | 1  | M        |           |                      |
| 2  | >    | CONTAINS        | Container | EV(101, 99_HS-KL, Klinische Angaben)                                                           | 1  | M        |           |                      |
| 3  | >>   | CONTAINS        | Text      | EV(ct_covid_clininfo, 99_HS-KL, Text: Klinische Angaben)                                       | 1  | M        |           |                      |
| 4  | >>   | CONTAINS        | Container | EV(10101, 99_HS-KL, Aufnahme Status)                                                           | 1  | M        |           |                      |
| 5  | >>>  | CONTAINS        | Code      | EV(ct_covid_status, 99_HS-KL, Code: Aufnahme Status)                                           | 1  | M        |           | CID 99_6             |
| 6  | >>   | CONTAINS        | Container | EV(10102, 99_HS-KL, Intubiert)                                                                 | 1  | M        |           |                      |
| 7  | >>>  | CONTAINS        | Code      | EV(ct_covid_intubiert, 99_HS-KL, Code: Intubiert)                                              | 1  | M        |           | CID 231              |
| 8  | >>   | CONTAINS        | Container | EV(10103, 99_HS-KL, COVID-PCR Status)                                                          | 1  | M        |           |                      |
| 9  | >>>  | CONTAINS        | Code      | EV(ct_covid_pcr, 99_HS-KL, Code: COVID-PCR Status)                                             | 1  | M        |           | CID 99_7             |
| 10 | >>>  | CONTAINS        | Date      | EV(ct_covid_pcr_date, 99_HS-KL, COVID-PCR Datum)                                               | 1  | M        |           |                      |
| 11 | >    | CONTAINS        | Container | EV(102, 99_HS-KL, Fragestellung)                                                               | 1  | M        |           |                      |
| 12 | >>   | CONTAINS        | Text      | EV(ct_covid_fragestellung, 99_HS-KL, Text: Fragestellung)                                      | 1  | M        |           |                      |
| 13 | >    | CONTAINS        | Container | EV(103, 99_HS-KL, Befund)                                                                      | 1  | M        |           |                      |
| 14 | >>   | CONTAINS        | Container | EV(10301, 99_HS-KL, Voruntersuchung)                                                           | 1  | M        |           |                      |
| 15 | >>>  | CONTAINS        | Code      | EV(ct_covid_vergleich, 99_HS-KL, Code: Voruntersuchung)                                        | 1  | M        |           | CID 99_8             |
| 16 | >>>  | CONTAINS        | Date      | EV(ct_covid_vergleich_date, 99_HS-KL, Datum der Voruntersuchung)                               | 1  | M        |           |                      |
| 17 | >>   | CONTAINS        | Container | EV(10302, 99_HS-KL, CT-Protokoll)                                                              | 1  | M        |           |                      |
| 18 | >>>  | CONTAINS        | Code      | EV(ct_covid_protokoll, 99_HS-KL, Code: CT-Protokoll)                                           | 1  | M        |           | CID 99_9             |
| 19 | >>   | CONTAINS        | Container | EV(10303, 99_HS-KL, Lungenparenchym/Atemwege)                                                  | 1  | M        |           |                      |
| 20 | >>>  | CONTAINS        | Container | EV(1030301, 99_HS-KL, Milchglastrübung)                                                        | 1  | M        |           |                      |
| 21 | >>>> | CONTAINS        | Code      | EV(ct_covid_milchglas, 99_HS-Kl, Code: Milchglastrübung)                                       | 1  | M        |           | CID 99_10            |
| 22 | >>>  | CONTAINS        | Container | EV(1030302, 99_HS-KL, Dominantes Milchglasmuster)                                              | 1  | M        |           |                      |
| 23 | >>>> | CONTAINS        | Code      | EV(ct_covid_milchglasmuster, 99_HS-KL, Code: Dominantes Milchglasmuster)                       | 1  | M        |           | CID 99_11            |
| 24 | >>>  | CONTAINS        | Container | EV(1030303, 99_HS-KL, Morphologie der Milchglastrübung)                                        | 1  | M        |           |                      |
| 25 | >>>> | CONTAINS        | Code      | EV(ct_covid_milchglasmorpho, 99_HS-KL, Code: Morphologie der Milchglastrübung)                 | 1  | M        |           | CID 99_12            |
| 26 | >>>  | CONTAINS        | Container | EV(1030304, 99_HS-KL, Verteilungsmuster der Milchglastrübung)                                  | 1  | M        |           |                      |
| 27 | >>>> | CONTAINS        | Code      | EV(ct_covid_milchglasverteilung, 99_HS-KL, Code: Verteilungsmuster der Milchglastrübung)       | 1  | M        |           | CID 99_13            |
| 28 | >>>  | CONTAINS        | Container | EV(1030305, 99_HS-KL, Seiten-Ausprägung der Milchglastrübung)                                  | 1  | M        |           |                      |
| 29 | >>>> | CONTAINS        | Code      | EV(ct_covid_milchglasseite, 99_HS-KL, Code: Seiten-Ausprägung der Milchglastrübung)            | 1  | M        |           | CID 99_14            |
| 30 | >>>  | CONTAINS        | Container | EV(1030306, 99_HS-KL, Dominantes Lungenfeld der Milchglastrübung)                              | 1  | M        |           |                      |
| 31 | >>>> | CONTAINS        | Code      | EV(ct_covid_milchglasfeld, 99_HS-KL, Code: Dominantes Lungenfeld der Milchglastrübung)         | 1  | M        |           | CID 99_15            |
| 32 | >>>  | CONTAINS        | Container | EV(1030307, 99_HS-KL, Ausdehnung/Serverity des Lungenbefalls quantitativ)                      | 1  | M        |           |                      |
| 33 | >>>> | CONTAINS        | Code      | EV(ct_covid_milchglasgrad, 99_HS-KL, Code: Ausdehnung/Serverity des Lungenbefalls quantitativ) | 1  | M        |           | CID 99_16            |
| 34 | >>>  | CONTAINS        | Container | EV(1030308, 99_HS-KL, Konsolidierungs-Muster)                                                  | 1  | M        |           |                      |
| 35 | >>>> | CONTAINS        | Code      | EV(ct_covid_konsolidierung, 99_HS-KL, Code: Konsolidierung)                                    | 1  | M        |           | CID 99_17            |
| 36 | >>>> | CONTAINS        | Code      | EV(ct_covid_konsolidierungmuster, 99_HS-KL, Code: Konsolidierungmuster)                        | 1  | M        |           | CID 99_18            |
| 37 | >>>  | CONTAINS        | Container | EV(1030309, 99_HS-KL, Zentrilobuläre Noduli/Tree in bud)                                       | 1  | M        |           |                      |
| 38 | >>>> | CONTAINS        | Code      | EV(ct_covid_noduli, 99_HS-KL, Code: Zentrilobuläre Noduli/Tree in bud)                         | 1  | M        |           | CID 231              |
| 39 | >>>  | CONTAINS        | Container | EV(10303010, 99_HS-KL, Lungengerüstveränderung)                                                | 1  | M        |           |                      |
| 40 | >>>> | CONTAINS        | Code      | EV(ct_covid_lungengerüst, 99_HS-KL, Code: Lungengerüstveränderung)                             | 1  | M        |           | CID 231              |
| 41 | >>>> | CONTAINS        | Text      | EV(ct_covid_lungengerüst_text, 99_Hs-Kl, Text: Lungengerüstveränderung)                        | 1  | M        |           |                      |
| 42 | >>   | CONTAINS        | Container | EV(10304, 99_HS-KL, Weitere Befunde)                                                           | 1  | M        |           |                      |
| 43 | >>>  | CONTAINS        | Container | EV(1030401, 99_HS-KL, Pleuraerguss links)                                                      | 1  | M        |           |                      |
| 44 | >>>> | CONTAINS        | Code      | EV(ct_covid_ple_li, 99_HS-KL, Code: Pleuraerguss links)                                        | 1  | M        |           | CID 99_19            |
| 45 | >>>  | CONTAINS        | Container | EV(1030402, 99_HS-KL, Pleuraerguss rechts)                                                     | 1  | M        |           |                      |
| 46 | >>>> | CONTAINS        | Code      | EV(ct_covid_ple_re, 99_HS-KL, Code: Pleuraerguss rechtes)                                      | 1  | M        |           | CID 99_19            |
| 47 | >>>  | CONTAINS        | Container | EV(1030403, 99_HS-KL, Lymphknoten)                                                             | 1  | M        |           |                      |
| 48 | >>>> | CONTAINS        | Code      | EV(ct_covid_lk, 99_HS-KL, Code: Lymphknoten)                                                   | 1  | M        |           | CID 99_20            |
| 49 | >>>> | CONTAINS        | Text      | EV(ct_covid_lk_text, 99_HS-KL, Text: Lymphknoten)                                              | 1  | M        |           |                      |
| 50 | >>>  | CONTAINS        | Container | EV(1030404, 99_HS-KL, Sonstiges)                                                               | 1  | M        |           |                      |
| 51 | >>>> | CONTAINS        | Text      | EV(ct_covid_other, 99_HS-KL, Text: Sonstiges)                                                  | 1  | M        |           |                      |
| 52 | >    | CONTAINS        | Container | EV(104, 99_HS-KL, Beurteilung)                                                                 | 1  | M        |           |                      |
| 53 | >>   | CONTAINS        | Container | EV(10401, 99_HS-KL, Klassifikation des Lungenbefalls)                                          | 1  | M        |           |                      |
| 54 | >>>  | CONTAINS        | Code      | EV(ct_covid_class, 99_HS-KL, Code: Klassifikation des Lungenbefalls)                           | 1  | M        |           | CID 99_21            |
| 55 | >>   | CONTAINS        | Container | EV(10402, 99_HS-KL, Sonstiges)                                                                 | 1  | M        |           |                      |
| 56 | >>>  | CONTAINS        | Text      | EV(ct_covid_Beurteilung, 99_HS-KL, Text: Sonstiges)                                            | 1  | M        |           |                      |
 
