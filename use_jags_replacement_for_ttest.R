# Suppose we have two manufactures and we are interested in figuring out which 
# manufacture makes the best widgets, as measured by their lifetime.
# To determine this, we obtain 9 widgets from manufacture 1 and 4 widgets from 
# manufacture 2. The results are given below:
x1 = c(41.26, 35.81, 36.01, 43.59, 37.50, 52.70, 42.43, 32.52, 56.20)
x2 = c(54.97, 47.07, 57.12, 40.84)
mean(x1); mean(x2); sd(x1); sd(x2)  # Get the basic informations

# Mostly, we will often start a t-test on x1 and x2, just like what I did below:
t.test(x1, x2, alternative = c('two.sided'), conf.level = 0.95)
# The result shows that p-value = 0.1301, which doesn't reject our null hypothesis.
# It may imply that there's no significant difference between the two manufactures.
# But is it really true? Do we have other different ways to test about it?


# Here comes the Bayesian!!
library('rjags')
# We will go through three different priors and see how it will affect our solution.


# Prior 1: Very Vague
model = "model
{
  # Prior(Note that we assume that the two groups have the same standard deviation)
  mu1 ~ dnorm(0, 1/1000^2)  # mean = 0, sd = 1000
  mu2 ~ dnorm(0, 1/1000^2)
  log_sigma ~ dunif(-10, 10)
  sigma = exp(log_sigma)
  
  # Likelihood
  for(i in 1:N1)
  {
    x1[i] ~ dnorm(mu1, 1/sigma^2)
  }
  for(i in 1:N2)
  {
    x2[i] ~ dnorm(mu2, 1/sigma^2)
  }
}
"

data = list(x1 = x1, x2 = x2, N1 = length(x1), N2 = length(x2))
variable_names = c('mu1', 'mu2', 'sigma')
burn_in = 500
steps = 5000
thin = 1
fileConn=file("model.temp")
writeLines(model, fileConn)
close(fileConn)

if(all(is.na(data)))
{
  m = jags.model(file="model.temp")
} else
{
  m = jags.model(file="model.temp", data=data)
}
update(m, burn_in)
draw = jags.samples(m, steps, thin=thin, variable.names = variable_names) 

# Convert to a list
make_list <- function(draw)
{
  results = list()
  for(name in names(draw))
  {
    # Extract "chain 1"
    results[[name]] = as.array(draw[[name]][,,1])
    # Transpose 2D arrays
    if(length(dim(results[[name]])) == 2)
      results[[name]] = t(results[[name]])
  }
  return(results)
}
results = make_list(draw)

hist(results$mu1, breaks = 100)
hist(results$mu2, breaks = 100)
plot(results$mu1, results$mu2, cex=0.1, xlab='mu1', ylab='mu2')
# Conclusion of Prior 1:
# This prior may be have a few problems in this data.
# What is the probability that mu1 = mu2? In classical t-tests, the whole point is to
# test the hypothesis that the two 'population means' are equal.
# However, our prior actually implies that the probability they are equal is nearly 0!
# Therefore, no matter what data we get, the posterior probability of mu1 = mu2 will
# always be zero.



# Prior 2: They might be equal!
# The problem with prior 1 is that mu1 has no chance to be the same to mu2.
# So here's another way we set up our priors.
# We'll start by defining the prior mu1 as we did in prior 1, then we consider mu2, 
# we need a way of giving it a 50% probability of equalling mu1, and if not, it 
# should have a 'bi-exponential' distribution centered around mu1.
model = "model
{
  # Prior
  # First mean
  mu1 ~ dnorm(0, 1/1000^2)  # mean = 0, sd = 1000
  
  # Prior for difference, mu2 - mu1
  u ~ dunif(-1, 1)
  
  # Length of exponential prior given difference != 0
  L = 5
  size_of_difference = step(u)*(-L*log(1 - u))
  
  # To make the difference positive or negative
  C ~ dbin(0.5, 1)
  difference = (2*C - 1)*size_of_difference
  
  # Second mean
  mu2 = mu1 + difference
  
  log_sigma ~ dunif(-10, 10)
  sigma = exp(log_sigma)
  
  # Likelihood
  for(i in 1:N1)
  {
  x1[i] ~ dnorm(mu1, 1/sigma^2)
  }
  for(i in 1:N2)
  {
  x2[i] ~ dnorm(mu2, 1/sigma^2)
  }
}
"

data = list(x1 = x1, x2 = x2, N1 = length(x1), N2 = length(x2))
variable_names = c('mu1', 'mu2', 'sigma')
burn_in = 500
steps = 5000
thin = 1
fileConn=file("model.temp")
writeLines(model, fileConn)
close(fileConn)

if(all(is.na(data)))
{
  m = jags.model(file="model.temp")
} else
{
  m = jags.model(file="model.temp", data=data)
}
update(m, burn_in)
draw = jags.samples(m, steps, thin=thin, variable.names = variable_names) 

# Convert to a list
make_list <- function(draw)
{
  results = list()
  for(name in names(draw))
  {
    # Extract "chain 1"
    results[[name]] = as.array(draw[[name]][,,1])
    # Transpose 2D arrays
    if(length(dim(results[[name]])) == 2)
      results[[name]] = t(results[[name]])
  }
  return(results)
}
results = make_list(draw)

hist(results$mu1, breaks = 100)
hist(results$mu2, breaks = 100)
plot(results$mu1, results$mu2, cex=0.1, xlab='mu1', ylab='mu2')
# Conclusion of Prior 2:
# Prior 2 is also a bit strange.
# If we're comparing these two manufactures of widgets, why would we think it's 
# possible that the two manufactures are exactly equal?
# In other words, we shouldn't worry so much about the prior probability of mu1 = mu2,
# but we should at least make sure there's a moderate prior probability that mu1 is similar to mu2.
# So the question mights seems to go back to the first prior, maybe we should adjust
# The normal distribution with a smaller standard deviation?
# Fortunately, we don't actually have to, and we're going to introduce a hierarchical model



# Prior 3: Alright, they're not equal, but they might be close
# In a hierarchical model, instead of directly assigning priors to our parameters, 
# we imagine that we knew the values of some other parameters(called 'hyperparameters'), 
# and assign our prior for the parameters given the hyperparameters.
# Then we assign a prior for the hyperparameters as well, to complete the model.

model = "model
{
  # Hierarchical priors for the means
  # Hyperparameters
  grand_mean ~ dnorm(0, 1/1000^2)
  log_diversity ~ dunif(-10, 10)
  diversity = exp(log_diversity)
  
  # Prior for the parameters given the hyperparameters
  mu1 ~ dnorm(grand_mean, 1/diversity^2)
  mu2 ~ dnorm(grand_mean, 1/diversity^2)
  
  log_sigma ~ dunif(-10, 10)
  sigma = exp(log_sigma)
  
  # Likelihood
  for(i in 1:N1)
  {
  x1[i] ~ dnorm(mu1, 1/sigma^2)
  }
  for(i in 1:N2)
  {
  x2[i] ~ dnorm(mu2, 1/sigma^2)
  }
}
"

data = list(x1 = x1, x2 = x2, N1 = length(x1), N2 = length(x2))
variable_names = c('mu1', 'mu2', 'sigma')
burn_in = 500
steps = 5000
thin = 1
fileConn=file("model.temp")
writeLines(model, fileConn)
close(fileConn)

if(all(is.na(data)))
{
  m = jags.model(file="model.temp")
} else
{
  m = jags.model(file="model.temp", data=data)
}
update(m, burn_in)
draw = jags.samples(m, steps, thin=thin, variable.names = variable_names) 

# Convert to a list
make_list <- function(draw)
{
  results = list()
  for(name in names(draw))
  {
    # Extract "chain 1"
    results[[name]] = as.array(draw[[name]][,,1])
    # Transpose 2D arrays
    if(length(dim(results[[name]])) == 2)
      results[[name]] = t(results[[name]])
  }
  return(results)
}
results = make_list(draw)

hist(results$mu1, breaks = 100)
hist(results$mu2, breaks = 100)
plot(results$mu1, results$mu2, cex=0.1, xlab='mu1', ylab='mu2')

