# Input Set Generator

```
cd inputset-generator
source venv/bin/activate
./inputset.py type source --get str --sort str str [...] --head int --sample int --meta str str str str
```

Where:
- **type** is one of [npm, pypi, git]
- **source** is one of [file.json, file.csv, name_of_web_resource]
- **-\-get** is one of [latest, major, all]
- **-\-sort** is any combination of [asc, desc, popularity, latest, name]
- **-\-head** is any positive integer
- **-\-sample** is any positive integer
- **-\-meta** is followed by input set name, description, author, and email [I'm still thinking through this]