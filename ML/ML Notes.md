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

## Lecture 4: Naive Bayes
##### The Naive Bayes Implementation
The Naive Bayes assumes that all probabilities are independent. 

We have that for ever class $j$,

$Pr(x_1,x_2,\dots,x_n | c_j) \approx \prod_{i=1}P(x_i | c_j)$

This is called a **conditional independence assumption**, and makes Naive Bayes a tractable method. 

```python
for every test instance:
    for every attribute in test instance:
        for every class label:
            calculate the probability (conditional independence)
    return the largest probability and find the corresponding class label
```

##### Probabilistic Smoothing
If you note the formula before, then multiplying any probability of 0 results in 0. This means that unseen events become an "impossible" event, which is untrue.

**Using epsilon:**  
To combat this, we assume that **no event is impossible** (i.e. every probability is greater than 0). This is implemented by replacing 0 with a value $\epsilon\rightarrow 0$, where $1+\epsilon \approx 1$, so we don't need change our approach with non-zero probabilities. 

**Using Laplace smoothing (or add-one):**   
BETTER ALTERNATIVE - *add-k smoothing*.  
Laplace smoothing essentially gives unseen events a count of 1. Then, all counts are increased to ensure that monotonicity is maintained. Let $V = \textrm{Number of attributes},

Then for every class $j$, and event $i$,  
$\hat{Pr}(x_i | c_j) = \frac{1 + freq(x_i, c_j)}{V + freq(c_j)}

##### Missing Values
- If a value is missing in a test instance, it is possible to just simply ignore that feature for the purposes of classification.    
- If a value is missing in a training instance, then it is possible to simply have it no contribute to the attribute-value counts/probability estimates for that feature. 
```python
if value == missing:
    pass
```