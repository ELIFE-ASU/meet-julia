compute_π <- function(trials) {
    inside <- 0.0
    for (i in 1:trials) {
        point <- runif(2)
        inside <- inside + (sum(point^2) <= 1.0)
    }
    return(4.0*inside/trials)
}

args = commandArgs(trailingOnly=TRUE)
if(length(args) < 1) {
    error("must provide number of trials")
}
trials = as.integer(args[1])
set.seed(2018)

start.time <- Sys.time()
invisible(compute_π(trials))
stop.time <- Sys.time()
cat("First invocation: ", stop.time - start.time, "s\n")

start.time <- Sys.time()
π <- compute_π(trials)
stop.time <- Sys.time()
cat("Second invocation:", stop.time - start.time, "s\n")

cat("π ≈ ", π, "\n")
