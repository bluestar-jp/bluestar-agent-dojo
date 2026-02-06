# Security Review: proc-importing-skill

Date: 2026-02-04
Status: Requires Security Enhancements

## Critical Issues

### 1. Command Injection Risk (HIGH)

**Location**: `scripts/fetch-definition.py` lines 96-113, 160-163

**Issue**: External URLs are downloaded without validation, potentially allowing:

- Arbitrary file execution
- Path traversal attacks
- Malicious content injection

**Recommendation**:

```python
# Add URL validation
from urllib.parse import urlparse

def _validate_url(url: str) -> bool:
    """Validate URL for safety"""
    parsed = urlparse(url)

    # Check scheme
    if parsed.scheme not in ['http', 'https']:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Block localhost and private IPs
    if parsed.hostname in ['localhost', '127.0.0.1', '0.0.0.0']:
        raise ValueError("Localhost access not allowed")

    return True
```

### 2. Path Traversal Vulnerability (MEDIUM)

**Location**: `scripts/import-workflow.sh` lines 261-267

**Issue**: User-provided paths are used without sanitization:

```bash
cp -r "$CONVERTED_PATH" "$TARGET_PATH"
```

**Recommendation**:

```bash
# Validate paths before use
if [[ "$TARGET_PATH" != "$PROJECT_ROOT"* ]]; then
    error_exit "Target path must be within project root"
fi
```

### 3. Arbitrary Code Execution (HIGH)

**Location**: Downloaded scripts are not scanned before execution

**Recommendation**:

- Add content scanning for suspicious patterns
- Warn users before executing external scripts
- Implement sandboxing for script validation

## Medium Priority Issues

### 4. Missing Input Validation

**Location**: `scripts/import-workflow.sh` lines 64-84

**Issue**: Command-line arguments lack proper validation

**Recommendation**:

```bash
# Validate SOURCE format
if [[ "$SOURCE" =~ [;\&\|] ]]; then
    error_exit "Invalid characters in source"
fi
```

### 5. Insufficient Content Type Verification

**Location**: `scripts/fetch-definition.py`

**Issue**: Downloaded files are assumed to be safe based on extension only

**Recommendation**:

- Verify MIME types using `file` command
- Check file signatures (magic bytes)
- Limit file sizes

## Low Priority Issues

### 6. Temporary File Cleanup

**Location**: `scripts/fetch-definition.py` line 258

**Issue**: Temporary files might not be cleaned up on error

**Recommendation**:

- Use `try/finally` blocks
- Implement proper cleanup handlers

## Best Practices Violations

### 7. Claude Code Tool Usage

**Location**: `SKILL.md` lines 24-32

**Issue**: Documentation shows bash commands instead of Claude Code tools

**Should be**:

```markdown
# Use Claude Code tools instead of raw commands
- WebFetch for HTTP(S) URLs
- Read for local files
- Bash only for git/gh CLI operations
```

### 8. Mixed Language Error Messages

**Location**: Multiple files

**Issue**: English and Japanese messages are mixed

**Recommendation**: Standardize on one language (Japanese for this project)

## Security Checklist

- [ ] Add URL validation and sanitization
- [ ] Implement path traversal protection
- [ ] Add content scanning for malicious code
- [ ] Validate file types and signatures
- [ ] Implement size limits for downloads
- [ ] Add rate limiting for external requests
- [ ] Create security audit logging
- [ ] Document security assumptions

## Priority Actions

1. **Immediate**: Add input validation to prevent command injection
2. **Short-term**: Implement content scanning before execution
3. **Long-term**: Create sandboxed execution environment

## Notes

This skill handles external, potentially untrusted content. Security measures are essential before production use.
