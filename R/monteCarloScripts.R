#Monte Carlo estimation of an integral
#if unbounded integral then cut in half since integral of pdf is 1, the half that goes
#to infinity will simply be 0.5
#if x is in the interval then use t = xy to make x in bound one and change t to xy in eq
# and also dt to xdy
#monte carlo estimate of theta = integral from 0 to pi/3 of sin(x)dx
x <- runif(1000, min=0, max = pi/3)
theta.hat <- mean(sin(x))*(pi/3)
theta.hat


#Monte Carlo Simulation
T <- 1
N <- 252
dt <- T/N
mu <- 0.1
dev <- 0.2
S_o <- 100
M <- 1000

S <- matrix(0, nrow = M, ncol = N)
R <- matrix(rnorm(M*N), nrow = M, ncol=N)

S[, 1] = 100

S
simulatei <- function(si,i){
  return(si*exp((mu-.5*dev^2)*dt+dev*sqrt(dt)*R[,i]))
}
simulatei(100)
for(i in 1:(N-1)){
  S[,i+1] = simulatei(S[,i], i)
}
S
matplot(t(S), type= "l")
count <- 0
for(i in 1:M){
  if(S[i, N] > 120){
    count = count + 1
  }
}
count/M
mean(S[,N])

#MONTE CARLO METHOD 
#The construction based on population is based on t CI
#Assume in reality the measurement is dist as chi squared with 2 df
#Compute the actual CI for the case of CI with nominal confidence lvl of 95%

mu <-2 #since 2 df of chi squared
n <- 25
CI <- replicate(10000, expr= {
  x <- rchisq(n, df = 2)
  xbar <- mean(x)
  se <- sd(x) / sqrt(n)
  xbar + se * qt(c(.025, .975), df = n-1)
})
LCL <- CI[1,]
UCL <- CI[2,]
sum(LCL < mu & UCL > mu)
mean(LCL < mu & UCL > mu)
#actual confidence of ~92%