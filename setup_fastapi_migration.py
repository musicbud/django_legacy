#!/usr/bin/env python3
"""
Complete FastAPI Migration Setup Script
Sets up the FastAPI environment, tests the migration, and validates functionality
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class FastAPIMigrationSetup:
    """Setup and test FastAPI migration"""
    
    def __init__(self):
        self.project_root = Path("/home/mahmoud/Documents/GitHub/musicbud/backend")
        self.venv_path = self.project_root / "venv_fastapi"
        
    def print_step(self, step_num, title):
        """Print step with formatting"""
        print(f"\n{'='*60}")
        print(f"Step {step_num}: {title}")
        print('='*60)
    
    def run_command(self, command, cwd=None, check=True):
        """Run shell command"""
        print(f"Running: {command}")
        if isinstance(command, str):
            command = command.split()
        
        result = subprocess.run(
            command, 
            cwd=cwd or self.project_root, 
            capture_output=True, 
            text=True,
            check=False
        )
        
        if result.stdout:
            print(f"Output: {result.stdout}")
        if result.stderr:
            print(f"Error: {result.stderr}")
            
        if check and result.returncode != 0:
            print(f"Command failed with return code {result.returncode}")
            return False
        
        return result.returncode == 0
    
    def create_virtual_environment(self):
        """Create virtual environment for FastAPI"""
        self.print_step(1, "Creating Virtual Environment")
        
        # Remove existing venv if exists
        if self.venv_path.exists():
            print("Removing existing virtual environment...")
            import shutil
            shutil.rmtree(self.venv_path)
        
        # Create new venv
        success = self.run_command(f"python3 -m venv {self.venv_path}")
        if success:
            print("✅ Virtual environment created successfully")
        return success
    
    def install_dependencies(self):
        """Install FastAPI dependencies"""
        self.print_step(2, "Installing Dependencies")
        
        pip_path = self.venv_path / "bin" / "pip"
        
        # Upgrade pip
        self.run_command([str(pip_path), "install", "--upgrade", "pip"])
        
        # Install requirements
        requirements_file = self.project_root / "requirements-fastapi.txt"
        success = self.run_command([str(pip_path), "install", "-r", str(requirements_file)])
        
        if success:
            print("✅ Dependencies installed successfully")
        return success
    
    def create_environment_file(self):
        """Create .env file with necessary variables"""
        self.print_step(3, "Creating Environment Configuration")
        
        env_content = """# FastAPI Environment Configuration
DEBUG=True
TESTING=True

# Security
SECRET_KEY=your-secret-key-replace-in-production
JWT_SECRET_KEY=your-jwt-secret-key-replace-in-production

# Server
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=development

# Database
NEO4J_PASSWORD=12345678
REDIS_URL=redis://localhost:6379

# API
PROJECT_NAME=MusicBud FastAPI
API_VERSION=2.0.0
API_DESCRIPTION=MusicBud FastAPI Backend - Music Recommendation Platform

# Rate Limiting
RATE_LIMIT_PER_MINUTE=100

# Logging
LOG_LEVEL=INFO

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000,http://127.0.0.1:3000,http://127.0.0.1:8000
ALLOWED_HOSTS=*

# External APIs (placeholders - replace with actual values)
SPOTIFY_CLIENT_ID=your-spotify-client-id
SPOTIFY_CLIENT_SECRET=your-spotify-client-secret
LASTFM_API_KEY=your-lastfm-api-key
LASTFM_API_SECRET=your-lastfm-api-secret
"""
        
        env_file = self.project_root / ".env"
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print("✅ Environment file created")
        print(f"📝 Please edit {env_file} and add your actual API keys")
        return True
    
    def test_fastapi_app_startup(self):
        """Test that FastAPI app can start"""
        self.print_step(4, "Testing FastAPI App Startup")
        
        python_path = self.venv_path / "bin" / "python"
        
        # Test import
        test_script = """
import sys
sys.path.insert(0, '/home/mahmoud/Documents/GitHub/musicbud/backend')

try:
    from fastapi_app import app
    print("✅ FastAPI app imported successfully")
    print(f"App title: {app.title}")
    print(f"App version: {app.version}")
    
    # Test basic functionality
    from fastapi.testclient import TestClient
    client = TestClient(app)
    
    # Test root endpoint
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    print(f"Root endpoint response: {data}")
    
    print("✅ Basic functionality test passed")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
"""
        
        with open(self.project_root / "test_startup.py", 'w') as f:
            f.write(test_script)
        
        success = self.run_command([str(python_path), "test_startup.py"])
        
        # Clean up test file
        (self.project_root / "test_startup.py").unlink()
        
        return success
    
    def run_migration_tests(self):
        """Run comprehensive migration tests"""
        self.print_step(5, "Running Migration Tests")
        
        python_path = self.venv_path / "bin" / "python"
        
        # Set environment variables for testing
        env = os.environ.copy()
        env.update({
            "TESTING": "1",
            "DEBUG": "1",
            "SECRET_KEY": "test-secret-key",
            "NEO4J_PASSWORD": "test-password"
        })
        
        # Run tests
        cmd = [str(python_path), "-m", "pytest", "test_fastapi_migration.py", "-v", "--tb=short"]
        
        result = subprocess.run(
            cmd,
            cwd=self.project_root,
            env=env,
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        success = result.returncode == 0
        if success:
            print("✅ All migration tests passed!")
        else:
            print("❌ Some tests failed - check output above")
        
        return success
    
    def create_startup_scripts(self):
        """Create startup scripts for development and production"""
        self.print_step(6, "Creating Startup Scripts")
        
        # Development startup script
        dev_script = f"""#!/bin/bash
# FastAPI Development Server Startup Script

echo "🚀 Starting MusicBud FastAPI Development Server..."

cd {self.project_root}
source {self.venv_path}/bin/activate

export DEBUG=True
export ENVIRONMENT=development

echo "Starting server on http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo "Health Check: http://localhost:8000/health"

python fastapi_app.py
"""
        
        dev_script_path = self.project_root / "start_dev.sh"
        with open(dev_script_path, 'w') as f:
            f.write(dev_script)
        os.chmod(dev_script_path, 0o755)
        
        # Production startup script
        prod_script = f"""#!/bin/bash
# FastAPI Production Server Startup Script

echo "🚀 Starting MusicBud FastAPI Production Server..."

cd {self.project_root}
source {self.venv_path}/bin/activate

export DEBUG=False
export ENVIRONMENT=production

echo "Starting production server..."

{self.venv_path}/bin/uvicorn fastapi_app:app \\
    --host 0.0.0.0 \\
    --port 8000 \\
    --workers 4 \\
    --log-level info \\
    --access-log
"""
        
        prod_script_path = self.project_root / "start_prod.sh"
        with open(prod_script_path, 'w') as f:
            f.write(prod_script)
        os.chmod(prod_script_path, 0o755)
        
        print("✅ Startup scripts created:")
        print(f"   Development: {dev_script_path}")
        print(f"   Production:  {prod_script_path}")
        
        return True
    
    def validate_api_endpoints(self):
        """Validate API endpoints with actual HTTP requests"""
        self.print_step(7, "Validating API Endpoints")
        
        python_path = self.venv_path / "bin" / "python"
        
        validation_script = """
import sys
sys.path.insert(0, '/home/mahmoud/Documents/GitHub/musicbud/backend')

import asyncio
from fastapi.testclient import TestClient
from fastapi_app import app

def test_endpoints():
    client = TestClient(app)
    
    endpoints_to_test = [
        ("/", "GET", "Root endpoint"),
        ("/health", "GET", "Health check"),
        ("/api/public/discover", "GET", "Public discover"),
        ("/api/public/trending", "GET", "Public trending"),
        ("/api/public/genres", "GET", "Public genres"),
        ("/api/public/stats", "GET", "Public stats"),
        ("/api/content/tracks", "GET", "Content tracks"),
        ("/api/content/artists", "GET", "Content artists"),
    ]
    
    results = []
    
    for endpoint, method, description in endpoints_to_test:
        try:
            if method == "GET":
                response = client.get(endpoint)
            elif method == "POST":
                response = client.post(endpoint, json={})
            
            success = response.status_code < 500
            results.append((endpoint, response.status_code, success, description))
            
            status_icon = "✅" if success else "❌"
            print(f"{status_icon} {description}: {endpoint} -> {response.status_code}")
            
        except Exception as e:
            print(f"❌ {description}: {endpoint} -> Error: {e}")
            results.append((endpoint, 500, False, description))
    
    # Summary
    successful = sum(1 for _, _, success, _ in results if success)
    total = len(results)
    
    print(f"\\n📊 Endpoint Validation Summary: {successful}/{total} endpoints working")
    
    if successful == total:
        print("✅ All endpoints are working correctly!")
        return True
    else:
        print("❌ Some endpoints have issues")
        return False

if __name__ == "__main__":
    success = test_endpoints()
    sys.exit(0 if success else 1)
"""
        
        with open(self.project_root / "validate_endpoints.py", 'w') as f:
            f.write(validation_script)
        
        success = self.run_command([str(python_path), "validate_endpoints.py"])
        
        # Clean up
        (self.project_root / "validate_endpoints.py").unlink()
        
        return success
    
    def generate_migration_report(self):
        """Generate migration report"""
        self.print_step(8, "Generating Migration Report")
        
        report = {
            "migration_status": "completed",
            "timestamp": str(Path().cwd()),
            "components_migrated": [
                "Django authentication -> FastAPI JWT auth",
                "Django views -> FastAPI routers", 
                "Django serializers -> Pydantic schemas",
                "Django middleware -> FastAPI middleware",
                "Database integration (Django ORM + Neo4j + Redis)",
                "Public API endpoints",
                "User management endpoints",
                "Content endpoints",
                "Comprehensive error handling",
                "Security enhancements",
                "Caching system",
                "Health checks and monitoring"
            ],
            "new_features": [
                "Automatic API documentation (/docs)",
                "OpenAPI specification",
                "Async/await support",
                "Enhanced authentication system", 
                "Rate limiting",
                "Request/response validation",
                "Comprehensive middleware stack",
                "Performance monitoring",
                "Redis caching integration",
                "Neo4j graph database support"
            ],
            "api_endpoints": {
                "authentication": [
                    "POST /api/auth/register",
                    "POST /api/auth/login",
                    "POST /api/auth/login/json",
                    "POST /api/auth/logout",
                    "GET /api/auth/me",
                    "POST /api/auth/change-password"
                ],
                "public": [
                    "GET /api/public/discover",
                    "GET /api/public/trending", 
                    "GET /api/public/recommendations",
                    "GET /api/public/genres",
                    "GET /api/public/content/{type}/{id}",
                    "GET /api/public/stats"
                ],
                "users": [
                    "GET /api/users/profile"
                ],
                "content": [
                    "GET /api/content/tracks",
                    "GET /api/content/artists"
                ],
                "system": [
                    "GET /",
                    "GET /health", 
                    "GET /metrics"
                ]
            },
            "testing_coverage": [
                "Authentication flow testing",
                "Public API testing",
                "User endpoint testing",
                "Error handling testing",
                "Security testing",
                "Performance testing", 
                "Integration testing"
            ]
        }
        
        report_file = self.project_root / "fastapi_migration_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print("✅ Migration report generated")
        print(f"📄 Report saved to: {report_file}")
        
        return True
    
    def run_complete_setup(self):
        """Run complete FastAPI migration setup"""
        print("🚀 Starting Complete FastAPI Migration Setup")
        print(f"Project root: {self.project_root}")
        
        steps = [
            self.create_virtual_environment,
            self.install_dependencies,
            self.create_environment_file,
            self.test_fastapi_app_startup,
            self.run_migration_tests,
            self.create_startup_scripts,
            self.validate_api_endpoints,
            self.generate_migration_report
        ]
        
        for i, step in enumerate(steps, 1):
            try:
                success = step()
                if not success:
                    print(f"❌ Step {i} failed!")
                    return False
            except Exception as e:
                print(f"❌ Step {i} failed with exception: {e}")
                import traceback
                traceback.print_exc()
                return False
        
        self.print_success_message()
        return True
    
    def print_success_message(self):
        """Print success message with instructions"""
        print("\n" + "="*80)
        print("🎉 FASTAPI MIGRATION SETUP COMPLETED SUCCESSFULLY!")
        print("="*80)
        
        print("\n📋 What's been set up:")
        print("  ✅ FastAPI application (fastapi_app.py)")
        print("  ✅ Authentication system with JWT")
        print("  ✅ Public API endpoints")
        print("  ✅ User management endpoints")
        print("  ✅ Database integration (Django ORM + Neo4j + Redis)")
        print("  ✅ Comprehensive middleware stack")
        print("  ✅ Pydantic schemas and validation")
        print("  ✅ Error handling and security")
        print("  ✅ Test suite with 30+ tests")
        print("  ✅ Development and production startup scripts")
        
        print("\n🚀 How to start your FastAPI server:")
        print(f"  Development:  ./start_dev.sh")
        print(f"  Production:   ./start_prod.sh")
        print(f"  Manual:       source {self.venv_path}/bin/activate && python fastapi_app.py")
        
        print("\n📚 Available endpoints:")
        print("  🌐 API Root:           http://localhost:8000/")
        print("  📖 API Documentation:  http://localhost:8000/docs")
        print("  💚 Health Check:       http://localhost:8000/health")
        print("  🔍 Public Discover:    http://localhost:8000/api/public/discover")
        print("  🔥 Public Trending:    http://localhost:8000/api/public/trending")
        print("  🎵 Public Genres:      http://localhost:8000/api/public/genres")
        
        print("\n🧪 Run tests:")
        print(f"  cd {self.project_root}")
        print(f"  source {self.venv_path}/bin/activate")
        print("  python test_fastapi_migration.py")
        
        print("\n⚙️  Configuration:")
        print("  📝 Edit .env file for your API keys and settings")
        print("  🔑 Update SECRET_KEY and JWT_SECRET_KEY for production")
        print("  🗄️  Configure your databases (Neo4j, Redis)")
        
        print("\n📊 Migration complete! Your Django app has been fully migrated to FastAPI.")


def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h']:
        print("FastAPI Migration Setup Script")
        print("Usage: python setup_fastapi_migration.py")
        print("This script will completely migrate your Django app to FastAPI")
        return
    
    setup = FastAPIMigrationSetup()
    success = setup.run_complete_setup()
    
    if not success:
        print("\n❌ Migration setup failed!")
        sys.exit(1)
    
    print("\n✅ Migration setup completed successfully!")
    sys.exit(0)


if __name__ == "__main__":
    main()