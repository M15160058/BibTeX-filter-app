# app.py
import streamlit as st
import re

def filter_bibtex(entry, fields):
    header_match = re.match(r'@(\w+)\{([^,]+),', entry)
    if not header_match:
        return "Invalid BibTeX entry"
    entry_type, citation_key = header_match.groups()
    
    filtered_fields = []
    for field in fields:
        pattern = rf'{field}\s*=\s*\{{(.*?)\}},?'
        match = re.search(pattern, entry, re.DOTALL)
        if match:
            value = match.group(1).strip()
            filtered_fields.append(f'  {field}={{ {value} }}')
    
    filtered_entry = f'@{entry_type}{{{citation_key},\n' + ',\n'.join(filtered_fields) + '\n}'
    filtered_entry = re.sub(r'\{\s+(.*?)\s+\}', r'{\1}', filtered_entry)
    return filtered_entry

st.title("BibTeX Field Filter")
# Author info with clickable link
st.markdown(
    "Developed by **Arif Hossin** – "
    "[Linkedin Profile](https://www.linkedin.com/in/arif-hossin-7ab23952/)\n"
    "[GitHub Profile](https://github.com/M15160058)"
)

bibtex_entry = st.text_area("Paste your BibTeX entry here:")

all_fields = ["title", "author", "journal", "volume", "number", "pages", "year", "doi", "url", "issn", "keywords", "abstract"]
fields_to_include = st.multiselect("Select fields to include:", options=all_fields, default=["title", "author", "journal", "volume", "number", "pages", "year"])

if st.button("Generate Filtered BibTeX"):
    if bibtex_entry.strip() == "":
        st.warning("Please paste a BibTeX entry first.")
    else:
        filtered = filter_bibtex(bibtex_entry, fields_to_include)
        st.code(filtered)
