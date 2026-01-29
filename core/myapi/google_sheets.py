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
    
    def ensure_email_column(self):
        """
        Ensure the email column exists in the sheet.
        If not, add it as the 4th column.
        """
        headers = self.sheet.row_values(1)
        if 'email' not in headers:
            # Add email header in column D
            self.sheet.update_cell(1, 4, 'email')
    
    def get_all_rows(self, user_email=None):
        """
        Get all rows from the sheet.
        
        Args:
            user_email: Optional email to filter by (for regular users).
            
        Returns:
            list: List of dictionaries representing rows.
        """
        records = self.sheet.get_all_records()
        
        # Filter by email if provided
        if user_email:
            records = [r for r in records if r.get('email') == user_email]
        
        return records
    
    def get_row(self, row_id, user_email=None):
        """
        Get a specific row by ID.
        
        Args:
            row_id: The ID of the row to retrieve.
            user_email: Optional email to verify ownership.
            
        Returns:
            dict: Row data or None if not found.
        """
        records = self.sheet.get_all_records()
        for record in records:
            if record.get('id') == row_id:
                # Check email ownership if provided
                if user_email and record.get('email') != user_email:
                    return None
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
    
    def create_row(self, data, user_email=None):
        """
        Create a new row in the sheet.
        
        Args:
            data: Dictionary with 'name' and 'description' keys.
            user_email: Email of the user creating the row.
            
        Returns:
            dict: The created row data with assigned ID.
        """
        # Ensure email column exists
        self.ensure_email_column()
        
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
            'description': data.get('description', ''),
            'email': user_email or data.get('email', '')
        }
        
        # Append to sheet
        self.sheet.append_row([new_row['id'], new_row['name'], new_row['description'], new_row['email']])
        
        return new_row
    
    def update_row(self, row_id, data, user_email=None):
        """
        Update an existing row.
        
        Args:
            row_id: The ID of the row to update.
            data: Dictionary with fields to update.
            user_email: Email to verify ownership.
            
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
        
        # Check ownership if email provided
        if user_email and current.get('email') != user_email:
            return None
        
        # Merge with updates (don't allow changing email)
        updated = {
            'id': row_id,
            'name': data.get('name', current.get('name', '')),
            'description': data.get('description', current.get('description', '')),
            'email': current.get('email', '')  # Keep original email
        }
        
        # Update the row
        self.sheet.update(f'A{row_number}:D{row_number}', 
                         [[updated['id'], updated['name'], updated['description'], updated['email']]])
        
        return updated
    
    def delete_row(self, row_id, user_email=None):
        """
        Delete a row by ID.
        
        Args:
            row_id: The ID of the row to delete.
            user_email: Email to verify ownership.
            
        Returns:
            bool: True if deleted, False if not found or not authorized.
        """
        # Check ownership first
        if user_email:
            current = self.get_row(row_id)
            if current is None or current.get('email') != user_email:
                return False
        
        row_number = self.get_row_number(row_id)
        if row_number is None:
            return False
        
        self.sheet.delete_rows(row_number)
        return True


# Singleton instance for easy access
sheets_service = GoogleSheetsService()
