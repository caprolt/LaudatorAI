"""Default resume template configuration."""

from typing import Dict, Any, List
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.shared import OxmlElement, qn


class DefaultResumeTemplate:
    """Default resume template with professional styling."""
    
    def __init__(self):
        self.name = "default"
        self.description = "Professional resume template with clean formatting"
        
        # Document settings
        self.margins = {
            'top': Inches(0.5),
            'bottom': Inches(0.5),
            'left': Inches(0.75),
            'right': Inches(0.75)
        }
        
        # Font settings
        self.fonts = {
            'name': {'name': 'Calibri', 'size': Pt(18), 'bold': True},
            'contact': {'name': 'Calibri', 'size': Pt(10)},
            'heading': {'name': 'Calibri', 'size': Pt(14), 'bold': True},
            'body': {'name': 'Calibri', 'size': Pt(11)},
            'skills': {'name': 'Calibri', 'size': Pt(10)}
        }
        
        # Section order
        self.sections = [
            'header',
            'summary',
            'experience',
            'education',
            'skills',
            'certifications',
            'projects'
        ]
    
    def get_section_config(self, section_name: str) -> Dict[str, Any]:
        """Get configuration for a specific section."""
        configs = {
            'header': {
                'alignment': WD_ALIGN_PARAGRAPH.CENTER,
                'spacing_after': Inches(0.2)
            },
            'summary': {
                'alignment': WD_ALIGN_PARAGRAPH.LEFT,
                'spacing_after': Inches(0.1)
            },
            'experience': {
                'alignment': WD_ALIGN_PARAGRAPH.LEFT,
                'spacing_after': Inches(0.1),
                'item_spacing': Inches(0.05)
            },
            'education': {
                'alignment': WD_ALIGN_PARAGRAPH.LEFT,
                'spacing_after': Inches(0.1)
            },
            'skills': {
                'alignment': WD_ALIGN_PARAGRAPH.LEFT,
                'spacing_after': Inches(0.1),
                'columns': 2
            },
            'certifications': {
                'alignment': WD_ALIGN_PARAGRAPH.LEFT,
                'spacing_after': Inches(0.1)
            },
            'projects': {
                'alignment': WD_ALIGN_PARAGRAPH.LEFT,
                'spacing_after': Inches(0.1)
            }
        }
        
        return configs.get(section_name, {})
    
    def format_personal_info(self, personal_info: Dict[str, Any]) -> List[str]:
        """Format personal information for display."""
        formatted_lines = []
        
        # Name (extract from first line or use placeholder)
        name = personal_info.get('name', 'Your Name')
        formatted_lines.append(name)
        
        # Contact information
        contact_parts = []
        if personal_info.get('email'):
            contact_parts.append(personal_info['email'])
        if personal_info.get('phone'):
            contact_parts.append(personal_info['phone'])
        if personal_info.get('address'):
            contact_parts.append(personal_info['address'])
        
        if contact_parts:
            formatted_lines.append(' | '.join(contact_parts))
        
        return formatted_lines
    
    def format_experience(self, experience: List[Dict[str, Any]]) -> List[str]:
        """Format experience entries."""
        formatted_lines = []
        
        for exp in experience:
            # Job title and company
            title = exp.get('title', 'Unknown Position')
            company = exp.get('company', '')
            duration = exp.get('duration', '')
            
            if company and duration:
                formatted_lines.append(f"{title} at {company} ({duration})")
            elif company:
                formatted_lines.append(f"{title} at {company}")
            else:
                formatted_lines.append(title)
            
            # Description
            description = exp.get('description', '')
            if description:
                formatted_lines.append(description)
            
            formatted_lines.append('')  # Spacing
        
        return formatted_lines
    
    def format_education(self, education: List[Dict[str, Any]]) -> List[str]:
        """Format education entries."""
        formatted_lines = []
        
        for edu in education:
            institution = edu.get('institution', 'Unknown Institution')
            degree = edu.get('degree', '')
            year = edu.get('year', '')
            
            if degree and year:
                formatted_lines.append(f"{degree} from {institution} ({year})")
            elif degree:
                formatted_lines.append(f"{degree} from {institution}")
            else:
                formatted_lines.append(institution)
            
            formatted_lines.append('')  # Spacing
        
        return formatted_lines
    
    def format_skills(self, skills: List[str]) -> str:
        """Format skills list."""
        if not skills:
            return ""
        
        # Group skills by category if they contain common prefixes
        skill_groups = {}
        other_skills = []
        
        for skill in skills:
            skill_lower = skill.lower()
            if any(tech in skill_lower for tech in ['python', 'java', 'javascript', 'react', 'node']):
                if 'Programming' not in skill_groups:
                    skill_groups['Programming'] = []
                skill_groups['Programming'].append(skill)
            elif any(tech in skill_lower for tech in ['sql', 'database', 'mysql', 'postgresql']):
                if 'Databases' not in skill_groups:
                    skill_groups['Databases'] = []
                skill_groups['Databases'].append(skill)
            elif any(tech in skill_lower for tech in ['aws', 'azure', 'docker', 'kubernetes']):
                if 'Cloud/DevOps' not in skill_groups:
                    skill_groups['Cloud/DevOps'] = []
                skill_groups['Cloud/DevOps'].append(skill)
            else:
                other_skills.append(skill)
        
        # Format grouped skills
        formatted_parts = []
        for group, group_skills in skill_groups.items():
            formatted_parts.append(f"{group}: {', '.join(group_skills)}")
        
        if other_skills:
            formatted_parts.append(f"Other: {', '.join(other_skills)}")
        
        return '; '.join(formatted_parts)


# Template registry
TEMPLATE_REGISTRY = {
    'default': DefaultResumeTemplate()
}


def get_template(template_name: str = 'default') -> DefaultResumeTemplate:
    """Get a resume template by name."""
    return TEMPLATE_REGISTRY.get(template_name, TEMPLATE_REGISTRY['default'])


def list_templates() -> List[Dict[str, str]]:
    """List available templates."""
    return [
        {
            'name': name,
            'description': template.description
        }
        for name, template in TEMPLATE_REGISTRY.items()
    ]
