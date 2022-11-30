|    | NL       | Rel with Parent | VT        | Concept Name                                                                                      | VM | Req Type | Condition | Value Set Constraint |
|----|----------|-----------------|-----------|---------------------------------------------------------------------------------------------------|----|----------|-----------|----------------------|
| 1  |          |                 | Container | EV(1, 99\_HS-KL, CT-Thorax Covid-19)                                                              | 1  | M        |           |                      |
| 2  | \>       | CONTAINS        | UidRef    | EV(101, 99\_HS-KL, ReferencedSeries)                                                              | 1  | M        |           |                      |
| 3  | \>       | CONTAINS        | Container | EV(102, 99\_HS-KL, Klinische Angaben)                                                             | 1  | M        |           |                      |
| 4  | \>\>     | CONTAINS        | Text      | EV(ct\_covid\_clininfo, 99\_HS-KL, Text: Klinische Angaben)                                       | 1  | M        |           |                      |
| 5  | \>\>     | CONTAINS        | Container | EV(10201, 99\_HS-KL, Aufnahme Status)                                                             | 1  | M        |           |                      |
| 6  | \>\>\>   | CONTAINS        | Code      | EV(ct\_covid\_status, 99\_HS-KL, Code: Aufnahme Status)                                           | 1  | M        |           | DCID 99\_6           |
| 7  | \>\>     | CONTAINS        | Container | EV(10202, 99\_HS-KL, Intubiert)                                                                   | 1  | M        |           |                      |
| 8  | \>\>\>   | CONTAINS        | Code      | EV(ct\_covid\_intubiert, 99\_HS-KL, Code: Intubiert)                                              | 1  | M        |           | DCID 231             |
| 9  | \>\>     | CONTAINS        | Container | EV(10203, 99\_HS-KL, COVID-PCR Status)                                                            | 1  | M        |           |                      |
| 10 | \>\>\>   | CONTAINS        | Code      | EV(ct\_covid\_pcr, 99\_HS-KL, Code: COVID-PCR Status)                                             | 1  | M        |           | DCID 99\_7           |
| 11 | \>\>\>   | CONTAINS        | Date      | EV(ct\_covid\_pcr\_date, 99\_HS-KL, COVID-PCR Datum)                                              | 1  | M        |           |                      |
| 12 | \>       | CONTAINS        | Container | EV(103, 99\_HS-KL, Fragestellung)                                                                 | 1  | M        |           |                      |
| 13 | \>\>     | CONTAINS        | Text      | EV(ct\_covid\_fragestellung, 99\_HS-KL, Text: Fragestellung)                                      | 1  | M        |           |                      |
| 14 | \>       | CONTAINS        | Container | EV(104, 99\_HS-KL, Befund)                                                                        | 1  | M        |           |                      |
| 15 | \>\>     | CONTAINS        | Container | EV(10401, 99\_HS-KL, Voruntersuchung)                                                             | 1  | M        |           |                      |
| 16 | \>\>\>   | CONTAINS        | Code      | EV(ct\_covid\_vergleich, 99\_HS-KL, Code: Voruntersuchung)                                        | 1  | M        |           | DCID 99\_8           |
| 17 | \>\>\>   | CONTAINS        | Date      | EV(ct\_covid\_vergleich\_date, 99\_HS-KL, Datum der Voruntersuchung)                              | 1  | M        |           |                      |
| 18 | \>\>     | CONTAINS        | Container | EV(10402, 99\_HS-KL, CT-Protokoll)                                                                | 1  | M        |           |                      |
| 19 | \>\>\>   | CONTAINS        | Code      | EV(ct\_covid\_protokoll, 99\_HS-KL, Code: CT-Protokoll)                                           | 1  | M        |           | DCID 99\_9           |
| 20 | \>\>     | CONTAINS        | Container | EV(10403, 99\_HS-KL, Lungenparenchym/Atemwege)                                                    | 1  | M        |           |                      |
| 21 | \>\>\>   | CONTAINS        | Container | EV(1040301, 99\_HS-KL, Milchglastrübung)                                                          | 1  | M        |           |                      |
| 22 | \>\>\>\> | CONTAINS        | Code      | EV(ct\_covid\_milchglas, 99\_HS-Kl, Code: Milchglastrübung)                                       | 1  | M        |           | DCID 99\_10          |
| 23 | \>\>\>   | CONTAINS        | Container | EV(1040302, 99\_HS-KL, Dominantes Milchglasmuster)                                                | 1  | M        |           |                      |
| 24 | \>\>\>\> | CONTAINS        | Code      | EV(ct\_covid\_milchglasmuster, 99\_HS-KL, Code: Dominantes Milchglasmuster)                       | 1  | M        |           | DCID 99\_11          |
| 25 | \>\>\>   | CONTAINS        | Container | EV(1040303, 99\_HS-KL, Morphologie der Milchglastrübung)                                          | 1  | M        |           |                      |
| 26 | \>\>\>\> | CONTAINS        | Code      | EV(ct\_covid\_milchglasmorpho, 99\_HS-KL, Code: Morphologie der Milchglastrübung)                 | 1  | M        |           | DCID 99\_12          |
| 27 | \>\>\>   | CONTAINS        | Container | EV(1040304, 99\_HS-KL, Verteilungsmuster der Milchglastrübung)                                    | 1  | M        |           |                      |
| 28 | \>\>\>\> | CONTAINS        | Code      | EV(ct\_covid\_milchglasverteilung, 99\_HS-KL, Code: Verteilungsmuster der Milchglastrübung)       | 1  | M        |           | DCID 99\_13          |
| 29 | \>\>\>   | CONTAINS        | Container | EV(1040305, 99\_HS-KL, Seiten-Ausprägung der Milchglastrübung)                                    | 1  | M        |           |                      |
| 30 | \>\>\>\> | CONTAINS        | Code      | EV(ct\_covid\_milchglasseite, 99\_HS-KL, Code: Seiten-Ausprägung der Milchglastrübung)            | 1  | M        |           | DCID 99\_14          |
| 31 | \>\>\>   | CONTAINS        | Container | EV(1040306, 99\_HS-KL, Dominantes Lungenfeld der Milchglastrübung)                                | 1  | M        |           |                      |
| 32 | \>\>\>\> | CONTAINS        | Code      | EV(ct\_covid\_milchglasfeld, 99\_HS-KL, Code: Dominantes Lungenfeld der Milchglastrübung)         | 1  | M        |           | DCID 99\_15          |
| 33 | \>\>\>   | CONTAINS        | Container | EV(1040307, 99\_HS-KL, Ausdehnung/Serverity des Lungenbefalls quantitativ)                        | 1  | M        |           |                      |
| 34 | \>\>\>\> | CONTAINS        | Code      | EV(ct\_covid\_milchglasgrad, 99\_HS-KL, Code: Ausdehnung/Serverity des Lungenbefalls quantitativ) | 1  | M        |           | DCID 99\_16          |
| 35 | \>\>\>   | CONTAINS        | Container | EV(1040308, 99\_HS-KL, Konsolidierungs-Muster)                                                    | 1  | M        |           |                      |
| 36 | \>\>\>\> | CONTAINS        | Code      | EV(ct\_covid\_konsolidierung, 99\_HS-KL, Code: Konsolidierung)                                    | 1  | M        |           | DCID 99\_17          |
| 37 | \>\>\>\> | CONTAINS        | Code      | EV(ct\_covid\_konsolidierungmuster, 99\_HS-KL, Code: Konsolidierungmuster)                        | 1  | M        |           | DCID 99\_18          |
| 38 | \>\>\>   | CONTAINS        | Container | EV(1040309, 99\_HS-KL, Zentrilobuläre Noduli/Tree in bud)                                         | 1  | M        |           |                      |
| 39 | \>\>\>\> | CONTAINS        | Code      | EV(ct\_covid\_noduli, 99\_HS-KL, Code: Zentrilobuläre Noduli/Tree in bud)                         | 1  | M        |           | DCID 231             |
| 40 | \>\>\>   | CONTAINS        | Container | EV(10403010, 99\_HS-KL, Lungengerüstveränderung)                                                  | 1  | M        |           |                      |
| 41 | \>\>\>\> | CONTAINS        | Code      | EV(ct\_covid\_lungengerüst, 99\_HS-KL, Code: Lungengerüstveränderung)                             | 1  | M        |           | DCID 231             |
| 42 | \>\>\>\> | CONTAINS        | Text      | EV(ct\_covid\_lungengerüst\_text, 99\_Hs-Kl, Text: Lungengerüstveränderung)                       | 1  | M        |           |                      |
| 43 | \>\>     | CONTAINS        | Container | EV(10404, 99\_HS-KL, Weitere Befunde)                                                             | 1  | M        |           |                      |
| 44 | \>\>\>   | CONTAINS        | Container | EV(1040401, 99\_HS-KL, Pleuraerguss links)                                                        | 1  | M        |           |                      |
| 45 | \>\>\>\> | CONTAINS        | Code      | EV(ct\_covid\_ple\_li, 99\_HS-KL, Code: Pleuraerguss links)                                       | 1  | M        |           | DCID 99\_19          |
| 46 | \>\>\>   | CONTAINS        | Container | EV(1040402, 99\_HS-KL, Pleuraerguss rechts)                                                       | 1  | M        |           |                      |
| 47 | \>\>\>\> | CONTAINS        | Code      | EV(ct\_covid\_ple\_re, 99\_HS-KL, Code: Pleuraerguss rechtes)                                     | 1  | M        |           | DCID 99\_19          |
| 48 | \>\>\>   | CONTAINS        | Container | EV(1040403, 99\_HS-KL, Lymphknoten)                                                               | 1  | M        |           |                      |
| 49 | \>\>\>\> | CONTAINS        | Code      | EV(ct\_covid\_lk, 99\_HS-KL, Code: Lymphknoten)                                                   | 1  | M        |           | DCID 99\_20          |
| 50 | \>\>\>\> | CONTAINS        | Text      | EV(ct\_covid\_lk\_text, 99\_HS-KL, Text: Lymphknoten)                                             | 1  | M        |           |                      |
| 51 | \>\>\>   | CONTAINS        | Container | EV(1040404, 99\_HS-KL, Sonstiges)                                                                 | 1  | M        |           |                      |
| 52 | \>\>\>\> | CONTAINS        | Text      | EV(ct\_covid\_other, 99\_HS-KL, Text: Sonstiges)                                                  | 1  | M        |           |                      |
| 53 | \>       | CONTAINS        | Container | EV(105, 99\_HS-KL, Beurteilung)                                                                   | 1  | M        |           |                      |
| 54 | \>\>     | CONTAINS        | Container | EV(10501, 99\_HS-KL, Klassifikation des Lungenbefalls)                                            | 1  | M        |           |                      |
| 55 | \>\>\>   | CONTAINS        | Code      | EV(ct\_covid\_class, 99\_HS-KL, Code: Klassifikation des Lungenbefalls)                           | 1  | M        |           | DCID 99\_21          |
| 56 | \>\>     | CONTAINS        | Container | EV(10502, 99\_HS-KL, Sonstiges)                                                                   | 1  | M        |           |                      |
| 57 | \>\>\>   | CONTAINS        | Text      | EV(ct\_covid\_Beurteilung, 99\_HS-KL, Text: Sonstiges)                                            | 1  | M        |           |                      |
 
