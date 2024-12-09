# OpenSpeed

OpenSpeed is a tool designed to check if a target is vulnerable to WebSpeed misconfigurations. WebSpeed is a legacy application used for building and deploying web applications. This tool can also send OS commands to exploit vulnerabilities if they are present in the WebSpeed setup.

## WebSpeed

WebSpeed is a legacy application, and this tool helps assess the security of such systems. Please ensure you are conducting tests responsibly and with proper authorization.

## Features

- Detect vulnerabilities in WebSpeed configurations.
- Scan a list of targets for vulnerabilities.
- Execute OS commands on vulnerable targets.
- Supports scanning for known file paths to identify issues.

## Prerequisites

- Python 3.6 or higher
- Install requirements.txt

## Usage

### Options

#### -u, --url

Specify a target URL to check for vulnerabilities.
Example:

```bash
./openwebspeed.py -u http://example.com
```

#### -l, --list

Specify a file containing a list of URLs to scan.
Example:

```bash
./openwebspeed.py -l targets.txt
```

#### -c, --oscommand

Send an OS command to a vulnerable target.
Example:

```bash
./openwebspeed.py -u http://example.com -c "ls -la"
```

#### -o, --output

Specify a file to save the results.
Example:

```bash
./openwebspeed.py -u http://example.com -o results.txt
```

#### -nb, --nobanner

Suppress the ASCII art banner.

#### -a, --all

Scan all known files for vulnerabilities.

## Example

#### Scan a single URL:

```bash

./openwebspeed.py -u http://example.com
```

#### Scan multiple URLs from a file:

```bash
./openwebspeed.py -l targets.txt
```

#### Send an OS command:

```bash

./openwebspeed.py -u http://example.com -c "whoami"
```

## ASCII Art

The script includes some creative ASCII art banners for a fun user experience =)

## Disclaimer

Hacking without permission is illegal. This tool is for educational purposes only. It should only be used on systems you own or have explicit permission to test. Unauthorized access to computer systems is a criminal offense and could lead to severe legal consequences. The author is not responsible for any misuse or damage caused by this tool.
