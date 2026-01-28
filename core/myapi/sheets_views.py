"""
Google Sheets API Views

REST API views for performing CRUD operations on Google Sheets data.
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .google_sheets import sheets_service


class SheetItemListCreateAPIView(APIView):
    """
    API view for listing all items and creating new items in Google Sheets.
    
    GET: Returns all rows from the sheet.
    POST: Creates a new row with provided data.
    """
    
    def get(self, request):
        """Get all items from Google Sheets."""
        try:
            items = sheets_service.get_all_rows()
            return Response(items, status=status.HTTP_200_OK)
        except Exception as e:
            error_msg = str(e) if str(e) else f"{type(e).__name__}: {repr(e)}"
            return Response(
                {'error': error_msg},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def post(self, request):
        """Create a new item in Google Sheets."""
        try:
            data = request.data
            if not data.get('name'):
                return Response(
                    {'error': 'Name is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            item = sheets_service.create_row(data)
            return Response(item, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_msg = str(e) if str(e) else f"{type(e).__name__}: {repr(e)}"
            return Response(
                {'error': error_msg},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SheetItemDetailAPIView(APIView):
    """
    API view for retrieving, updating, and deleting a specific item.
    
    GET: Returns a single row by ID.
    PUT: Updates a row by ID.
    DELETE: Deletes a row by ID.
    """
    
    def get(self, request, row_id):
        """Get a specific item by ID."""
        try:
            item = sheets_service.get_row(row_id)
            if item is None:
                return Response(
                    {'error': 'Item not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(item, status=status.HTTP_200_OK)
        except Exception as e:
            error_msg = str(e) if str(e) else f"{type(e).__name__}: {repr(e)}"
            return Response(
                {'error': error_msg},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def put(self, request, row_id):
        """Update a specific item by ID."""
        try:
            item = sheets_service.update_row(row_id, request.data)
            if item is None:
                return Response(
                    {'error': 'Item not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(item, status=status.HTTP_200_OK)
        except Exception as e:
            error_msg = str(e) if str(e) else f"{type(e).__name__}: {repr(e)}"
            return Response(
                {'error': error_msg},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def delete(self, request, row_id):
        """Delete a specific item by ID."""
        try:
            deleted = sheets_service.delete_row(row_id)
            if not deleted:
                return Response(
                    {'error': 'Item not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            error_msg = str(e) if str(e) else f"{type(e).__name__}: {repr(e)}"
            return Response(
                {'error': error_msg},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
