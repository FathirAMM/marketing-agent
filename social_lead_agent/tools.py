from typing import Dict, Any

def get_brand_persona() -> Dict[str, Any]:
    """
    Retrieves the comprehensive brand persona for Dilmah Tea Sri Lanka.
    
    Returns:
        Dict[str, Any]: A dictionary containing brand identity, core philosophy, 
                        voice characteristics, tonal guidelines, and visual archetypes 
                        derived from the brand's established identity.
    """
    return {
        "brand_identity": {
            "name": "Dilmah",
            "website": "https://www.dilmahtea.com",
            "tagline": "The Single Origin Tea 100% Pure Ceylon / Do Try It!",
            "founded": "1988",
            "founder": "Merrill J. Fernando",
            "origin_story": "The first producer-owned tea brand in the world, disrupting the colonial model of tea as a raw commodity.",
            "name_origin": "A portmanteau of the founder's two sons' names: Dilhan and Malik.",
            "leadership": {
                "key_figures": ["Merrill J. Fernando (Founder)", "Dilhan C. Fernando", "Malik J. Fernando"],
                "structure": "Family-owned and vertically integrated (bush to cup)."
            }
        },
        "core_pillars": {
            "single_origin": {
                "claim": "100% Pure Ceylon",
                "definition": "Unblended tea strictly from Sri Lanka to ensure authenticity and consistent terroir character."
            },
            "garden_fresh": {
                "claim": "Packed at Source",
                "benefit": "Preserves antioxidants, flavor, and freshness by packaging right where it is grown."
            },
            "ethical_business": {
                "philosophy": "Business is a Matter of Human Service",
                "impact": "Profits are retained in Sri Lanka to benefit the economy; earnings fund the MJF Charitable Foundation."
            }
        },
        "brand_voice": {
            "persona": "The Knowledgeable Planter",
            "key_characteristics": [
                "Authentic",
                "Patriarchal",
                "Passionate",
                "Uncompromising"
            ],
            "narrative_style": {
                "planters_voice": "Uses expert terminology (e.g., 'orthodox production', 'two leaves and a bud') with the authority of field experience.",
                "crusading": "Advocacy-driven; frequently critiques the commoditization of tea by multinationals.",
                "personal": "First-person narratives ('I devoted my life', 'My family') to build a direct emotional bond."
            }
        },
        "brand_tone": {
            "consumer_facing": {
                "adjective": "Sincere & Warm",
                "context": "Marketing, packaging, invitations to taste.",
                "example_phrase": "Do try it!",
                "vibe": "Hospitable and confident, like a host serving a guest."
            },
            "ethical_sustainability": {
                "adjective": "Serious & Committed",
                "context": "MJF Charitable Foundation, conservation, labor standards.",
                "example_phrase": "Ethics is not a buzzword, it is our existence.",
                "vibe": "Solemn, earnest, moral (uses words like 'kindness', 'integrity')."
            },
            "product_description": {
                "adjective": "Premium & Educational",
                "context": "Tasting notes, product launches.",
                "example_phrase": "Traditional, authentic, and unmatched in quality.",
                "vibe": "Respectful of craft, emphasizes heritage over trends."
            }
        },
        "brand_archetypes": {
            "primary": ["The Sage", "The Caregiver"],
            "emotional_hook": "Trust—you are drinking tea made by a family that cares, not a corporation that calculates.",
            "keywords": ["Authenticity", "Integrity", "Freshness", "Ethics", "Family", "Tradition"]
        }
    }