#!/usr/bin/env python3
"""
Test script to verify Coast Guard compliant citation generation.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from citation_formatter import CitationFormatter
from cg_docx_export import generate_cg_compliant_docx


def test_citation_generation():
    """Test citation generation for various award types."""
    
    formatter = CitationFormatter()
    
    # Test data
    test_cases = [
        {
            "award": "Coast Guard Achievement Medal",
            "awardee_info": {
                "name": "John Smith",
                "rank": "BM2",
                "unit": "Coast Guard Station Miami",
                "position": "Officer in Charge"
            },
            "achievement_data": {
                "time_period": "1 January 2024 to 31 December 2024",
                "achievements": [
                    "Led 15-person boat crew in conducting 127 search and rescue missions",
                    "Saved 23 lives during hazardous weather conditions",
                    "Implemented new training program improving crew readiness by 40%"
                ],
                "impacts": [
                    "Reduced response time by 35% through innovative patrol patterns",
                    "Saved $125,000 in equipment costs through preventive maintenance program"
                ],
                "leadership_details": [
                    "Supervised and trained 15 crew members",
                    "Coordinated with local emergency services"
                ],
                "scope": "sector",
                "justification": "Exceptional performance in maritime safety operations"
            }
        },
        {
            "award": "Meritorious Service Medal",
            "awardee_info": {
                "name": "Jane Doe",
                "rank": "LCDR",
                "unit": "Coast Guard District Seven",
                "position": "Operations Officer"
            },
            "achievement_data": {
                "time_period": "1 July 2022 to 30 June 2024",
                "achievements": [
                    "Orchestrated district-wide operational improvements affecting 45 units",
                    "Developed revolutionary resource allocation system",
                    "Led hurricane response operations saving 147 lives"
                ],
                "impacts": [
                    "Improved operational efficiency by 52% across the district",
                    "Reduced budget expenditures by $2.3 million annually"
                ],
                "scope": "district",
                "justification": "Outstanding leadership in transforming district operations"
            }
        }
    ]
    
    print("COAST GUARD CITATION COMPLIANCE TEST")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_case['award']}")
        print("-" * 40)
        
        # Generate citation
        citation = formatter.format_citation(
            test_case["award"],
            test_case["awardee_info"],
            test_case["achievement_data"]
        )
        
        # Validate citation
        is_valid, issues = formatter.validate_citation(citation, test_case["award"])
        
        # Display results
        print(f"Awardee: {test_case['awardee_info']['rank']} {test_case['awardee_info']['name']}")
        print(f"Valid: {'YES' if is_valid else 'NO'}")
        
        if issues:
            print("Issues:")
            for issue in issues:
                print(f"  - {issue}")
        
        print(f"\nCitation ({len(citation.split())} words, {len(citation.split('\\n'))} lines):")
        print("-" * 40)
        print(citation)
        print("-" * 40)
        
        # Check line limits
        max_lines = formatter.LINE_LIMITS.get(test_case["award"], 12)
        line_count = len(citation.split('\n'))
        print(f"Line Count: {line_count}/{max_lines} {'✓' if line_count <= max_lines else '✗'}")
        
        # Check for required elements (case-insensitive)
        citation_lower = citation.lower()
        has_opening = any(phrase.lower() in citation_lower for phrase in formatter.OPENING_PHRASES.values())
        has_closing = "traditions of the united states coast guard" in citation_lower
        print(f"Standard Opening: {'✓' if has_opening else '✗'}")
        print(f"Standard Closing: {'✓' if has_closing else '✗'}")


def test_docx_export():
    """Test DOCX export generation."""
    print("\n\nTesting DOCX Export")
    print("=" * 60)
    
    export_data = {
        "awardee_info": {
            "name": "Test Officer",
            "rank": "LT",
            "unit": "Test Unit"
        },
        "finalized_award": {
            "award": "Coast Guard Commendation Medal",
            "citation": "Test citation text"
        },
        "achievement_data": {
            "time_period": "2024",
            "achievements": ["Test achievement 1", "Test achievement 2"],
            "impacts": ["Test impact 1", "Test impact 2"]
        }
    }
    
    try:
        doc_bytes = generate_cg_compliant_docx(export_data)
        print(f"✓ DOCX generated successfully ({len(doc_bytes)} bytes)")
        
        # Save test file
        test_file = Path("test_cg_compliant_award.docx")
        test_file.write_bytes(doc_bytes)
        print(f"✓ Test file saved as: {test_file}")
        
    except Exception as e:
        print(f"✗ Error generating DOCX: {e}")


if __name__ == "__main__":
    test_citation_generation()
    test_docx_export()
    print("\n\nCompliance testing complete!")