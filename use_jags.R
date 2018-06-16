# When using jags, the first thing is to define our prior and likelihood.
# Remember that we should always write the prior before the likelihood.

# Maybe you'll feel confused about how did the program know which is our prior and 
# which is our likelihood since sometimes we may have a lot of priors(parameters).
# The answer is that we will later define a list and we will put the likelihood in the list.

# Define prior and likelihood
model = "model
{
  theta ~ dunif(0, 1)
  x ~ dbin(theta, N)
  }
"

# Define the list as 'data' (use NA for no data)
data = list(x=2, N=5)

# Variables to monitor, which means the variables that we care in posterior
variable_names = c('theta')

# How many burn-in steps?
# The burn-in is an initial part of the MCMC that are not saved.
# This is because sometimes it can take a while for the MCMC to locate the regions of high porsterior probability.
burn_in = 1000

# How many proper steps?
steps = 5000

# Thinning?
# If thin = 10, only every 10th iteration of the MCMC will appear in the results.
# This is useful for keeping the size of results list manageable.
thin = 1


library('rjags')
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


# To plot a trace plot of the MCMC run, we can simply run the code below.
# Notice that if our variable is not called theta, just changed it to what you named it.
plot(results$theta, type = 'l')  
# type = 'l' means that we use lines to connect the dots
# Remember that because the data follows the order so the plot can show how the MCMC runs.

# We could look at the posterior distribution using a histogram.
hist(results$theta, breaks = 100, xlim = c(0, 1))



