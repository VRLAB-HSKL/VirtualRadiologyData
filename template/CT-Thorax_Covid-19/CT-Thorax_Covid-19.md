|    | NL       | Rel with Parent | VT        | Concept Name                                                                                      | VM | Req Type | Condition | Value Set Constraint |
|----|----------|-----------------|-----------|---------------------------------------------------------------------------------------------------|----|----------|-----------|----------------------|
| 1  |          |                 | Container | EV(1, 99\_HS-KL, CT-Thorax Covid-19)                                                              | 1  | M        |           |                      |
| 2  | \>       | CONTAINS        | Container | EV(101, 99\_HS-KL, Klinische Angaben)                                                             | 1  | M        |           |                      |
| 3  | \>\>     | CONTAINS        | Text      | EV(ct\_covid\_clininfo, 99\_HS-KL, Text: Klinische Angaben)                                       | 1  | M        |           |                      |
| 4  | \>\>     | CONTAINS        | Container | EV(10101, 99\_HS-KL, Aufnahme Status)                                                             | 1  | M        |           |                      |
| 5  | \>\>\>   | CONTAINS        | Code      | EV(ct\_covid\_status, 99\_HS-KL, Code: Aufnahme Status)                                           | 1  | M        |           | CID 99\_6            |
| 6  | \>\>     | CONTAINS        | Container | EV(10102, 99\_HS-KL, Intubiert)                                                                   | 1  | M        |           |                      |
| 7  | \>\>\>   | CONTAINS        | Code      | EV(ct\_covid\_intubiert, 99\_HS-KL, Code: Intubiert)                                              | 1  | M        |           | CID 231              |
| 8  | \>\>     | CONTAINS        | Container | EV(10103, 99\_HS-KL, COVID-PCR Status)                                                            | 1  | M        |           |                      |
| 9  | \>\>\>   | CONTAINS        | Code      | EV(ct\_covid\_pcr, 99\_HS-KL, Code: COVID-PCR Status)                                             | 1  | M        |           | CID 99\_7            |
| 10 | \>\>\>   | CONTAINS        | Date      | EV(ct\_covid\_pcr\_date, 99\_HS-KL, COVID-PCR Datum)                                              | 1  | M        |           |                      |
| 11 | \>       | CONTAINS        | Container | EV(102, 99\_HS-KL, Fragestellung)                                                                 | 1  | M        |           |                      |
| 12 | \>\>     | CONTAINS        | Text      | EV(ct\_covid\_fragestellung, 99\_HS-KL, Text: Fragestellung)                                      | 1  | M        |           |                      |
| 13 | \>       | CONTAINS        | Container | EV(103, 99\_HS-KL, Befund)                                                                        | 1  | M        |           |                      |
| 14 | \>\>     | CONTAINS        | Container | EV(10301, 99\_HS-KL, Voruntersuchung)                                                             | 1  | M        |           |                      |
| 15 | \>\>\>   | CONTAINS        | Code      | EV(ct\_covid\_vergleich, 99\_HS-KL, Code: Voruntersuchung)                                        | 1  | M        |           | CID 99\_8            |
| 16 | \>\>\>   | CONTAINS        | Date      | EV(ct\_covid\_vergleich\_date, 99\_HS-KL, Datum der Voruntersuchung)                              | 1  | M        |           |                      |
| 17 | \>\>     | CONTAINS        | Container | EV(10302, 99\_HS-KL, CT-Protokoll)                                                                | 1  | M        |           |                      |
| 18 | \>\>\>   | CONTAINS        | Code      | EV(ct\_covid\_protokoll, 99\_HS-KL, Code: CT-Protokoll)                                           | 1  | M        |           | CID 99\_9            |
| 19 | \>\>     | CONTAINS        | Container | EV(10303, 99\_HS-KL, Lungenparenchym/Atemwege)                                                    | 1  | M        |           |                      |
| 20 | \>\>\>   | CONTAINS        | Container | EV(1030301, 99\_HS-KL, Milchglastrübung)                                                          | 1  | M        |           |                      |
| 21 | \>\>\>\> | CONTAINS        | Code      | EV(ct\_covid\_milchglas, 99\_HS-Kl, Code: Milchglastrübung)                                       | 1  | M        |           | CID 99\_10           |
| 22 | \>\>\>   | CONTAINS        | Container | EV(1030302, 99\_HS-KL, Dominantes Milchglasmuster)                                                | 1  | M        |           |                      |
| 23 | \>\>\>\> | CONTAINS        | Code      | EV(ct\_covid\_milchglasmuster, 99\_HS-KL, Code: Dominantes Milchglasmuster)                       | 1  | M        |           | CID 99\_11           |
| 24 | \>\>\>   | CONTAINS        | Container | EV(1030303, 99\_HS-KL, Morphologie der Milchglastrübung)                                          | 1  | M        |           |                      |
| 25 | \>\>\>\> | CONTAINS        | Code      | EV(ct\_covid\_milchglasmorpho, 99\_HS-KL, Code: Morphologie der Milchglastrübung)                 | 1  | M        |           | CID 99\_12           |
| 26 | \>\>\>   | CONTAINS        | Container | EV(1030304, 99\_HS-KL, Verteilungsmuster der Milchglastrübung)                                    | 1  | M        |           |                      |
| 27 | \>\>\>\> | CONTAINS        | Code      | EV(ct\_covid\_milchglasverteilung, 99\_HS-KL, Code: Verteilungsmuster der Milchglastrübung)       | 1  | M        |           | CID 99\_13           |
| 28 | \>\>\>   | CONTAINS        | Container | EV(1030305, 99\_HS-KL, Seiten-Ausprägung der Milchglastrübung)                                    | 1  | M        |           |                      |
| 29 | \>\>\>\> | CONTAINS        | Code      | EV(ct\_covid\_milchglasseite, 99\_HS-KL, Code: Seiten-Ausprägung der Milchglastrübung)            | 1  | M        |           | CID 99\_14           |
| 30 | \>\>\>   | CONTAINS        | Container | EV(1030306, 99\_HS-KL, Dominantes Lungenfeld der Milchglastrübung)                                | 1  | M        |           |                      |
| 31 | \>\>\>\> | CONTAINS        | Code      | EV(ct\_covid\_milchglasfeld, 99\_HS-KL, Code: Dominantes Lungenfeld der Milchglastrübung)         | 1  | M        |           | CID 99\_15           |
| 32 | \>\>\>   | CONTAINS        | Container | EV(1030307, 99\_HS-KL, Ausdehnung/Serverity des Lungenbefalls quantitativ)                        | 1  | M        |           |                      |
| 33 | \>\>\>\> | CONTAINS        | Code      | EV(ct\_covid\_milchglasgrad, 99\_HS-KL, Code: Ausdehnung/Serverity des Lungenbefalls quantitativ) | 1  | M        |           | CID 99\_16           |
| 34 | \>\>\>   | CONTAINS        | Container | EV(1030308, 99\_HS-KL, Konsolidierungs-Muster)                                                    | 1  | M        |           |                      |
| 35 | \>\>\>\> | CONTAINS        | Code      | EV(ct\_covid\_konsolidierung, 99\_HS-KL, Code: Konsolidierung)                                    | 1  | M        |           | CID 99\_17           |
| 36 | \>\>\>\> | CONTAINS        | Code      | EV(ct\_covid\_konsolidierungmuster, 99\_HS-KL, Code: Konsolidierungmuster)                        | 1  | M        |           | CID 99\_18           |
| 37 | \>\>\>   | CONTAINS        | Container | EV(1030309, 99\_HS-KL, Zentrilobuläre Noduli/Tree in bud)                                         | 1  | M        |           |                      |
| 38 | \>\>\>\> | CONTAINS        | Code      | EV(ct\_covid\_noduli, 99\_HS-KL, Code: Zentrilobuläre Noduli/Tree in bud)                         | 1  | M        |           | CID 231              |
| 39 | \>\>\>   | CONTAINS        | Container | EV(10303010, 99\_HS-KL, Lungengerüstveränderung)                                                  | 1  | M        |           |                      |
| 40 | \>\>\>\> | CONTAINS        | Code      | EV(ct\_covid\_lungengerüst, 99\_HS-KL, Code: Lungengerüstveränderung)                             | 1  | M        |           | CID 231              |
| 41 | \>\>\>\> | CONTAINS        | Text      | EV(ct\_covid\_lungengerüst\_text, 99\_Hs-Kl, Text: Lungengerüstveränderung)                       | 1  | M        |           |                      |
| 42 | \>\>     | CONTAINS        | Container | EV(10304, 99\_HS-KL, Weitere Befunde)                                                             | 1  | M        |           |                      |
| 43 | \>\>\>   | CONTAINS        | Container | EV(1030401, 99\_HS-KL, Pleuraerguss links)                                                        | 1  | M        |           |                      |
| 44 | \>\>\>\> | CONTAINS        | Code      | EV(ct\_covid\_ple\_li, 99\_HS-KL, Code: Pleuraerguss links)                                       | 1  | M        |           | CID 99\_19           |
| 45 | \>\>\>   | CONTAINS        | Container | EV(1030402, 99\_HS-KL, Pleuraerguss rechts)                                                       | 1  | M        |           |                      |
| 46 | \>\>\>\> | CONTAINS        | Code      | EV(ct\_covid\_ple\_re, 99\_HS-KL, Code: Pleuraerguss rechtes)                                     | 1  | M        |           | CID 99\_19           |
| 47 | \>\>\>   | CONTAINS        | Container | EV(1030403, 99\_HS-KL, Lymphknoten)                                                               | 1  | M        |           |                      |
| 48 | \>\>\>\> | CONTAINS        | Code      | EV(ct\_covid\_lk, 99\_HS-KL, Code: Lymphknoten)                                                   | 1  | M        |           | CID 99\_20           |
| 49 | \>\>\>\> | CONTAINS        | Text      | EV(ct\_covid\_lk\_text, 99\_HS-KL, Text: Lymphknoten)                                             | 1  | M        |           |                      |
| 50 | \>\>\>   | CONTAINS        | Container | EV(1030404, 99\_HS-KL, Sonstiges)                                                                 | 1  | M        |           |                      |
| 51 | \>\>\>\> | CONTAINS        | Text      | EV(ct\_covid\_other, 99\_HS-KL, Text: Sonstiges)                                                  | 1  | M        |           |                      |
| 52 | \>       | CONTAINS        | Container | EV(104, 99\_HS-KL, Beurteilung)                                                                   | 1  | M        |           |                      |
| 53 | \>\>     | CONTAINS        | Container | EV(10401, 99\_HS-KL, Klassifikation des Lungenbefalls)                                            | 1  | M        |           |                      |
| 54 | \>\>\>   | CONTAINS        | Code      | EV(ct\_covid\_class, 99\_HS-KL, Code: Klassifikation des Lungenbefalls)                           | 1  | M        |           | CID 99\_21           |
| 55 | \>\>     | CONTAINS        | Container | EV(10402, 99\_HS-KL, Sonstiges)                                                                   | 1  | M        |           |                      |
| 56 | \>\>\>   | CONTAINS        | Text      | EV(ct\_covid\_Beurteilung, 99\_HS-KL, Text: Sonstiges)                                            | 1  | M        |           |                      |
 
