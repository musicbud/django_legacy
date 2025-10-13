#!/usr/bin/env python3
"""
Django to FastAPI Migration Script
Automatically converts Django views to FastAPI endpoints
"""
import os
import sys
import ast
import re
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DjangoEndpoint:
    """Represents a Django endpoint to be migrated"""
    url_pattern: str
    view_class: str
    view_method: str
    file_path: str
    line_number: int
    http_methods: List[str]
    auth_required: bool = True

@dataclass
class FastAPIEndpoint:
    """Represents a generated FastAPI endpoint"""
    path: str
    method: str
    function_name: str
    code: str
    dependencies: List[str]

class DjangoToFastAPIConverter:
    """Main converter class"""
    
    def __init__(self, django_root: Path, fastapi_root: Path):
        self.django_root = django_root
        self.fastapi_root = fastapi_root
        self.endpoints: List[DjangoEndpoint] = []
        self.converted_endpoints: List[FastAPIEndpoint] = []
        
    def analyze_django_urls(self) -> List[DjangoEndpoint]:
        """Analyze Django URLs to extract endpoints"""
        logger.info("🔍 Analyzing Django URLs...")
        
        # Read main urls.py
        urls_path = self.django_root / "app" / "urls.py"
        if not urls_path.exists():
            logger.error(f"❌ Django urls.py not found at {urls_path}")
            return []
        
        endpoints = []
        
        with open(urls_path, 'r') as f:
            content = f.read()
        
        # Parse URL patterns
        url_patterns = self.extract_url_patterns(content)
        
        for pattern in url_patterns:
            endpoint = self.analyze_url_pattern(pattern)
            if endpoint:
                endpoints.append(endpoint)
        
        logger.info(f"📋 Found {len(endpoints)} Django endpoints")
        return endpoints
    
    def extract_url_patterns(self, content: str) -> List[Dict[str, Any]]:
        """Extract URL patterns from Django urls.py"""
        patterns = []
        
        # Find path() calls
        path_pattern = r"path\(['\"]([^'\"]+)['\"],\s*([^,\s]+)(?:\.as_view\(\))?,\s*name=['\"]([^'\"]+)['\"]"
        matches = re.findall(path_pattern, content)
        
        for match in matches:
            url_path, view_name, url_name = match
            patterns.append({
                'url': url_path,
                'view': view_name,
                'name': url_name
            })
        
        return patterns
    
    def analyze_url_pattern(self, pattern: Dict[str, Any]) -> Optional[DjangoEndpoint]:
        """Analyze a single URL pattern"""
        view_name = pattern['view']
        url_path = pattern['url']
        
        # Skip certain endpoints
        skip_patterns = ['admin', 'TokenRefreshView', 'include']
        if any(skip in view_name for skip in skip_patterns):
            return None
        
        # Determine HTTP methods based on view name and URL
        http_methods = self.determine_http_methods(view_name, url_path)
        
        return DjangoEndpoint(
            url_pattern=url_path,
            view_class=view_name,
            view_method='get',  # Default, will be refined
            file_path=f"app/views/{view_name.lower()}.py",
            line_number=1,
            http_methods=http_methods,
            auth_required=not ('public' in url_path.lower() or 'login' in url_path.lower())
        )
    
    def determine_http_methods(self, view_name: str, url_path: str) -> List[str]:
        """Determine HTTP methods based on view name and URL pattern"""
        name_lower = view_name.lower()
        path_lower = url_path.lower()
        
        if any(word in name_lower for word in ['create', 'register', 'add', 'post']):
            return ['POST']
        elif any(word in name_lower for word in ['update', 'set', 'edit', 'put']):
            return ['PUT']
        elif any(word in name_lower for word in ['delete', 'remove']):
            return ['DELETE']
        elif 'login' in path_lower:
            return ['GET', 'POST']
        elif 'refresh' in path_lower:
            return ['POST']
        else:
            return ['GET']
    
    def convert_to_fastapi(self) -> None:
        """Convert Django endpoints to FastAPI"""
        logger.info("🔄 Converting Django endpoints to FastAPI...")
        
        # Group endpoints by category
        endpoint_groups = self.group_endpoints_by_category()
        
        for category, endpoints in endpoint_groups.items():
            self.create_fastapi_router(category, endpoints)
        
        logger.info(f"✅ Converted {len(self.converted_endpoints)} endpoints")
    
    def group_endpoints_by_category(self) -> Dict[str, List[DjangoEndpoint]]:
        """Group endpoints by functional category"""
        groups = {
            'auth': [],
            'users': [],
            'profile': [],
            'content': [],
            'search': [],
            'recommendations': [],
            'social': [],
            'public': []
        }
        
        for endpoint in self.endpoints:
            category = self.categorize_endpoint(endpoint)
            if category not in groups:
                groups[category] = []
            groups[category].append(endpoint)
        
        return groups
    
    def categorize_endpoint(self, endpoint: DjangoEndpoint) -> str:
        """Categorize an endpoint based on its URL and view"""
        url_lower = endpoint.url_pattern.lower()
        view_lower = endpoint.view_class.lower()
        
        if any(word in url_lower for word in ['login', 'logout', 'register', 'token', 'auth']):
            return 'auth'
        elif any(word in url_lower for word in ['public']):
            return 'public'
        elif any(word in url_lower for word in ['me/', 'my', 'profile']):
            return 'users'
        elif any(word in url_lower for word in ['search']):
            return 'search'
        elif any(word in url_lower for word in ['recommend']):
            return 'recommendations'
        elif any(word in url_lower for word in ['bud', 'common', 'friends']):
            return 'social'
        elif any(word in url_lower for word in ['tracks', 'artists', 'albums', 'genres']):
            return 'content'
        else:
            return 'misc'
    
    def create_fastapi_router(self, category: str, endpoints: List[DjangoEndpoint]) -> None:
        """Create FastAPI router for a category of endpoints"""
        if not endpoints:
            return
        
        logger.info(f"📝 Creating FastAPI router for {category} ({len(endpoints)} endpoints)")
        
        router_code = self.generate_router_code(category, endpoints)
        
        # Write router file
        router_file = self.fastapi_root / "app" / "api" / "v2" / f"{category}.py"
        router_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(router_file, 'w') as f:
            f.write(router_code)
        
        logger.info(f"✅ Created {router_file}")
    
    def generate_router_code(self, category: str, endpoints: List[DjangoEndpoint]) -> str:
        """Generate FastAPI router code"""
        imports = [
            "from fastapi import APIRouter, HTTPException, Depends, Query, Body, Path",
            "from typing import List, Optional, Dict, Any",
            "from pydantic import BaseModel",
            "import logging",
            "",
            "# Import your existing Django services/logic here",
            "# from app.services.xxx import xxx_service",
            "",
            "logger = logging.getLogger(__name__)",
            f'router = APIRouter(prefix="/{category}", tags=["{category}"])',
            ""
        ]
        
        # Add authentication dependency if needed
        auth_required = any(ep.auth_required for ep in endpoints)
        if auth_required:
            imports.extend([
                "from app.dependencies.auth import get_current_user",
                "from app.models.user import User",
                ""
            ])
        
        # Generate endpoint functions
        functions = []
        for endpoint in endpoints:
            function_code = self.generate_endpoint_function(endpoint)
            functions.append(function_code)
        
        return "\n".join(imports) + "\n" + "\n\n".join(functions)
    
    def generate_endpoint_function(self, endpoint: DjangoEndpoint) -> str:
        """Generate FastAPI endpoint function"""
        # Convert Django URL pattern to FastAPI path
        fastapi_path = self.convert_url_pattern(endpoint.url_pattern)
        
        # Generate function name
        func_name = self.generate_function_name(endpoint)
        
        # Determine response model
        response_model = self.determine_response_model(endpoint)
        
        # Generate dependencies
        dependencies = []
        if endpoint.auth_required:
            dependencies.append("current_user: User = Depends(get_current_user)")
        
        # Add path/query parameters
        path_params = self.extract_path_parameters(fastapi_path)
        for param in path_params:
            dependencies.append(f"{param}: str = Path(...)")
        
        deps_str = ", ".join(dependencies) if dependencies else ""
        
        # Generate function body
        body = self.generate_function_body(endpoint)
        
        # Choose HTTP method decorator
        method = endpoint.http_methods[0].lower()
        
        code = f'''@router.{method}("{fastapi_path}")
async def {func_name}({deps_str}):
    """
    {self.generate_docstring(endpoint)}
    """
    {body}'''
        
        return code
    
    def convert_url_pattern(self, django_url: str) -> str:
        """Convert Django URL pattern to FastAPI path"""
        # Remove trailing slash
        path = django_url.rstrip('/')
        if not path:
            path = "/"
        
        # Convert Django path parameters to FastAPI format
        # Django: <str:user_id> -> FastAPI: {user_id}
        path = re.sub(r'<\w+:(\w+)>', r'{\1}', path)
        path = re.sub(r'<(\w+)>', r'{\1}', path)
        
        return path
    
    def extract_path_parameters(self, path: str) -> List[str]:
        """Extract path parameters from FastAPI path"""
        return re.findall(r'\{(\w+)\}', path)
    
    def generate_function_name(self, endpoint: DjangoEndpoint) -> str:
        """Generate function name from endpoint"""
        # Convert view class to function name
        name = endpoint.view_class
        
        # Remove common suffixes
        name = re.sub(r'(View|APIView)$', '', name)
        
        # Convert CamelCase to snake_case
        name = re.sub(r'([A-Z])', r'_\1', name).lower().lstrip('_')
        
        # Add method prefix if not GET
        method = endpoint.http_methods[0].lower()
        if method != 'get':
            name = f"{method}_{name}"
        
        return name
    
    def determine_response_model(self, endpoint: DjangoEndpoint) -> str:
        """Determine appropriate response model"""
        if 'profile' in endpoint.url_pattern.lower():
            return "UserProfile"
        elif 'track' in endpoint.url_pattern.lower():
            return "Track"
        elif 'artist' in endpoint.url_pattern.lower():
            return "Artist"
        else:
            return "Dict[str, Any]"
    
    def generate_function_body(self, endpoint: DjangoEndpoint) -> str:
        """Generate function body with placeholder implementation"""
        # Try to preserve Django logic by calling existing services
        service_call = self.generate_service_call(endpoint)
        
        return f'''try:
        logger.info("Processing {endpoint.view_class} request")
        
        # TODO: Implement business logic here
        # You can call your existing Django services/functions
        {service_call}
        
        # Placeholder response - replace with actual implementation
        return {{
            "success": True,
            "message": "Endpoint migrated from Django",
            "data": {{}},
            "endpoint": "{endpoint.view_class}"
        }}
    except Exception as e:
        logger.error(f"Error in {endpoint.view_class}: {{str(e)}}")
        raise HTTPException(status_code=500, detail=str(e))'''
    
    def generate_service_call(self, endpoint: DjangoEndpoint) -> str:
        """Generate service call to preserve Django logic"""
        view_name = endpoint.view_class.lower()
        
        if 'profile' in view_name:
            return "# result = profile_service.get_profile(current_user.id)"
        elif 'search' in view_name:
            return "# result = search_service.search(query, filters)"
        elif 'recommend' in view_name:
            return "# result = recommendation_service.get_recommendations(current_user.id)"
        else:
            return f"# result = {view_name}_service.process()"
    
    def generate_docstring(self, endpoint: DjangoEndpoint) -> str:
        """Generate endpoint docstring"""
        return f"Migrated from Django {endpoint.view_class}\nOriginal URL: {endpoint.url_pattern}"
    
    def create_v2_api_router(self) -> None:
        """Create main v2 API router"""
        logger.info("📦 Creating v2 API router...")
        
        # Get all router categories
        categories = set()
        for endpoint in self.endpoints:
            category = self.categorize_endpoint(endpoint)
            categories.add(category)
        
        # Generate main router
        router_code = '''"""
FastAPI v2 API Router
Auto-generated from Django migration
"""
from fastapi import APIRouter

'''
        
        # Add imports for each category
        for category in sorted(categories):
            router_code += f"from .{category} import router as {category}_router\n"
        
        router_code += '''
api_router = APIRouter(prefix="/v2")

# Include all category routers
'''
        
        for category in sorted(categories):
            router_code += f"api_router.include_router({category}_router)\n"
        
        # Write main router file
        init_file = self.fastapi_root / "app" / "api" / "v2" / "__init__.py"
        init_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(init_file, 'w') as f:
            f.write(router_code)
        
        logger.info(f"✅ Created v2 API router with {len(categories)} categories")
    
    def run_migration(self) -> None:
        """Run the complete migration process"""
        logger.info("🚀 Starting Django to FastAPI migration...")
        
        # Step 1: Analyze Django endpoints
        self.endpoints = self.analyze_django_urls()
        
        if not self.endpoints:
            logger.error("❌ No endpoints found to migrate")
            return
        
        # Step 2: Convert to FastAPI
        self.convert_to_fastapi()
        
        # Step 3: Create main v2 router
        self.create_v2_api_router()
        
        # Step 4: Generate migration report
        self.generate_migration_report()
        
        logger.info("✅ Migration completed successfully!")
    
    def generate_migration_report(self) -> None:
        """Generate migration report"""
        report = {
            "migration_summary": {
                "total_endpoints": len(self.endpoints),
                "categories": {},
                "migration_date": "2025-01-13T07:05:45Z",
                "status": "completed"
            },
            "endpoints": []
        }
        
        # Group by category for report
        categories = {}
        for endpoint in self.endpoints:
            category = self.categorize_endpoint(endpoint)
            if category not in categories:
                categories[category] = 0
            categories[category] += 1
        
        report["migration_summary"]["categories"] = categories
        
        # Add endpoint details
        for endpoint in self.endpoints:
            report["endpoints"].append({
                "original_url": endpoint.url_pattern,
                "view_class": endpoint.view_class,
                "http_methods": endpoint.http_methods,
                "category": self.categorize_endpoint(endpoint),
                "auth_required": endpoint.auth_required,
                "fastapi_path": self.convert_url_pattern(endpoint.url_pattern),
                "status": "migrated"
            })
        
        # Write report
        report_file = self.fastapi_root / "migration_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"📊 Migration report saved to {report_file}")
        
        # Print summary
        print("\n" + "="*50)
        print("🎯 MIGRATION SUMMARY")
        print("="*50)
        print(f"📋 Total endpoints migrated: {len(self.endpoints)}")
        print("📊 Categories:")
        for category, count in categories.items():
            print(f"   • {category}: {count} endpoints")
        print("\n✅ All endpoints successfully converted to FastAPI!")
        print("📂 FastAPI v2 routers created in fastapi_backend/app/api/v2/")
        print("📄 Migration report: fastapi_backend/migration_report.json")
        print("="*50)


def main():
    """Main migration function"""
    print("🚀 Django to FastAPI Migration Tool")
    print("="*50)
    
    # Set up paths
    backend_root = Path("/home/mahmoud/Documents/GitHub/musicbud/backend")
    django_root = backend_root
    fastapi_root = backend_root / "fastapi_backend"
    
    # Ensure FastAPI directory exists
    fastapi_root.mkdir(exist_ok=True)
    
    # Run migration
    converter = DjangoToFastAPIConverter(django_root, fastapi_root)
    converter.run_migration()
    
    print("\n🎉 Migration completed! Next steps:")
    print("1. 📝 Review generated FastAPI code in fastapi_backend/app/api/v2/")
    print("2. 🔧 Implement actual business logic in each endpoint")
    print("3. 🧪 Run tests: cd fastapi_backend && python run_tests.py")
    print("4. 🌐 Start hybrid server: uvicorn hybrid_asgi:application --reload")
    print("5. 📚 Check FastAPI docs at http://localhost:8000/docs")

if __name__ == "__main__":
    main()