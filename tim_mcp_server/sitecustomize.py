"""Enable coverage measurement in subprocesses during testing.

This file is automatically imported by Python when it's in the Python path.
It's used ONLY during testing to enable coverage tracking in subprocesses.

IMPORTANT: This file should NOT be included in production deployments.
It should only be present during test execution.
"""
import os

# Only run coverage if COVERAGE_PROCESS_START is set (test environment only)
if os.environ.get('COVERAGE_PROCESS_START'):
    import coverage
    import atexit
    import signal
    import sys
    
    # Start coverage immediately before any other imports
    cov = coverage.Coverage(config_file=os.environ.get('COVERAGE_PROCESS_START'))
    cov.start()
    
    # Save for later access
    import builtins
    builtins._coverage_instance = cov
    
    def save_coverage_data(signum=None, frame=None):
        """Save coverage data when process is terminated."""
        try:
            if hasattr(builtins, '_coverage_instance'):
                c = builtins._coverage_instance
                c.stop()
                c.save()
        except Exception:
            pass
        
        # Exit cleanly on signal
        if signum is not None:
            sys.exit(0)
    
    # Register handlers for saving coverage data
    atexit.register(save_coverage_data)
    signal.signal(signal.SIGTERM, save_coverage_data)
    signal.signal(signal.SIGINT, save_coverage_data)