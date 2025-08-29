# 2018-compatible: simple allowlist loader for RDS
# Blocks use of unexpected classes BEFORE any generic (print/summary/etc.) is called.

safe_read_rds <- function(path, allowed_classes = c("list", "data.frame", "numeric", "character", "integer")) {
  obj <- readRDS(path)  # readRDS alone does NOT execute code; danger happens on method dispatch.
  cls <- class(obj)
  if (!any(cls %in% allowed_classes)) {
    stop(paste("blocked: disallowed class", paste(cls, collapse = ",")))
  }
  obj
}
