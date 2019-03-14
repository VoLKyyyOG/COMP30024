COMP300027 - Machine Learning, The University of Melbourne
=========

LSM Notes: https://www.overleaf.com/1157211432bhswsxwjccmk 

## Lecture 2: Basics of Machine Learning
##### Some Terminology
- Instances (exemplars) are the rows of a dataset
- Attributes (features) are the columns of a dataset
- Concepts (labels or classes) are things we aim to learn from the dataset
- Nominal Quantities (categorical or discrete) have no relation between labels (`sunny, hot, rainy`)
- Ordinal Quantities have an implied ordering on the values (`cold < mild < hot`)
- Continuous Quantities are real-valued attributes with a defined zero point and no explicit upper bound

##### Methods
- **Supervised** methods have prior knowledge to a closed set of classes. Essentially "feed it" data and hope it can train itself to predict it.
- **Unsupervised** methods will dynamically discover "classes". These don't require labels and will train itself to categorize instances (usually mathematically).

##### Classification
- The learning algorithm is provided with a set of classified **training data**
- Uses the Split -> Test -> Train method to test for accuracy
- A **supervised** algorithm
- Works with *discrete* or *categorical* data

##### Clustering
- Finds groups of items that are similar 
- Works purely on a distance metric and therefore *does not* require a label
- Performance is subjective and is problematic when evaluating
- An **unsupervised** algorithm

##### Regression
- Technically a type of *Classification Learning*, but works with continuous data
- A **supervised** algorithm

##### Association Learning
- Detects patterns, associations or correlations among a set of items or objects
- Any kind of association is considered interesting with no "care" for what we want to predict
- An **unsupervised** algorithm

##### Values
- **Missing Values** can be caused by:
    - Malfunction equipment
    - Changes in experimental design
    - Collation of different datasets
    - A non-possible measurement
- **Inaccurate Values** can be caused by:
    - Errors or omissions that don't impact the data (`Age of Customer, Location`)
    - Typos when entering data
    - Deliberately false data to protect their own privacy

## Lecture 3: Revision of Probability Theory
##### Bayes Rule
$Pr(A|B) = \frac{Pr(A\cap B)}{Pr(B)} = \frac{Pr(B|A)Pr(A)}{Pr(B)}$
- $Pr(A)$, the prior, is the initial degree of belief in $A$
- $Pr(A|B)$, the posterior, is the degree of belief having counted for B

##### Some distributions you should know
- Bernoulli
- Binomial
- Multinomial

##### Entropy (Information Theory)
**Entropy**: a measure of *unpredictability* on the information required to predict an event.  
The entropy (in *bits*) of a discrete r.v $X$ is defined as:  

$H(X) = -\sum^n_{i=1}Pr(x_i)\log_2(Pr(x_i))$ where $H(X) \in [0, \log_2(n)]$.
- A **high** entropy value means $X$ is unpredictable. Each outcome gives *one bit* of information
- A **low** entropy value means $X$ is more predictable. We don't learn anything once we see the outcome

##### Entropy Example:
Let $Pr(X = Heads) = 0.9, Pr(X = Tails) = 0.1$. Then  

$
H(X) = -[Pr(X = Heads)\log_2(Pr(X = Heads)) + Pr(X = Tails)\log_2(Pr(X = Tails))] \\
= -[0.9\log_2(0.9) + 0.1\log_2(0.1)]\\
= 0.47
$

##### Estimating Probabilities (Frequentist Method)
If we don't have the whole population, we can take a sample of it to estimate the relative distribution (MLE in stats). 

$\hat{Pr}(X=x) = \frac{freq(x)}{\sum^k_{i=1}freq(x_k)} = \frac{freq(X)}{N}$

$\hat{Pr}(X=x,Y=y) = \frac{freq(x,y)}{N}$

$\hat{Pr}(X=x|Y=y) = \frac{freq(x,y)}{N}$










