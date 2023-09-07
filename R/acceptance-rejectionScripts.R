#Acception-Rejection Method
#X has density f(x) and cdf if not available but we want to generate X
#c just has to always be bigger than pdfs f(x)/g(x). Can choose different values 
#and efficiency will fluctuate based on how good your c is

#Lecture 9 
#Beta(2,2) has pdf f(x) = 6x(1-x), let g(x) ~ u(0,1)
#Then for f(x)/g(x) <= c, c >= 1.5 since 6 - 12x =0 
#when x = 0.5 which elicits max at f(0.5) = 1.5

n <- 1000
k <- 0
j <- 0
y <- numeric(n)


while(k < n){
  u <- runif(1)
  j <- j + 1 
  x <- runif(1)
  if(4*x*(1-x) > u){
    k <- k+1
    y[k] <- x
  }
}
j #j is simply a counter to see how many iterations it takes to accept 1000
# Compare empirical and theoretical percentiles
p <- seq(0.1, 0.9, 0.1)
Qhat <- quantile(y,p) # quantile of the sample
Q <- qbeta(p,2, 2) # theoretical quantiles
se <- sqrt( p*(1-p)/(n*dbeta(Q,2,2)^2)) # see chapter 2
round(rbind(Qhat,Q,se),3)

#Lecture 9 Question
#Q1
#beta pdf is (x^(a-1)*(1-x)^b-1)/[(a-1)!*(b-1)!/(a+b-1)!]
betaDistSamp <- function(n, a, b){
  #c <- ceiling(factorial(a+b-1)/(factorial(a-1)*factorial(b-1)))
  k <- 0
  j <- 0
  y <- numeric(n)
  while(k < n){
    u <- runif(1)
    j <- j+1
    x <- runif(1)
    if(x^(a-1)*(1-x)^(b-1) > u){
      k <- k+1
      y[k] <- x
    }
  }
  j
  return(y)
}
tmp <- betaDistSamp(1000, 3, 2)

p <- seq(0.1, 0.9, 0.1)
Qhat <- quantile(tmp,p) # quantile of the sample
Q <- qbeta(p,3, 2) # theoretical quantiles
se <- sqrt( p*(1-p)/(1000*dbeta(Q,3,2)^2)) # see chapter 2
round(rbind(Qhat,Q,se),3)
hist(tmp, freq = FALSE)
curve(x^2*(1-x)*12, add=TRUE)