Current Results
======
****************************************  
Enter k value for k-Fold Cross Validation: 10  
Drop all columns with absolutely no information gain? (y/n): y  
Print the information gain? (y/n): y  
****************************************  
Processing anneal.csv ...  
TESTING ON THE TRAIN DATA  
InfoGain(family | class) = 0.40908953764450995  
InfoGain(steel | class) = 0.30605153542894037  
InfoGain(carbon | class) = 0.051344088764403883  
InfoGain(hardness | class) = 0.2910822058599468  
InfoGain(temper_rolling | class) = 0.1471188622809554  
InfoGain(condition | class) = 0.21372288031590858  
InfoGain(formability | class) = 0.29223544065798424  
InfoGain(strength | class) = 0.1261663361036094  
InfoGain(non-ageing | class) = 0.1410737916381286  
InfoGain(surface-finish | class) = 0.032488406491841815  
InfoGain(surface-quality | class) = 0.4351778362628853  
InfoGain(enamelability | class) = 0.03870173274881039  
InfoGain(bc | class) = 0.0004376065202116308  
InfoGain(bf | class) = 0.039355574142836636  
InfoGain(bt | class) = 0.021775078259213432  
InfoGain(bw-me | class) = 0.03799747881351134  
InfoGain(bl | class) = 0.03670308136440803  
InfoGain(chrom | class) = 0.11722522630372034  
InfoGain(phos | class) = 0.029753745208638716  
InfoGain(cbond | class) = 0.027042353328676327  
InfoGain(exptl | class) = 0.015604780443500221  
InfoGain(ferro | class) = 0.13718113252042552  
InfoGain(bbvc | class) = 0.02239708985164568  
InfoGain(lustre | class) = 0.01824168402125026  
InfoGain(shape | class) = 0.043239605565149386  
InfoGain(oil | class) = 0.03303757117705697  
InfoGain(bore | class) = 0.019378864328318812  
InfoGain(packing | class) = 0.003958783545891853  
Accuracy for Testing on the Training Data: 99.11%  

10-FOLD CROSS VALIDATION  
... ...  
Accuracy using k-Fold Cross Validation: 98.89% 96.67% 98.89% 98.89% 98.89% 97.78% 100.00% 100.00% 100.00% 100.00%  
Average 10-Fold Cross Validation Accuracy: 99.00%  
****************************************  
Processing breast-cancer.csv ...  
TESTING ON THE TRAIN DATA  
InfoGain(age | class) = 0.010605956535614136  
InfoGain(menopause | class) = 0.0020016149737116518  
InfoGain(tumor-size | class) = 0.05717112532429669  
InfoGain(inv-nodes | class) = 0.06899508808988597  
InfoGain(node-caps | class) = 0.05136145395409375  
InfoGain(deg-malig | class) = 0.07700985251661441  
InfoGain(breast | class) = 0.0024889884332652823  
InfoGain(breast-quad | class) = 0.009338656255899025  
InfoGain(irradiat | class) = 0.025819023909141037  
Accuracy for Testing on the Training Data: 75.87%  

10-FOLD CROSS VALIDATION  
... ...  
Accuracy using k-Fold Cross Validation: 82.76% 72.41% 92.86% 75.86% 78.57% 68.97% 67.86% 79.31% 67.86% 68.97%  
Average 10-Fold Cross Validation Accuracy: 75.54%  
****************************************  
Processing car.csv ...  
TESTING ON THE TRAIN DATA  
InfoGain(buying | class) = 0.09644896916961376  
InfoGain(maint | class) = 0.07370394692148574  
InfoGain(doors | class) = 0.004485716626631886  
InfoGain(persons | class) = 0.21966296333990798  
InfoGain(lug_boot | class) = 0.030008141247605202  
InfoGain(safety | class) = 0.26218435655426375  
Accuracy for Testing on the Training Data: 87.38%  

10-FOLD CROSS VALIDATION  
... ...  
Accuracy using k-Fold Cross Validation: 87.28% 86.71% 85.55% 90.17% 83.24% 84.39% 87.79% 86.13% 83.72% 84.97%  
Average 10-Fold Cross Validation Accuracy: 86.00%  
****************************************  
Processing cmc.csv ...  
TESTING ON THE TRAIN DATA  
InfoGain(w-education | class) = 0.07090633894894571  
InfoGain(h-education | class) = 0.0401385992293839  
InfoGain(n-child | class) = 0.10173991727554066  
InfoGain(w-relation | class) = 0.00982050143438462  
InfoGain(w-work | class) = 0.002582332379721386  
InfoGain(h-occupation | class) = 0.030474214560266333  
InfoGain(standard-of-living | class) = 0.03251146005380634  
InfoGain(media-exposure | class) = 0.015786455595619975  
Accuracy for Testing on the Training Data: 50.58%  

10-FOLD CROSS VALIDATION  
... ...  
Accuracy using k-Fold Cross Validation: 51.70% 44.90% 53.74% 48.98% 50.00% 48.98% 49.32% 53.06% 49.32% 42.86%  
Average 10-Fold Cross Validation Accuracy: 49.29%  
****************************************  
Processing hepatitis.csv ...  
TESTING ON THE TRAIN DATA  
InfoGain(sex | class) = 0.03660746514280977  
InfoGain(steroid | class) = 0.013721237647576712  
InfoGain(antivirals | class) = 0.014490701150154384  
InfoGain(fatigue | class) = 0.08315059666094515  
InfoGain(malaise | class) = 0.08228641352644739  
InfoGain(anorexia | class) = 0.011963525360643712  
InfoGain(liver-big | class) = 0.00702561259050305  
InfoGain(liver-firm | class) = 0.0002889437074383716  
InfoGain(spleen-palpable | class) = 0.03517926772302904  
InfoGain(spiders | class) = 0.10367840650872329  
InfoGain(ascites | class) = 0.1275186922033822  
InfoGain(varices | class) = 0.07645578607607972  
InfoGain(histology | class) = 0.08493296456638777  
Accuracy for Testing on the Training Data: 84.52%  
  
10-FOLD CROSS VALIDATION  
... ...  
Accuracy using k-Fold Cross Validation: 81.25% 86.67% 100.00% 80.00% 81.25% 93.33% 68.75% 86.67% 62.50% 86.67%  
Average 10-Fold Cross Validation Accuracy: 82.71%  
****************************************  
Processing hypothyroid.csv ...  
TESTING ON THE TRAIN DATA  
InfoGain(sex | class) = 0.0002272085595206863  
InfoGain(on-thyroxine | class) = 0.0009139351160850073  
InfoGain(query-on-thyroxine | class) = 0.0012382074503017315  
InfoGain(on_antithyroid | class) = 0.00014844815831743796  
InfoGain(surgery | class) = 0.0009985293906336068  
InfoGain(query-hypothyroid | class) = 0.0013683791752741592  
InfoGain(query-hyperthyroid | class) = 0.0005423006444423839  
InfoGain(pregnant | class) = 0.0004350938464638965  
InfoGain(sick | class) = 0.0004888757691284829  
InfoGain(tumor | class) = 0.0008983004044028076  
InfoGain(lithium | class) = 4.463778824304043e-05  
InfoGain(goitre | class) = 7.868469847943649e-05  
InfoGain(TSH | class) = 0.009353710215580346  
InfoGain(T3 | class) = 0.004075493419623766  
InfoGain(TT4 | class) = 0.005792553705846859  
InfoGain(T4U | class) = 0.005768288201614624  
InfoGain(FTI | class) = 0.005744031245602799  
InfoGain(TBG | class) = 0.002580427555574416  
Accuracy for Testing on the Training Data: 95.23%  

10-FOLD CROSS VALIDATION  
... ...  
Accuracy using k-Fold Cross Validation: 94.62% 96.20% 95.57% 94.62% 95.25% 94.32% 96.52% 93.38% 93.67% 98.11%  
Average 10-Fold Cross Validation Accuracy: 95.23%  
****************************************  
Processing mushroom.csv ...  
TESTING ON THE TRAIN DATA  
InfoGain(cap-shape | class) = 0.04879670193537311  
InfoGain(cap-surface | class) = 0.028590232773772706  
InfoGain(cap-color | class) = 0.03604928297620391  
InfoGain(bruises | class) = 0.19237948576121977  
InfoGain(odor | class) = 0.9060749773839999  
InfoGain(gill-attachment | class) = 0.014165027250616302  
InfoGain(gill-spacing | class) = 0.10088318399657048  
InfoGain(gill-size | class) = 0.23015437514804604  
InfoGain(gill-color | class) = 0.41697752341613137  
InfoGain(stalk-shape | class) = 0.007516772569664321  
InfoGain(stalk-root | class) = 0.10834857380797525  
InfoGain(stalk-surface-above-ring | class) = 0.2847255992184845  
InfoGain(stalk-surface-below-ring | class) = 0.2718944733927465  
InfoGain(stalk-color-above-ring | class) = 0.2538451734622399  
InfoGain(stalk-color-below-ring | class) = 0.24141556652756657  
InfoGain(veil-color | class) = 0.02381701612091669  
InfoGain(ring-number | class) = 0.03845266924309054  
InfoGain(ring-type | class) = 0.3180215107935377  
InfoGain(spore-print-color | class) = 0.4807049176849154  
InfoGain(population | class) = 0.2019580190668524  
InfoGain(habitat | class) = 0.156833604605092  
Accuracy for Testing on the Training Data: 99.58%  

10-FOLD CROSS VALIDATION  
... ...  
Accuracy using k-Fold Cross Validation: 99.51% 99.63% 100.00% 99.75% 99.75% 99.51% 99.01% 99.51% 99.51% 99.75%  
Average 10-Fold Cross Validation Accuracy: 99.59%  
****************************************  
Processing nursery.csv ...  
TESTING ON THE TRAIN DATA  
InfoGain(parents | class) = 0.07293460750309944  
InfoGain(has_nurs | class) = 0.1964492804881155  
InfoGain(form | class) = 0.005572591715219843  
InfoGain(children | class) = 0.011886431475775838  
InfoGain(housing | class) = 0.019602025022872116  
InfoGain(finance | class) = 0.0043331270252000564  
InfoGain(social | class) = 0.02223261689401812  
InfoGain(health | class) = 0.9587749604699762  
Accuracy for Testing on the Training Data: 90.31%  

10-FOLD CROSS VALIDATION  
... ...  
Accuracy using k-Fold Cross Validation: 89.04% 89.35% 90.20% 91.20% 90.74% 91.13% 90.66% 91.20% 89.35% 90.59%  
Average 10-Fold Cross Validation Accuracy: 90.35%  
****************************************  
Processing primary-tumor.csv ...  
TESTING ON THE TRAIN DATA  
InfoGain(age | class) = 0.15474214188705826  
InfoGain(sex | class) = 0.32289865796149675  
InfoGain(histologic-type | class) = 0.3103754746615519  
InfoGain(degree-of-diffe | class) = 0.199205643547415  
InfoGain(bone | class) = 0.2124618990481646  
InfoGain(bone-marrow | class) = 0.020366938848046967  
InfoGain(lung | class) = 0.10088123982398978  
InfoGain(pleura | class) = 0.0678727757044224  
InfoGain(peritoneum | class) = 0.22052193470670467  
InfoGain(liver | class) = 0.19976143639025112  
InfoGain(brain | class) = 0.06714460241010434  
InfoGain(skin | class) = 0.054013531994907105  
InfoGain(neck | class) = 0.2915301360224922  
InfoGain(supraclavicular | class) = 0.12715354518198208  
InfoGain(axillar | class) = 0.24010574063173618  
InfoGain(mediastinum | class) = 0.18425767171538432  
InfoGain(abdominal | class) = 0.1701481108388716  
Accuracy for Testing on the Training Data: 57.52%  
  
10-FOLD CROSS VALIDATION  
... ...  
Accuracy using k-Fold Cross Validation: 50.00% 41.18% 47.06% 47.06% 55.88% 35.29% 58.82% 41.18% 44.12% 39.39%  
Average 10-Fold Cross Validation Accuracy: 46.00%  
****************************************  
======
  
This file describes the various data files associated with Project 1 for COMP30027 Machine Learning in Semester 1 2019. References for the data files are listed in the accompanying Project specifications.

The archive contains eleven files, of which nine are data files in (approximately) CSV format, headers.txt is a text file contains the corresponding CSV headers (if you require them), and README.txt is this file.

The data files are formatted as follows:
  - one instance per line;
  - each line is comprised of a list of attribute values separated by commas --- all attributes are categorical, but no attribute value contains the comma character or any space character, and consequently are not surrounded by quotation marks;
  - the final attribute is the class of the corresponding instance.


Detailed descriptions of the various datafiles:

anneal.csv
==========
This file is derived from the Annealing dataset (https://archive.ics.uci.edu/ml/datasets/Annealing). It is comprised of 989 instances, with 35 attributes (36 including the class). Hypothetically, there are six possible class labels, however, only five are attested in the dataset: {1, 2, 3, 4, U}. Some continuous attributes were removed from the original dataset. By convention, there are no missing attribute values in this dataset.

breast-cancer.csv
=================
This file is derived from the Breast Cancer dataset (https://archive.ics.uci.edu/ml/datasets/Breast+Cancer). It is comprised of 286 instances, with 9 attributes (10 including the class). There are two possible class labels: {recurrence-events, no-recurrence-events}. There are a small number of missing values in this dataset, which are indicated by a question mark ("?").

car.csv
=======
This file is derived from the Car Evaluation dataset (https://archive.ics.uci.edu/ml/datasets/Car+Evaluation). It is comprised of 1728 instances, with 6 attributes (7 including the class). There are four possible class labels: {unacc, acc, good, vgood}. There are no missing values in this dataset.

cmc.csv
=======
This file is derived from the Contraceptive Method Choice dataset (https://archive.ics.uci.edu/ml/datasets/Contraceptive+Method+Choice). It is comprised of 1473 instances, with 8 attributes (9 including the class). There are three possible class labels: {No-use, Short-term, Long-term}. There are no missing values in this dataset.

hepatitis.csv
=============
This file is derived from the Hepatitis dataset (https://archive.ics.uci.edu/ml/datasets/Hepatitis). It is comprised of 155 instances, with 13 attributes (14 including the class). There are two possible class labels: {LIVE, DIE}. Some continuous attributes were removed from the original dataset. There are a moderate number of missing values in this dataset, which are indicated by a question mark ("?").

hypothyroid.csv
===============
This file is derived from the Thyroid Disease dataset (https://archive.ics.uci.edu/ml/datasets/Thyroid+Disease). It is comprised of 3163 instances, with 18 attributes (19 including the class). There are two possible class labels: {hypothyroid, negative}. Some continuous attributes were removed from the original dataset. There are a moderate number of missing values in this dataset, which are indicated by a question mark ("?").

mushroom.csv
============
This file is derived from the Mushroom dataset (https://archive.ics.uci.edu/ml/datasets/Mushroom). It is comprised of 8124 instances, with 22 attributes (23 including the class). There are two possible class labels: {e, p}. There are a large number of missing values in this dataset, which are indicated by a question mark ("?").

nursery.csv
===========
This file is derived from the Nursery dataset (https://archive.ics.uci.edu/ml/datasets/Nursery). It is comprised of 12960 instances, with 8 attributes (9 including the class). There are five possible class labels: {not_recom, recommend, very_recom, priority, spec_prior}. There are no missing values in this dataset.

primary-tumor.csv
=================
This file is derived from the Primary Tumor dataset (https://archive.ics.uci.edu/ml/datasets/Primary+Tumor). It is comprised of 339 instances, with 17 attributes (18 including the class). Hypothetically, there are twenty-two possible class labels, however, only twenty-one are attested in the dataset: {A, B, C, D, E, F, G, H, J, K, L, M, N, O, P, Q, R, S, T, U, V}. The class labels have been abstracted away from more meaningful labels. There are a large number of missing values in this dataset, which are indicated by a question mark ("?").
