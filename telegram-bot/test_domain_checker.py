#!/usr/bin/env python3
"""
Test script for DomainIntelBot domain checking functionality
This can be used to test the core features without running the Telegram bot
"""

import asyncio
import sys
from domain_checker import DomainChecker

async def test_domain_check(domain: str):
    """Test domain checking functionality"""
    print(f"🔍 Testing domain: {domain}")
    print("-" * 50)
    
    checker = DomainChecker()
    
    try:
        # Perform domain analysis
        results = await checker.check_domain_async(domain)
        
        # Format and display results
        formatted_output = checker.format_results(domain, results)
        print(formatted_output)
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("-" * 50)

async def main():
    """Main test function"""
    # Test domains
    test_domains = [
        "google.com",
        "github.com", 
        "nonexistent-domain-12345.com"  # Should show "belum registered"
    ]
    
    if len(sys.argv) > 1:
        # Use domain from command line argument
        test_domains = [sys.argv[1]]
    
    print("🤖 DomainIntelBot - Test Mode")
    print("Testing domain checking functionality...\n")
    
    for domain in test_domains:
        await test_domain_check(domain)
        print()

if __name__ == "__main__":
    # Run the test
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Test interrupted")
    except Exception as e:
        print(f"❌ Test failed: {e}")