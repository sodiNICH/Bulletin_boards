"""
Handler HTTP error
"""

from django.shortcuts import render


def handler_404(request, exception=None):
    """
    Handler for error 404
    """
    return render(request, '/handler/404.html', status=404)
