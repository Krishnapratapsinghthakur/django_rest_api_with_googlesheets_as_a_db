"""
Google Sheets API Views

REST API views for performing CRUD operations on Google Sheets data.
With user-based data isolation using email.
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .google_sheets import sheets_service


class SheetItemListCreateAPIView(APIView):
    """
    API view for listing all items and creating new items in Google Sheets.
    
    GET: Returns all rows from the sheet (filtered by user email for non-superusers).
    POST: Creates a new row with user's email automatically assigned.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get all items from Google Sheets."""
        try:
            user = request.user
            # Superusers see all, regular users see only their items
            if user.is_superuser:
                items = sheets_service.get_all_rows()
            else:
                items = sheets_service.get_all_rows(user_email=user.email)
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
            
            # Auto-assign user's email
            user = request.user
            item = sheets_service.create_row(data, user_email=user.email)
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
    
    GET: Returns a single row by ID (with ownership check for non-superusers).
    PUT: Updates a row by ID (only if owned by user or superuser).
    DELETE: Deletes a row by ID (only if owned by user or superuser).
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, row_id):
        """Get a specific item by ID."""
        try:
            user = request.user
            user_email = None if user.is_superuser else user.email
            
            item = sheets_service.get_row(row_id, user_email=user_email)
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
            user = request.user
            user_email = None if user.is_superuser else user.email
            
            item = sheets_service.update_row(row_id, request.data, user_email=user_email)
            if item is None:
                return Response(
                    {'error': 'Item not found or not authorized'},
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
            user = request.user
            user_email = None if user.is_superuser else user.email
            
            deleted = sheets_service.delete_row(row_id, user_email=user_email)
            if not deleted:
                return Response(
                    {'error': 'Item not found or not authorized'},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            error_msg = str(e) if str(e) else f"{type(e).__name__}: {repr(e)}"
            return Response(
                {'error': error_msg},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
