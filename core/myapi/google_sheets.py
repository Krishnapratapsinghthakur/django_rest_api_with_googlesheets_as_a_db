"""
Google Sheets Service Module

This module provides a service class for interacting with Google Sheets
as a database backend. It supports CRUD operations on sheet data.
"""

import os
import gspread
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from django.conf import settings


class GoogleSheetsService:
    """Service class for Google Sheets CRUD operations."""
    
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    def __init__(self):
        """Initialize the Google Sheets connection."""
        self._client = None
        self._sheet = None
        self._token_file = os.path.join(settings.BASE_DIR, 'token.json')
    
    def _get_credentials(self):
        """Get OAuth2 credentials with token refresh support."""
        creds = None
        
        # Check if token.json exists (from previous authentication)
        if os.path.exists(self._token_file):
            creds = Credentials.from_authorized_user_file(self._token_file, self.SCOPES)
        
        # If no valid credentials, perform OAuth flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                # Refresh expired token
                creds.refresh(Request())
            else:
                # Run OAuth flow (opens browser for first-time auth)
                flow = InstalledAppFlow.from_client_secrets_file(
                    settings.GOOGLE_SHEETS_CREDENTIALS_FILE,
                    self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open(self._token_file, 'w') as token:
                token.write(creds.to_json())
        
        return creds
    
    @property
    def client(self):
        """Lazy-load the gspread client."""
        if self._client is None:
            credentials = self._get_credentials()
            self._client = gspread.authorize(credentials)
        return self._client
    
    @property
    def sheet(self):
        """Lazy-load the worksheet."""
        if self._sheet is None:
            spreadsheet = self.client.open_by_key(settings.GOOGLE_SHEETS_SPREADSHEET_ID)
            self._sheet = spreadsheet.sheet1  # Use first sheet
        return self._sheet
    
    def get_all_rows(self):
        """
        Get all rows from the sheet.
        
        Returns:
            list: List of dictionaries representing rows.
        """
        records = self.sheet.get_all_records()
        return records
    
    def get_row(self, row_id):
        """
        Get a specific row by ID.
        
        Args:
            row_id: The ID of the row to retrieve.
            
        Returns:
            dict: Row data or None if not found.
        """
        records = self.sheet.get_all_records()
        for record in records:
            if record.get('id') == row_id:
                return record
        return None
    
    def get_row_number(self, row_id):
        """
        Get the 1-indexed row number for a given ID.
        
        Args:
            row_id: The ID of the row.
            
        Returns:
            int: Row number (1-indexed, accounting for header) or None.
        """
        records = self.sheet.get_all_records()
        for idx, record in enumerate(records):
            if record.get('id') == row_id:
                return idx + 2  # +2 for header row (1) and 0-indexing
        return None
    
    def create_row(self, data):
        """
        Create a new row in the sheet.
        
        Args:
            data: Dictionary with 'name' and 'description' keys.
            
        Returns:
            dict: The created row data with assigned ID.
        """
        # Get the next ID - handle empty or non-integer IDs
        records = self.sheet.get_all_records()
        ids = []
        for r in records:
            id_val = r.get('id', 0)
            if isinstance(id_val, int):
                ids.append(id_val)
            elif isinstance(id_val, str) and id_val.isdigit():
                ids.append(int(id_val))
        next_id = max(ids, default=0) + 1
        
        # Prepare row data
        new_row = {
            'id': next_id,
            'name': data.get('name', ''),
            'description': data.get('description', '')
        }
        
        # Append to sheet
        self.sheet.append_row([new_row['id'], new_row['name'], new_row['description']])
        
        return new_row
    
    def update_row(self, row_id, data):
        """
        Update an existing row.
        
        Args:
            row_id: The ID of the row to update.
            data: Dictionary with fields to update.
            
        Returns:
            dict: Updated row data or None if not found.
        """
        row_number = self.get_row_number(row_id)
        if row_number is None:
            return None
        
        # Get current data
        current = self.get_row(row_id)
        if current is None:
            return None
        
        # Merge with updates
        updated = {
            'id': row_id,
            'name': data.get('name', current.get('name', '')),
            'description': data.get('description', current.get('description', ''))
        }
        
        # Update the row
        self.sheet.update(f'A{row_number}:C{row_number}', 
                         [[updated['id'], updated['name'], updated['description']]])
        
        return updated
    
    def delete_row(self, row_id):
        """
        Delete a row by ID.
        
        Args:
            row_id: The ID of the row to delete.
            
        Returns:
            bool: True if deleted, False if not found.
        """
        row_number = self.get_row_number(row_id)
        if row_number is None:
            return False
        
        self.sheet.delete_rows(row_number)
        return True


# Singleton instance for easy access
sheets_service = GoogleSheetsService()
