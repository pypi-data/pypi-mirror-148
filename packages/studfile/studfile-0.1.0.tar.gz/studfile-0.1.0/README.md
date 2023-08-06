# Stud

## Example Studfile.yaml

```yaml
test: 
  help: "Run test commands"
  options:
    - name: -m,--message
      default: Hello world
      nargs: '?'
      required: true
    - name: foobar
  cmd: |
    echo "{foobar}"
    
    for foo in ["bar", "baz"]:
      print(f"{message}: {foo}")
```
