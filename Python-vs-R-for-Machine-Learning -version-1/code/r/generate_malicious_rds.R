# 2018-compatible, Windows/POSIX safe
# Generates a crafted RDS to demonstrate why untrusted deserialization is unsafe.

# --- make working dir = script folder ---
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg)) {
  script_path <- normalizePath(sub("^--file=", "", file_arg))
  script_dir  <- dirname(script_path)
  setwd(script_dir)
}

# Ensure output dir exists
dir.create("artifacts", showWarnings = FALSE, recursive = TRUE)

# Minimal object with a custom S3 class
rce_obj <- structure(
  list(msg = "*** malicious RDS executed (demo) ***"),
  class = "RCE"
)

# Write artifact
saveRDS(rce_obj, file = "artifacts/malicious.rds")
cat("Wrote artifacts/malicious.rds\n")
