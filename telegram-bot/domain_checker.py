import whois
import dns.resolver
from builtwith import builtwith
import ipinfo
import socket
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import asyncio
import concurrent.futures
from config import IPINFO_TOKEN


class DomainChecker:
    def __init__(self):
        self.ipinfo_handler = ipinfo.getHandler(IPINFO_TOKEN) if IPINFO_TOKEN else ipinfo.getHandler()
    
    def get_whois_info(self, domain: str) -> Dict:
        """Get WHOIS information for a domain"""
        try:
            domain_info = whois.whois(domain)
            
            # Handle case where domain is not registered
            if not domain_info or not domain_info.registrar:
                return {"error": "not_registered"}
            
            # Format dates
            creation_date = domain_info.creation_date
            expiration_date = domain_info.expiration_date
            
            # Handle multiple dates (some domains return lists)
            if isinstance(creation_date, list):
                creation_date = creation_date[0] if creation_date else None
            if isinstance(expiration_date, list):
                expiration_date = expiration_date[0] if expiration_date else None
            
            # Format nameservers
            nameservers = domain_info.name_servers
            if isinstance(nameservers, list):
                nameservers = [ns.lower() for ns in nameservers if ns]
            else:
                nameservers = [nameservers.lower()] if nameservers else []
            
            return {
                "registrar": domain_info.registrar,
                "creation_date": creation_date.strftime("%Y-%m-%d") if creation_date else "N/A",
                "expiration_date": expiration_date.strftime("%Y-%m-%d") if expiration_date else "N/A",
                "nameservers": nameservers[:3]  # Limit to first 3 nameservers
            }
        except Exception as e:
            return {"error": "whois_failed", "message": str(e)}
    
    def get_dns_records(self, domain: str) -> Dict:
        """Get DNS records for a domain"""
        records = {}
        
        # DNS record types to query
        record_types = ['A', 'MX', 'NS', 'TXT']
        
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                if record_type == 'A':
                    records[record_type] = [str(rdata) for rdata in answers]
                elif record_type == 'MX':
                    records[record_type] = [f"{rdata.exchange} (priority: {rdata.preference})" for rdata in answers]
                elif record_type == 'NS':
                    records[record_type] = [str(rdata).rstrip('.') for rdata in answers]
                elif record_type == 'TXT':
                    # Join TXT record parts and limit length
                    txt_records = []
                    for rdata in answers:
                        txt_value = ''.join(str(part) for part in rdata.strings)
                        if len(txt_value) > 100:
                            txt_value = txt_value[:97] + "..."
                        txt_records.append(f'"{txt_value}"')
                    records[record_type] = txt_records[:2]  # Limit to 2 TXT records
            except Exception:
                records[record_type] = ["Not found"]
        
        return records
    
    def get_tech_stack(self, domain: str) -> Dict:
        """Get technology stack information using builtwith"""
        try:
            tech_info = builtwith(f"http://{domain}")
            
            result = {}
            
            # Extract relevant technologies
            tech_mapping = {
                'web-servers': 'Web Server',
                'cms': 'CMS',
                'javascript-frameworks': 'JS Frameworks',
                'programming-languages': 'Languages',
                'web-frameworks': 'Frameworks'
            }
            
            for tech_key, display_name in tech_mapping.items():
                if tech_key in tech_info and tech_info[tech_key]:
                    result[display_name] = tech_info[tech_key][:3]  # Limit to 3 items
            
            return result if result else {"message": "No technologies detected"}
            
        except Exception as e:
            return {"error": "tech_detection_failed", "message": str(e)}
    
    def get_ip_info(self, domain: str) -> Dict:
        """Get IP information and geolocation"""
        try:
            # Get IP address
            ip_address = socket.gethostbyname(domain)
            
            # Get IP details from IPinfo
            details = self.ipinfo_handler.getDetails(ip_address)
            
            return {
                "ip": ip_address,
                "country": getattr(details, 'country', 'N/A'),
                "region": getattr(details, 'region', 'N/A'),
                "city": getattr(details, 'city', 'N/A'),
                "org": getattr(details, 'org', 'N/A'),
                "asn": getattr(details, 'asn', {}).get('asn', 'N/A') if hasattr(details, 'asn') else 'N/A',
                "company": getattr(details, 'company', {}).get('name', 'N/A') if hasattr(details, 'company') else 'N/A'
            }
        except Exception as e:
            return {"error": "ip_info_failed", "message": str(e)}
    
    async def check_domain_async(self, domain: str) -> Dict:
        """Perform all domain checks asynchronously"""
        loop = asyncio.get_event_loop()
        
        # Run blocking operations in thread pool
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            # Submit all tasks
            whois_future = loop.run_in_executor(executor, self.get_whois_info, domain)
            dns_future = loop.run_in_executor(executor, self.get_dns_records, domain)
            tech_future = loop.run_in_executor(executor, self.get_tech_stack, domain)
            ip_future = loop.run_in_executor(executor, self.get_ip_info, domain)
            
            # Wait for all results
            whois_result = await whois_future
            dns_result = await dns_future
            tech_result = await tech_future
            ip_result = await ip_future
        
        return {
            "whois": whois_result,
            "dns": dns_result,
            "tech": tech_result,
            "ip": ip_result
        }
    
    def format_results(self, domain: str, results: Dict) -> str:
        """Format the results into a markdown message"""
        whois_data = results.get("whois", {})
        
        # Check if domain is not registered
        if whois_data.get("error") == "not_registered":
            return f"Domain *{domain}* belum registered, go own it! 🚀"
        
        message_parts = []
        
        # WHOIS Information
        if "error" not in whois_data:
            message_parts.append("*🔍 WHOIS*")
            message_parts.append(f"Registrar: {whois_data.get('registrar', 'N/A')}")
            message_parts.append(f"Creation: {whois_data.get('creation_date', 'N/A')}")
            message_parts.append(f"Expiry: {whois_data.get('expiration_date', 'N/A')}")
            
            nameservers = whois_data.get('nameservers', [])
            if nameservers:
                ns_list = ', '.join(nameservers)
                message_parts.append(f"Nameservers: {ns_list}")
            message_parts.append("")
        
        # DNS Records
        dns_data = results.get("dns", {})
        if dns_data:
            message_parts.append("*🌐 DNS Records*")
            for record_type, values in dns_data.items():
                if values and values != ["Not found"]:
                    if isinstance(values, list):
                        if len(values) == 1:
                            message_parts.append(f"{record_type}: {values[0]}")
                        else:
                            message_parts.append(f"{record_type}: {', '.join(values[:2])}")
                    else:
                        message_parts.append(f"{record_type}: {values}")
            message_parts.append("")
        
        # Technology Stack
        tech_data = results.get("tech", {})
        if tech_data and "error" not in tech_data and "message" not in tech_data:
            message_parts.append("*⚙️ Tech Stack*")
            for tech_type, technologies in tech_data.items():
                if isinstance(technologies, list):
                    tech_list = ', '.join(technologies)
                    message_parts.append(f"{tech_type}: {tech_list}")
            message_parts.append("")
        
        # IP Information
        ip_data = results.get("ip", {})
        if ip_data and "error" not in ip_data:
            message_parts.append("*📍 IP Info*")
            message_parts.append(f"IP: {ip_data.get('ip', 'N/A')}")
            message_parts.append(f"Country: {ip_data.get('country', 'N/A')}")
            if ip_data.get('city') != 'N/A':
                message_parts.append(f"City: {ip_data.get('city', 'N/A')}")
            
            org = ip_data.get('org', 'N/A')
            if org != 'N/A':
                message_parts.append(f"ISP: {org}")
        
        return '\n'.join(message_parts) if message_parts else f"Unable to gather information for domain *{domain}*"