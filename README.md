# Bayesian in Machine Learning using Python
* This is a practice of helping me to learn the background mathematics in Bayesian.
* I'll write down anything that I've learned and thought it was important in this procedure. 
* This practice is based on [LazyProgrammer.me](https://github.com/lazyprogrammer)

***
## Student's t-test
1. We need to know what t-test means in statistics. I'll suggest [Wikipedia](https://en.wikipedia.org/wiki/Student%27s_t-test)
2. Bonferroni Correction. I'll suggest [Wikipedia](https://en.wikipedia.org/wiki/Bonferroni_correction)
3. Chi-Squared test. I'll suggest [Wikipedia](https://en.wikipedia.org/wiki/Chi-squared_test) and [This Website](http://www.ling.upenn.edu/~clight/chisquared.htm)
4. There is always a question that bothers me since I've learned p-value.  
This is a statement quoted from a research paper: **_If such hypothesis is not rejected, it is usually because the sample size is too small.(Nunnally 1960)_**  
If so, then why is p-value still so popular in the world and lots of statistics experiments still use it as a judgement?

__*Ans*__ : 

We'll have to consider two cases in calculating p-value: 
> 1. The cost of increasing the samples.  
> >* In this case, we'll take t-test as an example.   
> >* In t-test, there is ![sqrt(n)](https://latex.codecogs.com/gif.latex?%5Csqrt%7Bn%7D) in our denominator.  
> >* It means that although we can increase the sample to make our t smaller, there's not much big influence comparing n = 100 to n = 300 because there's a square root.   
> >* So if the company or labotory want to reject the null hypothesis, they may need to choose n = 1000, which may increase the cost for finding more samples and may not be profitable.  

> 2. How large should be the difference that we will accept it as useful or meaningful?  
> >* Keep in mind that there's always a balance between money and efficiency.  
> >* For example, if we really increase our sample and showed that there's a difference between A for 30.0% click rate and B for 30.1% click rate.  
> >* Is it really meaningful for the company to select B?  

***
## Chi square test  
1. There are three types of Chi square tests and each fit in different purposes.  
2. Also Remember that Chi square test requires that the data cannot be less than 5 in each sample.(Not that specific)  
3. I'll start introduce three types of Chi square test:  
> 1. Chi square Goodness of Fit  
> >The purpose of this test is to see that if the distribution follows what we expected.  
> >For example, we would like to see if babies born in different months are different  

> 2. Chi square test of Independence  
> >The purpose of this test is to see if the two variables are independent.  
> >For example, we would like to see if failing a class or not in subject A is independent to failing a class or not in subject B.  

> 3. Chi square test of Homogeneity
> >The step of doing this test is the same as Chi square test of Independence, but the purpose is different.  
> >The purpose of this test is to see if the data are from the same population or if they all follow the same distributions.
> >For example, we would like to see if 
