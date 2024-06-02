# nmap_report_2_pdf
Convert nmap XML reports to a nice md and pdf structure.

# Installation

`pip install -r requirements.txt`

`npm install` in /pdf_generator


# Usage 

python `nmap_xml_2_mdPdf.py`  `<XML file>` `<output md file>`  `<output format ->[pdf, md]>`

## Example
python `nmap_xml_2_mdPdf.py`  `sample-nmap-output.xml` `report.md`  `pdf`

This will generate both md and a pdf. You can only use the md argument to only generate md file.

# Markdown generated example

## Host 192.168.0.1 is up Information:

| Address     | State   | Hostname   | Filtered   |
|:------------|:--------|:-----------|:-----------|
| 192.168.0.1 | up      | N/A        | False      |

---

### Ports Information:

| Port ID   | Protocol   | State   | Reason   | Reason TTL   | Service Name   | Product          | Version   | Extra Info                                 | Device Type   | Method   | Conf   | CPE                        |
|:----------|:-----------|:--------|:---------|:-------------|:---------------|:-----------------|:----------|:-------------------------------------------|:--------------|:---------|:-------|:---------------------------|
| 22        | tcp        | open    | syn-ack  | 0            | ssh            | OpenSSH          | 6.2       | protocol 2.0                               | N/A           | probed   | 10     | cpe:/a:openbsd:openssh:6.2 |
| 88        | tcp        | open    | syn-ack  | 0            | kerberos-sec   | Heimdal Kerberos | N/A       | server time: 2015-08-14 18:54:26Z          | N/A           | probed   | 10     | cpe:/a:heimdal:kerberos    |
| 548       | tcp        | open    | syn-ack  | 0            | afp            | N/A              | N/A       | N/A                                        | N/A           | table    | 3      | N/A                        |
| N/A       | N/A        | closed  | N/A      | N/A          | N/A            | N/A              | N/A       | Count: 97, Reason: conn-refused, Count: 97 | N/A           | N/A      | N/A    | N/A                        |

---
