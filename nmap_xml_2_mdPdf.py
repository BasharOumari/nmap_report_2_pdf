import xml.etree.ElementTree as ET
import pandas as pd
import sys
import subprocess
import os

def parse_nmap_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    hosts_data = []

    for host in root.findall('host'):
        host_info = {
            'Address': host.find('address').get('addr', 'N/A'),
            'State': host.find('status').get('state', 'N/A'),
            'Filtered': False
        }

        # Get the host's hostname
        hostname = host.find('hostnames/hostname')
        host_info['Hostname'] = hostname.get('name') if hostname is not None else 'N/A'

        # Ports information
        ports_info = []
        ports = host.find('ports')
        if ports is not None:
            for port in ports.findall('port'):
                port_info = {
                    'Port ID': port.get('portid'),
                    'Protocol': port.get('protocol'),
                    'State': port.find('state').get('state', 'N/A'),
                    'Reason': port.find('state').get('reason', 'N/A'),
                    'Reason TTL': port.find('state').get('reason_ttl', 'N/A'),
                    'Service Name': 'N/A',
                    'Product': 'N/A',
                    'Version': 'N/A',
                    'Extra Info': 'N/A',
                    'Device Type': 'N/A',
                    'Method': 'N/A',
                    'Conf': 'N/A',
                    'CPE': 'N/A',
                }
                service = port.find('service')
                if service is not None:
                    port_info.update({
                        'Service Name': service.get('name', 'N/A'),
                        'Product': service.get('product', 'N/A'),
                        'Version': service.get('version', 'N/A'),
                        'Extra Info': service.get('extrainfo', 'N/A'),
                        'Device Type': service.get('devicetype', 'N/A'),
                        'Method': service.get('method', 'N/A'),
                        'Conf': service.get('conf', 'N/A'),
                        'CPE': service.find('cpe').text if service.find('cpe') is not None else 'N/A',
                    })
                ports_info.append(port_info)

            # Check for extraports
            extraports = ports.find('extraports')
            if extraports is not None:
                state = extraports.get('state')
                host_info['Filtered'] = state == 'filtered'
                ports_info.append({
                    'Port ID': 'N/A',
                    'Protocol': 'N/A',
                    'State': state,
                    'Reason': 'N/A',
                    'Reason TTL': 'N/A',
                    'Service Name': 'N/A',
                    'Product': 'N/A',
                    'Version': 'N/A',
                    'Extra Info': f"Count: {extraports.get('count')}, Reason: {extraports.find('extrareasons').get('reason')}, Count: {extraports.find('extrareasons').get('count')}",
                    'Device Type': 'N/A',
                    'Method': 'N/A',
                    'Conf': 'N/A',
                    'CPE': 'N/A'
                })

        host_info['Ports'] = ports_info

        # Script outputs
        scripts_info = []
        if ports is not None:
            for port in ports.findall('port'):
                for script in port.findall('script'):
                    scripts_info.append({
                        'Port ID': port.get('portid'),
                        'Script ID': script.get('id'),
                        'Output': script.get('output')
                    })
        host_info['Scripts'] = scripts_info

        # OS information
        os_info = []
        os = host.find('os')
        if os is not None:
            for portused in os.findall('portused'):
                os_info.append({
                    'State': portused.get('state', ''),
                    'Proto': portused.get('proto', ''),
                    'Port ID': portused.get('portid', '')
                })
            for osclass in os.findall('osclass'):
                os_info.append({
                    'Type': osclass.get('type', ''),
                    'Vendor': osclass.get('vendor', ''),
                    'OS Family': osclass.get('osfamily', ''),
                    'OS Gen': osclass.get('osgen', ''),
                    'Accuracy': osclass.get('accuracy', '')
                })
            for osmatch in os.findall('osmatch'):
                os_info.append({
                    'Name': osmatch.get('name', ''),
                    'Accuracy': osmatch.get('accuracy', '')
                })
            os_fingerprint = os.find('osfingerprint')
            if os_fingerprint is not None:
                os_info.append({
                    'OS Fingerprint': os_fingerprint.get('fingerprint', '')
                })
        host_info['OS'] = os_info

        hosts_data.append(host_info)

    return hosts_data


def convert_to_markdown_table(hosts_data):
    markdown_output = []

    for host in hosts_data:
        # General Host Information Table
        host_df = pd.DataFrame([{
            'Address': host['Address'],
            'State': host['State'],
            'Hostname': host['Hostname'],
            'Filtered': host['Filtered']
        }])
        host_table = host_df.to_markdown(index=False)
        markdown_output.append(
            f"## Host {host['Hostname'] if host['Hostname'] != 'N/A' else host['Address']} is {host['State']} Information:\n")
        markdown_output.append(host_table + "\n")
        markdown_output.append("---\n")

        # Ports Information Table
        if host['Ports']:
            ports_df = pd.DataFrame(host['Ports']).fillna('')
            ports_table = ports_df.to_markdown(index=False)
            markdown_output.append("### Ports Information:\n")
            markdown_output.append(ports_table + "\n")
            markdown_output.append("---\n")

        # Script Outputs Table
        if host['Scripts']:
            scripts_df = pd.DataFrame(host['Scripts']).fillna('')
            scripts_table = scripts_df.to_markdown(index=False)
            markdown_output.append("### Script Outputs:\n")
            markdown_output.append(scripts_table + "\n")
            markdown_output.append("---\n")


        # OS Information Table
        if host['OS']:
            os_df = pd.DataFrame(host['OS']).fillna('')
            os_table = os_df.to_markdown(index=False)
            markdown_output.append("### OS Information:\n")
            markdown_output.append(os_table + "\n")
            markdown_output.append("---\n")


    return markdown_output


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python nmapxml.py <filename> <output_file> <output_format>")
        sys.exit(1)

    file_path = sys.argv[1]
    output_file = sys.argv[2]
    output_format = sys.argv[3]

    output_file = output_file if output_file.endswith('.md') else output_file + '.md'

    # Parse the XML file
    hosts_data = parse_nmap_xml(file_path)

    # Convert to Markdown tables
    markdown_tables = convert_to_markdown_table(hosts_data)

    # Write to .md file
    with open(output_file, 'w') as f:
        for table in markdown_tables:
            f.write(table)
            f.write("\n")

    if output_format == 'pdf':
        pdf_output_file = output_file.replace('.md', '.pdf')
        # Ensure the output directory exists
        output_dir = os.path.dirname(os.path.abspath(pdf_output_file))
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # Debugging: print the paths
        print(f"Markdown path: {os.path.abspath(output_file)}")
        print(f"PDF path: {os.path.abspath(pdf_output_file)}")

        # Convert markdown to PDF using Node.js script
        try:
            subprocess.run(['node', 'generate_pdf.mjs', output_file, pdf_output_file], check=True)
            print(f"PDF file generated: {pdf_output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error converting to PDF: {e}")
    else:
        print(f"Markdown file generated: {output_file}")
