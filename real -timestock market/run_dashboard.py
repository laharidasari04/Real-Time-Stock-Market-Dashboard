#!/usr/bin/env python3
"""
Launcher script for the Real-Time Stock Market Dashboard
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'pandas', 
        'plotly',
        'yfinance',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Installing missing packages...")
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            print("✅ All packages installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please run:")
            print("   pip install -r requirements.txt")
            return False
    
    return True

def main():
    """Main launcher function"""
    print("🚀 Starting Real-Time Stock Market Dashboard...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("stock_dashboard.py"):
        print("❌ Error: stock_dashboard.py not found!")
        print("   Please run this script from the project directory.")
        return
    
    # Check dependencies
    if not check_dependencies():
        return
    
    print("✅ Dependencies check passed!")
    print("🌐 Starting Streamlit server...")
    print("📱 Dashboard will open in your default browser")
    print("🔄 To stop the server, press Ctrl+C")
    print("=" * 50)
    
    try:
        # Run the Streamlit app
        subprocess.run([sys.executable, "-m", "streamlit", "run", "stock_dashboard.py"])
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error running dashboard: {e}")

if __name__ == "__main__":
    main() 