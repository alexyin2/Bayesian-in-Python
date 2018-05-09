# Bayesian in Machine Learning using Python
* This is a practice of helping me to learn the background mathematics in Bayesian.
* I'll write down anything that I've learned and thought it was important in this procedure. 
* This practice is based on [LazyProgrammer.me](https://github.com/lazyprogrammer)

***
## A/B test
1. We need to know what t-test means in statistics. I'll suggest [Wikipedia](https://en.wikipedia.org/wiki/Student%27s_t-test)
2. Bonferroni Correction. I'll suggest [Wikipedia](https://en.wikipedia.org/wiki/Bonferroni_correction)
3. Chi-Squared test. I'll suggest [Wikipedia](https://en.wikipedia.org/wiki/Chi-squared_test)
4. There is always a question that bothers me since I've learned p-value. THis is a statement quoted from a research paper: **_If such hypothesis is not rejected, it is usually because the sample size is too small.(Nunnally 1960)_** If so, then why is p-value still so popular in the world and lots of statistics experiments still use it as a judgement.

__Ans__: We'll have to consider two cases in calculating p-value: 
* The cost of increasing the samples. 

  In this case, we'll take t-test as an example. 
  
  In t-test, there is ![sqrt(n)](https://latex.codecogs.com/gif.latex?%5Csqrt%7Bn%7D) in our denominator. 
  
  It means that although we can increase the sample to make our t smaller, there's not much big influence comparing n = 100 to n = 300 because there's a square root.
* How large the difference will we accept it as useful or meaningful?

