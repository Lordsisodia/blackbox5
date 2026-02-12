# Integration Template

This directory contains a template for creating new integrations for BlackBox5.

## Files

- `__init__.py.template` - Template for the integration's `__init__.py` file
- `manager.py` - Template for the main manager class
- `types.py` - Template for type definitions
- `config.py.template` - Template for configuration
- `demo.py` - Example usage

## How to Create a New Integration

1. Copy the entire `_template` directory:
   ```bash
   cp -r _template my_service
   ```

2. Replace template placeholders:
   - `{SERVICE_NAME}` → Your service name (e.g., "GitHub", "Notion")
   - `{SERVICE_LOWER}` → Lowercase version (e.g., "github", "notion")
   - `{ServiceName}` → CamelCase version (e.g., "GitHub", "Notion")

3. Rename `__init__.py.template` to `__init__.py`:
   ```bash
   mv my_service/__init__.py.template my_service/__init__.py
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
sed -i 's/{SERVICE_NAME}/Slack/g' *.py
sed -i 's/{SERVICE_LOWER}/slack/g' *.py
sed -i 's/{ServiceName}/Slack/g' *.py
mv __init__.py.template __init__.py
```

## Notes

- The `__init__.py.template` file uses Python f-string-style placeholders that are NOT valid Python
- Always rename it to `__init__.py` after replacing placeholders
- See existing integrations (github, notion, vibe) for reference implementations
