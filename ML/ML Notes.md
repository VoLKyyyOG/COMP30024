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
$\hat{Pr}(x_i | c_j) = \frac{1 + freq(x_i, c_j)}{V + freq(c_j)}$

##### Missing Values

- If a value is missing in a test instance, it is possible to just simply ignore that feature for the purposes of classification.  
- If a value is missing in a training instance, then it is possible to simply have it no contribute to the attribute-value counts/probability estimates for that feature. 

```python
if value == missing:
    pass
```

## Lecture 5: Evaluation Part 1
The basic evaluation metric is *Accuracy*.  

$\textrm{Accuracy} = \frac{\textrm{Number of correctly labelled test instances}}{\textrm{Total number of test instances}}$  

Quantifies how frequently the classifier is correct, with respect to a fixed dataset with known labels. 

##### Strategies

Two main different strategies to evaluate your model.  


**Holdout:**  
- Each instance is randomly assigned as either a training instance or a test instance.
- The dataset is effectively partitioned with no overlap between datasets
- You build the model based on the trainin instance, and evaluate the trained model with the test instances
- Common train - test splits are: 50 - 50, 80 - 20, 90 - 10
- Advantages:
  - Simple to work with and implement
  - Fairly high reproducibility
- Disadvantages:
  - The split ratio affects the estimate of the classifier's behavior
    - Lots of test instances with few training instances leaves the model to build an inaccurate model
    - Lots of training instances with few test instannces leaves the model to be accurate, but the test data may not be representative

**Repeated Random Subsampling:**  
- Works similar to **holdout**, but over several iterations
  - New training set and test set are randomly chosen each iteration
  - The size of train-test split is fixed accross the iterations
  - A new model is built every iteration
- Advantages: 
  - Average holdout method tends to produce more reliable results
- Disadvantages:
  - Slower than the holdout method (by a constant factor)
  - A wrong choice of train-test split can lead to highly misleading results

**Cross-Validation:**  
- The **usual preferred method of evaluation**
- The dataset is progressively split into a number of $m$ partitions
  - One partition is used as test data
  - The other $m - 1$ partitions are used as training data
  - Evaluation metric is aggregated across the $m$ partitions
    - Take the average
    - Sum the accuracy across iterations
- Why is this better than holdout / repeated random subsampling?
  - Every instance is a test instance (for some partition)
    - Similar to testing on the training data, but without the dataset overlap
  - Takes roughly the **same time** as Repeated Random Subsampling
  - Can be shown to **minmise the bias and variance** of our estimates of the classifier's performance
- How big is $m$?
  - Small $m$: more instances per partition, **more variance** in performance estimates
  - Large $m$: fewer instances per partition, **less variance** but slower
  - We usually choose $m = 10$ which mimics the 90 - 10 holdout strategy
- An alternative is to use $m = N,\textrm{ the number of test instances}$ - called the **Leave One Out Cross Validation**
  - Maximises the training data for the model
  - Mimics the actual testing behaviour
  - **Far too slow to use in practice**

**Stratification:**  
- A type of inductive learning hypothesis
  - Any hypothesis found to approximate the target function over a large training dataset will also approximate the target function well over any **unseen** test examples
- However, machine learning suffers from **inductive bias** meaning assumptions must be made about the data to build a model and make predictions
- Stratification assumes that the **class distribution** of unseen instances will share the same distribution of see ninstances
  - Class distribution is used here to extend definitions from continuous domain to discrete domain 

##### Determining if a Classifier is Good
For a **two class* problem, we can assume:
- An *Interesting Class* I
- An *Uninteresting Class* U

A classifier may then classify:
- An Interesting Instance as I if it is True Positive (TP)
- An Interesting Instance as U if it is False Negative (FN)
- An Uninteresting Instance as I if it is False Positive (FP)
- An Uninteresting Instance as U if it is True Negative (TN)

##### Classification Accuracy
Classification Accuracy is the proportion of instances for which we have correctly predicted the label, given as  

$\textrm{Classification Accuracy} = \frac{TP + TN}{TP + FP + FN + TN}$

##### Error Rate
An Error Rate can also be used, where $ER = 1 - \textrm{Classification Accuracy}$

##### Precision and Recall
Given with respect to the **interesting class=** only
- Precision: How often are we correct, when we predict that an instance is interesting
  - $\textrm{Precision} = \frac{TP}{TP + FP}$
- Recall: What proportion of the truly interesting instances have we correctly identified as interesting
  - $\textrm{Recall} = \frac{TP}{TP + FN}$

High precision gives low recall, and high recall gives low precision. But, we want both precision and recall to be high. A popular metric that evaluates this is called the **F-Score**.

$F_\beta = \frac{(1+\beta^2)2PR}{\beta^2P + R}$  

$F_1 = \frac{2PR}{P + R}$

##### Baseline vs Benchmark
A **Baseline** is a naive method which we would expect any reasonably well-developed method to better it.
- Important in establishing whether any proposed method is doing better than "dumb and simple"
- Valuable in getting a sense for the intrinsic difficulty of a given task
  - Baseline accuracy of 5% vs 99%

A **Benchmark** is an established rival technique which we are pitching our method against (does our model perform better)

##### Types of Baseline
**Random Baseline:**  
- Method 1: randomly assign a class to each test instance
- Method 2: randomly assign a class $c_k$ to each test instance, weight the class assignment according to $Pr(c_k)$
  - Assumes we know the class prior probabilities

**Zero-R (or Majority Class):**  
- Method: classifies all instances according to the most common class in the training data
- Not appropriate if the majority class is "FALSE" and the learning task is to identify the "TRUE"s

**One-R:**
Creates a single rule for each attribute in the training data, then selects the rule with the **smallest error rate** as its "one rule"
- Method: create a *decision stump* for each attribute with branches for each value, then populate the leaf with the majority class at that leaf. Then, select the decision stump which leads to the lowest error rate over the training data  
  
```python
for each attribute:
    for each value of the attribute:
        count the class frequency
        find the most frequent class
        assing the class to the rule
    calculate the error rate of the rules
choose the attribute whose rules produce the smallest error rate
```

- Advantages:
  - Simple to understand and implement
  - Suprisingly good results
- Disadvantages:
  - Unable to capture attribute interactions
  - Bias towards attributes with several possible values

## Lecture 6: Decision Trees (ID3)
- Basic method: construct decision trees in recursive divide-and-conquer fashion
```python
def ID3(root):
    if all instances at root have same class:
        return 
    else:
        - select a new attribute to use in a partitioning root node instance
        - create a branch for each attribute value and partition up root node instances according to each value
        for each leaf node:
            ID3(leaf)
```

##### Information Gain
The expected *reduction* in entropy caused by knowing the value of an attribute.  
Compare:
- The entropy before splitting the tree using the attribute's values
- The weighted average of the entropy over the children after the split (known as **Mean Information**)  
- 
If the entropy *decreases*, then we have a better tree (more predictable)

##### Mean Information
We calculate the mean information for a tree stump with $m$ attribute values as:  

$\textrm{Mean Info}(x_1,x_2,\dots,x_m) = \sum^m_{i = 1}Pr(x_i)H(x_i)$

where $H(x_i)$ is the entropy of the class distribution for the instances at node $x_i$.

##### Analysis of Information Gain
Information gain tends to prefer highly-branching attributes
- A subset of instances is more likely to be homogeneous (all of a single class) if there are only a few instances
- Attributes with many values will have fewer instances at each child node

These factors may result in overfitting or fragmentation

##### Gain Ratio
- Gain Ratio (GR) reduces the bias for information gain towards highly branching attributes by normalizing relative to the split information
- Split Info (SI) (or called Intrinsic Value) is the entropy of a given split (evenness of the distribution of instances to attribute values)

$GR(R_A | R) = \frac{H(R) - \sum^m_{i=1}Pr(x_i)H(x_i)}{-\sum^m_{i=1}Pr(x_i)log_2(Pr(x_i))}$

##### Stopping Criteria
ID3 is defined in a way such that:
- The Info Gain / Gain Ratio allows us to choose the seemingly better attribute at a given node
- It is an approximate indication of how much absolute improvement we expect from partitioning the data according the values of a given attribute
- An Info Gain of $0$, or close to $0$ means that there is no improvement and is often unjustifiable
- A typical modification of ID3 is to choose the best attribute given it is greater than some threshold $\tau$
- Can be pruned to drop undesirable branches with close to no Info Gain / Gain Ratio improvements 

##### ID3 Decision Tree Analysis
- Highly regarded among basic supervised learners
- Fast train and classification
- Suspectible to the effects of irrelevant features
- Alternative Decision Trees:
  - **Oblivious Decision Trees** require the same attribute at every node in a layer
  - **Random Trees** only use samples of the possible attributes at any given node
    - Helps to account for irrelvant attributes
    - Basis for a better Decision Tree variant called the **Random Forest**