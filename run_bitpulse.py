import subprocess
import sys
import os
import signal

BACKEND_CMD = [sys.executable, '-m', 'uvicorn', 'app.main:app', '--reload']
FRONTEND_CMD = ['npm', 'run', 'dev']

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(ROOT_DIR, 'frontend')

backend_proc = None
frontend_proc = None

def run_backend():
    print('🔵 Starting FastAPI backend (پشتبان)...')
    return subprocess.Popen(BACKEND_CMD, cwd=ROOT_DIR)

def run_frontend():
    print('🟢 Starting Vite frontend (فرانت)...')
    return subprocess.Popen(FRONTEND_CMD, cwd=FRONTEND_DIR, shell=True)

def main():
    global backend_proc, frontend_proc
    try:
        backend_proc = run_backend()
        frontend_proc = run_frontend()
        print('\n✅ BitPulse is running!')
        print('Backend: http://localhost:8000')
        print('Frontend: http://localhost:3000')
        print('\nبرای خروج Ctrl+C را فشار دهید...')
        print('Press Ctrl+C to exit...')
        # Wait for both processes
        while True:
            if backend_proc.poll() is not None or frontend_proc.poll() is not None:
                break
    except KeyboardInterrupt:
        print('\n⏹ Shutting down...')
    finally:
        if backend_proc:
            backend_proc.terminate()
        if frontend_proc:
            frontend_proc.terminate()
        print('خروج انجام شد. (Exited)')

if __name__ == '__main__':
    main() 