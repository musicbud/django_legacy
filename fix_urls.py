#!/usr/bin/env python3
"""
Script to add trailing slashes to all URL patterns in app/urls.py
"""

import re

def fix_urls():
    urls_file = 'app/urls.py'
    
    # Read the file
    with open(urls_file, 'r') as f:
        content = f.read()
    
    # Pattern to match path() without trailing slash (but not already having one)
    # Matches: path('some/path', ...) but not path('some/path/', ...)
    # Also skip paths with <int:...> or other dynamic parts at the end
    pattern = r"path\('([^']+?)(?<!/)'\s*,"
    
    def add_trailing_slash(match):
        url = match.group(1)
        # Don't add slash if URL already ends with slash or has dynamic part at end
        if url.endswith('/') or '>' in url.split('/')[-1]:
            return match.group(0)
        # Add trailing slash
        return f"path('{url}/', "
    
    # Apply the fix
    fixed_content = re.sub(pattern, add_trailing_slash, content)
    
    # Write back
    with open(urls_file, 'w') as f:
        f.write(fixed_content)
    
    print(f"✅ Fixed URL patterns in {urls_file}")
    print("Added trailing slashes to all URL patterns (except those with dynamic parts)")

if __name__ == '__main__':
    fix_urls()
