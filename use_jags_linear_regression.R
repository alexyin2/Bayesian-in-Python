library('rjags')
# Create a data that describes the age of the driver and the maximum distance at 
# which they could read a newly designed road sign.
x = c(20, 22, 24, 25, 26, 29, 30, 31, 35, 40, 
      41, 42, 45, 50, 53, 55, 58, 60, 61, 62, 
      65, 66, 69, 71, 72, 73, 80, 85, 90, 95)
y = c(500, 600, 610, 550, 520, 570, 500, 490, 510, 495, 
      460, 400, 470, 430, 440, 490, 420, 410, 420, 390, 
      380, 350, 300, 360, 320, 300, 350, 370, 320, 290)
data = data.frame(x, y)
# Let's see how our original data looks like
plot(data$x, data$y, xlab = 'Age(years)', ylab = 'Distance(meters)', xlim = c(0, 100), ylim = c(0, 800))
# Let's see how the b0 and b1 looks like in our data when we fit linear regression
fit = lm(data$y ~ data$x)
summary(fit)

# Our goal is to calculate the posterior distribution for ß1 and ß0

# In beta0 ~ dnorm(0, 1/1000^2), you may feel quite strange why we set the varaince so small
# but indeed it doesn't mean what we think when we normally use dnorm().
# In jags, the first argument in dnorm() is the mean, and the second argument must be
# one over the variance. So here, 1/1000^2 in dnorm() means that the sd = 1000.
model = "model
{
  # Prior
  beta0 ~ dnorm(0, 1/1000^2)
  beta1 ~ dnorm(0, 1/1000^2)
  log_sigma ~ dunif(-10, 10)
  sigma = exp(log_sigma)
  
  # Likelihood
  for(i in 1:N)
  {
    y[i] ~ dnorm(beta0 + beta1 * x[i], 1/sigma^2)
  }
}
"

data = list(x = data$x, y = data$y, N = length(data$y))
variable_names = c('beta0', 'beta1', 'sigma')
burn_in = 1000
steps = 10000
thin = 1

# Write model out to file
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

# Plot trace plots
plot(results$beta0, type='l', xlab='Iteration', ylab='beta0')
plot(results$beta1, type='l', xlab='Iteration', ylab='beta1')
plot(results$sigma, type='l', xlab='Iteration', ylab='sigma')

# Plot histograms
hist(results$beta0, breaks=20, xlab='beta0')
hist(results$beta1, breaks=20, xlab='beta1')
hist(results$sigma, breaks=20, xlab='sigma')

# Plot joint posterior distribution of beta0 and beta1
plot(results$beta0, results$beta1, cex=0.1, xlab='beta0', ylab='beta1')

# Questions:
# I've found that if we've change sd larger in the prior, than the outcome will be less accurate.
# Why?
