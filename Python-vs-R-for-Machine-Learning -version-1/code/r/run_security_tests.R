# 2018-compatible, Windows/POSIX safe
# R security tests analogous to the Python suite.
# T1 print(), T2 summary(), T3 indexing, T4 allowlist, T5 CSV control, T6 integrity check.

# --- make working dir = script folder ---
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg)) {
  script_path <- normalizePath(sub("^--file=", "", file_arg))
  script_dir  <- dirname(script_path)
  setwd(script_dir)
}

ART <- "artifacts"
dir.create(ART, showWarnings = FALSE, recursive = TRUE)

# Cross-platform echo helper with safe quoting
echo_msg <- function(msg) {
  if (.Platform$OS.type == "windows") {
    system(paste("cmd /c echo", msg), invisible = TRUE)
  } else {
    # Use shQuote to avoid shell-quoting pitfalls
    system(paste("sh -c", shQuote(paste("echo", msg))), invisible = TRUE)
  }
}

# Malicious S3 methods for class RCE (benign demo payloads)
print.RCE <- function(x, ...) {
  echo_msg("*** malicious RDS executed via print (demo) ***")
  invisible(0L)
}
summary.RCE <- function(object, ...) {
  echo_msg("*** malicious RDS executed via summary (demo) ***")
  invisible(0L)
}
`[.RCE` <- function(x, ...) {
  echo_msg("*** malicious RDS executed via indexing (demo) ***")
  NextMethod("[")
}

# Load allowlist helper
source("safe_loader.R")

ok <- function(label) cat("[OK] ", label, "\n", sep = "")
fail <- function(label, e) { cat("[FAIL] ", label, ": ", conditionMessage(e), "\n", sep = ""); stop(e) }

# Utility: write baseline malicious.rds
write_malicious <- function() {
  rce_obj <- structure(list(msg = "*** malicious RDS executed (demo) ***"), class = "RCE")
  saveRDS(rce_obj, file = file.path(ART, "malicious.rds"))
}

t1_print <- function() {
  label <- "T1 RCE via print() on RCE object"
  tryCatch({
    if (!file.exists(file.path(ART, "malicious.rds"))) write_malicious()
    obj <- readRDS(file.path(ART, "malicious.rds"))
    res <- print(obj)  # triggers print.RCE
    if (!is.integer(res) && !identical(res, 0L)) stop("print() did not return invisible 0L")
    ok(label)
  }, error = function(e) fail(label, e))
}

t2_summary <- function() {
  label <- "T2 RCE via summary() on RCE object"
  tryCatch({
    obj <- readRDS(file.path(ART, "malicious.rds"))
    res <- summary(obj)  # triggers summary.RCE
    ok(label)
  }, error = function(e) fail(label, e))
}

t3_indexing <- function() {
  label <- "T3 RCE via indexing method `[.RCE`"
  tryCatch({
    obj <- readRDS(file.path(ART, "malicious.rds"))
    tmp <- obj[1]  # triggers `[.RCE`
    ok(label)
  }, error = function(e) fail(label, e))
}

t4_allowlist_blocks <- function() {
  label <- "T4 Allowlist blocks disallowed class before use"
  tryCatch({
    blocked <- FALSE
    tryCatch({
      safe_read_rds(file.path(ART, "malicious.rds"))
    }, error = function(e) { blocked <<- TRUE })
    if (!blocked) stop("safe_read_rds did not block RCE class")
    ok(label)
  }, error = function(e) fail(label, e))
}

t5_csv_control <- function() {
  label <- "T5 CSV control: no code execution"
  tryCatch({
    df <- data.frame(x = 1:3, y = c("a","b","c"), stringsAsFactors = FALSE)
    csv_path <- file.path(ART, "control.csv")
    write.csv(df, csv_path, row.names = FALSE)
    df2 <- read.csv(csv_path, stringsAsFactors = FALSE)
    if (!identical(df, df2)) stop("CSV roundtrip mismatch")
    ok(label)
  }, error = function(e) fail(label, e))
}

t6_integrity_check <- function() {
  label <- "T6 Integrity check (MD5 detects tamper)"
  tryCatch({
    path <- file.path(ART, "malicious.rds")
    if (!file.exists(path)) write_malicious()
    md5_known <- tools::md5sum(path)[[1]]
    # Tamper: flip one byte in a copy
    tampered <- file.path(ART, "malicious_tampered.rds")
    bytes <- readBin(path, what = "raw", n = file.info(path)$size)
    i <- min(10L, length(bytes))
    if (i < 1L) stop("file too small to tamper")
    bytes[i] <- as.raw(bitwXor(as.integer(bytes[i]), 0xFF))
    writeBin(bytes, tampered)
    md5_tampered <- tools::md5sum(tampered)[[1]]
    if (identical(md5_tampered, md5_known)) stop("Tamper not detected by MD5")
    ok(label)
  }, error = function(e) fail(label, e))
}

cat("Running R serialization security tests (T1–T6)...\n\n")
t1_print()
t2_summary()
t3_indexing()
t4_allowlist_blocks()
t5_csv_control()
t6_integrity_check()
cat("\nAll tests completed.\n")
