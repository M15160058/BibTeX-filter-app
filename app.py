# app.py
import streamlit as st
import re

def filter_bibtex(entry, fields):
    """
    Filters a BibTeX entry to include only the specified fields.
    Supports multi-line values and both {value} and "value" styles.
    """
    # Extract entry type and citation key
    header_match = re.match(r'@(\w+)\{([^,]+),', entry)
    if not header_match:
        return "Invalid BibTeX entry"
    entry_type, citation_key = header_match.groups()
    
    # Regex to match both {value} and "value", multi-line
    pattern = r'(\w+)\s*=\s*(?:\{(.*?)\}|"(.+?)")(?:,|$)'
    matches = re.findall(pattern, entry, re.DOTALL)
    
    # Build dictionary with cleaned values
    bib_dict = {}
    for key, val1, val2 in matches:
        value = val1 if val1 else val2
        # Replace newlines with spaces and strip
        value = re.sub(r'\s+', ' ', value.strip())
        bib_dict[key] = value
    
    # Build filtered BibTeX string
    filtered_fields = []
    for field in fields:
        if field in bib_dict:
            filtered_fields.append(f"  {field}={{{bib_dict[field]}}}")
    
    filtered_entry = f"@{entry_type}{{{citation_key},\n" + ",\n".join(filtered_fields) + "\n}"
    return filtered_entry

# ---------------------
# Streamlit UI
# ---------------------
st.title("BibTeX Field Filter")

# Author info with clickable links
st.markdown(
    """
    Developed by **Arif Hossin**  
    [LinkedIn Profile](https://www.linkedin.com/in/arif-hossin-7ab23952/) | 
    [GitHub Profile](https://github.com/M15160058)
    """
)

# Input area for BibTeX
bibtex_entry = st.text_area("Paste your BibTeX entry here:")

# Detect entry type to adjust default fields dynamically
entry_type_match = re.match(r'@(\w+)\{', bibtex_entry.strip())
if entry_type_match:
    entry_type = entry_type_match.group(1).lower()
else:
    entry_type = "article"  # fallback

# Default fields based on type
if entry_type == "article":
    default_fields = ["title", "author", "journal", "volume", "number", "pages", "year"]
elif entry_type in ["book", "inbook"]:
    default_fields = ["title", "author", "editor", "bookTitle", "publisher", "year", "pages"]
elif entry_type in ["misc", "online", "website"]:
    default_fields = ["title", "author", "year", "url"]
else:
    default_fields = ["title", "author", "year"]

# Fields options
all_fields = ["title", "author", "editor", "journal", "volume", "number", "pages", 
              "year", "doi", "url", "issn", "keywords", "abstract", "bookTitle", 
              "publisher", "address"]

fields_to_include = st.multiselect(
    "Select fields to include:", 
    options=all_fields, 
    default=default_fields
)

# Button to generate
if st.button("Generate Filtered BibTeX"):
    if bibtex_entry.strip() == "":
        st.warning("Please paste a BibTeX entry first.")
    else:
        filtered = filter_bibtex(bibtex_entry, fields_to_include)
        st.code(filtered) output:@article{IMPROTA1996323,
  title={Immunoglobulin-like modules from titin I-band: extensible components of muscle elasticity},
  author={Sabina Improta and Anastasia S Politou and Annalisa Pastore},
  journal={Structure},
  volume={4},
  number={3},
  pages={323-337},
  year={1996}
}} 
