#LINEAR REGRESSIONS
data(cars)
cars
head(cars)
pairs(cars)

lm.fit <- lm(dist ~ speed, data = cars)
print(lm.fit)
summary(lm.fit)
#residuals is y_i - y_ihat
#Pr(>|t|) for speed is small so there is a linear relationship
#Residual standard error (RSE) sqrt( zbar*(yi - yhat)^2/(n-2))
#Residual std error is 15.38 so when you use this model as an estimator, the average error is 15.38
#Multiple R^2 - Total sum of squares (TSS) = zbar(yi - yhat)^2, RSS = zbar(yi - yhat)^2
#R^2 = (TSS - RSS)/TSS, the larger the better

#predict distance when speed = 40mph
predict(lm.fit, data.frame(speed = 40))
predict(lm.fit, data.frame(speed = c(40, 50, 60, 70)))

plot(cars$speed, cars$dist)
abline(lm.fit, col='red')

#model diagnostic - residual vs fitted (should be about 0 and random cause we assume normality)
#Normal QQ - If the data values in the plot fall along a roughly straight line at a 45-degree angle, then the data is normally distributed
#Sigma should be constant so there shouldn't be much change
#Residual vs leverage - shows how much impact any one sample effects the model
# leverage > 2 means that one effects it a lot
par(mfrow=c(2,2)) #sets up matrix for the 4 following plots
plot(lm.fit)


hat <- as.data.frame(hatvalues(lm.fit))
hat

#above is not reasonable because y int is neg
lm.fit2 <- lm(dist ~ 0+speed, data = cars) #no intercept
summary(lm.fit2)

speednew <- data.frame(speed=c(4,5,30))
predict(lm.fit2, speednew, interval="prediction")
predict(lm.fit2, speednew, interval="confidence")

#now we'll do multiple linear regression
data("trees")
#view(trees)
pairs(trees) #matrix of scatterplots
cor(trees) #correlation matrix

lm.fit3 <- lm(volume ~ Girth + Height, data = trees)
summary(lm.fit)

par(mfrow=c(2,2))
plot(lm.fit)
par(mfrow=c(1,1))

#LOGISTIC REGRESSIONS
#install.packages("ISLR2")
library(ISLR2)
data(Default)
attach(Default)
View(Default)
summary(Default)

#build logistical regression model
glm.fit <- glm(default ~ balance, family = binomial, data = default)
summary(glm.fit)
#ln(P/(1-P)) = beta_o + beta_1x, from previous line beta_o = -10.65, beta_1 = 0.005499

#install.packages("effects")
library(effects)
plot(allEffects(glm.fit), type = "response")

#test our model on full data set (all of default)
glm.probs <- predict(glm.fit, type = "response")
glm.probs
glm.pred <- ifelse(glm.probs > 0.5, "Yes", "No")
table(glm.pred, Default$default) # diagonal are the correctly prediction
mean(glm.pred == Default$default)

#test our model with a test and training set (avoid overfit)
train = Default$income > 33000
glm.fits <- glm(default ~ balance, data = Default, family =binomial, subset = train)

test = Default[!train,]
glm.probs <- predict(glm.fits, newdata = test, type = "response")
glm.pred <- ifelse(glm.probs > 0.5, "Yes", "No")
table(glm.pred, test$default)
mean(glm.pred == test$default)

#a. Fit a logistic regression model to study the relationship between ObamaMargin and Vote result.
#b. print the model result.
#c. visualizing the fitted model.
#d. Interpret your result.

glm.fit <- glm(Vote ~ ObamaMargin, family = binomial, data = obamacare)
plot(allEffects(glm.fit), type = "response")
summary(glm.fit)
library(visreg)
visreg(glm.fit, scale = "response")

#The p value is small so there is a logistical relationship
#beta1 = 0.1241 so positive relationship between margin and vote
#Reject H0 and conclude there is an association between Vote and obamamargin