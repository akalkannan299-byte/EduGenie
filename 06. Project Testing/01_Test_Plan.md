# EduGenie – Testing Plan

## Testing Objectives
- Verify that the application starts correctly.
- Verify API routes are available.
- Verify invalid input is rejected.
- Verify the documentation endpoint is available.
- Verify Gemini configuration can be loaded.

## Test Cases

| ID | Test | Expected Result |
|---|---|---|
| TC01 | Open `/` | EduGenie web page loads |
| TC02 | Open `/health` | Health response is returned |
| TC03 | Open `/docs` | Swagger UI loads |
| TC04 | Empty Q&A input | Validation error |
| TC05 | Empty explanation input | Validation error |
| TC06 | Empty summary input | Validation error |
| TC07 | Empty quiz topic | Validation error |
| TC08 | Empty learning topic | Validation error |

## Automated Testing
Run:

```bash
pytest
```

## Important Integration Test
After adding a valid Gemini API key, manually test every learning operation because live model calls require external API access.