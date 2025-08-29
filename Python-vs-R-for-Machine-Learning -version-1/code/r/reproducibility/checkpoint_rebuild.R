# checkpoint_rebuild.R
# Requires R 3.4/3.5 and the 'checkpoint' package.
# install.packages("checkpoint")
library(checkpoint)
snapshot_date <- "2018-04-01"
pkgs <- c("tidyverse", "caret", "rmarkdown")

success <- 0
runs <- 10
for (i in seq_len(runs)) {
  cat(sprintf("=== Rebuild attempt %d/%d ===\n", i, runs))
  unlink("checkpoint", recursive = TRUE, force = TRUE)
  try({
    checkpoint(snapshotDate = snapshot_date, checkpointLocation = getwd(), scanForPackages = FALSE)
    # Install packages from the snapshot explicitly
    repos <- paste0("https://mran.microsoft.com/snapshot/", snapshot_date)
    install.packages(pkgs, repos = repos)
    success <- success + 1
  }, silent = TRUE)
}
cat(sprintf("Successful rebuilds: %d/%d\n", success, runs))
