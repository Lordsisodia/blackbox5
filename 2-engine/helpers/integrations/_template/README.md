# Integration Template

This directory contains a template for creating new integrations for BlackBox5.

## Files

- `__init__.py.template` - Template for the integration's `__init__.py` file
- `manager.py.template` - Template for the main manager class
- `types.py.template` - Template for type definitions
- `config.py.template` - Template for configuration
- `demo.py.template` - Example usage
- `tests/test_integration.py.template` - Template for integration tests

## How to Create a New Integration

1. Copy the entire `_template` directory:
   ```bash
   cp -r _template my_service
   ```

2. Replace template placeholders:
   - `{SERVICE_NAME}` → Your service name (e.g., "GitHub", "Notion")
   - `{SERVICE_LOWER}` → Lowercase version (e.g., "github", "notion")
   - `{ServiceName}` → CamelCase version (e.g., "GitHub", "Notion")

3. Rename all `.template` files to remove the `.template` extension:
   ```bash
   cd my_service
   mv __init__.py.template __init__.py
   mv manager.py.template manager.py
   mv types.py.template types.py
   mv config.py.template config.py
   mv demo.py.template demo.py
   cd tests
   mv test_integration.py.template test_integration.py
   ```

4. Replace template placeholders in all files using your text editor or:
   ```bash
   find my_service -type f -exec sed -i \
     -e 's/{SERVICE_NAME}/MyService/g' \
     -e 's/{SERVICE_LOWER}/my_service/g' \
     -e 's/{ServiceName}/MyService/g' {} \;
   ```

5. Implement the required methods in `manager.py`

6. Update `config.py` with your service's configuration

7. Test your integration using `demo.py`

## Example: Creating a Slack Integration

```bash
cd /opt/blackbox5/2-engine/helpers/integrations
cp -r _template slack
cd slack
sed -i 's/{SERVICE_NAME}/Slack/g' *.py *.template
sed -i 's/{SERVICE_LOWER}/slack/g' *.py *.template
sed -i 's/{ServiceName}/Slack/g' *.py *.template
# Remove .template extension from all template files
for f in *.template tests/*.template; do mv "$f" "${f%.template}"; done
```

## Notes

- All template files use the `.template` extension to avoid syntax errors and linter issues
- Template placeholders like `{SERVICE_NAME}` are NOT valid Python - files must be renamed before use
- Always remove the `.template` extension from all template files after replacing placeholders
- See existing integrations (github, notion, vibe) for reference implementations
