"""Default cover letter template with styling and structure."""

def get_template() -> dict:
    """Get the default cover letter template."""
    return {
        "name": "default_cover_letter",
        "version": "1.0",
        "description": "Professional cover letter template with clean formatting",
        "css": """
            @page {
                margin: 1in;
                size: letter;
            }
            
            body {
                font-family: 'Times New Roman', serif;
                font-size: 12pt;
                line-height: 1.5;
                color: #333;
                margin: 0;
                padding: 0;
            }
            
            .cover-letter {
                max-width: 8.5in;
                margin: 0 auto;
                padding: 0;
            }
            
            .header {
                margin-bottom: 1.5em;
            }
            
            .name {
                font-size: 16pt;
                font-weight: bold;
                margin-bottom: 0.5em;
                color: #2c3e50;
            }
            
            .contact-info {
                font-size: 10pt;
                line-height: 1.4;
                color: #555;
            }
            
            .date {
                margin-bottom: 1.5em;
                font-size: 10pt;
            }
            
            .recipient {
                margin-bottom: 1.5em;
                font-size: 10pt;
                line-height: 1.4;
            }
            
            .greeting {
                margin-bottom: 1em;
                font-size: 10pt;
            }
            
            .content {
                margin-bottom: 1.5em;
            }
            
            .content p {
                margin-bottom: 1em;
                text-align: justify;
                font-size: 10pt;
                line-height: 1.6;
            }
            
            .signature {
                margin-top: 2em;
                font-size: 10pt;
                line-height: 1.4;
            }
            
            /* Print styles */
            @media print {
                body {
                    font-size: 12pt;
                }
                
                .cover-letter {
                    max-width: none;
                }
            }
        """,
        "structure": {
            "sections": [
                "header",
                "date", 
                "recipient",
                "greeting",
                "content",
                "signature"
            ],
            "required_fields": [
                "name",
                "email", 
                "phone",
                "location",
                "company",
                "greeting",
                "opening",
                "body",
                "closing",
                "signature"
            ]
        },
        "defaults": {
            "greeting": "Dear Hiring Manager,",
            "signature_format": "Sincerely,\n{name}",
            "date_format": "%B %d, %Y",
            "recipient_format": "Hiring Manager\n{company}"
        },
        "styling": {
            "font_family": "Times New Roman",
            "font_size": "12pt",
            "line_height": "1.5",
            "margins": "1in",
            "page_size": "letter"
        }
    }


def get_template_variants() -> dict:
    """Get different cover letter template variants."""
    return {
        "modern": {
            "name": "modern_cover_letter",
            "css": """
                @page {
                    margin: 0.75in;
                    size: letter;
                }
                
                body {
                    font-family: 'Arial', sans-serif;
                    font-size: 11pt;
                    line-height: 1.6;
                    color: #2c3e50;
                    margin: 0;
                    padding: 0;
                }
                
                .cover-letter {
                    max-width: 8.5in;
                    margin: 0 auto;
                    padding: 0;
                }
                
                .header {
                    margin-bottom: 1.5em;
                    border-bottom: 2px solid #3498db;
                    padding-bottom: 1em;
                }
                
                .name {
                    font-size: 18pt;
                    font-weight: bold;
                    margin-bottom: 0.5em;
                    color: #2c3e50;
                }
                
                .contact-info {
                    font-size: 10pt;
                    line-height: 1.4;
                    color: #7f8c8d;
                }
                
                .date {
                    margin-bottom: 1.5em;
                    font-size: 10pt;
                    color: #7f8c8d;
                }
                
                .recipient {
                    margin-bottom: 1.5em;
                    font-size: 10pt;
                    line-height: 1.4;
                }
                
                .greeting {
                    margin-bottom: 1em;
                    font-size: 10pt;
                    font-weight: bold;
                }
                
                .content {
                    margin-bottom: 1.5em;
                }
                
                .content p {
                    margin-bottom: 1em;
                    text-align: justify;
                    font-size: 10pt;
                    line-height: 1.6;
                }
                
                .signature {
                    margin-top: 2em;
                    font-size: 10pt;
                    line-height: 1.4;
                }
            """
        },
        "executive": {
            "name": "executive_cover_letter", 
            "css": """
                @page {
                    margin: 1.25in;
                    size: letter;
                }
                
                body {
                    font-family: 'Georgia', serif;
                    font-size: 12pt;
                    line-height: 1.7;
                    color: #1a1a1a;
                    margin: 0;
                    padding: 0;
                }
                
                .cover-letter {
                    max-width: 8.5in;
                    margin: 0 auto;
                    padding: 0;
                }
                
                .header {
                    margin-bottom: 2em;
                    text-align: center;
                }
                
                .name {
                    font-size: 20pt;
                    font-weight: bold;
                    margin-bottom: 0.5em;
                    color: #1a1a1a;
                    letter-spacing: 1px;
                }
                
                .contact-info {
                    font-size: 11pt;
                    line-height: 1.5;
                    color: #666;
                }
                
                .date {
                    margin-bottom: 2em;
                    font-size: 11pt;
                    text-align: right;
                }
                
                .recipient {
                    margin-bottom: 2em;
                    font-size: 11pt;
                    line-height: 1.5;
                }
                
                .greeting {
                    margin-bottom: 1.5em;
                    font-size: 11pt;
                    font-weight: bold;
                }
                
                .content {
                    margin-bottom: 2em;
                }
                
                .content p {
                    margin-bottom: 1.5em;
                    text-align: justify;
                    font-size: 11pt;
                    line-height: 1.7;
                    text-indent: 0.5in;
                }
                
                .signature {
                    margin-top: 2.5em;
                    font-size: 11pt;
                    line-height: 1.5;
                }
            """
        }
    }


def validate_template_data(data: dict) -> bool:
    """Validate that template data contains all required fields."""
    template = get_template()
    required_fields = template["structure"]["required_fields"]
    
    for field in required_fields:
        if field not in data or not data[field]:
            return False
    
    return True


def format_template_data(data: dict) -> dict:
    """Format template data with defaults and proper structure."""
    template = get_template()
    defaults = template["defaults"]
    
    # Apply defaults for missing fields
    if "greeting" not in data or not data["greeting"]:
        data["greeting"] = defaults["greeting"]
    
    if "signature" not in data or not data["signature"]:
        data["signature"] = defaults["signature_format"].format(name=data.get("name", ""))
    
    return data
