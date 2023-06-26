import streamlit as st
import xml.etree.ElementTree as ET
import json
import io

def xml_to_json(xml_str):
    """Function to convert XML to JSON"""
    data = ET.parse(io.StringIO(xml_str))
    root = data.getroot()

    def _parse(node):
        json_node = dict()
        if len(list(node)) == 0:
            return node.text
        else:
            for child in node:
                if child.tag not in json_node:
                    json_node[child.tag] = _parse(child)
                else:
                    if type(json_node[child.tag]) is list:
                        json_node[child.tag].append(_parse(child))
                    else:
                        json_node[child.tag] = [json_node[child.tag], _parse(child)]
        return json_node

    return _parse(root)


def app():
    """Main function that contains Streamlit code"""
    st.title('XML to JSON converter')
    
    uploaded_file = st.file_uploader('Upload XML file', type='xml')

    if uploaded_file is not None:
        try:
            bytes_data = uploaded_file.read()  # read as bytes
            str_data = bytes_data.decode("utf-8")  # convert to string
            json_data = xml_to_json(str_data)
            st.code(json_data)
        except Exception as e:
            st.write("Error occurred:", str(e))

if __name__ == "__main__":
    app()
