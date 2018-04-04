compute_π <- function(trials) {
    points <- matrix(runif(2*trials), nrow=2)
    inside <- sum(colSums(points^2) <= 1.0)
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
