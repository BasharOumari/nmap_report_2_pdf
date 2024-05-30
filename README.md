# nmap_report_2_pdf
Convert nmap XML reports to a nice md and pdf structure.

# Usage 

python .\copy_nmap.py  <XML file> <output md file>  <output format ->[pdf, md]>

## example
python nmap_xml_2_mdPdf.py  sample-nmap-output.xml report.md  pdf

This will generate both md and a pdf. You can only use the md argument to only generate md file.

