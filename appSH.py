import streamlit as st
import requests
from urllib.parse import urlparse

def check_authentication(url):
    try:
        response = requests.head(url)
        if response.status_code == 401:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"Error checking authentication: {e}")
        return False

def delete_version_history(file_id, username, password):
    # Authenticate using provided credentials
    # ... (implement your authentication logic here)

    try:
        # Replace the placeholder with your API call to delete version history
        response = requests.delete(f"https://your-api-endpoint/{file_id}", auth=(username, password))
        if response.status_code == 200:
            st.success(f"Previous version history of file '{file_id}' deleted successfully.")
        else:
            st.error(f"Error deleting version history: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error deleting version history: {e}")

def get_file_list(folder_id, username, password):
    # Authenticate using provided credentials
    # ... (implement your authentication logic here)

    try:
        # Replace the placeholder with your API call to get file list
        response = requests.get(f"https://your-api-endpoint/{folder_id}", auth=(username, password))
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error getting file list: {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error getting file list: {e}")
        return []

def process_folder(folder_id, username, password):
    file_list = get_file_list(folder_id, username, password)
    for file in file_list:
        if file.get('mimeType') == 'application/vnd.google-apps.folder':
            process_folder(file.get('id'), username, password)
        else:
            st.write(f"File: {file.get('title')}")
            if st.checkbox(f"Delete previous version history for {file.get('title')}"):
                delete_version_history(file.get('id'), username, password)

def main():
    st.title("Delete SharePoint File Version History")

    sharepoint_link = st.text_input("Enter SharePoint link:")
    if sharepoint_link:
        # Check if authentication is required
        requires_authentication = check_authentication(sharepoint_link)
        if requires_authentication:
            username = st.text_input("Enter username:")
            password = st.text_input("Enter password:", type="password")
            if username and password:
                # Extract the file ID from the SharePoint link
                file_id = urlparse(sharepoint_link).path.strip("/")

                # Process the folder and its subfolders
                process_folder(file_id, username, password)
        else:
            st.warning("Authentication not required for this link.")

if __name__ == "__main__":
    main()
