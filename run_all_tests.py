#!/usr/bin/env python3
"""
Master test runner for the entire EEG Full Pipeline project.

This script coordinates testing across:
1. PySpark Pipeline (eeg-pyspark-pipeline/)
2. Ray Tuner (eeg-ray-tuner/) - when implemented
3. Root repository integration tests

Usage:
    python run_all_tests.py [OPTIONS]
"""

import subprocess
import sys
import argparse
import time
import os
from pathlib import Path
from typing import List, Tuple, Optional, Dict
import json


class TestRunner:
    """Master test runner for the EEG Full Pipeline project."""
    
    def __init__(self, verbose: bool = False, parallel: bool = False, coverage: bool = False):
        """
        Initialize the test runner.
        
        Args:
            verbose: Enable verbose output
            parallel: Run tests in parallel where possible
            coverage: Generate coverage reports
        """
        self.verbose = verbose
        self.parallel = parallel
        self.coverage = coverage
        self.project_root = Path(__file__).parent
        self.results = {
            'pyspark': {'status': 'not_run', 'duration': 0, 'details': {}},
            'root': {'status': 'not_run', 'duration': 0, 'details': {}},
            'ray': {'status': 'not_run', 'duration': 0, 'details': {}}  # Future
        }
        
    def print_header(self, title: str):
        """Print a formatted header."""
        print("\n" + "=" * 80)
        print(f"🧪 {title}")
        print("=" * 80)
        
    def print_section(self, title: str):
        """Print a formatted section header."""
        print(f"\n📋 {title}")
        print("-" * 60)
        
    def run_pyspark_tests(self, test_suite: str = "all", markers: Optional[str] = None) -> bool:
        """Run PySpark pipeline tests."""
        self.print_section("PySpark Pipeline Tests")
        
        pyspark_dir = self.project_root / "eeg-pyspark-pipeline"
        if not pyspark_dir.exists():
            print("❌ PySpark pipeline directory not found")
            self.results['pyspark']['status'] = 'failed'
            return False
        
        # Build command
        cmd = [sys.executable, "run_tests.py"]
        
        if test_suite != "all":
            cmd.extend(["--suite", test_suite])
        
        if markers:
            cmd.extend(["--markers", markers])
        
        if self.verbose:
            cmd.append("--verbose")
        
        if self.coverage:
            cmd.append("--coverage")
        
        if self.parallel:
            cmd.append("--parallel")
        
        print(f"🔄 Running PySpark tests: {' '.join(cmd)}")
        
        start_time = time.time()
        
        try:
            result = subprocess.run(
                cmd,
                cwd=pyspark_dir,
                capture_output=not self.verbose,
                text=True,
                timeout=600  # 10 minute timeout
            )
            
            duration = time.time() - start_time
            self.results['pyspark']['duration'] = duration
            
            if result.returncode == 0:
                print(f"✅ PySpark tests passed ({duration:.2f}s)")
                self.results['pyspark']['status'] = 'passed'
                return True
            else:
                print(f"❌ PySpark tests failed ({duration:.2f}s)")
                if not self.verbose and result.stderr:
                    print(f"   Error: {result.stderr.strip()}")
                self.results['pyspark']['status'] = 'failed'
                self.results['pyspark']['details']['error'] = result.stderr
                return False
                
        except subprocess.TimeoutExpired:
            print("⏰ PySpark tests timed out (>10 minutes)")
            self.results['pyspark']['status'] = 'timeout'
            return False
        except Exception as e:
            print(f"💥 PySpark tests crashed: {e}")
            self.results['pyspark']['status'] = 'crashed'
            self.results['pyspark']['details']['error'] = str(e)
            return False
    
    def run_root_tests(self, test_suite: str = "all", markers: Optional[str] = None) -> bool:
        """Run root repository integration tests."""
        self.print_section("Root Repository Integration Tests")
        
        # Build command
        cmd = [sys.executable, "-m", "pytest", "tests/"]
        
        if test_suite != "all":
            if test_suite == "unit":
                cmd.extend(["-m", "unit"])
            elif test_suite == "integration":
                cmd.extend(["-m", "integration"])
            elif test_suite == "config":
                cmd.extend(["-m", "config"])
            elif test_suite == "slow":
                cmd.extend(["-m", "slow"])
        
        if markers:
            cmd.extend(["-m", markers])
        
        if self.verbose:
            cmd.append("-v")
        else:
            cmd.append("-q")
        
        if self.coverage:
            cmd.extend([
                "--cov=.",
                "--cov-report=html:coverage_report",
                "--cov-report=term-missing"
            ])
        
        if self.parallel:
            cmd.extend(["-n", "auto"])
        
        # Add other useful options
        cmd.extend([
            "--tb=short",
            "--strict-markers",
            "--disable-warnings"
        ])
        
        print(f"🔄 Running root tests: {' '.join(cmd)}")
        
        start_time = time.time()
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=not self.verbose,
                text=True,
                timeout=600  # 10 minute timeout
            )
            
            duration = time.time() - start_time
            self.results['root']['duration'] = duration
            
            if result.returncode == 0:
                print(f"✅ Root tests passed ({duration:.2f}s)")
                self.results['root']['status'] = 'passed'
                return True
            else:
                print(f"❌ Root tests failed ({duration:.2f}s)")
                if not self.verbose and result.stderr:
                    print(f"   Error: {result.stderr.strip()}")
                self.results['root']['status'] = 'failed'
                self.results['root']['details']['error'] = result.stderr
                return False
                
        except subprocess.TimeoutExpired:
            print("⏰ Root tests timed out (>10 minutes)")
            self.results['root']['status'] = 'timeout'
            return False
        except Exception as e:
            print(f"💥 Root tests crashed: {e}")
            self.results['root']['status'] = 'crashed'
            self.results['root']['details']['error'] = str(e)
            return False
    
    def run_ray_tests(self, test_suite: str = "all", markers: Optional[str] = None) -> bool:
        """Run Ray tuner tests (placeholder for future implementation)."""
        self.print_section("Ray Tuner Tests")
        
        ray_dir = self.project_root / "eeg-ray-tuner"
        if not ray_dir.exists():
            print("⏭️  Ray tuner directory not found - skipping")
            self.results['ray']['status'] = 'skipped'
            return True
        
        # Check if Ray tests are implemented
        ray_tests_dir = ray_dir / "tests"
        if not ray_tests_dir.exists() or not any(ray_tests_dir.glob("test_*.py")):
            print("⏭️  Ray tuner tests not implemented yet - skipping")
            self.results['ray']['status'] = 'skipped'
            return True
        
        print("⏭️  Ray tuner tests not yet implemented - skipping")
        self.results['ray']['status'] = 'skipped'
        return True
    
    def run_containerized_tests(self, component: str = "pyspark") -> bool:
        """Run tests in containers."""
        self.print_section(f"Containerized Tests - {component.title()}")
        
        if component == "pyspark":
            script_path = self.project_root / "eeg-pyspark-pipeline" / "run_tests_container.sh"
            if not script_path.exists():
                print("❌ Containerized test script not found")
                return False
            
            cmd = ["bash", str(script_path)]
            if self.verbose:
                cmd.append("--verbose")
            if self.coverage:
                cmd.append("--coverage")
            
        else:
            print(f"⏭️  Containerized tests for {component} not implemented yet")
            return True
        
        print(f"🔄 Running containerized tests: {' '.join(cmd)}")
        
        start_time = time.time()
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=not self.verbose,
                text=True,
                timeout=900  # 15 minute timeout for containerized tests
            )
            
            duration = time.time() - start_time
            
            if result.returncode == 0:
                print(f"✅ Containerized tests passed ({duration:.2f}s)")
                return True
            else:
                print(f"❌ Containerized tests failed ({duration:.2f}s)")
                if not self.verbose and result.stderr:
                    print(f"   Error: {result.stderr.strip()}")
                return False
                
        except subprocess.TimeoutExpired:
            print("⏰ Containerized tests timed out (>15 minutes)")
            return False
        except Exception as e:
            print(f"💥 Containerized tests crashed: {e}")
            return False
    
    def print_summary(self):
        """Print a comprehensive test summary."""
        self.print_header("Test Summary")
        
        total_duration = sum(result['duration'] for result in self.results.values())
        
        print(f"📊 Total Duration: {total_duration:.2f} seconds")
        print()
        
        for component, result in self.results.items():
            status_emoji = {
                'passed': '✅',
                'failed': '❌',
                'timeout': '⏰',
                'crashed': '💥',
                'skipped': '⏭️',
                'not_run': '⏸️'
            }.get(result['status'], '❓')
            
            print(f"{status_emoji} {component.title()}: {result['status']} ({result['duration']:.2f}s)")
            
            if result['status'] == 'failed' and 'error' in result['details'] and result['details']['error']:
                print(f"   Error: {result['details']['error'][:100]}...")
        
        print()
        
        # Overall result
        failed_components = [comp for comp, result in self.results.items() 
                           if result['status'] in ['failed', 'timeout', 'crashed']]
        
        if failed_components:
            print(f"🔴 OVERALL RESULT: FAILED ({len(failed_components)} components failed)")
            print(f"   Failed components: {', '.join(failed_components)}")
            return False
        else:
            print(f"🟢 OVERALL RESULT: PASSED (All components successful)")
            return True
    
    def run_all_tests(self, 
                     components: List[str] = None,
                     test_suite: str = "all",
                     markers: Optional[str] = None,
                     containerized: bool = False) -> bool:
        """
        Run all tests across the project.
        
        Args:
            components: List of components to test (pyspark, root, ray)
            test_suite: Test suite to run (all, unit, integration, config, slow)
            markers: Pytest markers to filter tests
            containerized: Run containerized tests instead of local tests
            
        Returns:
            True if all tests passed, False otherwise
        """
        if components is None:
            components = ['pyspark', 'root']  # Skip ray for now
        
        self.print_header("EEG Full Pipeline Test Suite")
        
        print(f"🔍 Components: {', '.join(components)}")
        print(f"🔍 Test Suite: {test_suite}")
        print(f"🔍 Markers: {markers or 'None'}")
        print(f"🔍 Containerized: {containerized}")
        print(f"🔍 Verbose: {self.verbose}")
        print(f"🔍 Coverage: {self.coverage}")
        print(f"🔍 Parallel: {self.parallel}")
        
        start_time = time.time()
        
        # Run tests for each component
        success = True
        
        for component in components:
            if containerized and component == 'pyspark':
                success &= self.run_containerized_tests(component)
            elif component == 'pyspark':
                success &= self.run_pyspark_tests(test_suite, markers)
            elif component == 'root':
                success &= self.run_root_tests(test_suite, markers)
            elif component == 'ray':
                success &= self.run_ray_tests(test_suite, markers)
        
        total_duration = time.time() - start_time
        
        # Print summary
        summary_success = self.print_summary()
        print(f"\n⏱️  Total Duration: {total_duration:.2f} seconds")
        
        return success and summary_success


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run all tests for EEG Full Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run_all_tests.py                                    # Run all tests
    python run_all_tests.py --components pyspark root          # Run specific components
    python run_all_tests.py --suite unit                       # Run only unit tests
    python run_all_tests.py --markers "config and not slow"    # Run config tests that are not slow
    python run_all_tests.py --containerized                    # Run containerized tests
    python run_all_tests.py --coverage                         # Run with coverage report
    python run_all_tests.py --verbose                          # Run with verbose output
        """
    )
    
    parser.add_argument(
        "--components", "-c",
        nargs="+",
        choices=["pyspark", "root", "ray"],
        default=["pyspark", "root"],
        help="Components to test (default: pyspark root)"
    )
    
    parser.add_argument(
        "--suite", "-s",
        choices=["all", "unit", "integration", "config", "slow"],
        default="all",
        help="Test suite to run (default: all)"
    )
    
    parser.add_argument(
        "--markers", "-m",
        type=str,
        help="Pytest markers to filter tests (e.g., 'config and not slow')"
    )
    
    parser.add_argument(
        "--containerized",
        action="store_true",
        help="Run containerized tests instead of local tests"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Generate coverage reports"
    )
    
    parser.add_argument(
        "--parallel", "-p",
        action="store_true",
        help="Run tests in parallel where possible"
    )
    
    args = parser.parse_args()
    
    # Create and run test runner
    runner = TestRunner(
        verbose=args.verbose,
        parallel=args.parallel,
        coverage=args.coverage
    )
    
    success = runner.run_all_tests(
        components=args.components,
        test_suite=args.suite,
        markers=args.markers,
        containerized=args.containerized
    )
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
